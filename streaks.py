import json
import sys
from beerutil import group_by_day


def calculate_streaks(checkins):
    by_day = group_by_day(checkins, fill=True)
    streak = None
    streaks = []
    for date, checkins in sorted(by_day.items()):
        if len(checkins) > 0:
            if not streak:
                streak = []
                streaks.append(streak)
            streak.append((date, checkins))
        else:
            streak = None
    return streaks


def print_streak(name, streak_with_stats):
    bpd = streak_with_stats['count'] / streak_with_stats['length']
    length = streak_with_stats['length']
    count = streak_with_stats['count']
    start = streak_with_stats['streak'][0][0]
    end = streak_with_stats['streak'][-1][0]
    print(f'{name}: {start} .. {end}, length {length}, {count} total beers, {bpd} BPD')


def main():
    data = json.load(sys.stdin)
    streaks = calculate_streaks(data)

    streaks_with_stats = [
        {
            'length': len(streak),
            'count': sum(len(checkins) for (date, checkins) in streak),
            'streak': streak,
        }
        for streak
        in streaks
    ]

    print_streak('Longest streak', max(streaks_with_stats, key=lambda s: s['length']))
    print_streak('Beeriest streak', max(streaks_with_stats, key=lambda s: s['count']))
    print_streak('Most efficient streak', max(streaks_with_stats, key=lambda s: s['count'] / s['length']))


if __name__ == '__main__':
    main()
