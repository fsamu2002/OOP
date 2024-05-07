from OsztalyokLetrehozasa import Foglalas


class FoglalasKezelo:
    def __init__(self):
        self.foglalasok = []

    def foglalas(self, szoba, datum):
        self.foglalasok.append(Foglalas(szoba, datum))
        return szoba.ar

    def lemondas(self, foglalas):
        if foglalas in self.foglalasok:
            self.foglalasok.remove(foglalas)
            return True
        return False

    def osszes_foglalas(self):
        return self.foglalasok



