#!/usr/bin/env python3
"""Prepare a portrait for ASCII conversion.

Usage: python scripts/prep_photo.py source-photo.jpg
Output: data/source-prepped.png
"""
import sys
from pathlib import Path

import cv2
import numpy as np

OUT = Path("data/source-prepped.png")


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/prep_photo.py source-photo.jpg")
    src = cv2.imread(sys.argv[1])
    if src is None:
        raise SystemExit("Could not read the source image")
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUT), gray)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
