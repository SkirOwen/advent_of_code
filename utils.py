from __future__ import annotations

import os.path
import tomllib
import urllib.request
import urllib.error

from concurrent.futures import ThreadPoolExecutor
from http.client import HTTPResponse
# from tqdm.auto import tqdm

from typing import Iterable, Generator, Sequence

CHUNK_SIZE = 1024


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
	path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"{year}", f"day_{day:02}", "input.txt"))

	# response = urllib.request.urlopen(url)
	a_request = urllib.request.Request(url)
	a_request.add_header("Cookie", f"session={get_token()}")
	response = urllib.request.urlopen(a_request)
	chunks = _get_chunks(response)
	# pbar = tqdm(
	# 	desc=f"[{task}/{total}] Requesting ",
	# 	unit="B",
	# 	total=_get_response_size(response),
	# 	unit_scale=True,
	# 	# format to have current/total size with the full unit, e.g. 60kB/6MB
	# 	# https://github.com/tqdm/tqdm/issues/952
	# 	bar_format="{l_bar}{bar}| {n_fmt}{unit}/{total_fmt}{unit}"
	# 	           " [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
	# )
	# with pbar as t:
	with open(path, "wb") as file:
		for chunk in chunks:
			file.write(chunk)
			# t.update(len(chunk))
		# if done_event.is_set():
		# 	return
	print(f"Downloaded in {path}")


def main():
	download_input(year=2021, day=1)


if __name__ == '__main__':
	main()
