import datetime
from collections import defaultdict


ISO8601_DATE_FORMAT = '%Y-%m-%d'


def parse_iso8601_date(datestr):
    return datetime.datetime.strptime(datestr, '%Y-%m-%d').date()


def group_by_day(checkins, fill=False):
    by_day = defaultdict(list)
    for checkin in checkins:
        by_day[parse_iso8601_date(checkin['created_at'][:10])].append(checkin)

    if fill:
        # Fill in blanks.
        day = min(by_day.keys())
        last_day = max(by_day.keys())
        while day < last_day:
            by_day.setdefault(day, [])
            day += datetime.timedelta(days=1)

    return by_day
