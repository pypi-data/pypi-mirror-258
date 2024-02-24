from meili_sdk.models.base import BaseModel
import typing as t

__all__ = ("VehicleSettingsMessage",)


class VehicleSettingsMessage(BaseModel):
    message_frequency: float
