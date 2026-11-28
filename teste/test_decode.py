from arsenal.forensics.decode import desfa, desfa_straturi


def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"


def test_straturi_multiple():
    straturi, rez = desfa_straturi("NTM1OTU3NTk=")
    assert straturi == ["base64", "hex"]
    assert rez == "SYWY"