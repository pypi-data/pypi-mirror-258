"""Protocol for predict"""

import typing as tp

from stsp.protocols.models.common import OHLC
from stsp.protocols.predict.models import PredictResponse


class PredictionProtocol(tp.Protocol):
    async def predict(
        self,
        *,
        figi: str,
        current_ohlc: OHLC,
    ) -> list[PredictResponse]:
        """Predcit next N prices"""
