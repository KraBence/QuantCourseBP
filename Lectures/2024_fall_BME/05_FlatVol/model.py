from __future__ import annotations
from abc import ABC, abstractmethod

from scipy.constants import point

from market_data import *
from enums import *
import numpy as np


# TASK:
# Implement BSVol and FlatVol models in the pricing library


class MarketModel(ABC):
    def __init__(self, underlying: Stock) -> None:
        self.underlying: Stock = underlying
        self.risk_free_rate: float = MarketData.get_risk_free_rate()
        self.spot: float = MarketData.get_spot()[self.underlying]
        self.volgrid: VolGrid = MarketData.get_volgrid()[self.underlying]

    def bump_rate(self, bump_size: float) -> None:
        self.risk_free_rate += bump_size

    def bump_spot(self, bump_size: float) -> None:
        self.spot += bump_size

    def bump_volgrid(self, bump_size: float) -> None:
        self.volgrid.values += bump_size

    def calc_df(self, tenor: float) -> float:
        return np.exp(-1.0 * self.risk_free_rate * tenor)

    @abstractmethod
    def get_vol(self, strike: float, expiry: float) -> float:
        pass


class BSVolModel(MarketModel):
    def __init__(self, underlying: Stock) -> None:
        super().__init__(underlying)

    def get_vol(self, strike: float, expiry: float) -> float:
        atm_strike = 1.0 * self.spot
        expiry = 1.0
        coordinate = np.array([(atm_strike, expiry)])
        return self.volgrid.get_vol(coordinate)[0]


class FlatVolModel(MarketModel):
    def __init__(self, underlying: Stock) -> None:
        super().__init__(underlying)

    def get_vol(self, strike: float, expiry: float) -> float:
        coordinate = np.array([(strike, expiry)])
        return self.volgrid.get_vol(coordinate)[0]