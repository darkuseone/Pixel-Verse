#!/bin/bash
# Скопируй эти строки в Setup script облачной среды Claude Code (модуль 2 курса).
apt-get update -qq && apt-get install -y -qq ffmpeg > /dev/null
python3 -m pip install -q numpy pillow || python3 -m pip install -q --break-system-packages numpy pillow
