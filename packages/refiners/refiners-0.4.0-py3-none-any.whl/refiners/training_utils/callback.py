from typing import TYPE_CHECKING, Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from refiners.training_utils.config import BaseConfig
    from refiners.training_utils.trainer import Trainer

T = TypeVar("T", bound="Trainer[BaseConfig, Any]")


class CallbackConfig(BaseModel):
    """
    Base configuration for a callback.

    For your callback to be properly configured, you should inherit from this class and add your own configuration.
    """

    model_config = ConfigDict(extra="forbid")


class Callback(Generic[T]):
    def on_init_begin(self, trainer: T) -> None:
        ...

    def on_init_end(self, trainer: T) -> None:
        ...

    def on_train_begin(self, trainer: T) -> None:
        ...

    def on_train_end(self, trainer: T) -> None:
        ...

    def on_epoch_begin(self, trainer: T) -> None:
        ...

    def on_epoch_end(self, trainer: T) -> None:
        ...

    def on_batch_begin(self, trainer: T) -> None:
        ...

    def on_batch_end(self, trainer: T) -> None:
        ...

    def on_backward_begin(self, trainer: T) -> None:
        ...

    def on_backward_end(self, trainer: T) -> None:
        ...

    def on_optimizer_step_begin(self, trainer: T) -> None:
        ...

    def on_optimizer_step_end(self, trainer: T) -> None:
        ...

    def on_compute_loss_begin(self, trainer: T) -> None:
        ...

    def on_compute_loss_end(self, trainer: T) -> None:
        ...

    def on_evaluate_begin(self, trainer: T) -> None:
        ...

    def on_evaluate_end(self, trainer: T) -> None:
        ...

    def on_lr_scheduler_step_begin(self, trainer: T) -> None:
        ...

    def on_lr_scheduler_step_end(self, trainer: T) -> None:
        ...
