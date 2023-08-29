from program import Program, Language, detect_language
from pathlib import Path
from io import BytesIO


def test_detect_language_c() -> None:
    paths = [Path("vector.h"), Path("vector.c"), Path("main.c")]
    assert detect_language(paths) == Language.C

def test_detect_language_cpp() -> None:
    paths = [Path("vector.h"), Path("vector.cpp"), Path("main.cpp")]
    assert detect_language(paths) == Language.CPP

def test_detect_language_rust() -> None:
    paths = [Path("vector.rs"), Path("main.rs")]
    assert detect_language(paths) == Language.RUST

def test_from_zip_data() -> None:
    f = BytesIO()
    with ZipFile()