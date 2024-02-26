import argparse
import pathlib

from setuptools.command import easy_install

from . import Bitbar

try:
    from importlib.metadata import entry_points
except ImportError:
    from importlib_metadata import entry_points


class BitbarWriter(easy_install.ScriptWriter):
    @classmethod
    def format(cls, entry):
        header = cls.get_header()
        script = cls.template % {
            "spec": entry.dist.name,
            "name": entry.name,
            "group": entry.group,
        }
        return header, script


def install(args):
    for entry in entry_points(group="bitbar.install"):
        path = args.pluginsDirectory / entry.name
        header, script = BitbarWriter.format(entry)

        with path.open("w+") as fp:
            fp.write(header)
            fp.write(script)
        mode = 0o777 - easy_install.current_umask()
        path.chmod(mode)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    install_command = subparsers.add_parser("install")
    install_command.add_argument(
        "--pluginsDirectory", default=Bitbar.pluginsDirectory()
    )
    install_command.add_argument("package", type=pathlib.Path)
    install_command.set_defaults(func=install)

    args = parser.parse_args()
    args.func(args)
