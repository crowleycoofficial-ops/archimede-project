"""Utilities used by the demo: downloading assets (pretrained weights).
"""
import os
import shutil


def download_file(url: str, dest: str, chunk_size: int = 8192):
    """Download a file from url to dest. Overwrites existing file.

    Uses requests if available, otherwise falls back to urllib.
    """
    try:
        import requests
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
        return dest
    except Exception:
        # Fallback to urllib
        try:
            from urllib.request import urlopen
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with urlopen(url, timeout=30) as r, open(dest, "wb") as f:
                shutil.copyfileobj(r, f)
            return dest
        except Exception as e:
            raise RuntimeError(f"Failed to download {url}: {e}")


def ensure_weights(url: str, dest_path: str):
    """Ensure that pretrained weights exist at dest_path. If not, try to download from url."""
    if os.path.exists(dest_path):
        return dest_path
    if not url:
        raise RuntimeError("No weights found locally and no download URL provided.")
    return download_file(url, dest_path)
