
from typing import List
import datetime
from scipy.interpolate import interp1d
import random
import numpy as np


class DiscountCurve():

    def __init__(self,
                 rates: List[float],
                 dates: List[datetime.datetime]) -> None:
        self._today = dates[0]
        self._rates = rates
        self._dates = dates
        self._dates_as_ints = [int(x.strftime("%Y%m%d")) for x in dates]
        self._interpolator = interp1d(self._dates_as_ints, self._rates)

    def discount_factors(self, dates: List[datetime.datetime]) -> List[float]:
        dates_as_ints = [int(x.strftime("%Y%m%d")) for x in dates]
        rates = self._interpolator(dates_as_ints)
        dcfs = [(x - self._today).days / 365.0 for x in dates]
        return np.exp(-rates*dcfs)

    @classmethod
    def create_random(cls) -> "IRSwap":
        num_coupons = 240  # 60 years, 4 rates a year
        days_in_coupon = 90
        dates = [datetime.datetime.today() + datetime.timedelta(days=x * days_in_coupon) for x in range(0, num_coupons+1)]
        rate_base = random.choice([0.01, 0.02, 0.03, 0.04, 0.05])
        rates = [rate_base + 0.001 * random.random() for x in range(0, num_coupons+1)]

        return cls(rates, dates)


if __name__ == "__main__":
    dc = DiscountCurve.create_random()
    dates = [datetime.datetime.today() + datetime.timedelta(days=x * 47) for x in range(0, 30)]
    dfs = dc.discount_factors(dates)
    assert len(dfs) == 30