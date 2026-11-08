"""Kalkulator landed cost impor (contoh belajar Claude Code).

Tarif di bawah hanya CONTOH. Selalu verifikasi tarif bea masuk (BM),
PPN, dan PPh 22 sesuai HS code dan ketentuan yang berlaku.
"""

from dataclasses import dataclass


@dataclass
class ImportInput:
    fob_usd: float          # harga barang (FOB) dalam USD
    freight_usd: float      # ongkos kirim laut/udara
    insurance_usd: float    # asuransi
    kurs: float             # kurs pajak (IDR per USD)
    bm_rate: float = 0.05   # tarif bea masuk
    ppn_rate: float = 0.11  # PPN impor
    pph22_rate: float = 0.025  # PPh 22 impor (API)
    local_cost_idr: float = 0.0  # biaya lokal: THC, trucking, dll


def hitung_landed_cost(d: ImportInput) -> dict:
    cif_usd = d.fob_usd + d.freight_usd + d.insurance_usd
    nilai_pabean = cif_usd * d.kurs
    bea_masuk = nilai_pabean * d.bm_rate
    dasar_ppn = nilai_pabean + bea_masuk
    ppn = dasar_ppn * d.ppn_rate
    pph22 = dasar_ppn * d.pph22_rate
    # PPN dan PPh 22 impor umumnya bisa dikreditkan, jadi landed cost
    # (biaya riil) hanya memasukkan nilai pabean + BM + biaya lokal.
    landed_cost = nilai_pabean + bea_masuk + d.local_cost_idr
    return {
        "cif_usd": cif_usd,
        "nilai_pabean_idr": nilai_pabean,
        "bea_masuk_idr": bea_masuk,
        "ppn_idr": ppn,
        "pph22_idr": pph22,
        "landed_cost_idr": landed_cost,
    }


def main() -> None:
    contoh = ImportInput(
        fob_usd=100_000,
        freight_usd=5_000,
        insurance_usd=500,
        kurs=16_000,
        local_cost_idr=25_000_000,
    )
    hasil = hitung_landed_cost(contoh)
    for k, v in hasil.items():
        print(f"{k:20s}: {v:,.0f}")


if __name__ == "__main__":
    main()
