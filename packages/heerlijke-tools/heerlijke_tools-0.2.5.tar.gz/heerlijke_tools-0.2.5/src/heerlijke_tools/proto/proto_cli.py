import click

from .util.proto_command_runner import ProtoCommandRunner
from heerlijke_tools import cli


@cli.command(help="Generates Protobuf stubs for Python.")
@click.argument("api-version")
def generate_protobuf_stubs(api_version):
    command_runner = ProtoCommandRunner(api_version)

    command_runner.run_protoc_command()
    command_runner.run_protol_command()
