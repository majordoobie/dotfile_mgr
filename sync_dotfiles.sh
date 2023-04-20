#!/bin/zsh

cd ~/OneDrive/Code/active_projects/dotfiles
venv/bin/python dotfile_mgr.py --fetch_configs
git add .
git commit -m "[Updated dotfiles]"
git push origin main
