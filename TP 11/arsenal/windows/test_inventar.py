from arsenal.windows.inventar import Eveniment, Inventar, Proces


def test_proces_din_temp_e_suspect():
    p = Proces(1, "x.exe", "ana", "C:\\Users\\ana\\AppData\\Local\\Temp\\x.exe")
    assert p.e_suspect() is True


def test_proces_din_windows_nu_e_suspect():
    p = Proces(2, "svchost.exe", "SYSTEM", "C:\\Windows\\System32\\svchost.exe")
    assert p.e_suspect() is False


def test_eveniment_suspect():
    e_suspect = Eveniment(4625, "warning", "Security", "admin", "Failed logon")
    e_normal = Eveniment(4624, "information", "Security", "ana", "Logon success")
    assert e_suspect.e_suspect() is True
    assert e_normal.e_suspect() is False


def test_inventar_metode():
    p1 = Proces(10, "a.exe", "ana", r"C:\Users\ana\AppData\Roaming\a.exe")
    p2 = Proces(20, "b.exe", "ana", r"C:\Windows\b.exe")
    inv = Inventar([p1, p2])

    assert len(inv) == 2
    assert inv.suspecte() == [p1]
    assert inv.pe_user() == {"ana": ["a.exe", "b.exe"]}