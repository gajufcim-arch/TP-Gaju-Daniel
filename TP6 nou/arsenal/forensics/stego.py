from __future__ import annotations

from PIL import Image


def ascunde_mesaj(imagine_gazda: str, mesaj_text: str, imagine_iesire: str = "stego.png"):
    img = Image.open(imagine_gazda).convert("RGB")
    pixeli = list(img.getdata())

    date_mesaj = mesaj_text.encode("utf-8") + b"\x00"
    biti = "".join(f"{octet:08b}" for octet in date_mesaj)

    if len(biti) > len(pixeli) * 3:
        raise ValueError("Mesajul este prea lung pentru aceasta imagine!")

    pixeli_noi = []
    idx_bit = 0

    for r, g, b in pixeli:
        canale = [r, g, b]
        for i in range(3):
            if idx_bit < len(biti):
                canale[i] = (canale[i] & ~1) | int(biti[idx_bit])
                idx_bit += 1
        pixeli_noi.append(tuple(canale))

    img_noua = Image.new("RGB", img.size)
    img_noua.putdata(pixeli_noi)
    img_noua.save(imagine_iesire)
    print(f"Mesaj ascuns cu succes in '{imagine_iesire}'.")



def dezvaluie_mesaj(imagine_stego: str) -> str:
    img = Image.open(imagine_stego).convert("RGB")
    pixeli = list(img.getdata())

    biti = []
    for r, g, b in pixeli:
        biti.append(str(r & 1))
        biti.append(str(g & 1))
        biti.append(str(b & 1))

    octeti_gasiti = bytearray()
    for i in range(0, len(biti), 8):
        grup = "".join(biti[i : i + 8])
        if len(grup) < 8:
            break
        valoare = int(grup, 2)
        if valoare == 0:
            break
        octeti_gasiti.append(valoare)

    return octeti_gasiti.decode("utf-8", errors="replace")


if __name__ == "__main__":
    mesaj_secret = "FLAG{ascuns_in_pixeli}"
    ascunde_mesaj("probe/foto.jpg", mesaj_secret, "stego.png")
    recuperat = dezvaluie_mesaj("stego.png")
    print(f"Mesaj dezvaluit din 'stego.png': {recuperat}")