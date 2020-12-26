from version import get_version as version

if __name__ == "__main__":

    from AoC import Day
    import argparse
    import datetime
    from typing import Tuple, List

    this_year = datetime.datetime.now().year

    parser = argparse.ArgumentParser(prog="AoC2020",
                                     description=f"Implementation for AoC2020 made by me :). Version {version()}")
    parser.add_argument("--only-last", action="store_true", required=False, dest="only_last",
                        help="Only run latest Day that has been implemented. Overrides -y and -d")
    parser.add_argument("--no-log", action="store_true", required=False, dest="no_log",
                        help="Dont show log messages for Day")
    parser.add_argument("-v", "--version", action="store_true", required=False, dest="show_version",
                        help="Show version")
    parser.add_argument("-y", "--year", dest="aoc_year", required=False, type=int, default=this_year,
                        help=f"Year of AoC you want to run [Default: {this_year}]")
    parser.add_argument("-d", "--day", dest="aoc_day", required=False, type=int, default=None,
                        help="Day of AoC you want to run. Runs all days of year if none is given")
    args = parser.parse_args()

    if args.show_version:
        print(f"Version {version()}")
        exit(0)

    implemented_days = list(Day.Day.iterate_days())
    if args.only_last:
        implemented_days = implemented_days[-1:]
    elif args.aoc_day is not None:
        implemented_days = [x for x in implemented_days if x.get_day() == args.aoc_day]

    day_times: List[Tuple[Day.Day, float, bool]] = []

    for day in implemented_days:
        log, results, duration = day.run_all(show_log=not args.no_log)
        print(log)
        day_times.append((day, sum(duration.values()), any(x is not None for x in results.values())))

    if not any(x[2] for x in day_times):
        print("")
        print("No Day produced a result. SAAAAAAAAAAAAAAD")
    elif len(implemented_days) > 1:
        print("")
        print(
            f"Execution of Days {', '.join(str(x.get_day()) for x in implemented_days)} "
            f"took {datetime.timedelta(seconds=sum(x[1] for x in day_times))}")
        fast_slow = sorted((x for x in day_times if x[2]), key=lambda y: y[1])
        print(f"Fastest*: {fast_slow[0][0].get_name()} at {datetime.timedelta(seconds=fast_slow[0][1])}")
        print(f"Slowest*: {fast_slow[-1][0].get_name()} at {datetime.timedelta(seconds=fast_slow[-1][1])}")
        print("*Only Days that produced at least one result are considered in the fastest and slowest competition")
