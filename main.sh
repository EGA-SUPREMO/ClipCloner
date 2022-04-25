gettitle() {
    TITLE=$(youtube-dl --skip-download --get-title --no-warnings --youtube-skip-dash-manifest $1)
    #echo "youtube-dl --skip-download --get-title --no-warnings $1"
    youtube-dl --skip-download --no-warnings --write-description --youtube-skip-dash-manifest $1
    python3 main.py $TITLE $1
}

gettitle "link de youtubu uwu"