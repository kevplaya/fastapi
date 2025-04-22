import csv
import re
from collections import defaultdict

from consts import COMPANY_TAG_PREFIX, INPUT_COMPANY_TAG_CSV_FILE, LANGS, OUTPUT_TAG_CSV_FILE, TAG_DELIMITER

tag_groups = defaultdict(lambda: {lang: "" for lang in LANGS})

with open(INPUT_COMPANY_TAG_CSV_FILE, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        for lang in LANGS:
            col = f"{COMPANY_TAG_PREFIX}{lang}"
            tags = row.get(col, "").split(TAG_DELIMITER)
            for tag in tags:
                tag = tag.strip()
                match = re.search(r"(\d+)", tag)
                if match:
                    tag_id = match.group(1)
                    tag_groups[tag_id][lang] = tag


with open(OUTPUT_TAG_CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["tag_id"] + [f"{COMPANY_TAG_PREFIX}{lang}" for lang in LANGS])
    print(f"tag_groups: {tag_groups}")
    for tag_id, tag_group in tag_groups.items():
        row = [tag_id] + [tag_groups[tag_id][lang] for lang in LANGS]
        writer.writerow(row)
