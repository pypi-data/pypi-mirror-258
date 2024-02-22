"""
This is an example_agent_sithumi for public python module.
"""

import logging


class HelloSithumi:
    def __init__(self) -> None:
        """
        This will initiate the HelloSithumi demo class.
        """
        self.name = "Sithumi"
        self.age = 26

    def run(self) -> str:
        """
        This function will return Sithumi's user info.
        :return:
            Info: Name and Age as a description.
        """
        try:
            return f"My name is {self.name}. I'm {self.age} years old."
        except Exception as exception:
            logging.error(exception)
