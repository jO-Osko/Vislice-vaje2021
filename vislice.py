import bottle
import model

COOKIE_SECRET = "bkygnluob3764n78m9QN89ZXMZNZNHUZQIWDNASDMHSJMjsmdfs"

@bottle.get("/")
def index():
    return bottle.template("index.tpl")


@bottle.post("/igra/")
def nova_igra():

    visilice = model.Vislice.preberi_iz_datoteke(
        model.DATOTEKA_ZA_SHRANJEVANJE
    )

    id_igre = visilice.nova_igra()

    visilice.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
    
    bottle.response.set_cookie("ID_IGRE", str(id_igre), path="/", 
        secret=COOKIE_SECRET)
    
    bottle.redirect("/igraj/")


@bottle.get("/igraj/")
def pokazi_igro():

    cookie = bottle.request.get_cookie("ID_IGRE", secret=COOKIE_SECRET)
    if cookie is None:
        bottle.redirect("/")
        return

    id_igre = int(
        cookie
    )

    visilice = model.Vislice.preberi_iz_datoteke(
        model.DATOTEKA_ZA_SHRANJEVANJE
    )
    trenutna_igra, trenutno_stanje = \
        visilice.igre[id_igre]

    visilice.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)

    return bottle.template("igra.tpl",
        igra=trenutna_igra, stanje=trenutno_stanje
    )

@bottle.post("/igraj/")
def ugibaj_na_igri():
    id_igre = int(
        bottle.request.get_cookie("ID_IGRE", secret=COOKIE_SECRET)
    )
    visilice = model.Vislice.preberi_iz_datoteke(
        model.DATOTEKA_ZA_SHRANJEVANJE
    )
    ugibana = bottle.request.forms["crka"]
    
    visilice.ugibaj(id_igre, ugibana)
    visilice.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
    return bottle.redirect(f"/igraj/")




bottle.run(reloader=True, debug=True)