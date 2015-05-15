import politoschedule
import requests

if __name__ == "__main__":

    courses = politoschedule.find_courses_by_text('Corno')

    for corso in courses:
        print "%s (%s) - prof. %s - codice %s" % (corso['materia'], corso['alfabetica'], corso['docente'], corso['chiave'])

        print "Orario:"

        urlOrario = "http://www.swas.polito.it/dotnet/orari_lezione_pub/mobile/ws_orari_mobile.asmx/get_orario"
        parametriOrario = { 'listachiavimaterie': corso['chiave'], 'datarif': '2015-05-06'}

        r = requests.post(urlOrario,json=parametriOrario)

        orario = r.json()
        for item in orario['d']:
            print "\t%s -> %s: %s" % (item['start'], item['end'], item['text'] )
        r.close()

    urlAule = "http://www.swas.polito.it/dotnet/orari_lezione_pub/mobile/ws_orari_mobile.asmx/get_elenco_aule"
    parametriAule = {}

    r = requests.post(urlAule,json=parametriAule)

    aule = r.json()
    print "Ci sono %d aule" % len(aule['d'])
    for aula in aule['d']:
        print "Aula %s (sede %s %s), tipo %s, posti %d, (%.3f,%.3f)" % (aula['aula'], aula['sede'], aula['sito'],
                                                                        aula['tipo'], int(aula['posti']),
                                                                        float(aula['lat'].replace(',', '.')),
                                                                        float(aula['lon'].replace(',', '.')))


    print
    print "** ORARIO AULA 3I"

    urlOrarioAula = "http://www.swas.polito.it/dotnet/orari_lezione_pub/mobile/ws_orari_mobile.asmx/get_orario_aula"
    parametriOrarioAula = {'aula': '3I', 'datarif': '2015-05-14'}

    r = requests.post(urlOrarioAula,json=parametriOrarioAula)

    orarioAula = r.json()

    #print orarioAula

    for item in orarioAula['d']:
        print "\t%s -> %s: %s" % (item['start'], item['end'], item['text'] )



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


'''
METHOD
get_elenco_aule
parametro input: nessuno
output: elenco aule con sede e coordinate GPS

    public class objListaAule
    {
        public string aula { get; set; }
        public string sede { get; set; }
        public string sito { get; set; }
        public string posti { get; set; }
        public string tipo { get; set; }
        public string lat { get; set; }
        public string lon { get; set; }
    }
'''

'''
METHOD
get_orario_aula
parametri input: AULA, DATARIF
output: orario dell'aula per la giornata

    public class objListaEventi
    {
        public string id { get; set; }
        public string text { get; set; }
        public string start { get; set; }
        public string end { get; set; }
        public string tipo_evento { get; set; }
        public string titolo_materia { get; set; }
        public string nominativo_docente { get; set; }
        public string desc_evento { get; set; }
        public string aula { get; set; }
    }


'''