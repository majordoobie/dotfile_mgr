# Dotfile Fetching

The fetch_dotfile.py script helps users who use their GitHub as a place to store their 
dotfiles. What I found with storing my dotfiles on GitHub is that I would often forget 
where each dotfile goes/came from. So it became a challenge to update my dotfile repo. 
Additionally, when it came to pushing my configs onto a new system, I would forget 
where each file goes. Did they go in `~/` or did they go in common `~/.config/` folder?

This script is designed to automate the fetching (Grabbing the latest config) and 
deploying (Pushing the stored config to their proper home) by using a json file
for its configuration. 

The json file is stored in the `config_repo` directory which is ALWAYS relative to the
script itself. This name cannot be changed, it will be created for you. Inside this
folder is where each `deployment unit` will be stored. 

A `deployment unit` is a group of configuration s that belong to one entity. For example, 
my `alacritty` configuration has 3 total files. The `alacritty.yml` plus two color scheme yml files. These three
files are considered one `deployment unit` because they belong to `alacritty`. A 
`deployment unit` contains at least one `deployment object`. A `deployment object` 
is a pair of directory values, the `deployment_fpath` path and `storage_path` or 
`storage_fpath` where `_fpath` is the full path including the file name, and `_path`

The `deployment_fpath` is the path that the configuration file belongs to. Using 
the `~` is encouraged, but the full path is also acceptable. The `storage_$path` path 
is the path that the configuration file will be stored. It is recommended to use the 
`{D_ROOT}` prefix string with your path to allow the script to store the files automatically. 

Example:
```json
{
  "dotfiles": {
    "alacritty": [
      {
        "alacritty_conf": {
          "deployment_fpath": "~/.config/alacritty/alacritty.yml",
          "storage_fpath": "${D_ROOT}/alacritty.yml"
        },
        "alacritty_scheme_gruvbox": {
          "deployment": "~/.config/alacritty/color_scheme_gruvbox.yml",
          "storage_path": "${D_ROOT}"
        }
      }
    ]
  }
}
```

The example above shows 1 `deployment unit` **alacritty** containing two `deployment objects` 
**alacritty_conf** and **alacritty_scheme_gruvbox**

By using `${D_ROOT}` you are allowing the script to store both files above in the `config_repo/alacritty/` 
directory without you having to worry about where they are. But, you also have the option
of specifying where they are stored by NOT using the `${D_ROOT}` prefix for your storage string.

# TODO
- Create logging system to show the user the files that were updated or "ignored" because of configuration failure or no update needed
- Use hashing to determine if a file has changed and needs updating