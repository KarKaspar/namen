import pandas as pd
 
# -------------------------------------------------------
# Rules loaded from Tootmisreeglid.xlsx
# A  = aken (single window)
# TA = topeltaken (double window)
#
# Column meanings:
#   L, K  = laius (width), kõrgus (height)  -- total frame size input
#   raam  : L = raam length, H = raam height
#   klaas : L = glass length, H = glass height
#   konfig: P44-14 for all types
#
# A  type formulas:
#   raam_L  = L - 86        (1 tk)
#   raam_K  = K - 96        (1 tk)
#   klaas_L = L - 86 - 100  (1 tk)
#   klaas_K = K - 96 - 100  (1 tk)
#   lengi detailid:
#     ÜH (L)       = L        (1 tk)
#     AH (L-100)   = L - 100  (1 tk)
#     VERT (K-50)  = K - 50   (2 tk)
#   raami detailid:
#     ÜH (L-86)       = L - 86     (1 tk)
#     AH (L-86)       = L - 86     (1 tk)
#     VERT (K-96-96)  = K - 96     (2 tk)  -- K-96-96 means K-96, qty x2
#   klaasiliistud:
#     HOR  (L-86-100+4)  = L - 86 - 100 + 4  (2 tk)
#     VERT (K-96-100+4)  = K - 96 - 100 + 4  (2 tk)
#
# TA type formulas (double window, split horizontally):
#   raam_L  = (L - 80) / 2        (2 tk)
#   raam_K  = K - 96              (2 tk)
#   klaas_L = (L - 80) / 2 - 100  (2 tk)
#   klaas_K = K - 96 - 100        (2 tk)
#   lengi detailid:
#     ÜH (L)       = L        (1 tk)
#     AH (L-100)   = L - 100  (1 tk)
#     VERT (K-50)  = K - 50   (2 tk)
#   raami detailid:
#     ÜH  ((L-80)/2)      = (L-80)/2     (2 tk)
#     AH  ((L-80)/2)      = (L-80)/2     (2 tk)
#     VERT (K-96-96)      = K - 96       (4 tk)
#   klaasiliistud:
#     HOR  ((L-80)/2-100+4)  = (L-80)/2 - 100 + 4  (4 tk)
#     VERT (K-96-100+4)      = K - 96 - 100 + 4    (4 tk)
# -------------------------------------------------------
 
 
def calculate_A(L, K, tk):
    """Single window (aken) calculations"""
    raam_L = L - 86
    raam_K = K - 96
    klaas_L = L - 86 - 100
    klaas_K = K - 96 - 100
 
    lengi_UH = L
    lengi_AH = L - 100
    lengi_VERT = K - 50
 
    raami_UH = L - 86
    raami_AH = L - 86
    raami_VERT = K - 96
 
    klaasiliist_HOR = L - 86 - 100 + 4
    klaasiliist_VERT = K - 96 - 100 + 4
 
    return {
        'Tüüp': 'A (aken)',
        'Konfiguratsioon': 'P44-14',
        '--- Raam ---': '',
        'Raam L': f'{raam_L:.0f} mm',
        'Raam L (tk)': tk,
        'Raam K': f'{raam_K:.0f} mm',
        'Raam K (tk)': tk,
        '--- Klaas/KLP mõõt ---': '',
        'Klaas L': f'{klaas_L:.0f} mm',
        'Klaas L (tk)': tk,
        'Klaas K': f'{klaas_K:.0f} mm',
        'Klaas K (tk)': tk,
        '--- Lengi detailid ---': '',
        'Lengi ÜH': f'{lengi_UH:.0f} mm',
        'Lengi ÜH (tk)': tk,
        'Lengi AH': f'{lengi_AH:.0f} mm',
        'Lengi AH (tk)': tk,
        'Lengi VERT': f'{lengi_VERT:.0f} mm',
        'Lengi VERT (tk)': tk * 2,
        '--- Raami detailid ---': '',
        'Raami ÜH': f'{raami_UH:.0f} mm',
        'Raami ÜH (tk)': tk,
        'Raami AH': f'{raami_AH:.0f} mm',
        'Raami AH (tk)': tk,
        'Raami VERT': f'{raami_VERT:.0f} mm',
        'Raami VERT (tk)': tk * 2,
        '--- Klaasiliistud ---': '',
        'Klaasiliist HOR': f'{klaasiliist_HOR:.0f} mm',
        'Klaasiliist HOR (tk)': tk * 2,
        'Klaasiliist VERT': f'{klaasiliist_VERT:.0f} mm',
        'Klaasiliist VERT (tk)': tk * 2,
    }
 
 
