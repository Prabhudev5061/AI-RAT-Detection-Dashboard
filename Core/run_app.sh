#!/usr/bin/env bash
# AI RAT Detection Dashboard - Unix Launcher
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

if [ -f ".venv/bin/activate" ]; then
    source ".venv/bin/activate"
elif [ -f "../.venv/bin/activate" ]; then
    source "../.venv/bin/activate"
elif [ -f "../../.venv/bin/activate" ]; then
    source "../../.venv/bin/activate"
fi

python3 desktop_app.py "$@"
