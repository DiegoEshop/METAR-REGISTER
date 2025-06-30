from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
metar_data = {}  # Armazena os dados por ICAO

@app.route('/setmetar/<icao>', methods=['POST'])
def set_metar(icao):
    icao = icao.upper()
    data = request.json
    aps = data.get('aps')
    rrwy = data.get('rrwy')
    wind = data.get('wind')

    if not aps or not rrwy or not wind:
        return jsonify({"error": "Campos 'aps', 'rrwy' e 'wind' são obrigatórios."}), 400

    metar_data[icao] = {"aps": aps, "rrwy": rrwy, "wind": wind}
    return jsonify({"message": f"METAR para {icao} atualizado com sucesso."})

@app.route('/setmetars', methods=['POST'])
def set_metars():
    data = request.json

    if not isinstance(data, dict):
        return jsonify({"error": "Formato inválido, deve ser um objeto JSON com ICAOs."}), 400

    for icao, info in data.items():
        icao = icao.upper()
        aps = info.get('aps')
        rrwy = info.get('rrwy')
        wind = info.get('wind')
        if not aps or not rrwy or not wind:
            return jsonify({"error": f"Campos 'aps', 'rrwy' e 'wind' obrigatórios para {icao}."}), 400
        metar_data[icao] = {"aps": aps, "rrwy": rrwy, "wind": wind}

    return jsonify({"message": "METARs atualizados com sucesso."})

@app.route('/getmetar/<icao>', methods=['GET'])
def get_metar(icao):
    icao = icao.upper()
    if icao not in metar_data:
        return jsonify({"error": f"METAR não encontrado para {icao}."}), 404

    dados = metar_data[icao]
    return jsonify({
        "icao": icao,
        "aps": dados["aps"],
        "rrwy": dados["rrwy"],
        "wind": dados["wind"]
    })

@app.route('/metar/<icao>', methods=['GET'])
def metar_html(icao):
    icao = icao.upper()
    if icao not in metar_data:
        return f"<h3>⚠️ METAR não encontrado para {icao}</h3>", 404

    dados = metar_data[icao]
    template = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8" />
        <title>METAR Atual - {{ icao }}</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f4f9;
                color: #333;
                padding: 20px;
            }
            .metar-box {
                background: white;
                padding: 15px 25px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                max-width: 400px;
                margin: auto;
            }
            h1 {
                text-align: center;
                margin-bottom: 20px;
                color: #005f73;
            }
            p {
                font-size: 18px;
                margin: 8px 0;
            }
            .emoji {
                font-size: 24px;
                margin-right: 10px;
            }
        </style>
    </head>
    <body>
        <div class="metar-box">
            <h1>📡 METAR atual - {{ icao }}</h1>
            <p><span class="emoji">✈️</span> ICAO: {{ icao }}</p>
            <p><span class="emoji">🌡️</span> APS: {{ aps }} hPa</p>
            <p><span class="emoji">🛬</span> RRWY: {{ rrwy }}</p>
            <p><span class="emoji">💨</span> Vento: {{ wind }}</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(template, icao=icao, aps=dados["aps"], rrwy=dados["rrwy"], wind=dados["wind"])

@app.route('/tcptest', methods=['GET'])
def tcp_test():
    return "✅ Conexão com o servidor OK!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
