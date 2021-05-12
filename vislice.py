import bottle
import model

COOKIE_ID_IGRE = "ID_IGRE"
SECRET = "fsghjksaouvy985094n3bqbnm<"
@bottle.get("/")
def index():
    return bottle.template("index.tpl")


@bottle.post("/igra/")
def nova_igra():
    visilice = model.Vislice.preberi_iz_datoteke()

    id_igre = visilice.nova_igra()
    novi_url = f"/igra/{id_igre}/"

    visilice.zapisi_v_datoteko()

    bottle.response.set_cookie(COOKIE_ID_IGRE, id_igre, 
                path="/", secret="SECRET")

    bottle.redirect("/igraj/")

@bottle.get("/igraj/")
def igraj_igro():
    id_igre = int(bottle.request.get_cookie(
        COOKIE_ID_IGRE, secret="SECRET",
    )
        )
    visilice = model.Vislice.preberi_iz_datoteke()
    
    trenutna_igra, trenutno_stanje = \
        visilice.igre[id_igre]
    visilice.zapisi_v_datoteko()

    return bottle.template("igra.tpl",
        igra=trenutna_igra, stanje=trenutno_stanje
    )

@bottle.post("/igraj/")
def ugibaj_na_igri_igraj():
    id_igre = int(bottle.request.get_cookie(
        COOKIE_ID_IGRE, secret="SECRET",
    )
        )
    visilice = model.Vislice.preberi_iz_datoteke()
    ugibana = bottle.request.forms["crka"]
    
    visilice.ugibaj(id_igre, ugibana)
    visilice.zapisi_v_datoteko()
    
    return bottle.redirect(f"/igraj/")


@bottle.get("/igra/<id_igre:int>/")
def pokazi_igro(id_igre):

    visilice = model.Vislice.preberi_iz_datoteke()
    
    trenutna_igra, trenutno_stanje = \
        visilice.igre[id_igre]
    visilice.zapisi_v_datoteko()

    return bottle.template("igra.tpl",
        igra=trenutna_igra, stanje=trenutno_stanje
    )

@bottle.post("/igra/<id_igre:int>/")
def ugibaj_na_igri(id_igre):
    visilice = model.Vislice.preberi_iz_datoteke()
    ugibana = bottle.request.forms["crka"]
    
    visilice.ugibaj(id_igre, ugibana)
    visilice.zapisi_v_datoteko()
    
    return bottle.redirect(f"/igra/{id_igre}/")


@bottle.get("/img/<file_path:path>")
def img_static(file_path):
    return bottle.static_file(file_path, "img")
    #return bottle.static_file(file_path, "/img")


bottle.run(reloader=True, debug=True)