import json
import math
import os

from clip_generator.editter import dirs as dirs
from clip_generator.editter.audio_info import infosEdit


def curate_results(audio_offsets):
    curated_offsets = []
    current_start = audio_offsets[0][0]
    current_end = audio_offsets[0][1]
    for offset in audio_offsets:
        if offset[0] <= current_end:
            current_end = max(current_end, offset[1])
        else:
            curated_offsets.append((current_start, current_end))
            current_start = offset[0]
            current_end = offset[1]
    curated_offsets.append((current_start, current_end))
    final_offsets = []
    for i in range(len(curated_offsets)):
        for j in range(i+1, len(curated_offsets)):
            if curated_offsets[i][1] >= curated_offsets[j][0]:
                curated_offsets[i] = (curated_offsets[i][0], max(curated_offsets[i][1], curated_offsets[j][1]))
                curated_offsets[j] = (0,0)
    for offset in curated_offsets:
        if offset != (0,0):
            final_offsets.append(offset)
    if len(final_offsets) > 1:
        final_offsets = [(min([offset[0] for offset in final_offsets]), max([offset[1] for offset in final_offsets]))]
    return final_offsets


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


def write_infos_edit(average):
    print(infosEdit)
    append_json({'edit': infosEdit, 'times': average})


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
