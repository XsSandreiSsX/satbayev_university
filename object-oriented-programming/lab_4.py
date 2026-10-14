import csv
import json
import sys
from abc import ABC, abstractmethod

class FileExporter(ABC):
    @abstractmethod
    def export(self, data: dict):
        ...


class CSVExporter(FileExporter):
    def export(self, data: dict):
        writer = csv.writer(sys.stdout)

        writer.writerow(data.keys())
        writer.writerow(data.values())


class JSONExporter(FileExporter):
    def export(self, data: dict):
        print(json.dumps(data, indent=4, ensure_ascii=False))


data = {
    "name": "Андрей",
    "age": 19,
    "city": "Алматы",
    "Студент": True,
    "Навыки": ["Владеет ООП", "Владеет c++", "Владеет Python"]
}


JSONExporter().export(data)
CSVExporter().export(data)
