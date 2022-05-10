import copy
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
                            "deployment_fpath": "~/.config/alacritty/alacritty.yml",
                            "storage_fpath": "${D_ROOT}/alacritty.yml"
                        },
                        "alacritty_scheme_gruvbox": {
                            "deployment_fpath": "~/.config/alacritty/color_scheme_gruvbox.yml",
                            "storage_path": "${D_ROOT}"
                        }
                    }
                ]
            }
        }

        # Deep copy needed otherwise the lists will have the same pointers
        self.invalid_obj_key_count = copy.deepcopy(self.config_working)
        self.invalid_obj_key_count["dotfiles"]["alacritty"][0]["alacritty_conf"]["storage_path"] = "Path"

        # Create invalid by creating a non list deployment object
        self.no_list_config = copy.deepcopy(self.config_working)
        self.no_list_config["dotfiles"]["new_unit"] = {"No_list":  "Path"}

        # Create empty deployment unit
        self.empty_d_unit = copy.deepcopy(self.config_working)
        self.empty_d_unit["dotfiles"]["new_unit"] = []

    def test__get_config_empty_dict(self):
        """Test to make sure that we get a system exit for sending an empty
        dict without the mandatory dict key in this case \"dotfiles\" """
        with self.assertRaises(ValueError):
            fetch_dotfiles._get_config(self.config_empty_unit)

    def test__get_config_valid_dict(self):
        self.assertIsInstance(fetch_dotfiles._get_config(self.config_working), dict)

    def test__get_config_invalid_obj_key_count(self):
        with self.assertRaises(ValueError):
            fetch_dotfiles._get_config(self.invalid_obj_key_count)

    def test__get_config_no_list_deployment_unit(self):
        with self.assertRaises(ValueError):
            fetch_dotfiles._get_config(self.no_list_config)

    def test__get_config_empty_d_unit(self):
        with self.assertRaises(ValueError):
            fetch_dotfiles._get_config(self.empty_d_unit)


if __name__ == '__main__':
    unittest.main(verbosity=2)