def calculate_TA(L, K, tk):
    """Double window (topeltaken) calculations"""
    raam_L = (L - 80) / 2
    raam_K = K - 96
    klaas_L = (L - 80) / 2 - 100
    klaas_K = K - 96 - 100
 
    lengi_UH = L
    lengi_AH = L - 100
    lengi_VERT = K - 50
 
    raami_UH = (L - 80) / 2
    raami_AH = (L - 80) / 2
    raami_VERT = K - 96
 
    klaasiliist_HOR = (L - 80) / 2 - 100 + 4
    klaasiliist_VERT = K - 96 - 100 + 4
 
    return {
        'Tüüp': 'TA (topeltaken)',
        'Konfiguratsioon': 'P44-14',
        '--- Raam ---': '',
        'Raam L': f'{raam_L:.0f} mm',
        'Raam L (tk)': tk * 2,
        'Raam K': f'{raam_K:.0f} mm',
        'Raam K (tk)': tk * 2,
        '--- Klaas/KLP mõõt ---': '',
        'Klaas L': f'{klaas_L:.0f} mm',
        'Klaas L (tk)': tk * 2,
        'Klaas K': f'{klaas_K:.0f} mm',
        'Klaas K (tk)': tk * 2,
        '--- Lengi detailid ---': '',
        'Lengi ÜH': f'{lengi_UH:.0f} mm',
        'Lengi ÜH (tk)': tk,
        'Lengi AH': f'{lengi_AH:.0f} mm',
        'Lengi AH (tk)': tk,
        'Lengi VERT': f'{lengi_VERT:.0f} mm',
        'Lengi VERT (tk)': tk * 2,
        '--- Raami detailid ---': '',
        'Raami ÜH': f'{raami_UH:.0f} mm',
        'Raami ÜH (tk)': tk * 2,
        'Raami AH': f'{raami_AH:.0f} mm',
        'Raami AH (tk)': tk * 2,
        'Raami VERT': f'{raami_VERT:.0f} mm',
        'Raami VERT (tk)': tk * 4,
        '--- Klaasiliistud ---': '',
        'Klaasiliist HOR': f'{klaasiliist_HOR:.0f} mm',
        'Klaasiliist HOR (tk)': tk * 4,
        'Klaasiliist VERT': f'{klaasiliist_VERT:.0f} mm',
        'Klaasiliist VERT (tk)': tk * 4,
    }
 
 
if __name__ == "__main__":
    print("=== Akna kalkulaator ===")
    print("Tüübid: A (aken), TA (topeltaken)")
    print()
 
    try:
        window_type = input("Sisesta tüüp (A / TA): ").strip().upper()
        if window_type not in ('A', 'TA'):
            print("Vigane tüüp! Kasuta A või TA.")
            exit()
 
        L = float(input("Sisesta kogu raami laius (mm): "))
        K = float(input("Sisesta kogu raami kõrgus (mm): "))
        tk = int(input("Sisesta kogus (tk): "))
 
        if window_type == 'A':
            results = calculate_A(L, K, tk)
        else:
            results = calculate_TA(L, K, tk)
 
        print("\n=== Tulemused ===")
        for key, value in results.items():
            if key.startswith('---'):
                print(f"\n{value if value else key.replace('-','').strip()}")
            else:
                print(f"  {key}: {value}")
 
    except ValueError:
        print("Palun sisesta korrektsed numbrilised väärtused.")