import datetime
import argparse


def read_data_from_file(file):
    with open(file, "r") as f:
        content = f.read().splitlines()
    return content


def abbreviation_file_list(content):
    abbreviations = []
    for line in content:
        sep_data = line.split("_")
        abbreviations.append(sep_data)
    return abbreviations


def time_file_list(content):
    formatted_lines = []
    for line in content:
        sep_data = line.split("_")
        abb = sep_data[0][:3]
        start_date = sep_data[0][3:]
        start_time = sep_data[1]
        obj = [abb, start_date, start_time]
        formatted_lines.append(obj)
    return formatted_lines


def count_time(starts, finishes):
    delta_times = []
    for start_line in starts:
        for finish_line in finishes:
            if finish_line[0] == start_line[0]:
                format = "%I:%M:%S.%f"
                t1 = datetime.datetime.strptime(start_line[2], format)
                t2 = datetime.datetime.strptime(finish_line[2], format)
                time = t2 - t1
                line = [start_line[0], time]
                delta_times.append(line)
                break
    return delta_times


def built_report(delta_times, racers, parser):
    for time in delta_times:
        for racer in racers:
            if racer[0] == time[0]:
                racer.remove(racer[0])
                racer.append(time[1])
                break

    racers_sorted = []
    if parser.driver:
        for racer in racers:
            if racer[0] == parser.driver:
                return [racer]
    elif parser.desc:
        racers_sorted = sorted(racers, key=lambda x: - x[2])
    else:
        racers_sorted = sorted(racers, key=lambda x: x[2])

    return racers_sorted


def print_report(racers_sorted, limit):
    for place, racer in enumerate(racers_sorted, start=1):
        print("{0}. {1}| {2}| {3}".format(place, racer[0], racer[1], racer[2]))
        if limit == place:
            print("-" * 74)


def main():
    parser = argparse.ArgumentParser(prog="Report Generator",
                                     description="This tool will show results of racers at Q1 stage of "
                                                 "Formula 1 - Monaco 2018 Racing")
    parser.add_argument("--start_data_file", type=str,
                        help="Enter the path to the file with start data", metavar="PATH TO START DATA",
                        default="..\\data\\start.log")
    parser.add_argument("--finish_data_file", type=str,
                        help="Enter the path to the file with finish data", metavar="PATH TO FINISH DATA",
                        default="..\\data\\end.log")
    parser.add_argument("--abbreviations_file", type=str,
                        help="Enter the path to the file with abbreviations data", metavar="PATH TO ABBREVIATIONS DATA",
                        default="..\\data\\abbreviations.txt")
    parser.add_argument("--driver", type=str, help="Enter the name of the driver you want to know statistic about, "
                                                       "e.g. 'Sebastian Vettel'", metavar="NAME")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--asc", action="store_true", help="Enter 'asc' if you prefer to see the list of results in "
                                                          "ascending order")
    group.add_argument("--desc", action="store_true", help="Enter 'desc' if you prefer to see the list of results in "
                                                           "descending order")
    parser.add_argument("--limit", help="Number of racers going to the next stage", default=15)

    args = parser.parse_args()

    start_data = read_data_from_file(args.start_data_file)
    start_data_parsed = time_file_list(start_data)

    finish_data = read_data_from_file(args.finish_data_file)
    finish_data_parsed = time_file_list(finish_data)

    time_parsed = count_time(start_data_parsed, finish_data_parsed)

    abbreviations = read_data_from_file(args.abbreviations_file)
    abbreviations_parsed = abbreviation_file_list(abbreviations)

    report = built_report(time_parsed, abbreviations_parsed, args)

    print_report(report, args.limit)


if __name__ == "__main__":
    main()
