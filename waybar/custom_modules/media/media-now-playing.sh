#!/usr/bin/env bash

zscroll -l 20 \
	--delay 0.1 \
	--update-check true \
	"playerctl metadata --format '{{title}} - {{artist}}'" 2>/dev/null
wait
