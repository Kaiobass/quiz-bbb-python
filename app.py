from flask import Flask, render_template, request, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Banco de dados com Bios personalizadas e nomes de fotos
PARTICIPANTES = [
    {
        "nome": "Juliette", "res": 10, "rac": 6, "lea": 10, "soc": 9, "car": 10, "est": 7, 
        "foto": "juliette.jpg", 
        "bio": "Você é autêntico e resiliente. Sua força vem da sua verdade, e mesmo sendo alvo, você não se corrompe. Seu carisma é sua maior arma!"
    },
    {
        "nome": "Thelma", "res": 9, "rac": 8, "lea": 9, "soc": 8, "car": 7, "est": 8, 
        "foto": "thelma.jpg", 
        "bio": "Você é o equilíbrio entre razão e emoção. Observador e fiel aos seus aliados, você sabe a hora certa de agir com firmeza e inteligência."
    },
    {
        "nome": "Arthur Aguiar", "res": 9, "rac": 8, "lea": 7, "soc": 8, "car": 8, "est": 9, 
        "foto": "artur.jpg", 
        "bio": "Um mestre da estratégia! Sua capacidade analítica e oratória são impecáveis. Você joga com as regras debaixo do braço e foca no objetivo final."
    },
    {
        "nome": "Davi Brito", "res": 10, "rac": 4, "lea": 8, "soc": 6, "car": 9, "est": 5, 
        "foto": "davibritto.jpg", 
        "bio": "Corajoso e incansável! Você não tem medo do embate e defende o que acredita até o fim. Sua energia movimenta a casa e o público."
    },
    {
        "nome": "Prior", "res": 8, "rac": 7, "lea": 6, "soc": 7, "car": 8, "est": 8, 
        "foto": "prior.jpg", 
        "bio": "Intenso e competitivo! Você é o jogador que não foge da raia e joga com transparência total, transformando o jogo em um tabuleiro de pura adrenalina."
    },
    {
        "nome": "Gil do Vigor", "res": 8, "rac": 9, "lea": 8, "soc": 9, "car": 10, "est": 8, 
        "foto": "gildovigor.jpg", 
        "bio": "O coração do programa! Você entrega entretenimento, inteligência acadêmica e muita emoção. Sua intensidade é o que te torna inesquecível."
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['POST'])
def quiz():
    try:
        dados = request.json
        u_scores = dados.get('scores', {})
        
        melhor_match = PARTICIPANTES[0]
        menor_dist = 999
        
        # Cálculo matemático de proximidade
        for p in PARTICIPANTES:
            dist = abs(u_scores.get('res', 5) - p['res']) + \
                   abs(u_scores.get('rac', 5) - p['rac']) + \
                   abs(u_scores.get('lea', 5) - p['lea']) + \
                   abs(u_scores.get('soc', 5) - p['soc']) + \
                   abs(u_scores.get('car', 5) - p['car']) + \
                   abs(u_scores.get('est', 5) - p['est'])
            
            if dist < menor_dist:
                menor_dist = dist
                melhor_match = p
        
        # SALVAMENTO SEGURO EM CSV (Evita travamento no Render)
        try:
            # Verifica se o arquivo existe para não dar erro de permissão
            with open("leads_vendas.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                    dados.get('nome', 'Sem Nome'), 
                    dados.get('email', 'Sem Email'), 
                    melhor_match['nome']
                ])
        except Exception as csv_error:
            # Se der erro no CSV, ele apenas avisa no log do Render e não trava o site
            print(f"Aviso: Erro ao salvar lead no CSV (Ignore se o resultado aparecer): {csv_error}")

        return jsonify({
            "personagem": melhor_match['nome'],
            "foto": melhor_match['foto'],
            "bio": melhor_match['bio']
        })

    except Exception as e:
        print(f"Erro crítico no processamento: {e}")
        return jsonify({"error": "Erro interno no servidor"}), 500

if __name__ == '__main__':
    # Porta configurada para rodar localmente ou em produção
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
