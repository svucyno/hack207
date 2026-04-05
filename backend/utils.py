import os
import math
import re
import hashlib

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        return "error_hash"

def calculate_entropy(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            if not data:
                return 0.0
            entropy = 0.0
            for x in range(256):
                p_x = float(data.count(x)) / len(data)
                if p_x > 0:
                    entropy += - p_x * math.log(p_x, 2)
            return float(entropy)
    except Exception:
        return 0.0

def extract_metadata(file_path):
    size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
    ext = os.path.splitext(file_path)[1].lower()
    entropy = calculate_entropy(file_path)
    return {
        "size": size,
        "extension": ext,
        "entropy": entropy,
        "randomness": "High" if entropy > 7.0 else ("Medium" if entropy > 5.0 else "Low")
    }

def detect_urls(file_path):
    # Search for URLs in the file's binary or text content
    urls = []
    try:
        url_pattern = re.compile(rb'https?://[^\s<>"]+|www\.[^\s<>"]+')
        with open(file_path, "rb") as f:
            data = f.read()
            found = set(url_pattern.findall(data))
            urls = [url.decode('utf-8', errors='ignore') for url in found]
    except Exception:
        pass
    return urls
