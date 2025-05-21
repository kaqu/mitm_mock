from dataclasses import dataclass
from typing import Optional

@dataclass
class Configuration:
	path: str
	active_mock: Optional[str]
	record_session: bool

@dataclass
class Mock:
	enabled: bool
	path: str
	interactive: bool
	offline: bool
	status_code: Optional[int]
	headers: dict[str, str]
	body: Optional[str]
	body_path: Optional[str]

@dataclass
class MockConfiguration:
	name: str
	path: str
	mocks: list[Mock]
