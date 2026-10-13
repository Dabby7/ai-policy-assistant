from decimal import Decimal, ROUND_HALF_UP

def money(value):
    return Decimal(str(value)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

def calculate_upi_fee(amount, monthly_volume, as_of_date):
    amount = Decimal(str(amount))
    volume = Decimal(str(monthly_volume))
    date = str(as_of_date)

    if date >= "2026-08-01":
        cap_small, cap_large = Decimal("15"), Decimal("25")
        rate_small = Decimal("0.0025")
    else:
        cap_small, cap_large = Decimal("15"), Decimal("15")
        rate_small = Decimal("0.003")

    if volume <= Decimal("1000000"):
        mdr = min(amount * rate_small, cap_small)
    else:
        mdr = min(amount * Decimal("0.005"), cap_large)

    mdr = money(mdr)
    gst = money(mdr * Decimal("0.18"))

    return {
        "mdr": mdr,
        "gst": gst,
        "total_fee": money(mdr + gst),
    }