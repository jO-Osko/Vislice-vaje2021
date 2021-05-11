import bottle
import model


@bottle.get("/")
def index():
    return bottle.template("index.tpl")


@bottle.post("/igra/")
def nova_igra():

    visilice = model.Vislice.preberi_iz_datoteke(
        model.DATOTEKA_ZA_SHRANJEVANJE
    )

    id_igre = visilice.nova_igra()
    novi_url = f"/igra/{id_igre}/"

    visilice.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)

    bottle.redirect(novi_url)


@bottle.get("/igra/<id_igre:int>/")
def pokazi_igro(id_igre):
    visilice = model.Vislice.preberi_iz_datoteke(
        model.DATOTEKA_ZA_SHRANJEVANJE
    )
    trenutna_igra, trenutno_stanje = \
        visilice.igre[id_igre]

    visilice.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)

    return bottle.template("igra.tpl",
        igra=trenutna_igra, stanje=trenutno_stanje
    )

@bottle.post("/igra/<id_igre:int>/")
def ugibaj_na_igri(id_igre):
    visilice = model.Vislice.preberi_iz_datoteke(
        model.DATOTEKA_ZA_SHRANJEVANJE
    )
    ugibana = bottle.request.forms["crka"]
    
    visilice.ugibaj(id_igre, ugibana)
    visilice.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
    return bottle.redirect(f"/igra/{id_igre}/")




bottle.run(reloader=True, debug=True)