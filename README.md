# YouTube Video Copy Script
This Python script is designed to process YouTube clips, allowing for various functionalities such as downloading the specified clip, then the stream, and performing the same video edits on the stream as the original.

This script is primarily designed to copy clips from Hololive streams in mind. However, it can be adapted for use with other streamers as well. To achieve this, you will need to modify the relevant files located within the 'descript' folder.

For instance, it assumes that the first YouTube link in the clip description corresponds to the source stream. This assumption aligns with the [Hololive's clippers guidelines](https://hololivepro.com/en/terms/). If customization is needed, feel free to reach out—I'd be delighted to assist.

## Prerequisites
* Python 3.x
* ffmpeg
### Additional Python packages used within the script (dependencies):
* yt-dlp
* [audalign](https://github.com/benfmiller/audalign)

## Usage
Ensure you have the necessary prerequisites installed.

### Run the script using the following command:

```bash
python3 -m clip_generator.main 'https://www.youtube.com/watch?v=' 0 0
```

Replace <youtube.com> with the ID of the YouTube video you want to process.
<arg2> and <arg3> are required arguments that means the seconds offset, in case the clip has an intro or outro, if in doubt, use 0.
#### The script will execute the following actions in order:

* Run the main process on the specified clip.
* Download the specified clip and related stream copies.
* Process the video by adjusting speed and removing credits offsets that may no be present on the stream source.
* Trim the video based on specific criteria.
* Cut if necessary the trimmed stream to match as closely as possible the original clip.

### Running Tests
To run the tests, use the following command:
```bash
python3 -m tests.runner ""
```

This command will execute the test runner for the script.

## License
This script is licensed under [the GNU General Public License (GPL) version 3.](https://www.gnu.org/licenses/gpl-3.0.html)
