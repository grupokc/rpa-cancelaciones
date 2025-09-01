from dataclasses import dataclass
from pathlib import Path


@dataclass
class ETLResult:
    output_extract_path: Path
    output_result_path: Path
    total_records: int