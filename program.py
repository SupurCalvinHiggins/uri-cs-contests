from __future__ import annotations


import subprocess
from dataclasses import dataclass
from language import Language, detect_language
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
from typing import Optional


# TODO: add hash: source_hash = hashlib.sha256(source).hexdigest()

@dataclass
class Program:

    language: Language
    zip_data: bytes
    id: Optional[int] = None

    @staticmethod
    def from_zip_data(zip_data: bytes) -> Program:
        f = BytesIO(zip_data)
        with ZipFile(f) as zf:
            paths = [Path(s) for s in zf.namelist()]
        language = detect_language(paths)
        return Program(language=language, zip_data=zip_data)

    def compile(self, build_path: Path) -> None:
        assert build_path.exists()

        f = BytesIO(self.zip_data)
        with ZipFile(f) as zf:
            # TODO: This is dangerous.
            zf.extractall(build_path)

        make_path = build_path.joinpath("Makefile")
        if make_path.exists():
            # TODO: Build with make.
            return

        if self.language == Language.UNKNOWN:
            return

        main_path = build_path.joinpath("main")
        language_to_cmd = {
            Language.C: f"gcc {main_path}.c -O3 -std=c17 -o prog",
            Language.CPP: f"g++ {main_path}.cpp -O3 -std=c++20 -o prog",
            # TODO: Need to move executable to correct location.
            Language.RUST: f"cargo build --release",
        }
        cmd = language_to_cmd[self.language]
        subprocess.run(cmd)
