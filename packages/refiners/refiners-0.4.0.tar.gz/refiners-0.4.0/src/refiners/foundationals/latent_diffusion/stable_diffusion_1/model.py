import numpy as np
import torch
from PIL import Image
from torch import Tensor, device as Device, dtype as DType

from refiners.fluxion.utils import image_to_tensor, interpolate
from refiners.foundationals.clip.text_encoder import CLIPTextEncoderL
from refiners.foundationals.latent_diffusion.auto_encoder import LatentDiffusionAutoencoder
from refiners.foundationals.latent_diffusion.model import LatentDiffusionModel
from refiners.foundationals.latent_diffusion.solvers import DPMSolver, Solver
from refiners.foundationals.latent_diffusion.stable_diffusion_1.self_attention_guidance import SD1SAGAdapter
from refiners.foundationals.latent_diffusion.stable_diffusion_1.unet import SD1UNet


class SD1Autoencoder(LatentDiffusionAutoencoder):
    """Stable Diffusion 1.5 autoencoder model.

    Attributes:
        encoder_scale: The encoder scale to use.
    """

    encoder_scale: float = 0.18215


class StableDiffusion_1(LatentDiffusionModel):
    """Stable Diffusion 1.5 model.

    Attributes:
        unet: The U-Net model.
        clip_text_encoder: The text encoder.
        lda: The image autoencoder.
    """

    unet: SD1UNet
    clip_text_encoder: CLIPTextEncoderL
    lda: SD1Autoencoder

    def __init__(
        self,
        unet: SD1UNet | None = None,
        lda: SD1Autoencoder | None = None,
        clip_text_encoder: CLIPTextEncoderL | None = None,
        solver: Solver | None = None,
        device: Device | str = "cpu",
        dtype: DType = torch.float32,
    ) -> None:
        """Initializes the model.

        Args:
            unet: The SD1UNet U-Net model to use.
            lda: The SD1Autoencoder image autoencoder to use.
            clip_text_encoder: The CLIPTextEncoderL text encoder to use.
            solver: The solver to use.
            device: The PyTorch device to use.
            dtype: The PyTorch data type to use.
        """
        unet = unet or SD1UNet(in_channels=4)
        lda = lda or SD1Autoencoder()
        clip_text_encoder = clip_text_encoder or CLIPTextEncoderL()
        solver = solver or DPMSolver(num_inference_steps=30)

        super().__init__(
            unet=unet,
            lda=lda,
            clip_text_encoder=clip_text_encoder,
            solver=solver,
            device=device,
            dtype=dtype,
        )

    def compute_clip_text_embedding(self, text: str | list[str], negative_text: str | list[str] = "") -> Tensor:
        """Compute the CLIP text embedding associated with the given prompt and negative prompt.

        Args:
            text: The prompt to compute the CLIP text embedding of.
            negative_text: The negative prompt to compute the CLIP text embedding of.
                If not provided, the negative prompt is assumed to be empty (i.e., `""`).
        """
        text = [text] if isinstance(text, str) else text
        negative_text = [negative_text] if isinstance(negative_text, str) else negative_text
        assert len(text) == len(negative_text), "The length of the text list and negative_text should be the same"

        conditional_embedding = self.clip_text_encoder(text)
        negative_embedding = self.clip_text_encoder(negative_text)

        return torch.cat((negative_embedding, conditional_embedding))

    def set_unet_context(self, *, timestep: Tensor, clip_text_embedding: Tensor, **_: Tensor) -> None:
        """Set the various context parameters required by the U-Net model.

        Args:
            timestep: The timestep tensor to use.
            clip_text_embedding: The CLIP text embedding tensor to use.
        """
        self.unet.set_timestep(timestep=timestep)
        self.unet.set_clip_text_embedding(clip_text_embedding=clip_text_embedding)

    def set_self_attention_guidance(self, enable: bool, scale: float = 1.0) -> None:
        """Set whether to enable self-attention guidance.

        See [[arXiv:2210.00939] Improving Sample Quality of Diffusion Models Using Self-Attention Guidance](https://arxiv.org/abs/2210.00939)
        for more details.

        Args:
            enable: Whether to enable self-attention guidance.
            scale: The scale to use.
        """
        if enable:
            if sag := self._find_sag_adapter():
                sag.scale = scale
            else:
                SD1SAGAdapter(target=self.unet, scale=scale).inject()
        else:
            if sag := self._find_sag_adapter():
                sag.eject()

    def has_self_attention_guidance(self) -> bool:
        """Whether the model has self-attention guidance or not."""
        return self._find_sag_adapter() is not None

    def _find_sag_adapter(self) -> SD1SAGAdapter | None:
        """Finds the self-attention guidance adapter, if any."""
        for p in self.unet.get_parents():
            if isinstance(p, SD1SAGAdapter):
                return p
        return None

    def compute_self_attention_guidance(
        self, x: Tensor, noise: Tensor, step: int, *, clip_text_embedding: Tensor, **kwargs: Tensor
    ) -> Tensor:
        """Compute the self-attention guidance.

        Args:
            x: The input tensor.
            noise: The noise tensor.
            step: The step to compute the self-attention guidance at.
            clip_text_embedding: The CLIP text embedding to compute the self-attention guidance with.

        Returns:
            The computed self-attention guidance.
        """
        sag = self._find_sag_adapter()
        assert sag is not None

        degraded_latents = sag.compute_degraded_latents(
            solver=self.solver,
            latents=x,
            noise=noise,
            step=step,
            classifier_free_guidance=True,
        )

        timestep = self.solver.timesteps[step].unsqueeze(dim=0)
        negative_embedding, _ = clip_text_embedding.chunk(2)
        self.set_unet_context(timestep=timestep, clip_text_embedding=negative_embedding, **kwargs)
        if "ip_adapter" in self.unet.provider.contexts:
            # this implementation is a bit hacky, it should be refactored in the future
            ip_adapter_context = self.unet.use_context("ip_adapter")
            image_embedding_copy = ip_adapter_context["clip_image_embedding"].clone()
            ip_adapter_context["clip_image_embedding"], _ = ip_adapter_context["clip_image_embedding"].chunk(2)
            degraded_noise = self.unet(degraded_latents)
            ip_adapter_context["clip_image_embedding"] = image_embedding_copy
        else:
            degraded_noise = self.unet(degraded_latents)

        return sag.scale * (noise - degraded_noise)


