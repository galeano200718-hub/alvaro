import requests
import re
import os

# URLs de origen de confianza (IPTV-ORG)
URL_PARAGUAY = "https://iptv-org.github.io/iptv/countries/py.m3u"
URL_ESPANOL = "https://iptv-org.github.io/iptv/languages/spa.m3u"

# ===========================================================================
# CONFIGURACIÓN: Todos tus tvg-id autorizados para actualizarse cada 6 horas
# ===========================================================================
CANALES_A_ACTUALIZAR = {
    "alcancefmplaytv.py@sd", "almayatv.py@sd", "brunomasitv.py@sd", "c9n.py@sd",
    "canal5tvmax.py@sd", "canal8ccproducciones.py@sd", "canal8visiontv.py@sd", "canalpro.py@sd",
    "cosmostv.py@sd", "delreytv.py@sd", "dismarradiotv.py@sd", "e40.py@sd",
    "enlenguadesenastv.py@sd", "gotv.py@sd", "heinow.py@sd", "latele.py@sd",
    "megatv.py@sd", "mitv.py@sd", "monumentaltv.py@sd", "nandeportetepetv.py@sd",
    "nandejaraneetv.py@sd", "nanduti.py@sd", "nexthd.py@sd", "npy.py@sd",
    "oasistv.py@sd", "obediratv.py@sd", "occidentaltv.py@sd", "oviedotv.py@sd",
    "paraguaytv.py@sd", "productivatv.py@sd", "radiociudad989fmtv.py@sd", "radionacionaldelparaguay.py@sd",
    "radiosancristobal887fm.py@sd", "radiotvelarcadelpacto.py@sd", "rcctv.py@sd", "reddigital.py@sd",
    "redinteriortv.py@sd", "regionaltvyaguaron.py@sd", "rqpparaguay.py@sd", "snt.py@sd",
    "sucesotv.py@sd", "telequince.py@sd", "tvaire.py@sd", "tvcanindeyu.py@sd",
    "uniontv.py@sd", "uniradiotv.py@sd", "venusmedia.py@sd", "villaelisaradiotv.py@sd",
    "3abnlatino.us@sd", "6wisetv.us@sd", "canal7televalencia.es@sd", "8lamarinatv.es@sd",
    "8ntv.mx@sd", "9lalomatv.es@sd", "12tv.es@sd", "13c.cl@sd",
    "13e.cl@sd", "13festival.cl@sd", "13humor.cl@sd", "13kids.cl@sd",
    "13p.cl@sd", "13realities.cl@sd", "13t.cl@sd", "247canaldenoticias.ar@sd",
    "101tvaxarquia.es@sd", "101tvmalaga.es@sd", "101tvsevilla.es@sd", "360rftv.cr@sd",
    "opa.cr@sd", "a24.ar@sd", "abtvbariloche.ar@sd", "abyayalatv.bo@sd",
    "amp1.us@sd", "amp2.us@sd", "thecityofmarina.us@sd", "themontereychannel.us@sd",
    "thepeninsulachannel.us@sd", "acentotv.do@sd", "acsnetwork.pr@sd", "activatv.es@sd",
    "actualidad360.es@sd", "adn40.mx@sd", "adoramtv.do@sd", "adrenalinapuratv.us@sd",
    "aeradiotv.cl@sd", "agapetv.sv@sd", "agendamineratv.bo@sd", "aguilatv.do@hd",
    "ahoratv.do@sd", "aiontv.do@sd", "airedesantafe.ar@sd", "alacantitv.es@sd",
    "alcancetv.mx@sd", "alcarrizostv.do@sd", "alegretvrd.do@sd", "algomediatv.do@hd",
    "alientovision.us@sd", "alsaciastelevision.hn@sd", "altantotv.do@sd", "ame47.do@sd",
    "americaestereoguayaquil.ec@sd", "americaestereoibarra.ec@sd", "americaestereoquito.ec@sd", "americateve.pr@sd",
    "americatv.ar@sd", "amigostvchiquimula.gt@sd", "amxnoticias.mx@sd", "anaylos7.us@spain",
    "andromeda.us@spain", "angeltv.in@spanish", "antena7.do@sd", "antena21.do@sd",
    "antenaseistv.cr@sd", "antenasur.pe@sd", "antofagastatv.cl@sd", "arabitv.es@sd",
    "aragontvinternacional.es@sd", "arboldevidatv.sv@sd", "archivosforenses.us@spain", "argentinisimasatelital.ar@sd",
    "as3sporttv.ve@sd", "asiritv.pe@sd", "asomavision.ec@sd", "atabaltv.do@hd",
    "atacamanoticias.cl@sd", "atacamatv.cl@sd", "atccocanal2.ar@sd", "atntelevision.co@sd",
    "atvsur.pe@sd", "audaztv.ve@sd", "auroramediafilms.gt@sd", "australtv.ec@sd",
    "autenticatelevision.pe@sd", "avivamientotv.co@sd", "awapasportstv.sv@sd", "azaharesradiovisualmultimedia.ar@sd",
    "aztecahonduras.hn@sd", "aztecainternacional.mx@sd", "b15fresnillo.mx@sd", "b15zacatecas.mx@sd",
    "babyfirst.us@us", "babytv.uk@spain", "bacanteveo.ec@sd", "bajotechotv.do@sd",
    "bamostv.mx@sd", "banivision.do@hd", "bbcdrama.uk@spain", "bcngospeltv.es@hd",
    "beatsradio.ar@sd", "beinsportsxtraenespanol.us@sd", "bellavision.do@sd", "bendicionchannel.co@hd",
    "bestclasicostv.cr@sd", "betheltv.pe@sd", "bhtv.pe@sd", "bobesponja.us@spain",
    "bocachicatv.do@sd", "boliviatv72.bo@sd", "bolivision.bo@sd", "bonaotv.do@sd",
    "boncheslatinostv.do@sd", "boreal.do@sd", "bragadotv.ar@sd", "bravotv.ar@sd",
    "btatv.ve@sd", "buenatv.pr@sd", "bumtelevision.co@sd", "cableimagenarmstrong.ar@sd",
    "cadenaelite.es@sd", "cadenatv.pe@hd", "ctv.us@sd", "calitv.co@sd",
    "campustv.hn@sd", "campustv.cl@sd", "camutv.do@sd", "canatvdigital.do@sd",
    "canal1marmenortorrepacheco.es@sd", "canal1nuble.cl@sd", "canal2.cr@sd", "canal2alpavisionneiva.co@sd",
    "canal2deushuaia.ar@sd", "canal2gualeguay.ar@sd", "canal2mardelplata.ar@sd", "canal2misiones.ar@sd",
    "canal3formosa.ar@sd", "canal3impresionante.sv@sd", "canal3kmktv.cr@sd", "canal3lapampa.ar@sd",
    "canal3lasheras.ar@sd", "canal4.cr@sd", "canal4jujuy.ar@sd", "canal4manchacentro.es@sd",
    "canal4posadas.ar@sd", "canal4rd.do@sd", "canal4sanjuan.ar@sd", "canal4teleaire.ar@sd",
    "canal5delpueblo.ar@sd", "canal5santafe.ar@sd", "canal5tvchepes.ar@sd", "canal5tvcozumel.mx@sd",
    "canal6.cr@sd", "canal6panadish.gt@sd", "canal6posadas.ar@sd", "canal7jujuy.ar@sd",
    "canal7salta.ar@sd", "canal7tv.ar@sd", "canal8catacaos.pe@sd", "canal8tvplus.co@sd",
    "barbetv.gt@sd", "canal9biobiotelevision.cl@sd", "canal9litoral.ar@sd", "canal10.cr@sd",
    "xhttgtdt.mx@sd", "canal10cordoba.ar@sd", "canal10durango.mx@sd", "canal10mardelplata.ar@sd",
    "canal11.cr@sd", "canal11.hn@sd", "canal11delacosta.ar@sd", "canal11tutv.sv@sd",
    "canal12web.ar@sd", "canal13esquipulas.gt@sd", "canal13jujuy.ar@sd", "canal13sanluis.ar@sd",
    "canal14codazzi.co@sd", "canal15elzamorano.sv@sd", "ilcecanal15summasaberes.mx@sd", "canal15.ni@sd",
    "canal17rtvd.do@hd", "canal21huancayo.pe@hd", "canal21tachira.ve@sd", "canal21tv.ar@sd",
    "canal22.ar@sd", "24horas.es@sd", "24horascatalunya.es@sd", "canal26.ar@sd",
    "canal26.mx@sd", "canal26tviap.sv@sd", "canal30tvbethel.gt@sd", "canal33madrid.es@sd",
    "canal33tijuana.mx@sd", "canal34sanjuan.ar@sd", "canal44.mx@sd", "xhijtdt.mx@sd",
    "canal45.es@sd", "canal50morteros.ar@sd", "canal56.do@sd", "canal56.es@sd",
    "canal65.sv@sd", "canal79lacosta.ar@sd", "canal79mardelplata.ar@sd", "canal79puan.ar@sd",
    "canal79santaclaradelmar.ar@sd", "canal99miramar.ar@sd", "canalcdelzulia.ve@hd", "canalcalimatv.co@sd",
    "canalcatorce.do@sd", "canalchd.co@sd", "canalclaro.cl@sd", "canalclave.cu@sd",
    "canalcointv.es@sd", "canaldelsol.do@sd", "canaldiocesano.es@sd", "canaldonana.es@sd",
    "canaldtv.do@sd", "canale.ar@sd", "canaleducativo.cu@sd", "canaleducativo2.cu@sd",
    "canalextremadurasatelite.es@sd", "canalhabana.cu@sd", "canalinstitucional.co@sd", "canalisb.cl@sd",
    "canalmalagartv.es@sd", "canalmastelevision.co@sd", "canalmultivision.do@sd", "canalmundovision.co@sd",
    "canalnets.co@sd", "canalonce.ve@sd", "canaloracionconson.co@sd", "canalorbe21.ar@sd",
    "canalparlamento.es@sd", "canalparlamentodelcongresodejalisco.mx@sd", "canalprovincial.ar@sd", "canalpulpotv.ar@sd",
    "canalpyc.co@sd", "canalsanroque.es@sd", "canalsantamaria.ar@sd", "canalsierradecadiz.es@sd",
    "canalsur2.es@sd", "canalsurnoticias.es@sd", "canaltdc.ar@sd", "canaltelefamilia.co@sd",
    "canaltro.co@sd", "canaltroplus.co@sd", "canaltv3.co@sd", "canaluniversidad.ar@sd",
    "canalda26hd.do@hd", "canangatv.do@sd", "candelitatv.pr@sd", "canelatv.us@sd",
    "canicatv.co@sd", "caobatvradio.do@hd", "caprichotv.ec@sd", "carastv.ar@sd",
    "catv.pr@sd", "carivision.do@sd", "cartagomediostv.cr@sd", "cascaratv.do@sd",
    "catamarcatv.ar@sd", "catatumbotv.ve@sd", "cazadordehomicidas.us@spain", "cbnespanol.us@sd",
    "cdminternacional.pr@sd", "cdnn23.ni@sd", "ceacomtv.bo@sd", "celtatv.ar@sd",
    "cenovisionhd.do@hd", "cerritostv3.us@sd", "cgtnspanish.cn@sd", "chacotv.ar@sd",
    "chacratv.ar@sd", "chamametv.ar@sd", "chilechannel.cl@sd", "chilecitotv.ar@sd",
    "chiloered25.cl@sd", "chinolatv.do@sd", "cholutecatv.hn@sd", "chtv.hn@sd",
    "cielotv.do@sd", "cineadrenalina.us@sd", "cineamor.us@sd", "cinepremiere.us@sd",
    "cinesony.us@sd", "cineterror.us@sd", "cinevisioncanal19.do@sd", "ciracutv.ec@sd",
    "citricotv.do@sd", "ktop.us@sd", "ciudadesdelociotv.es@sd", "claninternacional.es@sd",
    "clan.es@sd", "clarotelevisiondominicana.do@sd", "clarovisiontv.do@sd", "clictv.ec@sd",
    "clicktvchile.cl@sd", "cmbtelevision.co@sd", "cmmtv.es@hd", "cncubgavision.co@sd",
    "cnclaunion.co@sd", "cncpereira.co@sd", "cnctulua.co@sd", "cntmastv.do@hd",
    "cocotv.do@sd", "codigotv.do@hd", "colimdotv.do@sd", "colometv.do@hd",
    "comedycentralenespanol.us@sd", "concertchannel.us@sd", "conecta2tv.pe@sd", "conectatv.mx@sd",
    "congresodelosdiputados1.es@sd", "congresodelosdiputados2.es@sd", "congresodelosdiputados3.es@sd", "congresodelosdiputados4.es@sd",
    "congresodelosdiputados5.es@sd", "constanzatv.do@sd", "contivision.cl@sd", "controversiatv.pe@sd",
    "coraltv.bo@sd", "correaradiovision.ar@sd", "corrientestv.ar@sd", "costanoroestetv.es@sd",
    "costaricachannel.cr@sd", "cotobrustv.cr@sd", "cotubanamatv.do@sd", "crtelevision.pe@sd",
    "creatv.mx@sd", "creatvchannel30.us@sd", "crimenhistoria.es@sd", "cristovisioncanal31.cr@sd",
    "cristovision.co@sd", "cromtv.do@sd", "cruztv.us@sd", "csienespanol.us@sd",
    "welu81.pr@hd", "ctv.bo@sd", "cubavision.cu@sd", "cubavisioninternacional.cu@sd",
    "cumbiamix.ar@hd", "cupertinocitychannel.us@sd", "curiquinguetv.ec@sd", "currojimenez.us@spain",
    "dancefm.cl@sd", "deultimominutotv.do@sd", "decimatv.cl@sd", "delpueblotv.do@hd",
    "deltatvcanal50.do@sd", "despiertatv.mx@sd", "detectiveconan.us@spain", "dieztvlasvillas.es@sd",
    "dieztvubeda.es@sd", "digital809tv.do@sd", "digitalvision63.do@sd", "diosteve.hn@sd",
    "diostevekids.hn@sd", "diostvtalanga.hn@sd", "disneyjunior.es@sd", "distritotv.es@sd",
    "dnjtv.pr@sd", "plutotvdogelcazarrecompensas.us@sd", "dsportsuruguay.uy@sd", "duendetv.ec@sd",
    "dw.de@espanol", "ebenezertv.hn@sd", "ebntelevision.pr@sd", "ecotelevision.pe@sd",
    "ecotv.ar@sd", "ecoscanal57.do@hd", "ecoteltv.ec@sd", "ecovision.do@sd",
    "ecuadortv.ec@sd", "ecuavisa.ec@guayaquil", "ecuavisa.ec@quito", "edntv.hn@sd",
    "educatv.ec@sd", "eduvision.co@sd", "elcaminotv.sv@sd", "elchavotv.mx@hd",
    "elcomisario.us@spain", "elencantadordeperros.us@spain", "elmueble.es@sd", "elmundodelcampo.co@sd",
    "elnuevodiariotv.do@sd", "elpitucotv.do@hd", "elpuertotv.do@sd", "plutotvelreinoinfantil.us@sd",
    "eyseis6.do@sd", "elsolnetworktv.ec@sd", "eltorotv.es@sd", "eltrece.ar@sd",
    "elroitv.gt@sd", "elche7tv.es@sd", "eliaspinatv.do@sd", "empenosalobestia.us@spain",
    "enelpuntodemira.us@spain", "energeek.cl@sd", "energeekfan.cl@sd", "energeekradio.cl@sd",
    "entchannel.uk@hd", "entfamily.uk@hd", "enteraterd.do@hd", "entunotv.do@hd",
    "escuchameradiotv.ni@sd", "esteponatelevision.es@sd", "estrellagames.us@sd", "estrellanews.us@sd",
    "estrellatv.us@sd", "plutotvestrellasdeaccion.us@sd", "estutele.es@sd", "etb2.es@sd",
    "etbevents1.es@sd", "euronewsspanish.fr@sd", "ewtnespana.es@sd", "ewtn.us@spainlatinamerica",
    "exitosatv.pe@sd", "exctv.ve@sd", "expresatv.mx@sd", "extra86tv.do@hd",
    "extremakidstv.cr@hd", "extrematv.cr@sd", "f10hd.bo@sd", "fabulosaestereo1005fm.pa@sd",
    "faptv.bo@sd", "farodesantidadtv.pr@sd", "farovision.do@sd", "filmex.mx@sd",
    "filmexclasico.mx@sd", "fmmundo.ec@sd", "forensicfiles.us@sd", "fortunatv.ve@sd",
    "foxdeportes.us@sd", "foxsports.ar@sd", "france24.fr@spanish", "fratatv.do@sd",
    "frecuenciaftv.co@sd", "fmtv.uk@sd", "ftv.bo@sd", "fuegotv.do@sd",
    "fuerteventuratv.es@sd", "galaxiateve.do@sd", "gamavision.ec@sd", "gamtvcr.cr@sd",
    "garabitotv.cr@sd", "garagetvlatinamerica.ar@sd", "ghtelevision.do@sd", "gitelevision.do@sd",
    "giktvmx.mx@sd", "girasoltv.hn@sd", "girovisual.cl@sd", "globaltv.do@sd",
    "goienaeus.es@sd", "golclassics.es@sd", "golden.mx@panregional", "grandetv.ve@sd",
    "guadatv.es@sd", "guarotv.ve@sd", "guayapetv.hn@sd", "hainavision.do@sd",
    "hamaikatelebista.es@sd", "hch.hn@sd", "hechosecuador.ec@sd", "hermanasmirabaltv.do@sd",
    "hilandofinotv.do@sd", "hispantv.ir@sd", "hispaniatv.pa@sd", "historia.es@sd",
    "historiayvida.es@sd", "plutotvhistoriasdeultratumba.us@sd", "holvoettv.cl@sd", "hopechannelinteramerica.us@sd",
    "hosannavision.pa@sd", "htvlive.do@sd", "icarly.us@east", "icndigital.hn@sd",
    "icrtvcolima.mx@sd", "ieanjesusecuador.ec@sd", "iertbcscanal82.mx@sd", "xhbzctdt.mx@sd",
    "imagentv.mx@sd", "imagenuniversaltv.do@sd", "imastv.es@sd", "impactotelevision.pe@sd",
    "imryt.mx@sd", "infinitatv.ec@sd", "informetv.do@hd", "interalmeriatv.es@sd",
    "intercomarcaltv.es@sd", "intertv.ve@sd", "intuitivatv.pe@sd", "iqchannel.cr@sd",
    "islatv.ve@sd", "italianissimo.ve@sd", "iteltvcanal2.ar@sd", "itvdeportes.mx@sd",
    "jaliscotv.mx@sd", "jarabacoatv.do@hd", "jbn.ni@sd", "jehovatv.hn@sd",
    "jfvtv.sv@sd", "jimanitv.do@sd", "jn19.pe@sd", "josuetv.sv@sd",
    "jpdtv.do@hd", "juniortechnologiatv.do@hd", "justiciatv.mx@sd", "juventudrenovadaenelespiritusanto.us@sd",
    "kalutv.co@sd", "kandelatv.ve@sd", "kasterweymedia.ec@hd", "kbev.us@sd",
    "plutotvkenanykel.us@sd", "kerussotv.hn@sd", "kpopmix.ar@sd", "krgvtv52.us@hd",
    "ksce382.us@hd", "la1.es@sd", "la1canarias.es@sd", "la1catalunya.es@sd",
    "la2canarias.es@sd", "la2catalunya.es@sd", "lacaletatv.do@sd", "lacityview35.us@sd",
    "ladescargatv.do@hd", "lahermandadsalsera.co@sd", "lahoratv.do@hd", "lakalle.co@sd",
    "lamoradaradiotv.co@sd", "laperlaradiotv.ec@sd", "lapopulartv.cl@sd", "lapotenteradiotv.cr@sd",
    "laquebuenaatlanta.us@sd", "lared.cl@sd", "lareinatv.do@hd", "larutatv.do@hd",
    "latop1029.hn@sd", "latop1077.hn@sd", "lavozdejesushd.do@hd", "lavozdemaria.do@sd",
    "lax.pr@sd", "lagunatv.do@hd", "lamil35tv.ar@sd", "lancelottv.es@sd",
    "laotra.es@sd", "larivisiontv.do@hd", "lasestrellas.mx@sd", "lastortugasninja.us@spain",
    "latacungatv.ec@sd", "latinzone.us@sd", "latina.pe@sd", "latinaclasicos.pe@sd",
    "latinatv.ve@sd", "latinatvinternacional.do@sd", "latv.us@sd", "legislativeassemblyofelsalvador.sv@sd",
    "lenatv.do@sd", "lencatv.hn@sd", "lgdtelevision.ve@sd", "ksce381.us@hd",
    "ksce383.us@hd", "llbntvlatino.us@sd", "linierostv.do@sd", "linktv.ar@sd",
    "litoralatlandicohd.hn@sd", "litustv.ar@sd", "livingfaithtv.us@sd", "lobotv.mx@sd",
    "logostv.es@sd", "logostvkids.es@sd", "logostvsalud.es@sd", "loretotv.ec@sd",
    "losarchivosdelfbi.us@spain", "losasesinatosdemidsomer.us@spain", "plutotvlosnuevosdetectives.us@sd", "lossantostv.cr@sd",
    "lovenature.ca@sd", "lovetheplanet.es@es", "ltv.hn@sd", "luchalibreaaa.us@sd",
    "lunatvcanal53.do@sd", "luzdivinatv.do@hd", "m95televisionmarbella.es@sd", "maimontvcanal3.do@sd",
    "majestadtelevision.ec@sd", "majestadtv.us@sd", "makaotv.do@sd", "makinatv.do@sd",
    "makrodigitaltelevision.ec@sd", "manaiglesiaonline.pt@sd", "manaclartelevision.do@sd", "manavision.ec@sd",
    "mariavision.mx@sd", "mariaplusvisionmedjugorje.ba@sd", "markatv.do@hd", "mas23tv.pa@sd",
    "masfm.ar@sd", "masnortetv.co@sd", "mastalk.ve@sd", "masmusicafm.co@sd",
    "maxivisiontv.gt@sd", "mayatv.hn@sd", "mcitelevision.co@sd", "megacinetv.do@hd",
    "megatvarequipa.pe@sd", "megatvjaen.pe@sd", "megabox.ni@sd", "megavisioncanal19.sv@sd",
    "megavisioncanal21.sv@sd", "melradiotv.ec@sd", "plutotvmelroseplace.us@spain", "mercurionoticias.ar@sd",
    "metaleitortv.us@sd", "metrotv.ar@sd", "metrotv.hn@sd", "metropolimediostv.ec@sd",
    "mexiquensetv.mx@sd", "miextranaobsesion.us@spain", "migentetv.co@sd", "miturnotv.do@sd",
    "miavisiontv.do@hd", "microvision10.do@sd", "mieltv.pe@sd", "mijas340tv.es@sd",
    "milenialtv.pe@sd", "mileniotelevision.mx@sd", "minfavtv.pa@sd", "ministeriolavozdeunremanentetv.us@sd",
    "plutotvminutoparaganar.us@sd", "misioneltv.do@sd", "misionescuatro.ar@sd", "plutotvmisteriosmedicos.us@sd",
    "misteriossinresolver.us@spain", "monagasvision.ve@sd", "montemaria.mx@sd", "montecristidigital8.do@hd",
    "monterricotv.pe@sd", "morrotv.do@sd", "mrbeananimated.uk@es", "mtnatv.cl@sd",
    "mtvembarazadaalos16.us@spain", "mtvenespanol.us@sd", "mtvoriginals.us@spain", "mtvplutotv.us@latam",
    "mtvtattooados.us@spain", "multivision.cu@sd", "multivisioncanal3.gt@sd", "multivisionfederal.ar@sd",
    "multivisionsports.gt@sd", "musavision.do@sd", "musictvgranada.es@sd", "musictop.ar@sd",
    "mytimemovienetwork.mx@sd", "mytimemovienetwork.es@sd", "myzentv.fr@sd", "narutoenespanol.us@sd",
    "narutoshippuden.us@latam", "nativa.pe@sd", "nativatvsatipo.pe@sd", "naturetime.ca@es",
    "naturetime.ca@latam", "naturetime.ca@sd", "navarretetelevision.do@hd", "nayaritcomunica.mx@sd",
    "nctv.cl@sd", "negociostv.es@sd", "neotv.ar@sd", "nettv.ar@sd",
    "nextvcanal21.pa@sd", "nexxotv.do@sd", "ngradiotv.pr@sd", "nickelodeon.es@sd",
    "nickenespanol.us@sd", "nicoyatv.cr@sd", "nimtv.gt@sd", "nitidatv.do@sd",
    "norteinformativotv.cr@sd", "nortenatv.ve@hd", "noticias16.do@sd", "noticiero90minutos.co@sd",
    "xhfgltdt.mx@sd", "notisurtv.do@hd", "nstv.co@sd", "nublevision.cl@sd",
    "nuevavidafm.pr@sd", "nuevetv.mx@sd", "nuevotiempo.br@sd", "nukatv.ec@sd",
    "oepmtv.do@sd", "olammetrotv.ni@sd", "onda15tv.es@sd", "ondaalgeciras.es@sd",
    "ondacadiz.es@sd", "ondadigital.pe@sd", "ondamadrid.es@sd", "ondatv.do@sd",
    "ondavalenciatv.es@sd", "ondambientaltv.co@sd", "ondasquevedenastv.ec@sd", "onepiece.us@latam",
    "onepiece.us@spain", "orbittv.do@sd", "orbitchiletv.cl@hd", "oromartv.ec@sd",
    "oxigenotv.ve@sd", "oxitv.do@hd", "pctchannel27.us@sd", "pctchannel26.us@sd",
    "palenquetv.bo@sd", "palmartv.do@sd", "panctv.ar@sd", "panctvperu.pe@sd",
    "paraisotv.pr@sd", "parrandavallenata.co@sd", "patlapaz.bo@sd", "penielky.gt@sd",
    "penielmusical.gt@sd", "penieltvbibliaabierta.gt@sd", "pequeradio.es@sd", "peraviavision.do@sd",
    "phxtv.us@sd", "pichilemutv.cl@sd", "pindintv.pa@sd", "planet1009fm.pa@sd",
    "planetachannel.ec@sd", "platzitv.es@sd", "ploustv.ve@sd", "plustv.ec@sd",
    "plutotvanimales.us@spain", "plutotvanime.us@latam", "plutotvanime.us@spain", "plutotvaventura.us@sd",
    "plutotvcineaccion.us@us", "plutotvcineclasico.us@us", "plutotvcinecomedia.us@spain", "plutotvcinedrama.us@us",
    "plutotvcineestelar.us@us", "plutotvcineromantico.us@spain", "plutotvcinesuspenso.us@sd", "plutotvcocina.us@spain",
    "comediamadeinspain.us@sd", "comedymovies.es@sd", "plutotvcompetencias.us@sd", "plutotvdeportes.us@sd",
    "plutotvdocumentales.us@spain", "plutotvhistoria.us@sd", "plutotvhorror.us@spain", "plutotvhumor.us@sd",
    "investiga.us@sd", "plutotvjunior.us@spain", "plutotvkids.us@spain", "plutotvmotor.us@spain",
    "plutotvmtvclassic.us@sd", "plutotvnaturaleza.us@sd", "plutotvnovelas.us@sd", "plutotvpeleas.us@sd",
    "plutotvscifi.us@us", "plutotvseriescomedia.us@spain", "plutotvserieslatinas.us@sd", "plutotvseriesretro.us@sd",
    "plutotvteen.us@sd", "plutotvtelenovelas.us@spain", "plutotvvelocidad.us@sd", "populartvmurcia.es@sd",
    "portaldigitaltv.do@hd", "portuguesatelevision.ve@sd", "powermaxradiotv.ar@sd", "powerhd.ar@sd",
    "prensalatinatv.cu@sd", "presumiendomexico.mx@sd", "pridetvlatam.cl@hd", "proclamaciontv.ve@sd",
    "pronemstv.do@sd", "psn.mx@sd", "psncanal452.mx@sd", "pucontv.cl@sd",
    "pulatv.do@sd", "punt3.es@sd", "puntacanatv.do@sd", "puntotv.do@sd",
    "puntotvdigital40.do@sd", "purapalabra.pr@sd", "puranoticiatv.cl@sd", "puringlatv.hn@sd",
    "puruwatv.ec@sd", "qhubotv.hn@sd", "quanticatv.ar@sd", "rtelevision.do@hd",
    "retv.do@sd", "radio3.es@sd", "radioancon.pa@sd", "radiobonita1067.ec@sd",
    "radiocarnavaltv.es@sd", "radioconexionwebtv.ar@sd", "radiocuencaestereo.ec@sd", "radiofiestademilagrostv.hn@sd",
    "radiohogar.pa@sd", "radioideal.hn@sd", "imagenfm1051.hn@sd", "radioislatv.pr@sd",
    "radiomaster.pe@hd", "radiomonumentaltv.ec@sd", "radiorealpolitik.ar@sd", "radioritmofm.cl@sd",
    "radiosublimegraciatv.ar@sd", "radiosuyaitv.cl@hd", "radiotropical.pe@sd", "radiotvneuquen.ar@sd",
    "radioup.ar@sd", "radioytelevisionmarti.us@sd", "radioyguazutv.ar@sd", "radiomensajetv.us@sd",
    "radiotvoriente.pe@sd", "rakutenviki.us@spain", "ralytv.mx@sd", "rctv3.us@sd",
    "rasdtv.eh@sd", "rcgtv.mx@sd", "rcgtv2.mx@sd", "rcnmas.co@sd",
    "noticiasrcn.co@sd", "rcvtv.hn@sd", "rdn.do@sd", "readytvcanal6.do@sd",
    "realmadridtv.es@sd", "redsocialcoditv.do@sd", "redtvshop.bo@sd", "redtveventanas.ec@sd",
    "redplus.co@sd", "reformatv.ve@sd", "reporterotv.do@hd", "retroplus2.cl@sd",
    "retroxtv.cr@sd", "reyali.co@sd", "rhematv.gt@sd", "riberatv.es@sd",
    "rntelevision.pe@sd", "rneparatodos.es@sd", "rnn.do@sd", "rocavisiontv.do@sd",
    "romanatvcanal42.do@sd", "rpptv.pe@sd", "rselvatv.pe@sd", "rsvhonduras.hn@sd",
    "rtg.mx@sd", "rtn.ar@sd", "rtp.bo@sd", "rtqqueretaro.mx@sd",
    "rtrtv.ec@sd", "rttv.cr@sd", "rtu.ec@sd", "rtvcanal57.sv@sd",
    "rtvchirripo.cr@sd", "radiotelevisionmarbella.es@sd", "rtv.ec@sd", "rtvvida.es@sd",
    "rugrats.us@spain", "runtimeespanol.us@sd", "ruta66tv.do@sd", "salsagordatelevision.co@sd",
    "sanisidrotv.do@sd", "sanjosetv.cr@sd", "sanluisplus.ar@sd", "sanpedrotv.ar@sd",
    "santacruztv.do@hd", "santamariatelevision.cl@sd", "santiagotv.do@sd", "sastv.gt@sd",
    "sccurrents.us@sd", "senalcolombia.co@sd", "senaldigitaltv.do@hd", "xhunestdt.mx@sd",
    "senalperutv.pe@sd", "senalpositivatv.ec@sd", "senalu.ar@sd", "senillosatv.ar@sd",
    "xhpbzctdt1.mx@sd", "xhpbzctdt2.mx@sd", "sevillafctv.es@sd", "sicarditv.ar@sd",
    "siembratv.do@sd", "siltv.gt@sd", "sintetasnohayparaiso.us@spain", "siontv.ar@sd",
    "sipsetv81.mx@sd", "sipsetvcun81.mx@sd", "sistemamichoacanodetv.mx@sd", "sistesurcanal49.do@sd",
    "xhzhztdt.mx@sd", "soltv.pe@sd", "soltv.gt@sd", "solidariatv.es@sd",
    "solivetv.ar@sd", "solobailalo.cl@sd", "soltv.gq@sd", "sonoondatv.ec@sd",
    "sophiatvespanol.de@sd", "soyplanchatv.cr@sd", "spektratv.es@sd", "sqcscanal4.mx@sd",
    "stingrayclassica.ca@sd", "stveterlebasica.hn@sd", "stztelebista.es@sd", "sulatv.hn@sd",
    "sumtvlatino.us@sd", "supercanal.do@sd", "superchannel12.mx@sd", "superdigitaltv.do@sd",
    "superqpanama.pa@sd", "supertv55.do@sd", "supermusicatv.co@sd", "supremateve.do@hd",
    "surtv.cl@sd", "suramtv.co@sd", "suyaitv.cl@sd", "suyapatv.hn@sd",
    "t5satelital.ar@sd", "tvinet.cl@sd", "tabertv.sv@sd", "taroteame.es@sd",
    "tastemadeenespanol.us@sd", "tbnespana.es@sd", "tdnmedios.do@sd", "tdtv.cr@sd",
    "teleamiga.co@sd", "teledominicanatv.do@sd", "teleelx.es@sd", "telemocoacanal10.co@sd",
    "teleola44.do@sd", "telepodertv.do@hd", "teleproyectotv.do@hd", "telerebelde.cu@sd",
    "telesafor.es@sd", "telesaltillo.mx@sd", "televid.co@sd", "teleyucatan.mx@sd",
    "teleamazonas.ec@quito", "teleantioquia.co@sd", "telearuba.aw@sd", "telebendicion.do@sd",
    "telebolivar.co@sd", "telebrunca.cr@sd", "telecafe.co@sd", "telecanal12.do@sd",
    "telecanal28.do@sd", "telecaribe.co@sd", "telecaribeplus.co@sd", "teleceiba.hn@sd",
    "telecibaohd.do@sd", "telecinco.ar@sd", "telecolor.ve@sd", "telecoloryurimaguas.pe@sd",
    "telecomerciotv.do@sd", "telecontacto.do@sd", "telecosta.gt@sd", "telecreativa.ar@sd",
    "teledanli.hn@sd", "telefides.cr@sd", "teleformula.mx@sd", "teleganes.es@sd",
    "teleimpacto.do@sd", "teleislas.co@sd", "telemadrid.es@sd", "telemadridint.es@sd",
    "telemar.ec@sd", "telemas.cr@sd", "telemas.hn@sd", "telemax.ar@sd",
    "telemax.do@sd", "xewhtdt.mx@sd", "telemedellin.co@sd", "telemetrotv.do@sd",
    "telemicro.do@sd", "telemotril.es@sd", "telemundocorpuschristi.us@sd", "telenewstv.do@sd",
    "telenord8.do@sd", "telenord10.do@sd", "telenord12.do@sd", "telenorte.pr@sd",
    "telenovisa43.do@sd", "teleonce.pr@sd", "telepacifico.co@sd", "teleplaysureste.mx@sd",
    "teleradionorte.do@sd", "telerama.ec@sd", "telerayo.hn@sd", "teleredtelevision.cr@sd",
    "telesangil.co@sd", "telesantodomingo.do@sd", "teleselva.pe@sd", "telesiglo.do@hd",
    "telesur.ve@sd", "telesurcostarica.cr@sd", "telesur.ve@hd", "teletraktv.cl@sd",
    "teletur.do@sd", "teleuniverso.do@sd", "telever.do@sd", "televida.cl@sd",
    "televida.do@sd", "televigo.es@sd", "televisionaranda.es@sd", "televisioncanaria.es@sd",
    "televisionconsciente.es@sd", "televisiondeleste.do@sd", "televisionmetropolis191.hn@sd", "televisionolanchana.hn@sd",
    "televisiontarapoto.pe@sd", "televisoradeoriente.ve@sd", "tencanal10.hn@sd", "tenarensestv.do@sd",
    "tevevidanetwork.us@sd", "tevecolombia.co@sd", "tevex.cl@sd", "thepetcollective.us@spain",
    "thewalkingdeadenespanol.us@sd", "thematelevision.cl@sd", "ticavision.cr@sd", "tigosports.sv@sd",
    "tigueritotv.do@hd", "titotv.es@hd", "tivtelevision.ar@sd", "tlaxcalatv.mx@sd",
    "tn8.ni@sd", "tne.cl@sd", "tnoradio.ve@sd", "topicalmoonrd.do@hd",
    "torococotv.ve@sd", "totalmusic.uk@hd", "totalmusic80s.uk@hd", "totalmusic2000s.uk@hd",
    "totalmusicconcerts.uk@hd", "totalmusicdance.uk@hd", "tourspottv.do@hd", "tra2.do@sd",
    "trctv.mx@sd", "trece.co@sd", "triunfo969fm.pr@sd", "trivision36.cr@sd",
    "trivu.pe@sd", "tropiq997fm.pa@sd", "trt.ve@sd", "trv.ve@sd",
    "tuuniversotv.co@sd", "tudn.mx@sd", "turbomixradiotv.pe@sd", "turfmovil.cl@sd",
    "turismohd.do@hd", "turismordtv.do@hd", "turistiktv.mx@sd", "tv3laplata.co@sd",
    "tv10sanjuan.do@sd", "tv45.ni@sd", "tvalmassora.es@sd", "tvandes.ve@sd",
    "tva.es@sd", "tvbricsspanish.es@hd", "tvcentro272hd.hn@sd", "tvcentrohd.hn@sd",
    "tvcisne.ec@sd", "tvcolorcanal36.ec@sd", "tvcopan.hn@sd", "tvcotuicanal31.do@sd",
    "tvcret.sv@sd", "tvcuatro41.mx@sd", "tvcuatro42.mx@sd", "tvcuatro43.mx@sd",
    "tvcuatro44.mx@sd", "tvdaja.do@sd", "tvestrealla.hn@sd", "tvexitos.do@sd",
    "tvflorencia.gt@sd", "tvgetsemani.sv@sd", "tvhigueydigital.do@sd", "tvhispanic.us@sd",
    "tvleondejuda.sv@sd", "tvlobo.mx@sd", "tvluz.do@sd", "tvmanaargentina.ar@sd",
    "tvmanaespanhol.pt@sd", "tvmarlapaz.mx@sd", "tvmarloscabos.mx@sd", "tvmarpuertovallarta.mx@sd",
    "tvmontanacanal10.do@sd", "tvoasismonay.ve@sd", "tvoff.bo@sd", "tvplata.do@sd",
    "tvpublicamarcospaz.ar@sd", "canal2quellon.cl@sd", "tvquisqueya.us@sd", "tvsenado.cl@sd",
    "tvsistemascuzco.pe@sd", "tvsolidaria.ar@sd", "tvsurcanal14.cr@sd", "tvuct.cl@sd",
    "tvug.mx@sd", "tvujat.mx@sd", "tvuniversalecuador.ec@sd", "tvuniversidad.ar@sd",
    "tvca.sv@sd", "tvcariblatino.sx@sd", "tveinternacionalamerica.es@sd", "tveinternacionalamerica.es@hd",
    "tveinternacionalasiaoceania.es@sd", "tveinternacionalasiaoceania.es@hd", "tveinternacionaleurope.es@sd", "tvestar.es@sd",
    "tvestar.es@hd", "tvmparati.ve@sd", "xhgvtdt.mx@sd", "tvn3.cl@sd",
    "tvo.do@sd", "tvojesus.es@sd", "tvosanvicente.cl@sd", "tvomix.es@hd",
    "tvonenicaragua.ni@sd", "tvpculiacan.mx@sd", "tvplosmochis.mx@sd", "tvpmazatlan.mx@sd",
    "tvpobregon.mx@sd", "tvr.cl@sd", "tvs.do@sd", "tvs.ve@sd",
    "tvsretro.gt@sd", "tvu.cl@sd", "tvuno.pe@sd", "tycsports.ar@sd",
    "ucl.uy@sd", "ucvtv.cl@sd", "uestv.cl@sd", "ultracasanaretv.co@sd",
    "ultratvpuebla.mx@sd", "umctv.co@sd", "umsatvuinternacional.bo@hd", "umsatvulp.bo@sd",
    "umtv.mx@sd", "unahutv.hn@sd", "unetv.hn@sd", "unevinalopo.es@sd",
    "uniandestv.ec@sd", "unidaddeinvestigacion.us@spain", "unifetv.ar@sd", "unifranz.bo@hd",
    "unitel.pe@sd", "uniteve.ar@sd", "unitv.ve@sd", "univalletelevision.bo@sd",
    "universtv.es@sd", "uatv.cl@sd", "upeatv.bo@sd", "upptv.bo@sd",
    "uraniotv.pe@sd", "urbanmix.ar@sd", "urbanotv.cr@sd", "usmptv.pe@sd",
    "utv.cl@sd", "vclassictv.cl@sd", "valetv.ve@sd", "vallenuevotv.do@sd",
    "vallevision.do@sd", "vayasemanita.us@spain", "vbmediatv.mx@sd", "vconline.cl@sd",
    "vegateve.do@sd", "vegavisioncanal18.do@sd", "venevision.ve@sd", "venevisioninternacional.ve@sd",
    "vepacotv.ve@sd", "vtv.ar@sd", "viaaltomayo.pe@sd", "viatelevision.pe@sd",
    "viajartv.ar@sd", "vidamejortv.us@sd", "villaaltagraciatv.do@sd", "villamanterotv.ar@sd",
    "vintagemusic.cr@sd", "vision3000.do@sd", "visionndv.do@sd", "visionplustv.cl@sd",
    "visionsur.pe@sd", "visiontelevision.mx@sd", "visiontv.gt@sd", "vivatvyurimaguas.pe@sd",
    "kanalddrama.tr@sd", "vivotv.uy@sd", "vmlatino.cr@sd", "vnp.pe@sd",
    "voiceoverradiotv.cr@sd", "vosytv.ec@sd", "vtv.hn@sd", "vtvcanal32.do@sd",
    "vtvvalledeaconcagua.cl@sd", "waldivisioninternacional.hn@sd", "wdwl581.pr@hd", "weatherspy.mx@sd",
    "wiprtv61.pr@hd", "wkaqtv21.pr@hd", "wkaqtv22.pr@hd", "wowtv.sv@sd",
    "wtvcanal20.ni@sd", "wwxydt1.pr@sd", "wwxydt3.pr@sd", "wxwzld231.pr@hd",
    "xlevelmedia.ar@sd", "xamatv.ar@sd", "xtratv.do@hd", "xtremaaccion.ar@sd",
    "xtremacartoons.ar@sd", "xtremacineclasico.ar@sd", "xtrematerror.ar@sd", "youdotgov.us@sd",
    "yuma77.us@sd", "yumachannel72.us@sd", "yumachannel73.us@sd", "yunavision.do@sd",
    "zaracaytv.ec@sd", "zaz.mx@sd", "zincnombretv.do@hd", "zonavisiontv.do@sd",
    "zurquitv.cr@sd"
}


