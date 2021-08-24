from dataclasses import dataclass
from typing import Optional

@dataclass
class Mock:
	enabled: bool
	path: str
	interactive: bool
	status_code: Optional[int]
	headers: dict[str, str]
	body: Optional[str]
	body_path: Optional[str]
