
from discount_curve import DiscountCurve
from forecast_curve import ForecastCurve
from fixed_float_ir_swap import IRSwap
from pricer import price_swaps
from typing import Tuple, Dict

DiscountCurveID = str
IndexID = str
DiscountCurveDict = Dict[DiscountCurveID, DiscountCurve]
ForecastCurveDict = Dict[IndexID, ForecastCurve]

def single_trade_pv(t: Tuple[DiscountCurveID, IRSwap],
                    dc_dict: DiscountCurveDict,
                    fc_dict: ForecastCurveDict) -> float:
    trade = t[1]
    dc = dc_dict[t[0]]
    fc = fc_dict[trade.index_id()]
    pay_rec = 1 if trade.receives_fixed() else -1
    dfs = dc.discount_factors(trade.payment_dates())
    rates = fc.index_rates(trade.reset_dates())
    return sum(trade.notional() * pay_rec * (trade.fixed_coupon() - rates) * dfs)


def test_swap_pricer():

    dc1 = DiscountCurve.create_random()
    dc2 = DiscountCurve.create_random()
    dc3 = DiscountCurve.create_random()

    fc1 = ForecastCurve.create_random()
    fc2 = ForecastCurve.create_random()
    fc3 = ForecastCurve.create_random()

    dc_dict = {"USD.DISC.1": dc1, "USD.DISC.2": dc2, "USD.DISC.3": dc3}
    fc_dict = {"LIBOR3M": fc1, "LIBOR6M": fc2, "SOFR": fc3}

    t1 = IRSwap.create_random()
    t2 = IRSwap.create_random()
    t3 = IRSwap.create_random()
    t4 = IRSwap.create_random()
    t5 = IRSwap.create_random()
    t_dict = {
        "Trade1": ("USD.DISC.1", t1),
        "Trade2": ("USD.DISC.2", t2),
        "Trade3": ("USD.DISC.3", t3),
        "Trade4": ("USD.DISC.2", t4),
        "Trade5": ("USD.DISC.3", t5),
    }

    result = price_swaps(t_dict, dc_dict, fc_dict)
    assert len(result.columns) == 2
    assert result.columns.all() in ["TRADE_ID", "PV"]
    result["REL_DIFF"] = result.apply(
        lambda row: abs(single_trade_pv(t_dict[row.TRADE_ID], dc_dict, fc_dict) - row.PV)/ row.PV, axis=1)
    assert (result.REL_DIFF < 1.e-4).all()
