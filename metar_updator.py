import requests
import time

SERVER_URL = "http://192.168.127.137:5000"  # Altere conforme seu servidor

ICAOS_MONITORADOS = ["IPPH", "ITKO", "IRFD"]  # Altere aqui os ICAOs que deseja monitorar

def get_metar(icao):
    try:
        resp = requests.get(f"{SERVER_URL}/getmetar/{icao}")
        if resp.status_code == 200:
            d = resp.json()
            return f"📡 {icao} | 🌡️ APS: {d['aps']} hPa | 🛬 RRWY: {d['rrwy']}"
        else:
            return f"⚠️ {icao} não encontrado."
    except Exception as e:
        return f"❌ Erro em {icao}: {e}"

def monitor_loop():
    print("🔄 Iniciando monitoramento de METARs...\n(Pressione Ctrl+C para parar)\n")
    try:
        while True:
            print("=== Atualização ===")
            for icao in ICAOS_MONITORADOS:
                print(get_metar(icao.upper()))
            print()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n🛑 Monitoramento encerrado.")

if __name__ == "__main__":
    monitor_loop()
