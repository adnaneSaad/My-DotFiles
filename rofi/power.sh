#!/usr/bin/env bash

chosen=$(echo -e "<span font='16' color='#ffaa33'>󰌾</span>    Lock\n<span font='16' color='#4da6ff'>󰍃</span>    Suspend\n<span font='16' color='#ff5149'>󰐥</span>    Shutdown\n<span font='16' color='#00ff00'>⟳</span>    Reboot" | rofi -dmenu -markup-rows -p "Power" -theme "~/.config/rofi/power-menu.rasi")

# Let's print out what rofi actually selected to your terminal if you run it manually, 
# or handle it matching any part of the string safely:

if [[ "$chosen" == *"Lock"* ]]; then
    dm-tool lock
elif [[ "$chosen" == *"Suspend"* ]]; then
    systemctl suspend
elif [[ "$chosen" == *"Shutdown"* ]]; then
    pkexec systemctl poweroff
elif [[ "$chosen" == *"Reboot"* ]]; then
    pkexec systemctl reboot
fi
