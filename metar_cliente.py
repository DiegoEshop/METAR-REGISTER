import requests
import json

SERVER_URL = "https://DiegoEshop.pythonanywhere.com"  # Altere se necessário

def set_metar(icao, aps, rrwy, wind):
    icao = icao.upper()
    data = {"aps": aps, "rrwy": rrwy, "wind": wind}
    try:
        resp = requests.post(f"{SERVER_URL}/setmetar/{icao}", json=data)
        if resp.status_code == 200:
            print(f"✅ METAR para {icao} atualizado.")
        else:
            print("❌ Erro:", resp.json().get("error"))
    except Exception as e:
        print("❌ Erro ao conectar:", e)

def get_metar(icao):
    icao = icao.upper()
    try:
        resp = requests.get(f"{SERVER_URL}/getmetar/{icao}")
        if resp.status_code == 200:
            d = resp.json()
            print(f"\n📡 METAR para {icao}:")
            print(f"✈️ ICAO: {d['icao']}")
            print(f"🌡️ APS: {d['aps']} hPa")
            print(f"🛬 RRWY: {d['rrwy']}")
            print(f"💨 Vento: {d['wind']}\n")
        else:
            print("⚠️", resp.json().get("error"))
    except Exception as e:
        print("❌ Erro ao conectar:", e)

def tcp_test():
    try:
        resp = requests.get(f"{SERVER_URL}/tcptest")
        print(resp.text)
    except Exception as e:
        print("❌ Erro na conexão:", e)

if __name__ == "__main__":
    print("Comandos disponíveis:")
    print("👉 /metset ICAO APS RRWY VENTO")
    print("👉 /metar ICAO")
    print("👉 /tcptest")
    print("Digite 'sair' para encerrar.\n")

    while True:
        try:
            comando = input(">>> ")
            if comando.lower() in ['sair', 'exit']:
                break

            partes = comando.strip().split(maxsplit=1)
            cmd = partes[0].lower()

            if cmd == "/metset" and len(partes) > 1:
                args = partes[1].split(maxsplit=3)
                if len(args) != 4:
                    print("❌ Use: /metset ICAO APS RRWY VENTO")
                    continue
                icao, aps, rrwy, wind = args
                set_metar(icao, aps, rrwy, wind)

            elif cmd == "/metar" and len(partes) > 1:
                icao = partes[1].strip()
                get_metar(icao)

            elif cmd == "/tcptest":
                tcp_test()

            else:
                print("❓ Comando desconhecido.")

        except KeyboardInterrupt:
            print("\nEncerrando...")
            break
