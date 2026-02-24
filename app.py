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
        u_scores = dados['scores']
        
        melhor_match = None
        menor_dist = 999
        
        for p in PARTICIPANTES:
            dist = abs(u_scores['res'] - p['res']) + \
                   abs(u_scores['rac'] - p['rac']) + \
                   abs(u_scores['lea'] - p['lea']) + \
                   abs(u_scores['soc'] - p['soc']) + \
                   abs(u_scores['car'] - p['car']) + \
                   abs(u_scores['est'] - p['est'])
            
            if dist < menor_dist:
                menor_dist = dist
                melhor_match = p
        
        # Salvar Lead no CSV para suas futuras vendas
        with open("leads_vendas.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now(), dados['nome'], dados['email'], melhor_match['nome']])
        
        return jsonify({
            "personagem": melhor_match['nome'],
            "foto": melhor_match['foto'],
            "bio": melhor_match['bio']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)