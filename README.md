# landed-cost

Project latihan pertama dengan Claude Code: kalkulator landed cost impor
(CIF → nilai pabean → bea masuk → PPN/PPh 22 → landed cost).

## Instalasi

```bash
pip install -r requirements.txt
```

## Menjalankan kalkulator tunggal

```bash
python landed_cost.py
```

## Membandingkan penawaran beberapa vendor (dari Excel)

```bash
python bandingkan_vendor.py contoh_penawaran.xlsx
python bandingkan_vendor.py contoh_penawaran.xlsx --output hasil.xlsx
```

Kolom wajib di baris pertama file Excel: `vendor`, `fob_usd`, `freight_usd`,
`insurance_usd`, `kurs`. Kolom opsional: `bm_rate`, `ppn_rate`, `pph22_rate`,
`local_cost_idr` (jika kosong dipakai nilai bawaan di `landed_cost.py`).
Hasil diurutkan dari landed cost termurah beserta selisihnya.

## Tes

```bash
pytest
```

> Tarif di kode hanya contoh; verifikasi sesuai HS code dan regulasi berlaku.
> Data di `contoh_penawaran.xlsx` hanya ilustrasi, bukan penawaran nyata.
