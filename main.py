if __name__ == "__main__":

    import Day
    import argparse

    parser = argparse.ArgumentParser(prog="AoC2020")
    parser.add_argument("--only-last", action="store_true", required=False, dest="only_last",
                        help="Only run latest Day that has been implemented")
    parser.add_argument("--no-log", action="store_true", required=False, dest="no_log",
                        help="Dont show log messages for Day")
    args = parser.parse_args()

    implemented_days = list(Day.Day.iterate_days())
    if args.only_last:
        implemented_days = implemented_days[-1:]

    for day in implemented_days:
        log, results, duration = day.run_all(show_log=not args.no_log)
        print(log)
