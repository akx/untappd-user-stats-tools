import collections
import json
import math
import sys

def print_histogram(values, bar_width=40):
    value_ctr = collections.Counter(values)
    max_value_num = max(value_ctr.values())
    for value, num in sorted(value_ctr.items()):
        bar = '*' * int(round(num / max_value_num * bar_width))
        print(f'{str(value):4} | {num:8} | {bar:{bar_width}} |')


def main():
    checkins = json.load(sys.stdin)
    ratings = [c['rating_score'] for c in checkins]
    ratings = [float(r) for r in ratings if r]
    avg_rating = sum(ratings) / len(ratings)
    variance = sum((r - avg_rating) ** 2 for r in ratings) / len(ratings)
    stdev = math.sqrt(variance)
    print(f'Average rating: {avg_rating}')
    print(f'       Std.dev: {stdev}')
    print_histogram(ratings)


if __name__ == '__main__':
    main()
