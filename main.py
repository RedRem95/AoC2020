from version import get_version as version

if __name__ == "__main__":

    from AoC import Day
    import argparse
    import datetime
    from typing import Tuple, Optional
    from math import inf

    parser = argparse.ArgumentParser(prog="AoC2020",
                                     description=f"Implementation for AoC2020 made by me :). Version {version()}")
    parser.add_argument("--only-last", action="store_true", required=False, dest="only_last",
                        help="Only run latest Day that has been implemented")
    parser.add_argument("--no-log", action="store_true", required=False, dest="no_log",
                        help="Dont show log messages for Day")
    parser.add_argument("-v", "--version", action="store_true", required=False, dest="show_version",
                        help="Show version")
    args = parser.parse_args()

    if args.show_version:
        print(f"Version {version()}")
        exit(0)

    implemented_days = list(Day.Day.iterate_days())
    if args.only_last:
        implemented_days = implemented_days[-1:]

    all_time = 0
    fastest: Tuple[Optional[Day.Day], float] = (None, inf)

    for day in implemented_days:
        log, results, duration = day.run_all(show_log=not args.no_log)
        print(log)
        if not all(x is None for x in results.values()):
            comb_time = sum(duration.values())
            all_time += comb_time
            if fastest[0] is None or comb_time < fastest[1]:
                fastest = (day, comb_time)

    if fastest[0] is None:
        print("")
        print("No Day produced a result. SAAAAAAAAAAAAAAD")
    elif len(implemented_days) > 1:
        print("")
        print(
            f"Execution of Days {', '.join(str(x.get_day()) for x in implemented_days)} took {datetime.timedelta(seconds=all_time)}")
        print(f"Fastest*: {fastest[0].get_name()} at {datetime.timedelta(seconds=fastest[1])}")
        print("*Only Days that produced at least one result are considered in the fastest competition")
