# assets.py
"""
Asset loading & data URIs:
- Remote UBS SVGs (contact/search)
- WebArchive-backed resources (logo, hero image, fonts)
- fontface_blocks() helper used by Streamlit CSS
"""
from __future__ import annotations

import base64
import plistlib
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, List, Dict

import requests

# --------------------------- WebArchive base ---------------------------
ARCHIVE_PATH = "UBS website.webarchive"

def _b64_uri(data: bytes, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"

def _data_uri_from_wa(r: dict, mime_override: Optional[str] = None) -> str:
    mime = mime_override or r.get("WebResourceMIMEType", "application/octet-stream")
    return _b64_uri(r.get("WebResourceData", b""), mime)

def _find_first_data_uri(needles: List[str], mime_override: Optional[str] = None) -> Optional[str]:
    try:
        with open(ARCHIVE_PATH, "rb") as f:
            wa = plistlib.load(f)
    except Exception:
        return None
    for r in wa.get("WebSubresources", []):
        url = (r.get("WebResourceURL", "") or "").lower()
        if all(n.lower() in url for n in needles):
            return _data_uri_from_wa(r, mime_override)
    return None

# --------------------------- Remote icons ---------------------------
def _download_svg_data_uri(url: str) -> str:
    svg = requests.get(url).content
    return _b64_uri(svg, "image/svg+xml")

# UBS contact icon
CONTACT_ICON_URI = _download_svg_data_uri(
    "https://www.ubs.com/content/dam/wcms/icons/fixed/header-buttons/Support-contact.svg"
)

# UBS search icon from defs — convert <path> into standalone <svg>
_search_defs = requests.get(
    "https://www.ubs.com/etc/designs/fit/includes/shared_assets/img/icons/definitions/searchround.20062023.svg"
).content.decode("utf-8")
root = ET.fromstring(_search_defs)
ns = {"svg": "http://www.w3.org/2000/svg"}
path_el = root.find(".//svg:path", ns)
search_svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>{ET.tostring(path_el, encoding='unicode')}</svg>"
SEARCH_ICON_URI = "data:image/svg+xml;base64," + base64.b64encode(search_svg.encode()).decode()

# --------------------------- Assets from WebArchive (with fallbacks) ---------------------------
LOGO_URI = (
    _find_first_data_uri(["ubs_", "logo", "semibold", ".svg"])
    or "https://www.ubs.com/etc/designs/fit/img/UBS_Logo_Semibold.svg"
)
HERO_URI = (
    _find_first_data_uri(["promotion", "image-l", ".jpg"])
    or "https://www.ubs.com/content/homepage/uk/en/new-promotions/gwr2025/jcr:content/promotion/image-l.3840.jpg/1750249353973.jpg"
)

# Fonts (prefer local WA; otherwise None)
FONT_LT = _find_first_data_uri(["frutiger", "-lt", ".woff2"], "font/woff2") or _find_first_data_uri(
    ["frutiger", "light", ".woff2"], "font/woff2"
)
FONT_RG = (
    _find_first_data_uri(["frutiger", "-rg", ".woff2"], "font/woff2")
    or _find_first_data_uri(["frutiger", "regular", ".woff2"], "font/woff2")
    or _find_first_data_uri(["frutiger", "roman", ".woff2"], "font/woff2")
)
FONT_MD = _find_first_data_uri(["frutiger", "-md", ".woff2"], "font/woff2") or _find_first_data_uri(
    ["frutiger", "medium", ".woff2"], "font/woff2"
)
UBS_ICONS = _find_first_data_uri(["ubs-homepagev3-font-icons", ".woff2"], "font/woff2")

# --------------------------- Public helper for @font-face ---------------------------
def fontface_blocks() -> str:
    faces = []
    if FONT_LT:
        faces.append(
            f"@font-face{{font-family:'FrutigerforUBSWeb';font-style:normal;font-weight:300;font-display:swap;src:url({FONT_LT}) format('woff2');}}"
        )
    if FONT_RG:
        faces.append(
            f"@font-face{{font-family:'FrutigerforUBSWeb';font-style:normal;font-weight:400;font-display:swap;src:url({FONT_RG}) format('woff2');}}"
        )
    if FONT_MD:
        faces.append(
            f"@font-face{{font-family:'FrutigerforUBSWeb';font-style:normal;font-weight:500;font-display:swap;src:url({FONT_MD}) format('woff2');}}"
        )
    # Alias Light → 400 if Regular missing
    if FONT_LT and not FONT_RG:
        faces.append(
            f"@font-face{{font-family:'FrutigerforUBSWeb';font-style:normal;font-weight:400;font-display:swap;src:url({FONT_LT}) format('woff2');}}"
        )
    if UBS_ICONS:
        faces.append(
            f"@font-face{{font-family:'ubs-icons';font-style:normal;font-weight:300;font-display:block;src:url({UBS_ICONS}) format('woff2');}}"
        )
    return "\n".join(faces)