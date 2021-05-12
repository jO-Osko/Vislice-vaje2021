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

DATOTEKA_S_STANJEM = "podatki.json"

class Vislice:
    def __init__(self, zacetne_igre,
           datoteka_s_stanjem=DATOTEKA_S_STANJEM):
        self.igre = zacetne_igre
        self.datoteka_s_stanjem = datoteka_s_stanjem

    def prost_id_igre(self):
        if not self.igre: return 1
        return max(self.igre.keys()) + 1
    
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

    def dobi_json_slovar(self):
        slovar_iger = {}
        for id_igre, (igra, stanje) in self.igre.items():
            slovar_iger[id_igre] = [
                igra.dobi_json_slovar(), # Kličem serializacijo igre
                stanje,
            ]

        return {
            "igre": slovar_iger,
            "datoteka_s_stanjem": self.datoteka_s_stanjem,
        }

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke=DATOTEKA_S_STANJEM):
        with open(ime_datoteke, "r") as in_file:
            slovar = json.load(in_file) # Slovar

        return Vislice.dobi_vislice_iz_slovarja(slovar)

    @staticmethod
    def dobi_vislice_iz_slovarja(slovar):
        slovar_iger = {} # To je slovar objektov "Igra"
        for id_igre, (igra_slovar, stanje) in slovar["igre"].items():
            slovar_iger[int(id_igre)] = (
                Igra.dobi_igro_iz_slovarja(igra_slovar),
                stanje
            )
        
        return Vislice(
            slovar_iger, slovar["datoteka_s_stanjem"] 
        )


    def zapisi_v_datoteko(self):
        # Naredi slovar
        slovar = self.dobi_json_slovar()

        # Zapiši ga v datoteko
        with open(self.datoteka_s_stanjem, "w") as out_file:
            json.dump(slovar, out_file, indent=4)

class Igra:
    def __init__(self, geslo, crke): 
        self.geslo = geslo.upper() # Pravilno geslo
        # Kar je uporabnik do sedaj ugibal
        self.crke = crke.upper() # Do sedaj ugibane črke
        # Vse stvari v igri so zgolj velike črke

    def dobi_json_slovar(self):
        return {
            "geslo": self.geslo,
            "crke": self.crke,
        }

    @staticmethod
    def dobi_igro_iz_slovarja(slovar):
        return Igra(
            slovar["geslo"], slovar.get("crke", ""),
        )

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


