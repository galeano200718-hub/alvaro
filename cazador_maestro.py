import os
from playwright.sync_api import sync_playwright

# CAMBIO: Ahora el script lee y escribe directamente en tu lista principal
ARCHIVO_M3U = "Alvaro01.m3u"

# Diccionario completo con todos tus canales e iframes
CANALES_CONFIG = {
    # SPORTS
    "ESPN Premium": "https://embed.ksdjugfsddeports.com/embed2/espnpremium.html",
    "ESPN": "https://embed.ksdjugfsddeports.com/embed2/espn.html",
    "ESPN 2": "https://embed.ksdjugfsddeports.com/embed2/espn2.html",
    "ESPN 3": "https://embed.ksdjugfsddeports.com/embed2/espn3.html",
    "ESPN 4": "https://embed.ksdjugfsddeports.com/embed2/espn4.html",
    "ESPN 5": "https://embed.ksdjugfsddeports.com/embed2/espn5.html",
    "ESPN 6": "https://embed.ksdjugfsddeports.com/embed2/espn6.html",
    "ESPN 7": "https://embed.ksdjugfsddeports.com/embed2/espn7.html",
    "Fox Sports": "https://embed.ksdjugfsddeports.com/embed2/foxsports.html",
    "Fox Sports 2": "https://embed.ksdjugfsddeports.com/embed2/foxsports2.html",
    "Fox Sports 3": "https://embed.ksdjugfsddeports.com/embed2/foxsports3.html",
    "TUDN": "https://embed.ksdjugfsddeports.com/embed/tudn.html",
    "TyC Sports": "https://embed.ksdjugfsddeports.com/embed2/tycsports.html",
    "DirecTV Sports": "https://embed.ksdjugfsddeports.com/embed2/directvsports.html",
    "DirecTV Sports 2": "https://embed.ksdjugfsddeports.com/embed2/directvsports2.html",
    "Liga 1": "https://embed.ksdjugfsddeports.com/embed2/liga1.html",
    "DAZN LaLiga": "https://embed.ksdjugfsddeports.com/embed2/daznlaliga.html",
    "Movistar Liga de Campeones": "https://embed.ksdjugfsddeports.com/embed2/movistarligadecampeones.html",
    "Win Sports": "https://embed.ksdjugfsddeports.com/embed2/winsports.html",
    "Win Sports Plus": "https://embed.ksdjugfsddeports.com/embed2/winsportsplus.html",
    "beIN Sports XTRA": "https://embed.ksdjugfsddeports.com/embed2/beinsportsxtra.html",
    
    # ENTERTAINMENT
    "Space": "https://embed.ksdjugfsddeports.com/embed2/space.html",
    "Warner Channel": "https://embed.ksdjugfsddeports.com/embed2/warnerchannel.html",
    "TNT": "https://embed.ksdjugfsddeports.com/embed2/tnt.html",
    "Star Channel": "https://embed.ksdjugfsddeports.com/embed2/starchannel.html",
    "Cinemax": "https://embed.ksdjugfsddeports.com/embed2/cinemax.html",
    "Cinecanal": "https://embed.ksdjugfsddeports.com/embed2/cinecanal.html",
    "Distrito Comedia": "https://embed.ksdjugfsddeports.com/embed2/distritocomedia.html",
    "History": "https://embed.ksdjugfsddeports.com/embed2/history.html",
    "History 2": "https://embed.ksdjugfsddeports.com/embed2/history2.html",
    "Pasiones": "https://embed.ksdjugfsddeports.com/embed2/pasiones.html",
    "Tlnovelas": "https://embed.ksdjugfsddeports.com/embed2/tlnovelas.html",
    "Las Estrellas": "https://embed.ksdjugfsddeports.com/embed2/lasestrellas.html",
    "FX": "https://embed.ksdjugfsddeports.com/embed2/fx.html",
    "Golden Plus": "https://embed.ksdjugfsddeports.com/embed2/goldenplus.html",
    "Golden Edge": "https://embed.ksdjugfsddeports.com/embed2/goldenedge.html",
    "TNT Series": "https://embed.ksdjugfsddeports.com/embed2/tntseries.html",
    "Sony Channel": "https://embed.ksdjugfsddeports.com/embed2/sony.html",
    "AXN": "https://embed.ksdjugfsddeports.com/embed2/axn.html",
    "AMC": "https://embed.ksdjugfsddeports.com/embed2/amc.html",
    "Nat Geo": "https://embed.ksdjugfsddeports.com/embed2/natgeo.html",
    "Animal Planet": "https://embed.ksdjugfsddeports.com/embed2/animalplanet.html",
    "Discovery Channel": "https://embed.ksdjugfsddeports.com/embed2/discoverychannel.html",
    "TNT Novelas": "https://embed.ksdjugfsddeports.com/embed2/tntnovelas.html",
    "Discovery A&E": "https://embed.ksdjugfsddeports.com/embed2/discoveryaye.html",
    "Investigation Discovery": "https://embed.ksdjugfsddeports.com/embed2/idinvestigation.html",
    
    # KIDS
    "Cartoon Network": "https://embed.ksdjugfsddeports.com/embed2/cartoonnetwork.html",
    "Tooncast": "https://embed.ksdjugfsddeports.com/embed2/tooncast.html",
    "Disney Channel": "https://embed.ksdjugfsddeports.com/embed2/disneychannel.html"
}

