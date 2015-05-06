import requests
# uses HTTP request library from http://www.python-requests.org/en/latest/

if __name__ == "__main__":

    urlMaterie = "http://www.swas.polito.it/dotnet/orari_lezione_pub/mobile/ws_orari_mobile.asmx/get_elenco_materie"
    parametriMaterie = { 'txt': 'Corno' }

    r = requests.post(urlMaterie,json=parametriMaterie)

    corsi = r.json()

    r.close()

    for corso in corsi['d']:
        print "%s (%s) - prof. %s - codice %s" % (corso['materia'], corso['alfabetica'], corso['docente'], corso['chiave'])

        print "Orario:"

        urlOrario = "http://www.swas.polito.it/dotnet/orari_lezione_pub/mobile/ws_orari_mobile.asmx/get_orario"
        parametriOrario = { 'listachiavimaterie': corso['chiave'], 'datarif': '2015-05-06'}

        r = requests.post(urlOrario,json=parametriOrario)

        orario = r.json()
        for item in orario['d']:
            print "\t%s -> %s: %s" % (item['start'], item['end'], item['text'] )
        r.close()


'''
Metodo: http://www.swas.polito.it/dotnet/orari_lezione_pub/mobile/ws_orari_mobile.asmx/get_elenco_materie
parametro: txt (qui puoi inserire o parte del nome del docente "Mezza" o parte del nome della materia "Analisi")
risultato: una lista di materie descritte da: chiave, materia, docente, alfabetica, pd

Esempio per le richieste Json :
$.ajax({
                    url: "ws_orari_mobile.asmx/get_elenco_materie",
                    type: "POST",
                    dataType: "json",
                    contentType: "application/json; charset=utf-8",
                    crossDomain: false,
                    data: "{ 'txt': '" + $input.val() + "'}"

                })


Metodo: http://www.swas.polito.it/dotnet/orari_lezione_pub/mobile/ws_orari_mobile.asmx/ get_orario
Parametro 1: listachiavimaterie (inserire l'elenco delle "chiavi" del primo metodo separati da virgola es:)
Parametro 2: datarif (data di riferimento per cui si vuole l'orario es.: 2015-05-05)
Risultato: un elenco di eventi fatto da: id, text , start, end (questi eventi sono compresi tra la settimana prima della data di riferimento e 2 settimane dopo)

Esempio per le richieste Json :
$.ajax({
                url: "ws_orari_mobile.asmx/get_orario",
                type: "POST",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                crossDomain: false,
                data: "{ 'listachiavimaterie': '" + param + "', 'datarif': '" + datarif_getorario.toDateString() + "'}"

            })
'''