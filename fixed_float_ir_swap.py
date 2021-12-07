
from typing import List
import datetime
import random


class IRSwap():

    def __init__(self,
                 ccy: str,
                 notional: float,
                 index_id: str,
                 fixed_coupon: float,
                 payment_dates: List[datetime.datetime],
                 reset_dates: List[datetime.datetime],
                 receives_fixed) -> None:
        self._ccy = ccy
        self._notional = notional
        self._index_id = index_id
        self._fixed_coupon = fixed_coupon
        self._payment_dates = payment_dates
        self._reset_dates = reset_dates
        self._receives_fixed = receives_fixed

    def ccy(self) -> str:
        return self._ccy

    def notional(self) -> float:
        return self._notional

    def index_id(self) -> str:
        return self._index_id

    def fixed_coupon(self) -> float:
        return self._fixed_coupon

    def payment_dates(self) -> List[datetime.datetime]:
        return self._payment_dates

    def reset_dates(self) -> List[datetime.datetime]:
        return self._reset_dates

    def receives_fixed(self) -> bool:
        return self._receives_fixed

    @classmethod
    def create_random(cls) -> "IRSwap":

        ccy = "USD"
        notional = random.randrange(1000000, 5000001)
        index_id = random.choice(["LIBOR3M", "LIBOR6M", "SOFR"])
        fixed_coupon = random.choice([0.01, 0.02, 0.03, 0.04, 0.05])
        days_in_coupon = random.choice([90, 180, 360])
        num_coupons = random.choice([10, 20, 30])
        payment_dates = [datetime.datetime.today() + datetime.timedelta(days=x*days_in_coupon) for x in range(1, num_coupons + 1)]
        reset_dates = [datetime.datetime.today() + datetime.timedelta(days=2) + datetime.timedelta(days=x*days_in_coupon) for x in range(0, num_coupons)]
        receives_fixed = random.choice([True, False])

        return cls(ccy, notional, index_id, fixed_coupon, payment_dates, reset_dates, receives_fixed)



if __name__ == "__main__":
    t = IRSwap.create_random()
    assert t.ccy() == "USD"