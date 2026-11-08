"""Bandingkan landed cost beberapa penawaran vendor dari satu file Excel.

Cara pakai:
    python bandingkan_vendor.py contoh_penawaran.xlsx
    python bandingkan_vendor.py contoh_penawaran.xlsx --output hasil.xlsx

Kolom wajib di baris pertama (header) sheet aktif:
    vendor, fob_usd, freight_usd, insurance_usd, kurs
Kolom opsional (jika kosong dipakai nilai bawaan dari landed_cost.py):
    bm_rate, ppn_rate, pph22_rate, local_cost_idr
"""

import argparse

from openpyxl import Workbook, load_workbook

from landed_cost import ImportInput, hitung_landed_cost

WAJIB = ["vendor", "fob_usd", "freight_usd", "insurance_usd", "kurs"]
OPSIONAL = ["bm_rate", "ppn_rate", "pph22_rate", "local_cost_idr"]


def baca_penawaran(path: str) -> list[dict]:
    """Baca file Excel, kembalikan list baris (dict) per vendor."""
    ws = load_workbook(path, data_only=True).active
    baris = list(ws.iter_rows(values_only=True))
    if not baris:
        raise ValueError("File Excel kosong.")

    header = [str(h).strip().lower() if h is not None else "" for h in baris[0]]
    hilang = [k for k in WAJIB if k not in header]
    if hilang:
        raise ValueError(f"Kolom wajib tidak ditemukan: {', '.join(hilang)}")

    hasil = []
    for no, r in enumerate(baris[1:], start=2):
        if all(c is None for c in r):
            continue  # lewati baris kosong
        data = dict(zip(header, r))
        for k in WAJIB[1:]:
            if data.get(k) is None:
                raise ValueError(f"Baris {no}: kolom '{k}' kosong.")
        hasil.append(data)
    return hasil


def bandingkan(penawaran: list[dict]) -> list[dict]:
    """Hitung landed cost tiap vendor, urut dari termurah. Beri peringkat."""
    rows = []
    for p in penawaran:
        kwargs = {k: float(p[k]) for k in WAJIB[1:]}
        for k in OPSIONAL:
            if p.get(k) is not None:
                kwargs[k] = float(p[k])
        hitung = hitung_landed_cost(ImportInput(**kwargs))
        rows.append({"vendor": p["vendor"], **hitung})

    rows.sort(key=lambda r: r["landed_cost_idr"])
    termurah = rows[0]["landed_cost_idr"] if rows else 0
    for i, r in enumerate(rows, start=1):
        r["peringkat"] = i
        r["selisih_vs_termurah_idr"] = r["landed_cost_idr"] - termurah
        r["selisih_pct"] = (
            r["selisih_vs_termurah_idr"] / termurah if termurah else 0.0
        )
    return rows


def cetak(rows: list[dict]) -> None:
    print(f"{'#':>2}  {'Vendor':<20}{'Landed cost (IDR)':>20}{'Selisih (IDR)':>18}{'%':>8}")
    for r in rows:
        print(
            f"{r['peringkat']:>2}  {str(r['vendor']):<20}"
            f"{r['landed_cost_idr']:>20,.0f}"
            f"{r['selisih_vs_termurah_idr']:>18,.0f}"
            f"{r['selisih_pct']:>8.1%}"
        )


def simpan_excel(rows: list[dict], path: str) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Perbandingan"
    kolom = [
        "peringkat", "vendor", "cif_usd", "nilai_pabean_idr", "bea_masuk_idr",
        "ppn_idr", "pph22_idr", "landed_cost_idr",
        "selisih_vs_termurah_idr", "selisih_pct",
    ]
    ws.append(kolom)
    for r in rows:
        ws.append([r[k] for k in kolom])
    for sel in ws["J"][1:]:
        sel.number_format = "0.0%"
    wb.save(path)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file_excel", help="file .xlsx berisi penawaran vendor")
    ap.add_argument("--output", help="simpan hasil ke file .xlsx baru")
    args = ap.parse_args()

    rows = bandingkan(baca_penawaran(args.file_excel))
    cetak(rows)
    if args.output:
        simpan_excel(rows, args.output)
        print(f"\nHasil disimpan ke {args.output}")


if __name__ == "__main__":
    main()
