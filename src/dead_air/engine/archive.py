import json
import shutil
import uuid

from datetime import datetime
from pathlib import Path


class ArchiveManager:
    def __init__(self, dr: Path):
        self.dir = dr
        self.rec_dir = dr / "rec"

        self.rec_dir.mkdir(parents=True, exist_ok=True)

        self.index = dr / "archive.json"  # hollow milee knowledge comming in clutch??

        if self.index.exists():
            self.data = json.loads(self.index.read_text(encoding="utf-8"))
        else:
            self.data = {"recordings": [], "logs": []}

    def save(self):
        self.dir.mkdir(parents=True, exist_ok=True)

        self.index.write_text(json.dumps(self.data, indent=4), encoding="utf-8")

    def add_rec(self, src: Path, freq: float, name: str):
        rec_id = uuid.uuid4().hex[
            :8
        ]  # i havent compained about this because i made my variables _id and stuff cuz ik id is a taken function name but it annoys me soooooooooooo much
        file = f"{rec_id}.wav"

        dest = self.rec_dir / file

        shutil.copy(src, dest)

        entry = {
            "id": rec_id,
            "name": name,
            "freq": freq,
            "file": file,
            "recorded_at": datetime.now().isoformat(timespec="seconds"),
        }

        self.data["recordings"].append(entry)
        self.save()

        return entry

    def add_log(self, title: str, body: str):
        entry = {
            "title": title,
            "body": body,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        self.data["logs"].append(entry)
        self.save()

        return entry
