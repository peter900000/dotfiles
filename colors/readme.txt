Short answer: yes, totally doable, and it’s a great idea 👍
Long answer: you do it by making one source of truth (usually shell-parsable files) and then including / sourcing / templating that file in each app in the way that app understands.

Below is a clean, battle-tested setup that works nicely on Ubuntu with kitty, vifm, cmus, i3, and polybar.

1️⃣ Create a central colors directory

Let’s say:

~/.config/colors/


Inside it, keep one canonical format, then derive others if needed.

Recommended structure
~/.config/colors/
├── palette.conf        # key=value, shell-friendly (source of truth)
├── kitty.conf          # generated or symlinked
├── i3.conf
├── polybar.ini
├── vifm.vifm
└── cmus.theme

2️⃣ Define the source of truth (palette.conf)

Use a simple shell-style format so it can be reused easily:

# ~/.config/colors/palette.conf
BG="#1e1e2e"
FG="#cdd6f4"

BLACK="#45475a"
RED="#f38ba8"
GREEN="#a6e3a1"
YELLOW="#f9e2af"
BLUE="#89b4fa"
MAGENTA="#f5c2e7"
CYAN="#94e2d5"

WHITE="#bac2de"


This format is:

easy to source in bash

easy to parse with sed / awk

human-readable

3️⃣ App-specific usage

Each app has different capabilities, so here’s the best practice per app.
