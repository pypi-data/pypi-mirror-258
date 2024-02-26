import configparser
import logging
import os
import pathlib
import subprocess
import sys

logger = logging.getLogger(__name__)


class Bitbar:
    plugin_directory_search = [
        ["defaults", "read", "com.ameba.SwiftBar", "PluginDirectory"],
        ["defaults", "read", "com.matryer.BitBar", "pluginsDirectory"],
    ]

    base_path = pathlib.Path.cwd()
    config_file = pathlib.Path.home() / ".config" / "bitbar" / "default.ini"

    def setup(self):
        if "LANG" not in os.environ:
            logging.basicConfig(level=logging.WARNING)
            sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf8")
        else:
            logging.basicConfig(level=logging.DEBUG)

    @classmethod
    def pluginsDirectory(cls):
        for command in cls.plugin_directory_search:
            try:
                return pathlib.Path(
                    subprocess.check_output(command).decode("utf8").strip()
                )
            except subprocess.CalledProcessError:
                print("Skipping", command)

    def read(self, fname):
        with (self.base_path / fname).open() as fp:
            logger.debug("Reading %s", fp.name)
            return fp.read()

    def load(self):
        self.config = configparser.ConfigParser()
        if self.config_file.exists():
            with self.config_file.open() as fp:
                logger.debug("Reading config %s", fp.name)
                self.config.read_file(fp)

    def print(self, *args, **kwargs):
        print(self.format(*args, **kwargs))

    # https://github.com/swiftbar/SwiftBar#parameters
    # https://github.com/matryer/xbar-plugins/blob/main/CONTRIBUTING.md#parameters
    def format(self, *args, **kwargs):
        buffer = [str(x) for x in args]

        if kwargs:
            buffer.append("|")

            for key, value in kwargs.items():
                if key == "image":
                    value = self.read(value)
                buffer.append(f"{key}={value}")

        return " ".join(buffer)
