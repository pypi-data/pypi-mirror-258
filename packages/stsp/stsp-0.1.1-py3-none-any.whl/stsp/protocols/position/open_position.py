import typing as tp

from protocols.models.common import OHLC
from stsp.protocols.position.models import EntryPointResponse
from stsp.protocols.predict.models import PredictResponse


class OpenPositionProtocol(tp.Protocol):
    async def definition_entry_point(
        self,
        *,
        figi: str,
        currnet_ohls: OHLC,
        prediction: PredictResponse,
    ) -> EntryPointResponse:
        """Provide position entry point"""