def obtener_urls_frescas_de_org():
    """Descarga las listas de iptv-org y extrae las URLs de los canales objetivos"""
    print(f"-> Buscando transmisiones para {len(CANALES_A_ACTUALIZAR)} canales configurados...")
    urls_encontradas = {}
    fuentes = [URL_PARAGUAY, URL_ESPANOL]
    
    for url in fuentes:
        try:
            respuesta = requests.get(url, timeout=20)
            respuesta.raise_for_status()
            lineas = respuesta.text.splitlines()
        except Exception as e:
            print(f"[ERROR] No se pudo conectar a {url}: {e}")
            continue
            
        i = 0
        total_lineas = len(lineas)
        while i < total_lineas:
            linea_actual = lineas[i].strip()
            
            if linea_actual.startswith("#EXTINF"):
                info_canal = linea_actual
                
                tvg_id_match = re.search(r'tvg-id="([^"]+)"', info_canal, re.IGNORECASE)
                nombre_canal = info_canal.split(",")[-1].strip().lower() if "," in info_canal else "desconocido"
                id_canal = tvg_id_match.group(1).lower() if tvg_id_match else nombre_canal
                
                if id_canal in CANALES_A_ACTUALIZAR:
                    j = i + 1
                    while j < total_lineas:
                        siguiente_linea = lineas[j].strip()
                        if siguiente_linea.startswith("#") or not siguiente_linea:
                            j += 1
                        else:
                            if id_canal not in urls_encontradas:
                                urls_encontradas[id_canal] = siguiente_linea
                            break
                    i = j
            i += 1
            
    return urls_encontradas


