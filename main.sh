gettitle() {
    TITLE=$(youtube-dl --skip-download --get-title --no-warnings $1)
    #echo "youtube-dl --skip-download --get-title --no-warnings $1"
    python3 main.py $TITLE
}

gettitle hey