from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Union

def get_date_span(*, anchor_date: Union[date, str], month_offset: int) -> tuple[date, date]:
    """
    Calculate a date span, returning the first and last day of a period.

    The function anchors to the provided date and calculates a new date by
    adding or subtracting months. It returns the first day of the earlier
    month and the last day of the later month (both dates inclusive).

    Args:
        anchor_date: The date to calculate from. Can be a date object or a
                     string in 'YYYY-MM-DD' format.
        month_offset: The number of months to offset from the anchor date.
                      Negative values (-12) go back in time.
                      Positive values (3) go forward in time.
                      Zero (0) returns the start and end of the anchor month.

    Returns:
        A tuple of two date objects: (period_start_date, period_end_date).
        Both dates are inclusive.

    Raises:
        TypeError: If anchor_date is not a date object or valid date string.
        ValueError: If anchor_date string is not in 'YYYY-MM-DD' format.

    Examples:
        >>> # Go BACK 12 months from a specific date
        >>> start, end = get_date_span(anchor_date='2026-01-10', month_offset=-12)
        >>> print(f"Going back 12 months: {start} to {end}")
        Going back 12 months: 2025-01-01 to 2026-01-31

        >>> # Go FORWARD 3 months from a specific date
        >>> start, end = get_date_span(anchor_date='2026-01-10', month_offset=3)
        >>> print(f"Going forward 3 months: {start} to {end}")
        Going forward 3 months: 2026-01-01 to 2026-04-30

        >>> # Get the current month (offset = 0)
        >>> start, end = get_date_span(anchor_date='2026-01-15', month_offset=0)
        >>> print(f"Current month: {start} to {end}")
        Current month: 2026-01-01 to 2026-01-31

        >>> # Handle leap years correctly
        >>> start, end = get_date_span(anchor_date='2024-01-15', month_offset=1)
        >>> print(f"Leap year February: {start} to {end}")
        Leap year February: 2024-01-01 to 2024-02-29
    """
    
    # Validate and convert the input date
    if isinstance(anchor_date, str):
        try:
            proc_anchor_date = date.fromisoformat(anchor_date)
        except ValueError as e:
            raise ValueError(
                f"anchor_date string must be in 'YYYY-MM-DD' format, got: '{anchor_date}'"
            ) from e
    elif isinstance(anchor_date, datetime):
        # Handle datetime objects by extracting the date part
        proc_anchor_date = anchor_date.date()
    elif isinstance(anchor_date, date):
        proc_anchor_date = anchor_date
    else:
        raise TypeError(
            f"anchor_date must be a date object or string in 'YYYY-MM-DD' format, "
            f"got type: {type(anchor_date).__name__}"
        )

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
