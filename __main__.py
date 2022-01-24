import json
import sys

from dotenv import load_dotenv
load_dotenv()

from src.console import init_console
init_console()
from src.console import console     # NOQA: E402


sys.argv.pop(0)
if len(sys.argv) < 3 or len(db_paths := set(sys.argv[:-1])) < 2:
    console.error("Too few parameters passed.")
    console.hint(
        "There are minimum two [bold](not duplicated)[/bold] input",
        "and one output database paths required.")
    console.exit()
output_path = sys.argv.pop()
console.debug("Input paths:", repr(db_paths))
console.debug("Output path:", repr(output_path))


words = set()
for path in db_paths:
    try:
        db = json.load(open(path, encoding='utf-8'))
    except FileNotFoundError:
        console.warn("Database", repr(path), "not found. Skipping...")
        continue
    console.debug("Size of", repr(path), ":", len(db))
    words |= {tuple([word['wordEn'], word['wordPl']]) for word in db}

out_db = list()
for word in words:
    out_db.append({'wordEn': word[0], 'wordPl': word[1]})
out_db.sort(key=lambda x: x['wordPl'])
console.debug("Output size:", len(out_db))
console.debug("Output data:", out_db)

json.dump(out_db, open(output_path, 'w', encoding='utf8'), ensure_ascii=False)
