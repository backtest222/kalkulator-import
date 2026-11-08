from landed_cost import ImportInput, hitung_landed_cost


def test_cif_dan_pabean():
    d = ImportInput(fob_usd=100, freight_usd=10, insurance_usd=1, kurs=10_000)
    h = hitung_landed_cost(d)
    assert h["cif_usd"] == 111
    assert h["nilai_pabean_idr"] == 1_110_000


def test_bea_masuk_dan_landed_cost():
    d = ImportInput(
        fob_usd=100, freight_usd=0, insurance_usd=0, kurs=10_000,
        bm_rate=0.10, local_cost_idr=50_000,
    )
    h = hitung_landed_cost(d)
    assert h["bea_masuk_idr"] == 100_000
    assert h["landed_cost_idr"] == 1_000_000 + 100_000 + 50_000
