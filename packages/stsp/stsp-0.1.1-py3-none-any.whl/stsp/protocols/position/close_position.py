import typing as tp

from protocols.models.common import OHLC
from stsp.protocols.position.models import ExitPointResponse
from stsp.protocols.predict.models import PredictResponse


class ClosePositionProtocol(tp.Protocol):
    async def definition_exit_point(
        self,
        *,
        figi: str,
        currnet_ohls: OHLC,
        prediction: PredictResponse,
    ) -> ExitPointResponse:
        """Provide position exit point"""
