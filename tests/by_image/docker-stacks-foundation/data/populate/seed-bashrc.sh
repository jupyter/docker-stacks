#!/bin/bash
# A start-notebook.d hook creating .bashrc before the home dir is populated
echo "# seeded-by-hook" >/home/jovyan/.bashrc
