#!/bin/bash
mkfifo fifo.mp3
youtube-dl "$1" -x --audio-format mp3 -o fifo.mp3 2> /dev/null >/dev/null &
mpv fifo.mp3
rm fifo.mp3
