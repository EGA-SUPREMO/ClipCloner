[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)
# ClipCloner
![screenshot](https://github.com/EGA-SUPREMO/ClipCloner/blob/master/Screenshot%202024-04-21%2018%3A56%3A16.webp)
* <sub><sup>Note: it does not burn or translates subtitles</sub></sup>

This Python script is designed to process YouTube clips, allowing for various functionalities such as downloading the specified clip, then the stream, and performing the same video edits on the stream as the original.

This script is primarily designed to copy clips from Hololive streams in mind. However, it can be adapted for use with other streamers as well. To achieve this, you will need to modify the relevant files located within the 'descript' folder.

For instance, it assumes that the first YouTube link in the clip description corresponds to the source stream. This assumption aligns with the [Hololive's clippers guidelines](https://hololivepro.com/en/terms/). If customization is needed, feel free to reach out—I'd be delighted to assist.

## Prerequisites
* Python 3.x
* ffmpeg
### Additional Python packages used within the script (dependencies):
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [audalign](https://github.com/benfmiller/audalign)
* [align-videos-by-sound](https://github.com/align-videos-by-sound/align-videos-by-sound)

## Usage
Ensure you have the necessary prerequisites installed.

### Run the script using the following command:

```bash
python3 -m clip_generator.main 'https://www.youtube.com/watch?v=' 0 0
```

Replace <youtube.com> with the ID of the YouTube video you want to process.
<arg2> and <arg3> are required arguments that means the seconds offset, in case the clip has an intro or outro, in doubt, use 0.
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

## Use Case
This script was developed with the aim of simplifying the translation process for Hololive clips by:

* Generating a description file that aligns with [Hololive's clippers guidelines](https://hololivepro.com/en/terms/)
* Identifying the specific timestamps from which the clip was extracted.
* Automatically segmenting the raw stream into distinct files to facilitate simple editing
* Downloading the thumbnail to serve as a template for the translated clip.

**However, please be aware that utilizing this script may carry a risk of YouTube demonetization due to reused content.**

### Youtube Channels that used this script
* [UsaKen Translations](https://www.youtube.com/@UsaKenTranslations) (For some videos)
* [ElNo Studió](https://www.youtube.com/@elnostudio8994) (All of them)

## License
This script is licensed under [the GNU General Public License (GPL) version 3.](https://www.gnu.org/licenses/gpl-3.0.html)
