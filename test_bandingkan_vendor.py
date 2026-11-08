import pytest
from openpyxl import Workbook

from bandingkan_vendor import bandingkan, baca_penawaran

HEADER = ["vendor", "fob_usd", "freight_usd", "insurance_usd", "kurs",
          "bm_rate", "local_cost_idr"]


def buat_excel(path, baris, header=HEADER):
    wb = Workbook()
    ws = wb.active
    ws.append(header)
    for b in baris:
        ws.append(b)
    wb.save(path)


def test_urut_termurah_dan_selisih(tmp_path):
    f = tmp_path / "p.xlsx"
    buat_excel(f, [
        ["A", 100, 0, 0, 10_000, 0.0, 0],   # landed 1.000.000
        ["B", 90, 0, 0, 10_000, 0.0, 0],    # landed   900.000
    ])
    rows = bandingkan(baca_penawaran(str(f)))
    assert [r["vendor"] for r in rows] == ["B", "A"]
    assert rows[0]["peringkat"] == 1
    assert rows[0]["selisih_vs_termurah_idr"] == 0
    assert rows[1]["selisih_vs_termurah_idr"] == 100_000
    assert rows[1]["selisih_pct"] == pytest.approx(100_000 / 900_000)


def test_kolom_opsional_kosong_pakai_default(tmp_path):
    f = tmp_path / "p.xlsx"
    buat_excel(f, [["A", 100, 0, 0, 10_000, None, None]])
    r = bandingkan(baca_penawaran(str(f)))[0]
    # bm_rate bawaan 5%: 1.000.000 + 50.000
    assert r["landed_cost_idr"] == 1_050_000


def test_kolom_wajib_hilang(tmp_path):
    f = tmp_path / "p.xlsx"
    buat_excel(f, [["A", 100]], header=["vendor", "fob_usd"])
    with pytest.raises(ValueError, match="Kolom wajib"):
        baca_penawaran(str(f))


def test_sel_wajib_kosong(tmp_path):
    f = tmp_path / "p.xlsx"
    buat_excel(f, [["A", None, 0, 0, 10_000, 0.05, 0]])
    with pytest.raises(ValueError, match="Baris 2"):
        baca_penawaran(str(f))


def test_baris_kosong_dilewati(tmp_path):
    f = tmp_path / "p.xlsx"
    buat_excel(f, [["A", 100, 0, 0, 10_000, 0.0, 0],
                   [None] * 7,
                   ["B", 80, 0, 0, 10_000, 0.0, 0]])
    assert len(baca_penawaran(str(f))) == 2
