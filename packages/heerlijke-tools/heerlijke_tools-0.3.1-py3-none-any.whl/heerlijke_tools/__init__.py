import click

from heerlijke_tools.proto.util.proto_command_runner import ProtoCommandRunner


EXISTING_DIR_TYPE = click.Path(
    exists=True,
    file_okay=False,
    dir_okay=True, readable=True
)


@click.group()
def cli():
    """
    Empty CLI group to which all HeerlijkeTools commands will belong.
    """


@cli.command(help="Generates Protobuf stubs for Python.")
@click.option(
    "--proto-path",
    type=EXISTING_DIR_TYPE,
    default=None,
    help="Relative path to your protocol buffer definitions."
)
@click.option(
    "--output-dir",
    type=EXISTING_DIR_TYPE,
    default=None,
    help="Relative path to where to put the generated stubs."
)
@click.argument("api-version")
def generate_protobuf_stubs(api_version, proto_path, output_dir):
    command_runner = ProtoCommandRunner(api_version, proto_path, output_dir)

    command_runner.run_protoc_command()
    command_runner.run_protol_command()
