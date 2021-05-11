import random
import json

# Najprej konstante
STEVILO_DOVOLJENIH_NAPAK = 10

PRAVILNA_CRKA = "+"
PONOVLJENA_CRKA = "o"
NAPACNA_CRKA = "-"

ZACETEK = "S"
ZMAGA = "W"
PORAZ = "X"


DATOTEKA_ZA_SHRANJEVANJE = "podatki.json"


class Vislice:
    def __init__(self, zacetne_igre=None, zacetni_id=0):
        self.igre = zacetne_igre or {}
        self.max_id = zacetni_id

    def pretvori_v_json_slovar(self):
        slovar_iger = {}

        for id_igre, (igra, stanje) in self.igre.items():
            slovar_iger[id_igre] = (
                igra.pretvori_v_json_slovar(), 
                stanje
            )

        return {
            "max_id": self.max_id,
            "igre": slovar_iger
        }

    def zapisi_v_datoteko(self, datoteka):
        with open(datoteka, "w") as out_file:
            json_slovar = self.pretvori_v_json_slovar()
            json.dump(json_slovar, out_file, indent=2)

    @classmethod
    def dobi_iz_json_slovarja(cls, slovar):
        slovar_iger = {}
        for id_igre, (igra_slovar, stanje) in slovar["igre"].items():
            slovar_iger[int(id_igre)] = (
                Igra.dobi_iz_json_slovarja(igra_slovar), stanje
            )

        return Vislice(slovar_iger, slovar["max_id"])

    @staticmethod
    def preberi_iz_datoteke(datoteka):
        with open(datoteka, "r") as in_file:
            json_slovar = json.load(in_file)
        
        return Vislice.dobi_iz_json_slovarja(json_slovar)

    def prost_id_igre(self):
        self.max_id += 1
        return self.max_id
    
    """ Druga možnost: 
    def prost_id_igre_drugace(self):
        if not self.igre: return 0
        m = max(self.igre.keys())
        return m + 1
    """

    def nova_igra(self,):
        nov_id = self.prost_id_igre()
        sveza_igra = nova_igra(bazen_besed)

        self.igre[nov_id] = (sveza_igra, ZACETEK)
         
        return nov_id 

    def ugibaj(self, id_igre, crka):
        # Najdi
        # Trenutno stanje nas ne zanima
        igra, _ = self.igre[id_igre]

        # Posodobi z delegiranjem
        novo_stanje = igra.ugibaj(crka)
        
        # Popravi v slovarju
        self.igre[id_igre] = (igra, novo_stanje)

        return novo_stanje

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
    

    def pretvori_v_json_slovar(self):
        return {
            "geslo": self.geslo,
            "crke": self.crke,
        }

    @staticmethod
    def dobi_iz_json_slovarja(slovar):
        return Igra(slovar["geslo"], slovar["crke"])

bazen_besed = []
with open("besede.txt", encoding="utf8") as input_file:
    bazen_besed = input_file.readlines()

def nova_igra(bazen_besed):
    beseda = random.choice(bazen_besed).strip()

    return Igra(beseda, "")


