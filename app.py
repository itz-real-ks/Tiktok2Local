#!/usr/bin/env python3

import argparse
import asyncio
import csv
import json
import subprocess
from pathlib import Path
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

class TikTokNoWatermarkDownloader:
    API_URL = "https://api.twitterpicker.com/tiktok/mediav2?id={id}"

    API_HEADERS = {
        "User-Agent":
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://twitterpicker.com/",
    }

    CURL_HEADERS = [
        "-H",
        "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "-H",
        "Referer: https://www.tiktok.com/",
    ]

    def __init__(self, output_dir: Path, csv_log: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.csv_log = csv_log
        self._init_csv()

    # -------------------------
    # CSV logging
    # -------------------------
    def _init_csv(self):
        if not self.csv_log.exists():
            with open(self.csv_log, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "status", "filename", "error"])

    def log(self, video_id, status, filename="", error=""):
        with open(self.csv_log, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([video_id, status, filename, error])

    # -------------------------
    # Metadata fetch
    # -------------------------
    def fetch_metadata(self, video_id: str) -> dict:
        req = Request(
            self.API_URL.format(id=video_id),
            headers=self.API_HEADERS,
        )
        with urlopen(req, timeout=15) as resp:
            text = resp.read().decode()

        soup = BeautifulSoup(text, "html.parser")
        return json.loads(soup.get_text())

    # -------------------------
    # Strict no-watermark
    # -------------------------
    @staticmethod
    def extract_no_watermark_url(data: dict) -> str:
        url = data.get("video_no_watermark", {}).get("url")
        if not url:
            raise RuntimeError("no_watermark video not available")
        return url

    # -------------------------
    # curl download
    # -------------------------
    async def download_with_curl(self, out_path: Path, url: str):
        cmd = [
            "curl",
            "-L",
            "--progress-bar",
            *self.CURL_HEADERS,
            "-o",
            str(out_path),
            url,
        ]

        proc = await asyncio.create_subprocess_exec(*cmd)
        await proc.wait()

        if proc.returncode != 0:
            raise RuntimeError("curl failed")

    # -------------------------
    # Pipeline
    # -------------------------
    async def process_video(self, video_id: str, filename: str | None):
        try:
            data = self.fetch_metadata(video_id)
            url = self.extract_no_watermark_url(data)

            fname = filename or f"{video_id}.mp4"
            out_path = self.output_dir / fname

            await self.download_with_curl(out_path, url)

            self.log(video_id, "success", fname)
            print(f"[OK] {video_id} → {fname}")

        except Exception as e:
            self.log(video_id, "failed", "", str(e))
            print(f"[FAIL] {video_id}: {e}")

    # -------------------------
    # Batch runner
    # -------------------------
    async def run(self, video_ids: list[str], filename: str | None):
        tasks = [self.process_video(vid, filename) for vid in video_ids]
        await asyncio.gather(*tasks)


# =========================
# CLI
# =========================
def main():
    parser = argparse.ArgumentParser(
        description="Download TikTok no-watermark videos using curl")
    parser.add_argument(
        "--id",
        nargs="+",
        required=True,
        help="TikTok video ID(s)",
    )
    parser.add_argument(
        "--out",
        default="videos",
        help="Output directory (default: videos)",
    )
    parser.add_argument(
        "--name",
        help="Custom output filename (default: {id}.mp4)",
    )
    parser.add_argument(
        "--log",
        default="download_log.csv",
        help="CSV log file (default: download_log.csv)",
    )

    args = parser.parse_args()

    downloader = TikTokNoWatermarkDownloader(
        output_dir=Path(args.out),
        csv_log=Path(args.log),
    )

    asyncio.run(downloader.run(args.id, args.name))


if __name__ == "__main__":
    main()
