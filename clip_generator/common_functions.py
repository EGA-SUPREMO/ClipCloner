import subprocess
import difflib

def getDuration(filename):
    duration=subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filename], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return float(duration) 

def removeAll(folder_path):
    for path in Path(folder_path).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)

    os.makedirs("tests/Clips/audio_parts")
    os.makedirs("tests/Clips/fixed_audio_parts")

def checkTwoFilesAreTheSame(filename1, filename2):
    IsSame = True
    with open(filename1) as file_1:
        file_1_text = file_1.readlines()

    with open(filename2) as file_2:
        file_2_text = file_2.readlines()

    for line in difflib.unified_diff(
        file_1_text, file_2_text, fromfile=filename1,
        tofile=filename2, lineterm=''):
        print(line)
        if line is not None:
            IsSame = False
    return IsSame