from __future__ import annotations
import argparse
import base64
import hashlib
import json
import os
import re
from urllib.parse import unquote


def ghici_strat(s: str) -> str:
    s = s.strip()
    if not s:
        return "necunoscut"
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    if len(s) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", s):
        return "hex"
    if len(s) % 4 == 0 and re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"
    return "necunoscut"


def desfa(s: str) -> tuple[str, bytes]:
    s = s.strip()
    strat = ghici_strat(s)
    if strat == "url":
        return strat, unquote(s).encode("utf-8")
    if strat == "hex":
        return strat, bytes.fromhex(s)
    if strat == "base64":
        return strat, base64.b64decode(s)
    return "necunoscut", s.encode("utf-8")



def citibil(b: bytes) -> bool:
    return len(b) > 0 and all(32 <= c < 127 for c in b)


def desfa_straturi(text_initial: str, max_pasi: int = 8) -> tuple[list[str], str]:
    curent = text_initial.strip()
    straturi_gasite = []

    for _ in range(max_pasi):
        strat = ghici_strat(curent)
        if strat == "necunoscut":
            break
        _, octeti_decodati = desfa(curent)
        if not citibil(octeti_decodati):
            break
        straturi_gasite.append(strat)
        curent = octeti_decodati.decode("utf-8")

    return straturi_gasite, curent



def sparge_xor(date_binare: bytes) -> tuple[int, str] | None:
    for k in range(256):
        clar = bytes(b ^ k for b in date_binare)
        if citibil(clar):
            return k, clar.decode("utf-8")
    return None



def hash_cuvant(cuvant: str, lungime_hash: int) -> str:
    date = cuvant.encode("utf-8")
    if lungime_hash == 32:
        return hashlib.md5(date).hexdigest()
    if lungime_hash == 40:
        return hashlib.sha1(date).hexdigest()
    if lungime_hash == 64:
        return hashlib.sha256(date).hexdigest()
    return ""


def sparge_hashuri(cale_hashuri: str, cale_wordlist: str) -> dict[str, str]:
    with open(cale_hashuri, "r", encoding="utf-8") as f:
        tinte = [linie.strip() for linie in f if linie.strip()]

    with open(cale_wordlist, "r", encoding="latin1") as f:
        cuvinte = [linie.strip() for linie in f if linie.strip()]

    rezultate = {}
    for tinta in tinte:
        for cuv in cuvinte:
            if hash_cuvant(cuv, len(tinta)) == tinta:
                rezultate[tinta] = cuv
                break
    return rezultate



def main():
    parser = argparse.ArgumentParser(description="Decoder universal si spargator XOR/hash")
    parser.add_argument("intrare", help="Sirul de decodat sau calea catre fisier")
    parser.add_argument("--fisier", action="store_true", help="Trateaza intrarea ca cale de fisier")
    parser.add_argument("--xor", action="store_true", help="Sparge fisierul prin XOR pe 1 octet")
    parser.add_argument("--hash", action="store_true", help="Sparge hash-urile din fisier")
    parser.add_argument("--wordlist", default="probe/wordlist.txt", help="Calea catre wordlist")
    args = parser.parse_args()

    if args.xor:
        with open(args.intrare, "rb") as f:
            date = f.read()
        rezultat_xor = sparge_xor(date)
        if rezultat_xor:
            cheie, mesaj = rezultat_xor
            print(f"[XOR] Cheie gasita: {cheie} (0x{cheie:02x})")
            print(f"[XOR] Mesaj: {mesaj}")
        else:
            print("[XOR] Nu s-a gasit nicio cheie valida.")
        return

    if args.hash:
        sparte = sparge_hashuri(args.intrare, args.wordlist)
        for h, parola in sparte.items():
            print(f"[HASH] {h} -> {parola}")
        return

    if args.fisier:
        with open(args.intrare, "r", encoding="utf-8") as f:
            continut = f.read().strip()
    else:
        continut = args.intrare

    straturi, rezultat = desfa_straturi(continut)
    strat_afisat = " -> ".join(straturi) if straturi else "necunoscut"
    print(f"Straturi detectate: {strat_afisat}")
    print(f"Rezultat final:     {rezultat}")

    fisa = {
        "strat": strat_afisat,
        "rezultat": rezultat,
    }
    cale_fisa = os.path.join("arsenal", "forensics", "fisa.json")
    with open(cale_fisa, "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=2, ensure_ascii=False)
    print(f"Fisa salvata in {cale_fisa}")


if __name__ == "__main__":
    main()