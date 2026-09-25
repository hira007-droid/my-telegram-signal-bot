# timing.py
# ------------------------------------------------------------------
# Turns "what time is it in Paris?" into a traffic-light label, using
# your trading_timing document. All times are Paris time. Python
# handles summer/winter clock changes automatically.
# ------------------------------------------------------------------
from datetime import datetime
from zoneinfo import ZoneInfo   # needs:  pip install tzdata   (on Windows)

TZ = ZoneInfo("Europe/Paris")


def now_paris():
    """Current date and time in Paris."""
    return datetime.now(TZ)


def time_window(dt):
    """Return (emoji, text_key) for a Paris datetime.
    text_key is a name from texts.py, so it is translated for you."""
    weekday = dt.weekday()             # Monday = 0 ... Sunday = 6
    hour = dt.hour + dt.minute / 60    # 14:30 becomes 14.5

    if weekday >= 5:                                   # Saturday, Sunday
        return "🔴", "win_weekend"
    if weekday == 0 and 9 <= hour < 10:                # Monday market open
        return "🔴", "win_avoid_monday"
    if weekday == 4 and hour >= 17:                    # Friday after 17:00
        return "🔴", "win_avoid_friday"
    if 14 <= hour < 17:                                # London-NY overlap
        return "🟢", "win_best"
    if 9 <= hour < 12:                                 # London morning
        return "🟡", "win_ok"
    if 12 <= hour < 14:                                # lunch, slow market
        return "🟠", "win_slow"
    return "🔴", "win_closed"                          # everything else
