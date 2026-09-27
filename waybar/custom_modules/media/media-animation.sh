#!/usr/bin/env bash

animation_frames=("▂▄▆" "▄▂▆" "▄▆▂" "▆▄▂" "▆▂▄")
i=0

while :; do
  status=$(playerctl status 2>/dev/null)

  if [ "$status" = "Playing" ]; then
      echo "${animation_frames[i]}"
      i=$(( (i + 1) % ${#animation_frames[@]} ))
      sleep 0.1
  elif [ "$status" = "Paused" ]; then
      echo ""
      sleep 0.5
  else
      echo ""
      sleep 1
  fi
done
