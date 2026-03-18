Akna Kalkulaator (kok.py)
Tööriist aknaraamide detailide mõõtmete ja koguste arvutamiseks. Sisendiks on akna kogulaius, kõrgus ja kogus (tk).

Süsteeminõuded

Python 3.7+
pandas

bashpip install pandas

Käivitamine on käsurealt: 
python3 /home/karl_kaspar/my-project1/src/kok.py

Sisendid
SisendTüüpKirjeldusTüüp (A / TA)tekstAkna tüüp: A = aken, TA = topeltakenLaius (mm)numberKogu raami laius millimeetritesKõrgus (mm)numberKogu raami kõrgus millimeetritesKogus (tk)täisarvToodetavate akende arv

Akna tüübid

A — tavaaken (aken)
TA — topeltaken (kaks sektsiooni kõrvuti)


Arvutusvalemid

L = kogu raamlaius, K = kogu raamkõrgus, tk = kogus

DetailA (aken)TA (topeltaken)Raam LL - 86 × tk(L - 80) / 2 × tk×2Raam KK - 96 × tkK - 96 × tk×2Klaas LL - 86 - 100 × tk(L - 80) / 2 - 100 × tk×2Klaas KK - 96 - 100 × tkK - 96 - 100 × tk×2Lengi ÜHL × tkL × tkLengi AHL - 100 × tkL - 100 × tkLengi VERTK - 50 × tk×2K - 50 × tk×2Raami ÜHL - 86 × tk(L - 80) / 2 × tk×2Raami AHL - 86 × tk(L - 80) / 2 × tk×2Raami VERTK - 96 × tk×2K - 96 × tk×4Klaasiliist HORL - 86 - 100 + 4 × tk×2(L-80)/2 - 100 + 4 × tk×4Klaasiliist VERTK - 96 - 100 + 4 × tk×2K - 96 - 100 + 4 × tk×4
Konfiguratsioon: P44-14 kõikidel tüüpidel.

Näide
Sisend:
Sisesta tüüp (A / TA): A
Sisesta kogu raami laius (mm): 900
Sisesta kogu raami kõrgus (mm): 900
Sisesta kogus (tk): 3
Väljund:
Raam L:            814 mm  (3 tk)
Raam K:            804 mm  (3 tk)
Klaas L:           714 mm  (3 tk)
Klaas K:           704 mm  (3 tk)
Lengi ÜH:          900 mm  (3 tk)
Lengi AH:          800 mm  (3 tk)
Lengi VERT:        850 mm  (6 tk)
Raami ÜH:          814 mm  (3 tk)
Raami AH:          814 mm  (3 tk)
Raami VERT:        804 mm  (6 tk)
Klaasiliist HOR:   718 mm  (6 tk)
Klaasiliist VERT:  608 mm  (6 tk)

Koodi struktuur
FunktsioonKirjelduscalculate_A(L, K, tk)Arvutab kõik detailid A-tüüpi aknalecalculate_TA(L, K, tk)Arvutab kõik detailid TA-tüüpi topeltaknale__main__Kasutajaliides: küsib sisendit ja kuvab tulemused

Veatöötlus

Vale tüüp — programm kuvab veateate ja lõpetab töö
Mittenumbriline sisend — ValueError, palutakse sisestada korrektne väärtus
Excel-faili laadimisviga — kasutatakse vaikimisi reegleid


Reeglite allikas
Arvutusreeglid on laetud failist Tootmisreeglid.xlsx
## License
MIT License - Free to use and modify.

## Contributing
Pull requests are welcome. For major changes, please open an issue first.
