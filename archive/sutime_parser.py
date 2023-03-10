import json
from sutime import SUTime

if __name__ == '__main__':
    sutime = SUTime(mark_time_ranges=True, include_range=True)
    for test_case in [
        'Tomorrow at 11am',
        'This coming Tuesday at 9pm',
        'Next Tuesday at 9pm',
            'Teuesdey oif Nexx weak att 9 pm']:
        print(json.dumps(sutime.parse(test_case), sort_keys=True, indent=4))
