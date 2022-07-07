#!/bin/zsh

cd ~/OneDrive/Cybernetic/active_projects/dotfiles
venv2/bin/python dotfile_mgr.py --fetch_configs
git add .
git commit -m "[Updated dotfiles]"
git push origin main
