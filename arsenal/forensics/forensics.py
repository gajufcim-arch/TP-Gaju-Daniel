from __future__ import annotations

import re
import zipfile
from PIL import Image
from PIL.ExifTags import TAGS


def tip_real(cale: str) -> str:
    with open(cale, "rb") as f:
        cap = f.read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return f"necunoscut ({cap.hex()})"



def extrage_strings(cale: str, lungime_min: int = 4) -> list[str]:
    with open(cale, "rb") as f:
        date = f.read()
    pattern = rb"[ -~]{" + str(lungime_min).encode() + rb",}"
    return [m.decode("ascii") for m in re.findall(pattern, date)]



def dms_in_zecimal(dms, emisfera: str) -> float:
    grade, minute, secunde = [float(x) for x in dms]
    val = grade + minute / 60.0 + secunde / 3600.0
    if emisfera in ("S", "W"):
        val = -val
    return round(val, 6)


def analizeaza_exif(cale: str):
    img = Image.open(cale)
    exif = img._getexif() or {}
    for tag_id, val in exif.items():
        nume_tag = TAGS.get(tag_id, tag_id)
        if tag_id != 34853:
            print(f"  {nume_tag} = {val}")

    gps = exif.get(34853)
    if gps:
        lat = dms_in_zecimal(gps[2], gps[1])
        lon = dms_in_zecimal(gps[4], gps[3])
        print(f"  [GPS] Latitudine:  {lat} ({gps[1]})")
        print(f"  [GPS] Longitudine: {lon} ({gps[3]})")



def extrage_zip_ascuns(cale_imagine: str, cale_iesire: str = "gasit.zip"):
    with open(cale_imagine, "rb") as f:
        date = f.read()

    pozitie = date.find(b"PK\x03\x04")
    if pozitie == -1:
        print("Nu s-a gasit nicio arhiva ZIP ascunsa.")
        return

    with open(cale_iesire, "wb") as f:
        f.write(date[pozitie:])
    print(f"Arhiva ZIP extrasa de la octetul {pozitie} in '{cale_iesire}'.")

    with zipfile.ZipFile(cale_iesire, "r") as z:
        for nume in z.namelist():
            continut = z.read(nume).decode("utf-8", errors="replace").strip()
            print(f"  Continut '{nume}': {continut}")


if __name__ == "__main__":
    print("=== B1. Tipul real al fisierelor ===")
    for fis in ["probe/foto.jpg", "probe/ascuns.png", "probe/xor.bin"]:
        print(f"  {fis} -> {tip_real(fis)}")

    print("\n=== B2. Ultimele siruri citibile din probe/ascuns.png ===")
    siruri = extrage_strings("probe/ascuns.png", lungime_min=5)
    for s in siruri[-5:]:
        print(f"  {s}")

    print("\n=== B3. Metadate EXIF si GPS din probe/foto.jpg ===")
    analizeaza_exif("probe/foto.jpg")

    print("\n=== B4. File carving din probe/ascuns.png ===")
    extrage_zip_ascuns("probe/ascuns.png", "gasit.zip")