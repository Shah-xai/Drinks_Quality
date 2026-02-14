import os
from pathlib import Path
import gdown
from drinks_quality import logger
from drinks_quality.utils.common import get_size  # assuming you have this

class DataIngestion:
    def __init__(self, config):
        self.config = config

    def download_data(self):
        logger.info(f"Downloading data from {self.config.source_URL} to {self.config.local_data_file}")

        out_path = Path(self.config.local_data_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if out_path.exists():
            logger.info(f"File already exists of size: {get_size(out_path)}")
            return

        # Works with either full share link or direct id URL
        gdown.download(self.config.source_URL, str(out_path), quiet=False, fuzzy=True)

        # Safety check: ensure it's not HTML
        head = out_path.read_text(encoding="utf-8", errors="ignore")[:200].lower()
        if "<html" in head or "doctype html" in head:
            out_path.unlink(missing_ok=True)
            raise ValueError("Downloaded HTML from Google Drive instead of the CSV. Check sharing permissions/link.")

        logger.info(f"Downloaded file saved to: {out_path} ({get_size(out_path)})")
