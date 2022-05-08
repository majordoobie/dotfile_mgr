import unittest
from unittest import TestCase
import fetch_dotfiles


class Test(TestCase):
    def setUp(self) -> None:
        self.config_empty_unit = {}

        self.config_working = {
            "dotfiles": {
                "alacritty": [
                    {
                        "alacritty_conf": {
                            "deployment": "~/.config/alacritty/alacritty.yml",
                            "storage": "${D_ROOT}/alacritty.yml"
                        },
                        "alacritty_scheme_gruvbox": {
                            "deployment": "~/.config/alacritty/color_scheme_gruvbox.yml",
                            "storage": "${D_ROOT}/color_scheme_gruvbox.yml"
                        }
                    }
                ]
            }
        }
        self.config_empty_unit = {
            "dotfiles": {
                "alacritty": [
                    {
                        "alacritty_conf": {
                            "deployment": "~/.config/alacritty/alacritty.yml",
                            "storage": "${D_ROOT}/alacritty.yml"
                        },
                        "alacritty_scheme_gruvbox": {
                            "deployment": "~/.config/alacritty/color_scheme_gruvbox.yml",
                            "storage": "${D_ROOT}/color_scheme_gruvbox.yml"
                        }
                    }
                ],
                "tmux": []
            }
        }

        self.invalid_keys = {
            "dotfiles": {
                "alacritty": [
                    {
                        "alacritty_conf": {
                            "deployment": "~/.config/alacritty/alacritty.yml",
                            "storage": "${D_ROOT}/alacritty.yml"
                        },
                        "alacritty_scheme_gruvbox": {
                            "deployment": "~/.config/alacritty/color_scheme_gruvbox.yml",
                            "storage": "${D_ROOT}/color_scheme_gruvbox.yml"
                        }
                    }
                ],
                "tmux": {
                    "tmux": {
                        "only_one_key": "val"
                    }
                }
            }
        }

    def test__get_config_empty_dict(self):
        """Test to make sure that we get a system exit for sending an empty
        dict without the mandatory dict key in this case \"dotfiles\" """
        with self.assertRaises(SystemExit):
            fetch_dotfiles._get_config(self.config_empty_unit)

    def test__get_config_empty_unittest(self):
        """Test that an empty deployment unit results in a exit"""
        with self.assertRaises(SystemExit):
            fetch_dotfiles._get_config(self.config_empty_unit)

    def test__get_config_invalid_unit_key_count(self):
        with self.assertRaises(SystemExit):
            fetch_dotfiles._get_config(self.invalid_keys)

    def test__get_config_working(self):
        """Test a working good dict"""
        fetch_dotfiles._get_config(self.config_working)

    def test__get_deployment(self):
        _dict = fetch_dotfiles._get_config(self.config_working)
        d_list = fetch_dotfiles._get_deployments(_dict)


if __name__ == '__main__':
    unittest.main(verbosity=2)
