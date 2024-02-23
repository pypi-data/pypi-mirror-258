import subprocess

import click

from .proto_command_builder import ProtoCommandBuilder


class ProtoCommandRunner:
    protoc_command: dict
    protol_command: dict

    def __init__(self, api_version, proto_path, output_dir):
        self.command_builder = ProtoCommandBuilder(
            api_version,
            proto_path,
            output_dir
        )

    def run_protoc_command(self):
        self.protoc_command = self.command_builder.build_protoc_command()

        self._run_command("protoc")

    def run_protol_command(self):
        self.protol_command = self.command_builder.build_protol_command()

        self._run_command("protol")

    def _run_command(self, command_name):
        command = getattr(self, f"{command_name}_command")

        if (result := subprocess.run(**command)).returncode != 0:
            click.echo("Running command failed with the following error:")
            click.echo(result.stderr)
