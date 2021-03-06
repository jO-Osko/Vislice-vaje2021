import random

# Najprej konstante
STEVILO_DOVOLJENIH_NAPAK = 10

ZACETEK = "A"

PRAVILNA_CRKA = "+"
PONOVLJENA_CRKA = "o"
NAPACNA_CRKA = "-"

ZMAGA = "W"
PORAZ = "X"


class Vislice:
    """
    Krovni objekt, ki upravlja z vsemi igrami
    """
    def __init__(self):
        self.igre = {}

    def prost_id_igre(self):
        return max(self.igre.keys()) + 1 

    def nova_igra(self):
        nov_id = self.prost_id_igre()

        sveza = nova_igra(bazen_besed)

        self.igre[nov_id] = (sveza, ZACETEK)

        return nov_id

    def ugibaj(self, id_igre, crka):
        igra, stanje = self.igre[id_igre]
        
        novo_stanje = igra.ugibaj(crka)
        self.igre[id_igre] = (igra, novo_stanje)

class Igra:
    def __init__(self, geslo, crke): 
        self.geslo = geslo.upper() # Pravilno geslo
        # Kar je uporabnik do sedaj ugibal
        self.crke = crke.upper() # Do sedaj ugibane črke
        # Vse stvari v igri so zgolj velike črke

    def napacne_crke(self):
        return [c for c in self.crke if c not in self.geslo]

    def pravilne_crke(self):
        return [c for c in self.crke if c in self.geslo]

    def stevilo_napak(self):
        return len(self.napacne_crke())

    def poraz(self):
        return self.stevilo_napak() > STEVILO_DOVOLJENIH_NAPAK

    def zmaga(self):
        return all([i in self.crke for i in self.geslo])

    def pravilni_del_gesla(self):
        rezultat = ""
        for c in self.geslo:

            if c in self.crke: # Smo uganili
                rezultat += c
            else: # Nismo še uganili te črke
                rezultat += "_"
        return rezultat

    def nepravilni_ugibi(self):
        return " ".join(self.napacne_crke())

    # Uporabnik poskuša "uganit" črko `crka` ~~~ "X"
    def ugibaj(self, crka):
        crka = crka.upper()
        if self.poraz():
            return PORAZ 
        
        if crka in self.crke:
            return PONOVLJENA_CRKA

        self.crke += crka

        if self.zmaga():
            return ZMAGA
        if crka in self.geslo:
            return PRAVILNA_CRKA
        if self.poraz():
            return PORAZ
        return NAPACNA_CRKA

bazen_besed = []
with open("besede.txt", encoding="utf8") as input_file:
    bazen_besed = input_file.readlines()

def nova_igra(bazen_besed):
    beseda = random.choice(bazen_besed).strip()

    return Igra(beseda, "")


