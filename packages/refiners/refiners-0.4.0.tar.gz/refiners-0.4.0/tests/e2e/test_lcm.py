import gc
from pathlib import Path
from warnings import warn

import pytest
import torch
from PIL import Image

from refiners.fluxion.utils import load_from_safetensors, manual_seed, no_grad
from refiners.foundationals.latent_diffusion.lora import SDLoraManager
from refiners.foundationals.latent_diffusion.solvers import LCMSolver
from refiners.foundationals.latent_diffusion.stable_diffusion_xl.lcm import SDXLLcmAdapter
from refiners.foundationals.latent_diffusion.stable_diffusion_xl.lcm_lora import add_lcm_lora
from refiners.foundationals.latent_diffusion.stable_diffusion_xl.model import StableDiffusion_XL
from tests.utils import ensure_similar_images


@pytest.fixture(autouse=True)
def ensure_gc():
    # Avoid GPU OOMs
    # See https://github.com/pytest-dev/pytest/discussions/8153#discussioncomment-214812
    gc.collect()


@pytest.fixture
def sdxl_lda_fp16_fix_weights(test_weights_path: Path) -> Path:
    r = test_weights_path / "sdxl-lda-fp16-fix.safetensors"
    if not r.is_file():
        warn(f"could not find weights at {r}, skipping")
        pytest.skip(allow_module_level=True)
    return r


@pytest.fixture
def sdxl_unet_weights(test_weights_path: Path) -> Path:
    r = test_weights_path / "sdxl-unet.safetensors"
    if not r.is_file():
        warn(f"could not find weights at {r}, skipping")
        pytest.skip(allow_module_level=True)
    return r


@pytest.fixture
def sdxl_lcm_unet_weights(test_weights_path: Path) -> Path:
    r = test_weights_path / "sdxl-lcm-unet.safetensors"
    if not r.is_file():
        warn(f"could not find weights at {r}, skipping")
        pytest.skip(allow_module_level=True)
    return r


@pytest.fixture
def sdxl_text_encoder_weights(test_weights_path: Path) -> Path:
    r = test_weights_path / "DoubleCLIPTextEncoder.safetensors"
    if not r.is_file():
        warn(f"could not find weights at {r}, skipping")
        pytest.skip(allow_module_level=True)
    return r


@pytest.fixture
def sdxl_lcm_lora_weights(test_weights_path: Path) -> Path:
    r = test_weights_path / "sdxl-lcm-lora.safetensors"
    if not r.is_file():
        warn(f"could not find weights at {r}, skipping")
        pytest.skip(allow_module_level=True)
    return r


@pytest.fixture(scope="module")
def ref_path(test_e2e_path: Path) -> Path:
    return test_e2e_path / "test_lcm_ref"


@pytest.fixture
def expected_lcm_base(ref_path: Path) -> Image.Image:
    return Image.open(ref_path / "expected_lcm_base.png").convert("RGB")


@pytest.fixture
def expected_lcm_lora_1_0(ref_path: Path) -> Image.Image:
    return Image.open(ref_path / "expected_lcm_lora_1_0.png").convert("RGB")


@pytest.fixture
def expected_lcm_lora_1_2(ref_path: Path) -> Image.Image:
    return Image.open(ref_path / "expected_lcm_lora_1_2.png").convert("RGB")


@no_grad()
def test_lcm_base(
    test_device: torch.device,
    sdxl_lda_fp16_fix_weights: Path,
    sdxl_lcm_unet_weights: Path,
    sdxl_text_encoder_weights: Path,
    expected_lcm_base: Image.Image,
) -> None:
    if test_device.type == "cpu":
        warn(message="not running on CPU, skipping")
        pytest.skip()

    solver = LCMSolver(num_inference_steps=4)
    sdxl = StableDiffusion_XL(device=test_device, dtype=torch.float16, solver=solver)
    sdxl.classifier_free_guidance = False

    # With standard LCM the condition scale is passed to the adapter,
    # not in the diffusion loop.
    SDXLLcmAdapter(sdxl.unet, condition_scale=8.0).inject()

    sdxl.clip_text_encoder.load_from_safetensors(sdxl_text_encoder_weights)
    sdxl.lda.load_from_safetensors(sdxl_lda_fp16_fix_weights)
    sdxl.unet.load_from_safetensors(sdxl_lcm_unet_weights)

    prompt = "Self-portrait oil painting, a beautiful cyborg with golden hair, 8k"
    expected_image = expected_lcm_base

    # *NOT* compute_clip_text_embedding! We disable classifier-free guidance.
    clip_text_embedding, pooled_text_embedding = sdxl.clip_text_encoder(prompt)
    time_ids = sdxl.default_time_ids

    manual_seed(2)
    x = sdxl.init_latents((1024, 1024)).to(sdxl.device, sdxl.dtype)

    for step in sdxl.steps:
        x = sdxl(
            x,
            step=step,
            clip_text_embedding=clip_text_embedding,
            pooled_text_embedding=pooled_text_embedding,
            time_ids=time_ids,
        )
    predicted_image = sdxl.lda.latents_to_image(x)

    ensure_similar_images(predicted_image, expected_image, min_psnr=35, min_ssim=0.98)


