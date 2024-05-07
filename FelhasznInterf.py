from datetime import datetime
from OsztalyokLetrehozasa import EgyagyasSzoba,KetagyasSzoba,Szalloda
from FoglalasokKezelese import FoglalasKezelo


def pelda_adatok_feltoltese(szalloda):
    egyagyas1 = EgyagyasSzoba("101")
    egyagyas2 = EgyagyasSzoba("102")
    ketagyas1 = KetagyasSzoba("201")
    szalloda.uj_szoba(egyagyas1)
    szalloda.uj_szoba(egyagyas2)
    szalloda.uj_szoba(ketagyas1)

    foglalas_kezelo = FoglalasKezelo()
    foglalas_kezelo.foglalas(egyagyas1, datetime(2024, 5, 22))
    foglalas_kezelo.foglalas(egyagyas2, datetime(2024, 5, 28))
    foglalas_kezelo.foglalas(ketagyas1, datetime(2024, 6, 7))
    foglalas_kezelo.foglalas(egyagyas1, datetime(2024, 8, 25))
    foglalas_kezelo.foglalas(egyagyas2, datetime(2024, 11, 23))

    return foglalas_kezelo
szalloda = Szalloda("Azúrkék Palota")
foglalas_kezelo = pelda_adatok_feltoltese(szalloda)


class FelhasznaloiFelulet:
    def __init__(self, szalloda, foglalas_kezelo):
        self.szalloda = szalloda
        self.foglalas_kezelo = foglalas_kezelo

    def foglalas_felvetele(self):
        while True:
            print("\nMilyen típusú szobát szeretne foglalni?")
            print("1. Egy ágyas szoba")
            print("2. Két ágyas szoba")
            valasztas = input("Kérem adja meg a választott típus sorszámát: ")

            if valasztas == "1":
                szobak = [szoba for szoba in self.szalloda.szobak if isinstance(szoba, EgyagyasSzoba)]
                break
            elif valasztas == "2":
                szobak = [szoba for szoba in self.szalloda.szobak if isinstance(szoba, KetagyasSzoba)]
                break
            else:
                print("\nÉrvénytelen választás! Kérem válasszon újra.")

        print("\nElérhető szobák:")
        for szoba in szobak:
            print(f"Szobaszám: {szoba.szobaszam}, Ár: {szoba.ar}")

        while True:
            szobaszam = input("Kérem adja meg a foglalni kívánt szoba számát: ")
            if any(szobaszam == szoba.szobaszam for szoba in szobak):
                break
            else:
                print("\nÉrvénytelen szobaszám! Kérem válasszon újra.")

        for szoba in szobak:
            if szoba.szobaszam == szobaszam:
                while True:
                    datum_str = input("Kérem adja meg a foglalás dátumát (YYYY-MM-DD formátumban): ")
                    try:
                        datum = datetime.strptime(datum_str, "%Y-%m-%d")
                        if not self.ervenyes_datum(datum):
                            print("\nÉrvénytelen időpont! Kérjük adjon meg érvényes dátumot.")
                        elif not self.szoba_elerheto(szoba, datum):
                            print("\nEz a szoba már foglalt erre az időpontra! Kérjük válasszon másik időpontot.")
                        elif datum < datetime.now():
                            print("\nÉrvénytelen időpont! Nem lehet visszamenőleg foglalni.")
                        else:
                            ar = self.foglalas_kezelo.foglalas(szoba, datum)
                            print(f"\nA foglalás sikeres! Ár: {ar} Ft/Éj")
                            return
                    except ValueError:
                        print("\nÉrvénytelen dátum formátum! Kérjük adjon meg érvényes dátumot.")

    def foglalas_leadasa(self):
        while True:
            print("\nFoglalások:")
            foglalasok = self.foglalas_kezelo.osszes_foglalas()
            if not foglalasok:
                print("\nNincs aktuális foglalás.")
                return

            for i, foglalas in enumerate(foglalasok):
                print(f"{i+1}. Szobaszám: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}")
            valasztas = input("Kérem adja meg a lemondani kívánt foglalás sorszámát (vagy '0' visszalépéshez): ")
            if valasztas == '0':
                return

            if valasztas.isdigit():
                valasztas = int(valasztas)
                if 1 <= valasztas <= len(foglalasok):
                    if self.foglalas_kezelo.lemondas(foglalasok[valasztas - 1]):
                        print("\nA foglalás sikeresen lemondva!")
                        return
                    else:
                        print("\nA foglalás lemondása sikertelen!")
                else:
                    print("\nA foglalás lemondása sikertelen, érvénytelen sorszám!")
            else:
                print("\nÉrvénytelen választás! Kérem adjon meg egy sorszámot vagy '0'-t visszalépéshez.")

    def foglalasok_listazasa(self):
        foglalasok = self.foglalas_kezelo.osszes_foglalas()
        if not foglalasok:
            print("\nNincs aktuális foglalás.")
        else:
            print("\nAktuális foglalások:")
            for foglalas in foglalasok:
                print(f"Szobaszám: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}")

    def ervenyes_datum(self, datum):
        return datum >= datetime.now()

    def szoba_elerheto(self, szoba, datum):
        for foglalas in self.foglalas_kezelo.osszes_foglalas():
            if foglalas.szoba == szoba and foglalas.datum == datum:
                return False
        return True

    def futtat(self):
        while True:
            print("\nAzúrkék Palota")
            print("\nVálasszon műveletet:")
            print("1. Foglalás")
            print("2. Foglalás lemondása")
            print("3. Foglalások listázása")
            print("0. Kilépés")
            valasztas = input("Kérem adja meg a választott művelet sorszámát: ")

            if valasztas == "1":
                self.foglalas_felvetele()
            elif valasztas == "2":
                self.foglalas_leadasa()
            elif valasztas == "3":
                self.foglalasok_listazasa()
            elif valasztas == "0":
                print("Kilépés...")
                break
            else:
                print("\nÉrvénytelen választás!")

felhasznaloi_felulet = FelhasznaloiFelulet(szalloda, foglalas_kezelo)
felhasznaloi_felulet.futtat()
