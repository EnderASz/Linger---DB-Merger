import json
import pathlib
import sys

from dotenv import load_dotenv
load_dotenv()

from src.console import init_console    # NOQA: E402
init_console()
from src.console import console         # NOQA: E402


def parse_args() -> tuple[set[str | pathlib.Path], str | pathlib.Path]:
    sys.argv.pop(0)
    if len(sys.argv) < 3 or len(db_paths := set(sys.argv[:-1])) < 2:
        console.error("Too few parameters passed.")
        console.hint(
            "There are minimum two [bold](not duplicated)[/bold] input",
            "and one output database paths required.")
        console.exit()
    output_path = sys.argv.pop()
    return db_paths, output_path


db_paths, output_path = parse_args()
console.debug("Input paths:", repr(db_paths))
console.debug("Output path:", repr(output_path))


def load_db(path: str | pathlib.Path) -> set[tuple[str, str]]:
    try:
        db = json.load(open(path, encoding='utf-8'))
    except FileNotFoundError:
        console.warn("Database", repr(path), "not found. Skipping...")
        return None
    console.debug("Size of", repr(path), ":", len(db))
    return {tuple([word['wordEn'], word['wordPl']]) for word in db}


words: set[tuple[str, str]] = set()
for path in db_paths:
    words |= load_db(path)


def pack(data: set[tuple[str, str]]) -> list[dict[str, str]]:
    out_db = [{'wordEn': word[0], 'wordPl': word[1]} for word in data]
    out_db.sort(key=lambda x: x['wordPl'])
    return out_db


out_db = pack(words)
console.debug("Output size:", len(out_db))
console.debug("Output data:", out_db)

json.dump(out_db, open(output_path, 'w', encoding='utf8'), ensure_ascii=False)
