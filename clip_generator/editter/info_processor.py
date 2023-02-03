import json
import math
import os

from clip_generator.editter import dirs as dirs


def curate_results(offsets):
    to_be_merged_range = []

    print(offsets)

    for i in range(len(offsets) - 1):
        consecutive_number = 0
        for j in range(i, len(offsets) - 1):
            current_end = offsets[i][1]
            current_start = offsets[j + 1][0]

            current_range = current_start - current_end

            consecutive_number = get_consecutive_number(offsets, i, j)

            i_range = j - i# + consecutive_number
            expected_range = i_range * dirs.get_second_for_edit()
            if math.isclose(current_range, expected_range, abs_tol=expected_range/10):
                to_be_merged_range.append([i, j+1])

    merged_tuple_range = merge_tuple(to_be_merged_range, offsets)

    offsets = duplicate_tuples_to_be_merged(offsets, merged_tuple_range)
    offsets = remove_wrong_matches(offsets, merged_tuple_range)

    return offsets


def get_consecutive_number(offsets, i, j):
    consecutive_number = 0
    for x in range(i + 1, j):
        current_end_to_be_tested = offsets[x][1]
        current_start_to_be_tested = offsets[x][0]

        current_range_to_be_tested = current_end_to_be_tested - current_start_to_be_tested
        if round(current_range_to_be_tested) > 1:
            consecutive_number += round(current_range_to_be_tested) - 1
        print(x)
        print("ranges in between:")
        print(current_range_to_be_tested)

    return consecutive_number

def merge_tuple(indexes, times):
    if not indexes:
        return

    result = [indexes[0]]

    for i in range(1, len(indexes)):
        if indexes[i][0] == result[-1][1]:
            result[-1][1] = indexes[i][1]
        elif indexes[i][0] < result[-1][1] and (indexes[i][0] == result[-1][0] or indexes[i][1] == result[-1][1]):
            result[-1][1] = indexes[i][1]
        else:
            if indexes[i][0] > result[-1][1]:
                result.append(indexes[i])
            else:
                difference_start = times[indexes[i][0]][1] - times[indexes[i][0]][0]
                difference_end = times[indexes[i][1]][1] - times[indexes[i][1]][0]
                difference_start_inserted = times[result[-1][0]][1] - times[result[-1][0]][0]
                difference_end_inserted = times[result[-1][1]][1] - times[result[-1][1]][0]
                if math.isclose(min(difference_start, difference_end),
                                 min(difference_start_inserted, difference_end_inserted), abs_tol=0.4):
                    if (difference_start + difference_end) > (difference_start_inserted + difference_end_inserted):
                        result.pop()
                        result.append(indexes[i])
                elif min(difference_start, difference_end) > min(difference_start_inserted, difference_end_inserted):
                    result.pop()
                    result.append(indexes[i])

    return result


# TODO NEEDS TESTS
def duplicate_tuples_to_be_merged(offsets, merged_tuple_range):
    if not merged_tuple_range:
        return offsets

    for merged_tuple in merged_tuple_range:
        offsets = offsets[:merged_tuple[0]] + [(offsets[merged_tuple[0]][0], offsets[merged_tuple[1]][1])] +\
                  offsets[merged_tuple[0]+1:]
        offsets = offsets[:merged_tuple[1]] + [(offsets[merged_tuple[0]][0], offsets[merged_tuple[1]][1])] +\
                  offsets[merged_tuple[1]+1:]

    return offsets


# TODO NEEDS TESTS
def remove_wrong_matches(offsets, merged_tuple_range):
    if not merged_tuple_range:
        return offsets

    wrong_match_range = []

    for x in range(len(merged_tuple_range)):
            for index in range(merged_tuple_range[x][0] + 1, merged_tuple_range[x][1]):
                wrong_match_range.append(offsets[index])

    for k in wrong_match_range:
        offsets.remove(k)

    return list(dict.fromkeys(offsets))


def get_timestamps_from_times(times):
    temp_end = 0
    temp_start = times[0]
    timestamps = []

    for i in range(1, len(times)):
        if not math.isclose(times[i] - times[i - 1], dirs.get_second_for_edit(), abs_tol=(max(dirs.get_second_for_edit() / 10, 0.1))):
            temp_end = times[i - 1] + dirs.get_second_for_edit()
            timestamps.append((temp_start, temp_end))
            temp_start = times[i]

    temp_end = times[-1] + dirs.get_second_for_edit() + 1 # el offset, conviertelo en una variable
    timestamps.append((temp_start, temp_end))

    return timestamps


# TODO add the offset at the begining of 0.5,and at the end 1s,must make those variables in the other places,NEEDS TESTS
def offset_info_edit():
    pass


def write_infos_trim(from_second: float, to_second: float):
    print(str(from_second) + " - " + str(to_second))
    append_json({'trim': [from_second, to_second]})


def write_infos_edit(infos_edit, times):
    print(infos_edit)
    append_json({'edit': infos_edit, 'times': times})


def write_correlation(start: float, end: float):
    print({'correlation': {'trim': [start, end]}})
    append_json({'correlation': {'trim': [start, end]}})


def append_json(value):
    filepath = dirs.dir_clip_folder + "timestamps.json"
    dic = value

    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            dic = json.load(f)
            dic.update(value)

    with open(filepath, 'w') as f:
        json.dump(dic, f)
        f.close()
