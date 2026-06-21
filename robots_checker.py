import urllib.robotparser
import time

def evaluar_robots_txt(url_base, ruta_destino, nombre_fuente):
    print(f"\n🔍 Analizando restricciones éticas para: {nombre_fuente}")
    url_robots = url_base.rstrip('/') + '/robots.txt'
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url_robots)
    
    try:
        rp.read()
        permitido = rp.can_fetch('*', ruta_destino)
        print(f"🤖 Archivo localizado en: {url_robots}")
        if permitido:
            print(f"✅ ¡PERMITIDO! El sitio autoriza extraer datos en: {ruta_destino}")
        else:
            print(f"❌ ¡BLOQUEADO! El robots.txt explícitamente prohibe la ruta: {ruta_destino}")
        return permitido
    except Exception as e:
        print(f"⚠️ No se pudo leer el archivo robots.txt. Motivo: {e}")
        return True

if __name__ == "__main__":
    print("==================================================")
    print("   VALIDADOR AUTOMÁTICO DE ROBOTS.TXT (FELIPE)   ")
    print("==================================================")
    
    evaluar_robots_txt(
        url_base="https://medlineplus.gov", 
        ruta_destino="https://medlineplus.gov/spanish/healthtopics.html",
        nombre_fuente="Fuente 1 - MedlinePlus"
    )
    
    time.sleep(1)
    
    evaluar_robots_txt(
        url_base="https://www.meneame.net", 
        ruta_destino="https://www.meneame.net/c/ciencia",
        nombre_fuente="Fuente 2 - Menéame"
    )
    print("\n==================================================")