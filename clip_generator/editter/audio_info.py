from PIL import Image
from align_videos_by_soundtrack.align import SyncDetector
from align_videos_by_soundtrack.align_params import *
from align_videos_by_soundtrack.utils import *

import clip_generator.editter.dirs as dirs
from clip_generator.common_functions import getDuration
import clip_generator.editter.compare_sound_by_images.offset as offset
from clip_generator.editter import auto_edit_by_audalign
from clip_generator.editter.info_processor import get_timestamps_from_times, write_infos_edit

misalignment=6000
sample_rate=8000

data = {}
data['logs'] = []

infosEdit = list()
infosTrim = [0, 0]


def get_alignment_info(fps: list):
    file_specs = check_and_decode_filenames(fps, min_num_files=2)
    # default max_misalignment=1800. But this produced inaccurate results for some videos.
    # changing it to 6000 improved results although seems to make it run slower.
    # Have to test if max_misalignment=1800 is good enough
    # Seems changing sample_rate could make more precise results
    summarizer_params = SyncDetectorSummarizerParams(max_misalignment=misalignment, sample_rate=sample_rate)
    with SyncDetector(params=summarizer_params, clear_cache=False) as det:
        result = det.align(file_specs, known_delay_map={})
    return list(zip(file_specs, result))


# TODO needs tests
def set_audio_infos_edit(seconds: str, recognizer, fromAudio, toAudio):
    global infosEdit
    times = []
    for x in range(fromAudio, toAudio):
        filename = "S" + seconds + "_clip_audio" + str(x) + ".mp4"
        match recognizer:
            case "corr":
                offset = auto_edit_by_audalign.get_offset(filename)
                times.append(offset)
            case "video_align":
                try:
                    times.append(get_alignment_info(
                        [dirs.dirFixedAudioParts + filename, dirs.dir_stream])[0][1]['pad'])
                except Exception:
                    times.append(99999999)

    infosEdit = get_timestamps_from_times(times)

    write_infos_edit(infosEdit, times)


# TODO borrar, es inutil, ya hay otras funcitones que las replazan
def set_audio_infos_trim(dir_stream=""):
    global infosTrim
    if not dir_stream:
        dir_stream = dirs.dir_stream

    infosTrim = [get_alignment_info([dirs.dir_current_start_clip, dir_stream]),
                 get_alignment_info([dirs.dir_current_end_clip, dir_stream])]


# TODO needs tests
def set_audio_infos_trim_start(dir_stream):
    global infosTrim
    if dir_stream == dirs.dir_start_only_untrimmed_stream:
        raise Exception("Set audio info trim can't trim the start from an already trimmed stream")

    infosTrim[0] = get_alignment_info([dirs.dir_current_start_clip, dir_stream])


# TODO nedes tests
def set_audio_infos_trim_end(dir_stream):
    global infosTrim
    if dir_stream == dirs.dir_end_only_untrimmed_stream:
        raise Exception("Set audio info trim can't trim the end from an already trimmed stream")

    infosTrim[1] = get_alignment_info([dirs.dir_current_end_clip, dir_stream])

# TODO Needs no tests
def set_audio_infos_edit_by_image():
    global infosEdit

    clip_image = Image.open(dirs.dir_audio_clip_image)
    stream_image = Image.open(dirs.dir_audio_stream_image)
    clip_image = offset.crop_height_image(clip_image, 512, 512)
    stream_image = offset.crop_height_image(stream_image, 512, 512)

    stream_image.save("stream.png")
    clip_image.save("clip.png")
    average_max = []
    similarity_max = []
    for x in range(0, clip_image.width, int(dirs.get_second_for_edit() * dirs.scale_edit)):
        print(x)
        width = min(dirs.get_second_for_edit() * dirs.scale_edit, clip_image.width - x)
        cropped_clip = offset.crop_width_image(clip_image, x, width)
        
        similarity_indexes, accuracy_indexes, average_indexes = offset.compare_images(cropped_clip, stream_image)

        similarity_max.append(offset.pixels_into_seconds(similarity_indexes.index(max(similarity_indexes))))
        average_max.append(offset.pixels_into_seconds(average_indexes.index(max(average_indexes))))

    infosEdit = get_timestamps_from_times(similarity_max)
    print(infosEdit)
    print(similarity_max)
    print("Average:")
    print(average_max)

# TODO update tests of write info edit
    write_infos_edit(infosEdit, similarity_max)


def get_last_seconds_for_ffmpeg_argument_to(file, seconds: int):
    return float(getDuration(file)) - seconds


