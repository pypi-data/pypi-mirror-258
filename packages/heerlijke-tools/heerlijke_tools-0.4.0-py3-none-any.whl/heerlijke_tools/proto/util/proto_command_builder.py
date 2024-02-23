from pathlib import Path


class ProtoCommandBuilder:
    command_template = {
        "capture_output": True,
        "text": True
    }
    proto_path = Path("./src/proto/definitions")
    output_dir = Path("./src/proto/stubs")

    def __init__(self, api_version, proto_path, output_dir):
        self.api_version = api_version
        self._set_proto_path(proto_path)
        self._set_output_dir(output_dir)

        self.proto_files = self._get_all_proto_files()

    def _set_proto_path(self, proto_path):
        if proto_path:
            self.proto_path = Path(proto_path)

    def _set_output_dir(self, output_dir):
        if output_dir:
            self.output_dir = Path(output_dir)

    def _get_all_proto_files(self):
        return [
            proto_file.relative_to(self.proto_path)
            for proto_file
            in self.proto_path.rglob("*.proto")
        ]

    def build_protoc_command(self) -> dict:
        protoc_args = self._build_protoc_args()

        return self._build_command(protoc_args)

    def build_protol_command(self) -> dict:
        protol_args = self._build_protol_args()

        return self._build_command(protol_args)

    def _build_command(self, command_args):
        return self.command_template | {"args": command_args}

    def _build_protoc_args(self):
        return [
            "rye", "run", "python", "-m", "grpc_tools.protoc",
            f"-I{self.proto_path}",
            f"--python_out={self.output_dir}",
            f"--pyi_out={self.output_dir}",
            f"--grpc_python_out={self.output_dir}",
            *self.proto_files
        ]

    def _build_protol_args(self):
        return [
            "rye",
            "run",
            "protol",
            "--create-package",
            "--in-place",
            f"--python-out={self.output_dir}",
            f"protoc",
            f"--proto-path={self.proto_path}",
            *self.proto_files
        ]
