import sys

from clip_generator.downloader import download_stream

if __name__ == '__main__':
    from_second = int(sys.argv[1:][1])
    to_second = int(sys.argv[1:][2])

    download_stream(sys.argv[1:][0], from_second, to_second)
