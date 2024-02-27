import random
from enum import Enum
from functools import wraps
from typing import Any, Callable, Iterable

import numpy as np
import torch
from loguru import logger
from torch import Tensor, cuda, nn
from typing_extensions import TypedDict

from refiners.fluxion.utils import manual_seed


def compute_grad_norm(parameters: Iterable[nn.Parameter]) -> float:
    """
    Computes the gradient norm of the parameters of a given model similar to `clip_grad_norm_` returned value.
    """
    gradients: list[Tensor] = [p.grad.detach() for p in parameters if p.grad is not None]
    assert gradients, "The model has no gradients to compute the norm."
    total_norm = torch.stack(tensors=[gradient.norm() for gradient in gradients]).norm().item()  # type: ignore
    return total_norm  # type: ignore


def count_learnable_parameters(parameters: Iterable[nn.Parameter]) -> int:
    return sum(p.numel() for p in parameters if p.requires_grad)


def human_readable_number(number: int) -> str:
    float_number = float(number)
    for unit in ["", "K", "M", "G", "T", "P"]:
        if abs(float_number) < 1000:
            return f"{float_number:.1f}{unit}"
        float_number /= 1000
    return f"{float_number:.1f}E"


def seed_everything(seed: int | None = None) -> None:
    if seed is None:
        seed = random.randint(0, 2**32 - 1)
        logger.info(f"Using random seed: {seed}")
    random.seed(a=seed)
    np.random.seed(seed=seed)
    manual_seed(seed=seed)
    cuda.manual_seed_all(seed=seed)


def scoped_seed(seed: int | Callable[..., int] | None = None) -> Callable[..., Callable[..., Any]]:
    """
    Decorator for setting a random seed within the scope of a function.

    This decorator sets the random seed for Python's built-in `random` module,
    `numpy`, and `torch` and `torch.cuda` at the beginning of the decorated function. After the
    function is executed, it restores the state of the random number generators
    to what it was before the function was called. This is useful for ensuring
    reproducibility for specific parts of the code without affecting randomness
    elsewhere.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def inner_wrapper(*args: Any, **kwargs: Any) -> Any:
            random_state = random.getstate()
            numpy_state = np.random.get_state()
            torch_state = torch.get_rng_state()
            cuda_torch_state = cuda.get_rng_state()
            actual_seed = seed(*args) if callable(seed) else seed
            seed_everything(seed=actual_seed)
            result = func(*args, **kwargs)
            random.setstate(random_state)
            np.random.set_state(numpy_state)
            torch.set_rng_state(torch_state)
            cuda.set_rng_state(cuda_torch_state)
            return result

        return inner_wrapper

    return decorator


class TimeUnit(Enum):
    STEP = "step"
    EPOCH = "epoch"
    ITERATION = "iteration"
    DEFAULT = "step"


class TimeValue(TypedDict):
    number: int
    unit: TimeUnit


def parse_number_unit_field(value: str | int | dict[str, str | int]) -> TimeValue:
    match value:
        case str(value_str):
            number, unit = value_str.split(sep=":")
            return {"number": int(number.strip()), "unit": TimeUnit(value=unit.strip().lower())}
        case int(number):
            return {"number": number, "unit": TimeUnit.DEFAULT}
        case {"number": int(number), "unit": str(unit)}:
            return {"number": number, "unit": TimeUnit(value=unit.lower())}
        case _:
            raise ValueError(f"Unsupported value format: {value}")
