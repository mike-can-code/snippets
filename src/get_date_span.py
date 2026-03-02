from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from typing import Union, Tuple

def get_date_span(*, anchor_date: Union[date, str], month_offset: int) -> Tuple[date, date]:
    """
    Calculates a date span, returning the first day and last day of a period.

    The function anchors itself to the provided date and calculates a new date by
    adding or subtracting a number of months. It then returns the first day of the
    earlier month and the last day of the later month.

    Args:
        anchor_date: The date to calculate from. Can be a date object or a
                     string in 'YYYY-MM-DD' format.
        month_offset: The number of months to offset from the anchor date.
                      A negative integer (-12) goes back in time.
                      A positive integer (3) goes forward in time.
                      Zero (0) results in the start and end of the anchor month.

    Returns:
        A tuple containing two date objects: (period_start_date, period_end_date).

    Examples:
        >>> # Go BACK 12 months from a specific date
        >>> start, end = get_date_span(anchor_date='2026-01-10', month_offset=-12)
        >>> print(f"Going back 12 months: {start} to {end}")
        Going back 12 months: 2025-01-01 to 2026-01-31

        >>> # Go FORWARD 3 months from a specific date
        >>> start, end = get_date_span(anchor_date='2026-01-10', month_offset=3)
        >>> print(f"Going forward 3 months: {start} to {end}")
        Going forward 3 months: 2026-01-01 to 2026-04-30
    """
    
    # Validate and convert the input date
    if isinstance(anchor_date, str):
        proc_anchor_date = date.fromisoformat(anchor_date)
    elif isinstance(anchor_date, date):
        proc_anchor_date = anchor_date
    else:
        raise TypeError("anchor_date must be a date object or a string in 'YYYY-MM-DD' format.")

    # Calculate the target date based on the offset
    target_date = proc_anchor_date + relativedelta(months=month_offset)

    # Determine which date is earlier and which is later
    start_ref_date = min(proc_anchor_date, target_date)
    end_ref_date = max(proc_anchor_date, target_date)

    # Calculate the first day of the start month
    period_start_date = start_ref_date.replace(day=1)

    # Calculate the last day of the end month
    first_day_of_next_month = end_ref_date.replace(day=1) + relativedelta(months=1)
    period_end_date = first_day_of_next_month - timedelta(days=1)

    return period_start_date, period_end_date

