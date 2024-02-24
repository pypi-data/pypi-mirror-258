"""The only class in this package."""

import os
from warnings import warn
from typing import Iterable
from dotenv import load_dotenv

class ENV:
    '''provides nice central access to grab ENV vals'''

    db_params: set[str] = {"USER", "PASSWORD", "HOST", "PORT", "DATABASE"}

    def __init__(self, env_file: str = ".env", env_path: str = None):
        self.env_file = env_file
        self.env_path = env_path

        load_dotenv(dotenv_path = self._find_env_file())


    def _find_env_file(self):
        """
        Recursively search for a .env file starting from the specified directory
        (or the current working directory if not specified).
        """
        if self.env_path:
            return self.env_path

        current_dir = os.getcwd()

        while 1:
            file = os.path.join(current_dir, self.env_file)
            if os.path.isfile(file):
                return file

            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                break

            current_dir = parent_dir

        return False


    def get(self, vars: Iterable[str], dont_assert: bool | Iterable[str] = False) -> dict:
        '''pass list of env values to get, returns key-value mapping of env val name : value'''
        var_dict: dict[str, str] = {}
        non_reqs: set[str] = {}

        if dont_assert is True:
            non_reqs = vars
        elif isinstance(dont_assert, Iterable):
            non_reqs = dont_assert

        checks = [item for item in non_reqs if item not in vars]

        if checks:
            warn(f"""The following variables were found
                 in dont_assert but not in the vars being searched for-
                 it's likely they were meant to be included in vars: {checks}""")

        for entry in vars:
            value = os.environ.get(entry, False)
            if entry not in non_reqs:
                assert value, f'ENV value {entry} not found'
            if value:
                var_dict[entry] = value

        return var_dict


    def get_db_auth(self) -> dict:
        '''just for ease/standardization of accessing database auth'''
        return self.get(self.db_params)
