"""Restore the tiny demonstration remote outside the Git repository."""

from pathlib import Path
from zipfile import ZipFile


def main() -> None:
    project = Path(__file__).resolve().parents[1]
    remote = (project / "../../HW3_DVC_remote").resolve()
    with ZipFile(project / "remote_seed.zip") as archive:
        for item in archive.infolist():
            # Never allow archive members to escape the requested output folder.
            destination = (remote / item.filename).resolve()
            if not destination.is_relative_to(remote):
                raise ValueError(f"Unsafe archive member: {item.filename}")
        archive.extractall(remote)
    print(f"DVC local remote restored: {remote}")


if __name__ == "__main__":
    main()