def cazar_m3u8(url_iframe, nombre_canal):
    url_capturada = None
    print(f"[->] Extrayendo flujo silencioso para: {nombre_canal}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
        )
        page = context.new_page()
        
        def evaluar_peticion(request):
            nonlocal url_capturada
            if ".m3u8" in request.url and "temporal.com" not in request.url:
                url_capturada = request.url

        page.on("request", evaluar_peticion)
        
        try:
            page.goto(url_iframe, wait_until="load", timeout=20000)
            page.wait_for_timeout(3000)
            page.mouse.click(640, 360)
            page.wait_for_timeout(4000)
        except Exception:
            pass
        finally:
            browser.close()
            
    return url_capturada

def parchar_archivo_m3u(diccionario_enlaces):
    if not os.path.exists(ARCHIVO_M3U):
        print(f"[-] Error: No se encontró el archivo {ARCHIVO_M3U}")
        return

    with open(ARCHIVO_M3U, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    nuevas_lineas = []
    i = 0
    conteo = 0

    while i < len(lineas):
        linea = lineas[i]
        nuevas_lineas.append(linea)
        
        if linea.startswith("#EXTINF"):
            canal_detectado = None
            # Verificamos minuciosamente si la línea termina con la etiqueta exacta de nuestro diccionario
            for nombre_canal in diccionario_enlaces.keys():
                if linea.strip().endswith("," + nombre_canal):
                    canal_detectado = nombre_canal
                    break
            
            # Si es uno de los canales extraídos, buscamos su URL para actualizarla
            if canal_detectado and diccionario_enlaces[canal_detectado]:
                j = i + 1
                while j < len(lineas):
                    if lineas[j].strip().startswith("http"):
                        nuevas_lineas.append(diccionario_enlaces[canal_detectado] + "\n")
                        conteo += 1
                        i = j
                        break
                    else:
                        nuevas_lineas.append(lineas[j])
                        j += 1
        i += 1

    with open(ARCHIVO_M3U, "w", encoding="utf-8") as f:
        f.writelines(nuevas_lineas)
        
    print(f"\n[+] Proceso terminado. Se actualizaron {conteo} canales dentro de tu lista '{ARCHIVO_M3U}'. Los demás canales no fueron tocados.")

if __name__ == "__main__":
    print("[*] Iniciando cacería completa sobre tu lista personal...")
    enlaces_frescos = {}
    
    for canal, url in CANALES_CONFIG.items():
        link = cazar_m3u8(url, canal)
        if link:
            print(f"    [OK] Enlace cazado.")
            enlaces_frescos[canal] = link
        else:
            print(f"    [X] No se detectó flujo.")
            enlaces_frescos[canal] = None

    parchar_archivo_m3u(enlaces_frescos)