class StableDiffusion_1_Inpainting(StableDiffusion_1):
    """Stable Diffusion 1.5 inpainting model.

    Attributes:
        unet: The U-Net model.
        clip_text_encoder: The text encoder.
        lda: The image autoencoder.
    """

    def __init__(
        self,
        unet: SD1UNet | None = None,
        lda: SD1Autoencoder | None = None,
        clip_text_encoder: CLIPTextEncoderL | None = None,
        solver: Solver | None = None,
        device: Device | str = "cpu",
        dtype: DType = torch.float32,
    ) -> None:
        self.mask_latents: Tensor | None = None
        self.target_image_latents: Tensor | None = None
        super().__init__(
            unet=unet, lda=lda, clip_text_encoder=clip_text_encoder, solver=solver, device=device, dtype=dtype
        )

    def forward(
        self, x: Tensor, step: int, *, clip_text_embedding: Tensor, condition_scale: float = 7.5, **_: Tensor
    ) -> Tensor:
        assert self.mask_latents is not None
        assert self.target_image_latents is not None
        x = torch.cat(tensors=(x, self.mask_latents, self.target_image_latents), dim=1)
        return super().forward(
            x=x,
            step=step,
            clip_text_embedding=clip_text_embedding,
            condition_scale=condition_scale,
        )

    def set_inpainting_conditions(
        self,
        target_image: Image.Image,
        mask: Image.Image,
        latents_size: tuple[int, int] = (64, 64),
    ) -> tuple[Tensor, Tensor]:
        """Set the inpainting conditions.

        Args:
            target_image: The target image to inpaint.
            mask: The mask to use for inpainting.
            latents_size: The size of the latents to use.

        Returns:
            The mask latents and the target image latents.
        """
        target_image = target_image.convert(mode="RGB")
        mask = mask.convert(mode="L")

        mask_tensor = torch.tensor(data=np.array(object=mask).astype(dtype=np.float32) / 255.0).to(device=self.device)
        mask_tensor = (mask_tensor > 0.5).unsqueeze(dim=0).unsqueeze(dim=0).to(dtype=self.dtype)
        self.mask_latents = interpolate(x=mask_tensor, factor=torch.Size(latents_size))

        init_image_tensor = image_to_tensor(image=target_image, device=self.device, dtype=self.dtype) * 2 - 1
        masked_init_image = init_image_tensor * (1 - mask_tensor)
        self.target_image_latents = self.lda.encode(x=masked_init_image)

        return self.mask_latents, self.target_image_latents

    def compute_self_attention_guidance(
        self, x: Tensor, noise: Tensor, step: int, *, clip_text_embedding: Tensor, **kwargs: Tensor
    ) -> Tensor:
        """Compute the self-attention guidance.

        Args:
            x: The input tensor.
            noise: The noise tensor.
            step: The step to compute the self-attention guidance at.
            clip_text_embedding: The CLIP text embedding to compute the self-attention guidance with.

        Returns:
            The computed self-attention guidance.
        """
        sag = self._find_sag_adapter()
        assert sag is not None
        assert self.mask_latents is not None
        assert self.target_image_latents is not None

        degraded_latents = sag.compute_degraded_latents(
            solver=self.solver,
            latents=x,
            noise=noise,
            step=step,
            classifier_free_guidance=True,
        )
        x = torch.cat(
            tensors=(degraded_latents, self.mask_latents, self.target_image_latents),
            dim=1,
        )

        timestep = self.solver.timesteps[step].unsqueeze(dim=0)
        negative_embedding, _ = clip_text_embedding.chunk(2)
        self.set_unet_context(timestep=timestep, clip_text_embedding=negative_embedding, **kwargs)

        if "ip_adapter" in self.unet.provider.contexts:
            # this implementation is a bit hacky, it should be refactored in the future
            ip_adapter_context = self.unet.use_context("ip_adapter")
            image_embedding_copy = ip_adapter_context["clip_image_embedding"].clone()
            ip_adapter_context["clip_image_embedding"], _ = ip_adapter_context["clip_image_embedding"].chunk(2)
            degraded_noise = self.unet(x)
            ip_adapter_context["clip_image_embedding"] = image_embedding_copy
        else:
            degraded_noise = self.unet(x)

        return sag.scale * (noise - degraded_noise)
