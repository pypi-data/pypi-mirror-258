import typing as tp
from stsp.protocols.predict.prediction import PredictionProtocol
from stsp.protocols.position.open_position import OpenPositionProtocol
from stsp.protocols.position.close_position import ClosePositionProtocol
from stsp.protocols.risk.risk import RiskProtocol
from stsp.protocols.limits.limit import LimitProtocol


class StrategyProtocol(tp.Protocol):
    """Protocol of strategy"""

    @property
    async def name(self) -> str:
        """"""

    async def limits(self) -> LimitProtocol:
        """"""

    async def predict(self) -> PredictionProtocol:
        """"""

    async def open_position(self) -> OpenPositionProtocol:
        """"""

    async def close_position(self) -> ClosePositionProtocol:
        """"""

    async def risk(self) -> RiskProtocol:
        """"""