def inyeccion_quirurgica(file_path, urls_frescas):
    """Reemplaza SOLO las URLs de los canales autorizados en tu Alvaro01.m3u"""
    if not os.path.exists(file_path):
        print(f"[X] Error: El archivo {file_path} no existe en el repositorio.")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    modificado = False
    nuevas_lineas = []
    i = 0
    total_lineas = len(lineas)

    while i < total_lineas:
        linea = lineas[i]
        nuevas_lineas.append(linea)
        
        if "#EXTINF" in linea:
            tvg_id_match = re.search(r'tvg-id="([^"]+)"', linea, re.IGNORECASE)
            nombre_canal = linea.split(",")[-1].strip().lower() if "," in linea else "desconocido"
            id_canal_archivo = tvg_id_match.group(1).lower() if tvg_id_match else nombre_canal
            
            if id_canal_archivo in urls_frescas:
                j = i + 1
                while j < total_lineas:
                    siguiente_linea = lineas[j]
                    if siguiente_linea.strip().startswith('#') or not siguiente_linea.strip():
                        nuevas_lineas.append(siguiente_linea)
                        j += 1
                        i += 1
                    else:
                        url_nueva = urls_frescas[id_canal_archivo]
                        url_vieja = siguiente_linea.strip()
                        
                        if url_vieja != url_nueva:
                            nuevas_lineas.append(url_nueva + '\n')
                            print(f" [✓] Canal '{id_canal_archivo}': Enlace actualizado quirúrgicamente.")
                            modificado = True
                        else:
                            nuevas_lineas.append(siguiente_linea)
                        
                        i = j
                        break
        i += 1

    if modificado:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(nuevas_lineas)
        return True
    
    print(" [INFO] No se requirieron cambios en tu lista (todo al día).")
    return False


if __name__ == "__main__":
    archivo_objetivo = "Alvaro01.m3u"
    
    enlaces_frescos = obtener_urls_frescas_de_org()
    
    if enlaces_frescos:
        inyeccion_quirurgica(archivo_objetivo, enlaces_frescos)
    else:
        print("[X] No se encontraron URLs nuevas en las fuentes de iptv-org.")
