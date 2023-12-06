from __future__ import annotations

import os.path
import tomllib
import urllib.request
import urllib.error
import shutil

from concurrent.futures import ThreadPoolExecutor
from http.client import HTTPResponse
from datetime import date

from typing import Iterable, Generator, Sequence

CHUNK_SIZE = 1024


def guarantee_existence(path: str) -> str:
	if not os.path.exists(path):
		os.makedirs(path)
	return os.path.abspath(path)


def get_token(config_file: str = "config.toml") -> str:
	"""Get token from TOML config file"""
	# Read config to get connexion settings (ie: token)
	path = os.path.join(os.path.dirname(__file__), config_file)
	with open(path, "rb") as f:
	    CONFIG = tomllib.load(f)
	return CONFIG['session']

def _get_response_size(resp: HTTPResponse) -> None | int:
	"""
	Get the size of the file to download
	"""
	try:
		return int(resp.info()["Content-length"])
	except (ValueError, KeyError, TypeError):
		return None


def _get_chunks(resp: HTTPResponse) -> Generator[bytes, None]:
	"""
	Generator of the chunks to download
	"""
	while True:
		chunk = resp.read(CHUNK_SIZE)
		if not chunk:
			break
		yield chunk


def download_input(year: int | str, day: int | str) -> None:
	url = f"https://adventofcode.com/{year}/day/{day}/input"
	path = os.path.join(guarantee_existence(os.path.join(os.path.dirname(__file__), f"{year}", f"day_{day:02}")), "input.txt")

	# response = urllib.request.urlopen(url)
	a_request = urllib.request.Request(url)
	a_request.add_header("Cookie", f"session={get_token()}")
	response = urllib.request.urlopen(a_request)
	chunks = _get_chunks(response)

	with open(path, "wb") as file:
		for chunk in chunks:
			file.write(chunk)
	print(f"Downloaded in {path}")


def init_day(year: int | str, day: int | str) -> None:
	template_path = os.path.join(os.path.dirname(__file__), "utils", "template.py")
	code_path = os.path.join(guarantee_existence(os.path.join(os.path.dirname(__file__), f"{year}", f"day_{day:02}")), f"day_{day:02}.py")

	if not os.path.exists(code_path):
		print("day code file created")
		shutil.copyfile(template_path, code_path)


def main():
	today = date.today()
	year = today.year
	day = today.day
	download_input(year=year, day=day)
	init_day(year=year, day=day)


if __name__ == '__main__':
	main()
