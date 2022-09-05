import subprocess

def getDuration(filename):
    duration=subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filename], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return float(duration) 
