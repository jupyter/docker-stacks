#!/bin/bash
# A before-notebook.d hook checking that the home dir is already populated
if [[ -f /home/jovyan/.profile ]]; then
    echo "HOOK_SEES_PROFILE"
else
    echo "HOOK_MISSES_PROFILE"
fi
