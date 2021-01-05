#!/usr/bin/env bash

ln -sf $(pwd) ~/.local/share/ulauncher/extensions/

# restart ulauncher
pkill ulauncher
ulauncher &