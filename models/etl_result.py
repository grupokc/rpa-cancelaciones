from dataclasses import dataclass
from pathlib import Path


@dataclass
class ETLResult:
    output_path: Path
    total_records: int