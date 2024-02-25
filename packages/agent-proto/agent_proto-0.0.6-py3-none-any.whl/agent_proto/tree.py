from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel


class FsTree(BaseModel):
    """
    Represents a file system tree.
    """

    path: str
    type: Literal["file", "dir"]
    children: list[FsTree] | None
    content: str | None

    @classmethod
    def build(cls, path: str) -> FsTree:
        """
        Build a file system tree from a path.

        Args:
                        path (str): The path to build the file system tree from.

        Returns:
                        FsTree: The file system tree.
        """
        path_ = Path(path)
        if path_.is_file():
            try:
                return cls(
                    path=str(path),
                    type="file",
                    children=None,
                    content=path_.read_text(),
                )
            except UnicodeDecodeError:
                return cls(
                    path=str(path),
                    type="file",
                    children=None,
                    content="binary",
                )
        children = [cls.build(str(child)) for child in path_.iterdir()]
        return cls(path=str(path), type="dir", children=children, content=None)


tree = FsTree.build(".")
print(tree.model_dump_json())
