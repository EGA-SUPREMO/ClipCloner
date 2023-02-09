import sys

from datetime import datetime
from datetime import timedelta

def time_to_seconds(time_str):
    time = datetime.strptime(time_str, "%H:%M:%S.%f")
    return (time - datetime(1900, 1, 1)).total_seconds()

def format_td(seconds, digits=3):
    isec, fsec = divmod(round(seconds*10**digits), 10**digits)
    return f'{timedelta(seconds=isec)}.{fsec:0{digits}.0f}'

def seconds_to_time(seconds):
    return format_td(seconds, 2)

def increase_speed(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("Dialogue:"):
            parts = line.split(',')
            start = time_to_seconds(parts[1])
            end = time_to_seconds(parts[2])
            start *= 0.95
            end *= 0.95
            parts[1] = seconds_to_time(start)
            parts[2] = seconds_to_time(end)
            line = ','.join(parts)
        new_lines.append(line)

    with open("sub_output.ass", 'w') as file:
        file.writelines(new_lines)

    print(f"The subtitles in {filename} have been increased by 5%.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the filename as an argument.")
        sys.exit(1)

    filename = sys.argv[1]
    increase_speed(filename)
