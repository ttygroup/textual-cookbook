"""This script demonstrates how to use the configparser module in a Textual application.

Recipe by Edward Jazzhands"""

import sys
import configparser
from pathlib import Path
from textual.app import App

class TextualApp(App[None]):
    
    def __init__(self):
        super().__init__()

        config_path = Path(__file__).resolve().parent / "config.ini"
        if not config_path.exists():
            raise FileNotFoundError("config.ini file not found.")

        self.config = configparser.ConfigParser()  # Available globally as self.app.config
        self.config.read(config_path)

        ## Config settings ##
        self.my_string  = self.config.get("MAIN", "my_string")
        self.my_boolean = self.config.getboolean("MAIN", "my_boolean")
        self.my_integer = self.config.getint("MAIN", "my_integer")
        self.my_float   = self.config.getfloat("MAIN", "my_float")

    def on_mount(self) -> None:

        assert self.my_string == "Hello, World!"
        assert self.my_boolean is True
        assert self.my_integer == 42
        assert self.my_float == 3.14

    def on_ready(self) -> None:
        self.log("Configuration loaded successfully!")
        self.log(f"String: {self.my_string}")
        self.log(f"Boolean: {self.my_boolean}")
        self.log(f"Integer: {self.my_integer}")
        self.log(f"Float: {self.my_float}")
        


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)