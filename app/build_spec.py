import argparse
import json
import logging
import os
import sys
import yaml
from uvicorn.importer import import_from_string

logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.DEBUG)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", help='App import string. Eg. "main:app"', default="main:app")
    parser.add_argument("--app-dir", help="Directory containing the app", default="app")
    parser.add_argument("--out-dir", help="Source directory for docs output", default="docs")
    parser.add_argument("--out", help="Output file ending in .json or .yaml", default="openapi.yaml")
    parser.add_argument("--version", help="Override version. You can control documentation version from outside build tools")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    add_app_dir_to_sys_path(args.app_dir)
    logging.info(f"🏭 importing app from {args.app}")
    app = import_from_string(args.app)
    openapi = app.openapi()
    if args.version:
        version = args.version
        openapi["info"]["version"] = version
    else:    
        version = openapi.get("info", {}).get("version", "unknown version")

    if not os.path.exists(args.out_dir):
        logging.info(f"Creating directory {args.out_dir}")
        os.makedirs(args.out_dir)

    version_directory = create_version_directory(args.out_dir, version)
    spec_file_path = os.path.join(version_directory, args.out)
    write_openapi_spec(openapi, spec_file_path)
    logging.info(f"🧾 documentation {version=} written to {spec_file_path}")


def add_app_dir_to_sys_path(app_dir: str) -> None:
    if app_dir is not None:
        logging.info(f"📂 adding {app_dir} to sys.path")
        sys.path.insert(0, app_dir)


def get_version(override_version: str | None, openapi: dict) -> str:
    spec_version = openapi.get("info", {}).get("version", "unknown version")
    return override_version if override_version else spec_version


def create_version_directory(out_dir: str, version: str) -> str:
    version_directory = os.path.join(out_dir, version)
    if not os.path.exists(version_directory):
        logging.info(f"📂 creating directory {version_directory}")
        os.makedirs(version_directory)
    else:
        logging.info(f"📂 {version_directory} already exists, skipping documentation creation")
        sys.exit(0)
    return version_directory


def write_openapi_spec(openapi: dict, spec_file_path: str) -> None:
    with open(spec_file_path, "w") as f:
        logging.info(f"🧾 writing OpenAPI spec to {spec_file_path}")
        if spec_file_path.endswith(".json"):
            json.dump(openapi, f, indent=2)
        else:
            yaml.dump(openapi, f, sort_keys=False)


if __name__ == "__main__":
    main()
