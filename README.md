YouTube Video Copy Script
This Python script is designed to process YouTube clips, allowing for various functionalities such as downloading the specified clip, then the stream, and performing the same video edits on the stream as the original.

## Prerequisites
* Python 3.x
* ffmpeg
### Additional Python packages used within the script (dependencies):
* yt-dlp
* [audalign](https://github.com/benfmiller/audalign)

## Usage
Ensure you have the necessary prerequisites installed.

Run the script using the following command:

python script.py <clip_id> <arg2> <arg3>
Replace <clip_id> with the ID of the YouTube video you want to process.
<arg2> and <arg3> are optional arguments that may be required based on the specific functionality of the script.
#### The script will execute the following actions in order:

Run the main process on the specified clip.
Download the specified clip and related stream copies.
Process the video by adjusting speed and removing credits offsets.
Trim the video based on specific criteria.
Download the processed stream.
Functions and Operations
maini.run(<clip_id>): Runs the main process for the specified clip.

downloader.download_clip(<clip_id>): Downloads the specified clip.

downloader.download_video("worstaudio", dirs.dir_worstaudio_stream, maini.stream_links[0]): Downloads the video's worst audio.

chopper.increase_speed_video(dirs.dir_clip, dirs.dir_clip_with_speed): Increases the speed of the video.

clip_generator.editter.chopper.remove_credits_offsets(<arg2>, <arg3>): Removes credits offsets using specified arguments.

trimmer.trim_to_clip(False): Trims the video to a specified clip.

downloader.download_stream(maini.stream_links[0], from_second, to_second): Downloads the processed stream.

clip_generator.editter.auto_editter.copy_edit(): Copies video edits.

Please replace <clip_id>, <arg2>, and <arg3> with appropriate values and adjust the README according to your specific use case and application.