@no_grad()
@pytest.mark.parametrize("condition_scale", [1.0, 1.2])
def test_lcm_lora_with_guidance(
    test_device: torch.device,
    sdxl_lda_fp16_fix_weights: Path,
    sdxl_unet_weights: Path,
    sdxl_text_encoder_weights: Path,
    sdxl_lcm_lora_weights: Path,
    expected_lcm_lora_1_0: Image.Image,
    expected_lcm_lora_1_2: Image.Image,
    condition_scale: float,
) -> None:
    if test_device.type == "cpu":
        warn(message="not running on CPU, skipping")
        pytest.skip()

    solver = LCMSolver(num_inference_steps=4)
    sdxl = StableDiffusion_XL(device=test_device, dtype=torch.float16, solver=solver)

    sdxl.clip_text_encoder.load_from_safetensors(sdxl_text_encoder_weights)
    sdxl.lda.load_from_safetensors(sdxl_lda_fp16_fix_weights)
    sdxl.unet.load_from_safetensors(sdxl_unet_weights)

    manager = SDLoraManager(sdxl)
    add_lcm_lora(manager, load_from_safetensors(sdxl_lcm_lora_weights))

    prompt = "Self-portrait oil painting, a beautiful cyborg with golden hair, 8k"
    expected_image = expected_lcm_lora_1_0 if condition_scale == 1.0 else expected_lcm_lora_1_2

    # *NOT* clip_text_encoder! We use classifier-free guidance here.
    clip_text_embedding, pooled_text_embedding = sdxl.compute_clip_text_embedding(prompt)
    time_ids = sdxl.default_time_ids
    assert time_ids.shape == (2, 6)  # CFG

    manual_seed(2)
    x = sdxl.init_latents((1024, 1024)).to(sdxl.device, sdxl.dtype)

    for step in sdxl.steps:
        x = sdxl(
            x,
            step=step,
            clip_text_embedding=clip_text_embedding,
            pooled_text_embedding=pooled_text_embedding,
            time_ids=time_ids,
            condition_scale=condition_scale,
        )
    predicted_image = sdxl.lda.latents_to_image(x)

    psnr = 35 if condition_scale == 1.0 else 33
    ensure_similar_images(predicted_image, expected_image, min_psnr=psnr, min_ssim=0.98)


@no_grad()
def test_lcm_lora_without_guidance(
    test_device: torch.device,
    sdxl_lda_fp16_fix_weights: Path,
    sdxl_unet_weights: Path,
    sdxl_text_encoder_weights: Path,
    sdxl_lcm_lora_weights: Path,
    expected_lcm_lora_1_0: Image.Image,
) -> None:
    if test_device.type == "cpu":
        warn(message="not running on CPU, skipping")
        pytest.skip()

    solver = LCMSolver(num_inference_steps=4)
    sdxl = StableDiffusion_XL(device=test_device, dtype=torch.float16, solver=solver)
    sdxl.classifier_free_guidance = False

    sdxl.clip_text_encoder.load_from_safetensors(sdxl_text_encoder_weights)
    sdxl.lda.load_from_safetensors(sdxl_lda_fp16_fix_weights)
    sdxl.unet.load_from_safetensors(sdxl_unet_weights)

    manager = SDLoraManager(sdxl)
    add_lcm_lora(manager, load_from_safetensors(sdxl_lcm_lora_weights))

    prompt = "Self-portrait oil painting, a beautiful cyborg with golden hair, 8k"
    expected_image = expected_lcm_lora_1_0

    # *NOT* compute_clip_text_embedding! We disable classifier-free guidance.
    clip_text_embedding, pooled_text_embedding = sdxl.clip_text_encoder(prompt)
    time_ids = sdxl.default_time_ids
    assert time_ids.shape == (1, 6)  # no CFG

    manual_seed(2)
    x = sdxl.init_latents((1024, 1024)).to(sdxl.device, sdxl.dtype)

    for step in sdxl.steps:
        x = sdxl(
            x,
            step=step,
            clip_text_embedding=clip_text_embedding,
            pooled_text_embedding=pooled_text_embedding,
            time_ids=time_ids,
            condition_scale=0.0,
        )
    predicted_image = sdxl.lda.latents_to_image(x)

    ensure_similar_images(predicted_image, expected_image, min_psnr=35, min_ssim=0.98)
