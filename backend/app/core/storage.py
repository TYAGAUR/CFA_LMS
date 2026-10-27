"""File storage behind a small interface. Local disk now; S3 for cloud (A-05)."""

import re
from pathlib import Path
from typing import BinaryIO

from app.core.config import get_settings
from app.core.ids import uuid7

SAFE = re.compile(r"[^A-Za-z0-9._-]+")


class LocalStorage:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def new_key(self, prefix: str, filename: str) -> str:
        name = SAFE.sub("_", Path(filename).name)[-80:] or "file"
        return f"{prefix}/{uuid7().hex}_{name}"

    def save(self, key: str, src: BinaryIO, max_bytes: int) -> int:
        path = self.path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        size = 0
        with path.open("wb") as out:
            while chunk := src.read(1024 * 1024):
                size += len(chunk)
                if size > max_bytes:
                    out.close()
                    path.unlink(missing_ok=True)
                    raise ValueError("file too large")
                out.write(chunk)
        return size

    def path(self, key: str) -> Path:
        p = (self.root / key).resolve()
        if self.root.resolve() not in p.parents:
            raise ValueError("invalid key")
        return p

    def delete(self, key: str) -> None:
        self.path(key).unlink(missing_ok=True)


def storage() -> LocalStorage:
    return LocalStorage(get_settings().storage_dir)
