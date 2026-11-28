## Laboratorul 6 — Informații invizibile: forensics și steganografie

### Lucrarea A — Decoder universal (`arsenal/forensics/decode.py`)
* **Mesaj în straturi (`probe/mesaj.txt`):** `base64 -> base64 -> hex` -> `FLAG{straturi_de_encoding}`
* **Spargere XOR (`probe/xor.bin`):** Cheia găsită este `128` (`0x80`), iar mesajul decriptat este `Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}`
* **Spargere hash-uri MD5 (`probe/hashuri.txt`):**
  * `5f4dcc3b5aa765d61d8327deb882cf99` -> `password`
  * `8621ffdbc5698829397d97767ac13db3` -> `dragon`
  * `d8578edf8458ce06fbc5bb76a58c5ca4` -> `qwerty`
  * `0d107d09f5bbe40cade3de5c71e9e9b7` -> `letmein`
  * `d0763edaa9d9bd2a9516280e9044d885` -> `monkey`
* **Verificare:** `python -m pytest` trece (`2 passed` în `teste/test_decode.py`), iar `arsenal/forensics/fisa.json` a fost salvat.

### Lucrarea B — Forensics pe fișiere și steganografie LSB
* **Magic bytes (`arsenal/forensics/forensics.py`):** `probe/foto.jpg` este `jpeg` (`ffd8`), `probe/ascuns.png` este `png` (`89504e47`), iar `probe/xor.bin` este binar necunoscut.
* **Metadate EXIF și GPS (`probe/foto.jpg`):** Dispozitiv `Apple iPhone 13`, data `2026:09:14 10:30:00`, coordonate GPS `47.016667 N, 28.8575 E` (Chișinău).
* **File carving (`probe/ascuns.png`):** Arhiva ZIP ascunsă la coada imaginii a fost extrasă de la octetul `782` în `gasit.zip`; fișierul `secret.txt` din interior conține `FLAG{ascuns_prin_carving}`.
* **Steganografie LSB (`arsenal/forensics/stego.py`, `stego.png`):** S-a ascuns și apoi s-a dezvăluit din biții LSB mesajul `FLAG{ascuns_in_pixeli}`.
* **Bonus (`probe/challenge.bin`):** Decodat din Base64 și spart prin XOR cu cheia `128` (`0x80`) -> `FLAG{lant_complet_despicat}`.