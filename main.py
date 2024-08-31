from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from double import play  # Importe a classe play corretamente
import threading

app = Flask(__name__)
CORS(app)  # Habilita CORS para todos os domínios
api = Api(app)

# Dicionários globais para armazenar instâncias de 'play' e threads por usuário
plays = {}
threads = {}

class DoubleStart(Resource):
    def post(self):
        data = request.get_json()
        bet = data['bet']
        currency = data['currency']
        username = data['username']
        password = data['password']
        
        # Verifica se já existe uma instância de 'play' para este usuário
        if username not in plays:
            plays[username] = play()
        
        # Verifica se o processo já está em execução para este usuário
        if not plays[username].running:
            plays[username].running = True  # Define o estado como em execução
            thread = threading.Thread(target=plays[username].double, args=(bet, currency, username, password))
            threads[username] = thread
            thread.start()
            return {"status": "started"}, 200
        else:
            return {"status": "already running"}, 400

class DoubleStop(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        
        # Verifica se existe uma instância de 'play' para este usuário
        if username in plays and plays[username].running:
            plays[username].stop()  # Para o processo
            threads[username].join()  # Aguarda o término da thread
            plays[username].running = False  # Redefine o estado como não em execução
            del plays[username]  # Remove a instância do dicionário
            del threads[username]  # Remove a thread do dicionário
            return {"status": "stopped"}, 200
        else:
            return {"status": "not running"}, 400

api.add_resource(DoubleStart, '/double/start')
api.add_resource(DoubleStop, '/double/stop')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

