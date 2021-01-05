from pathlib import Path
from proto_builder import builder


BASE_DIR = Path(__file__).resolve().parent

PROTO_DIR = BASE_DIR.joinpath('proto')
PACKAGE_DIR = BASE_DIR.joinpath('project')
MYPY_EXCLUDE = ['/proto/options.proto']


if __name__ == '__main__':
    builder.proto_codegen(
        proto_dir=PROTO_DIR,
        python_out=BASE_DIR,
        package_dir=PACKAGE_DIR,
        my_py_exclude=MYPY_EXCLUDE
    )