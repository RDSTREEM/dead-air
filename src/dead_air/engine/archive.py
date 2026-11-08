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

    def seed_casefile(self):
        initial_notes = [
            {
                "title": "CASE 01 // Assignment",
                "body": (
                    "BLACKWATER MUNICIPAL EMERGENCY AUTHORITY\n\n"
                    "You have been contracted to audit station BCR-17 "
                    "following several missed operator check-ins.\n\n"
                    "The station's automated broadcasts continue to "
                    "appear in the monitoring network. However, "
                    "recent archive records contain unexplained "
                    "discrepancies.\n\n"
                    "Your assignment is to reconstruct the station's "
                    "final transmissions, preserve relevant recordings, "
                    "and identify the source of the irregularities.\n\n"
                    "Operator: Elias Venn\n"
                    "Station: BCR-17\n"
                    "Location: Blackwater Coastal District\n"
                    "Case status: OPEN"
                ),
            },
            {
                "title": "CASE 01 // Station handover",
                "body": (
                    "BCR-17 operates as a coastal weather and emergency "
                    "broadcast station.\n\n"
                    "Routine broadcasts include weather reports, "
                    "navigation notices, and scheduled time signals.\n\n"
                    "The station's archive is incomplete. Preserve "
                    "every relevant transmission before drawing "
                    "conclusions."
                ),
            },
            {
                "title": "EQUIPMENT INVENTORY // Cabinet 4B",
                "body": (
                    "An older spectrum analyzer was removed from the "
                    "main receiver console during the last equipment "
                    "replacement.\n\n"
                    "Inventory indicates that the analyzer and its "
                    "service documentation remain in cabinet 4B "
                    "in the signal room.\n\n"
                    "The equipment has not been checked out."
                ),
                "unlock_id": "spectrum_analyzer",
            },
            {
                "title": "CASE 02 // Preliminary instruction",
                "body": (
                    "The archive timestamps must be checked against "
                    "an independent reference signal.\n\n"
                    "Do not assume that the station's clock and "
                    "the reference clock are synchronized."
                ),
            },
        ]

        existing = {note["title"] for note in self.data["notes"]}

        for note in initial_notes:
            if note["title"] not in existing:
                note["created_at"] = datetime.now().isoformat(timespec="seconds")
                self.data["notes"].append(note)

        self.data.setdefault("discovered_tools", [])

        self.save()
