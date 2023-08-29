from enum import Enum
from pathlib import Path
from typing import Iterable


class Language(Enum):
    C = "C"
    CPP = "CPP"
    RUST = "RUST"
    UNKNOWN = "UNKNOWN"


def detect_language(paths: Iterable[Path]) -> Language:
    main_to_language = {
        "main.c": Language.C,
        "main.cpp": Language.CPP,
        "main.rs": Language.RUST,
    }

    for path in paths:
        if path.name in main_to_language:
            return main_to_language[path.name]

    return Language.UNKNOWN
