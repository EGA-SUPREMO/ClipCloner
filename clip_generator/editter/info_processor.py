import json
import math
import os

from clip_generator.editter import dirs as dirs


def curate_results(offsets):
    print(offsets)
    start = offsets[0][0]
    wrong_match = 0

    wrong_match_range = []
    wrong_match_range_indexes = []
    for i in range(len(offsets) - 1):
        for j in range(i, len(offsets) - 1):
            current_end = offsets[i][1]
            current_start = offsets[j + 1][0]

            current_range = current_start - current_end
            i_range = j - i
            expected_range = i_range * dirs.get_second_for_edit()
            if math.isclose(current_range, expected_range, rel_tol=expected_range/10):
                for k in range(i_range):
                    wrong_match_range.append(offsets[i + k + 1])
                    wrong_match_range_indexes.append(i + k + 1)
                wrong_match += 1

    wrong_match_range = list(set(wrong_match_range))
    wrong_match_range_indexes = list(set(wrong_match_range_indexes))

    for k in wrong_match_range:
        offsets.remove(k)
    offsets.pop(wrong_match_range_indexes[0]-1)
    offsets = [(start, offsets[0][1]), *offsets[1:]]
    print(wrong_match_range_indexes)
    print(offsets)
    return offsets


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
