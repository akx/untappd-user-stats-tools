import json
import sys
from beerutil import group_by_day


def calculate_streaks(by_day, unstreaks=False):
    streak = None
    streaks = []
    for date, checkins in sorted(by_day.items()):
        if bool(checkins) != unstreaks:
            # The comparison above is a bit weird, but it basically hinges on
            # empty checkin lists being falsy in a boolean context.
            # If we're looking for unstreaks, days with checkins trigger a new
            # unstreak.  If we're looking for streaks, the days without checkins
            # trigger a new streak.
            if not streak:
                streak = []
                streaks.append(streak)
            streak.append((date, checkins))
        else:
            streak = None
    return streaks


def statsify_streak(streak):
    return {
        'length': len(streak),
        'count': sum(len(checkins) for (date, checkins) in streak),
        'streak': streak,
    }


def print_streak(name, streak_with_stats):
    bpd = streak_with_stats['count'] / streak_with_stats['length']
    length = streak_with_stats['length']
    count = streak_with_stats['count']
    start = streak_with_stats['streak'][0][0]
    end = streak_with_stats['streak'][-1][0]
    print(f'{name}: {start} .. {end}, length {length}, {count} total beers, {bpd} BPD')


def main():
    checkins = json.load(sys.stdin)
    by_day = group_by_day(checkins, fill=True)
    streaks = calculate_streaks(by_day)
    unstreaks = calculate_streaks(by_day, unstreaks=True)

    streaks_with_stats = [statsify_streak(streak) for streak in streaks]
    unstreaks_with_stats = [statsify_streak(unstreak) for unstreak in unstreaks]

    print_streak('Longest streak', max(streaks_with_stats, key=lambda s: s['length']))
    print_streak('Beeriest streak', max(streaks_with_stats, key=lambda s: s['count']))
    print_streak('Most efficient streak', max(streaks_with_stats, key=lambda s: s['count'] / s['length']))
    if unstreaks_with_stats:
        print_streak('Longest detox', max(unstreaks_with_stats, key=lambda s: s['length']))
    beeriest_day = max(by_day.items(), key=lambda p: len(p[1]))
    print(f'Beeriest day: {beeriest_day[0]}, {len(beeriest_day[1])} beers')


if __name__ == '__main__':
    main()
