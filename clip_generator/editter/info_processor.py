import json
import math
import os

from clip_generator.editter import dirs as dirs


def curate_results(offsets):
    to_be_merged_range = []

    for i in range(len(offsets) - 1):
        for j in range(i, len(offsets) - 1):
            current_end = offsets[i][1]
            current_start = offsets[j + 1][0]

            current_range = current_start - current_end

            consecutive_number = get_consecutive_number(offsets, i, j+1)
            expected_range = consecutive_number * dirs.get_second_for_edit()

            if math.isclose(current_range, expected_range, abs_tol=dirs.get_second_for_edit()/5):
                difference_inbetween_merge_tuple = 0
                difference_between_merge_tuple_ends = offsets[i][1] - offsets[i][0] + offsets[j+1][1] - offsets[j+1][0]
                for to_be_merge_index in range(i+1, j+1):
                    if should_count(to_be_merged_range, to_be_merge_index):
                        difference_inbetween_merge_tuple += offsets[to_be_merge_index][1] - offsets[to_be_merge_index][
                            0] - 1
                if difference_inbetween_merge_tuple < difference_between_merge_tuple_ends:
                    to_be_merged_range.append([i, j+1])

    merged_tuple_range = merge_tuple(to_be_merged_range, offsets)

    offsets = duplicate_tuples_to_be_merged(offsets, merged_tuple_range)
    offsets = remove_wrong_matches(offsets, merged_tuple_range)

    return offsets


# TODO TESTS????
def should_count(to_be_merged_range, to_be_merge_index):
    should_get_counted = True
    for i in range(len(to_be_merged_range)):
        if to_be_merge_index == to_be_merged_range[i][0] or to_be_merge_index == to_be_merged_range[i][1]:
            should_get_counted = False
    return should_get_counted


def get_consecutive_number(offsets, i, j):
    count = 0
    for start, end in offsets[i+1:j]:
        count += end - start
    return round(count)


def merge_tuple(indexes, times):
    if not indexes:
        return

    indexes = remove_tuples_with_starts_below_previous_ends(indexes)
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


def remove_tuples_with_starts_below_previous_ends(tuples_input):
    ends = []
    result = []
    for t in tuples_input:
        if t[0] not in ends or t[1] not in ends:
            ends.append(t[1])
            result.append(t)
    return result


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


def set_transitions(times):
    new_times = []
    skip = False
    for i in range(len(times)):
        start, end = times[i]
        if skip:
            skip = False
            continue
        if end - start == 1:
            if i > 0 and i < len(times) - 1:
                if (times[i-1][1] - times[i-1][0] > 1) and (times[i+1][1] - times[i+1][0] > 1):
                    new_times.pop()
                    new_times.append((times[i-1][0], times[i-1][1] + 0.5))
                    new_times.append((times[i+1][0] - 0.5, times[i+1][1]))
                    skip = True
                else:
                    new_times.append((start, end))
            else:
                new_times.append((start, end))
        else:
            new_times.append((start, end))
    return new_times

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
