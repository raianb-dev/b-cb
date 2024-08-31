import asyncio
import json
import websockets
from reqoperator import operator
from auth_inout import auth_wss
import time
import ssl
import random

from login import session_user

class play():
    def __init__(self):
        self.running = False  # Flag para controlar a execução do processo

    def double(self, bet: int, currency: str, username: str, password:str):
        TOKEN, r = session_user(session_user,username, password)
        
        self.running = True
        op, auth = operator(TOKEN)
        token = auth_wss(TOKEN)
        print("bet aqui::", type(bet))
        bet = float(bet)
        print("bet convertida", type(bet))
        # Config bets
        stake = bet
        last_result = []
        currency = currency
        color = ''
        loss = 1
        bet_placed = False
        color_to_bet = 'black'

        async def send_messages():
            # Url do websocket
            uri = f"wss://api.inout.games/io/?operatorId={op}&Authorization={token}&gameMode=new-double&EIO=4&transport=websocket"
            key_api = "5328905392:AAG29HHnR1vZQpCs5wcAvtDMfhzqJXzfrMA"

            # Criando uma fila para armazenar as mensagens
            message_queue = asyncio.Queue()
            
            # Desabilitando a verificação do certificado SSL
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            async with websockets.connect(uri, timeout=60, ssl=ssl_context) as websocket:
                # Enviando mensagem "40"
                await websocket.send("40")

                # Iniciando uma tarefa para receber mensagens do servidor
                async def receive_messages():
                    nonlocal stake, color, color_to_bet
                    while self.running:
                        try:
                            # Recebendo mensagens do websocket
                            message = await websocket.recv()
                            await message_queue.put(message)

                            # Capturando mensagem desejada
                            if 'gameService-game-status-changed' in message:
                                message_list = message.split('["gameService-game-status-changed",')[1:]
                                message_dict = json.loads(message_list[0][:-1])
                                status = message_dict.get('status')
                                print(status)

                                if status == 'WAIT_GAME':
                                    print("bet antes da mensagem:", type(stake))
                                    bet_message = f'42["gameService",{{"action":"make-bet","messageId":"1","payload":{{"betAmount":"{stake}","currency":"{currency}","color":"{color_to_bet}"}}}}]'
                                    await websocket.send(bet_message)
                                    print(f'Sending message: {bet_message}')

                                if status == 'IN_GAME':
                                    cellResult = message_dict.get('cellResult')
                                    print('aqui:::', message_dict.get('cellResult'))   
                                    color = cellResult['color']

                                    if color == 'black' and color_to_bet == 'black':
                                        stake = bet
                                    elif color == 'red' and color_to_bet == 'red':
                                        stake = bet
                                    elif (color == 'red' and color_to_bet == 'black') or (color == 'black' and color_to_bet == 'red'):
                                        if stake < bet*32:
                                            stake *=3
                                        else:
                                            stake = bet
                                    
                
                                    color_to_bet = 'red' if color != 'black' else 'black'
                        except websockets.exceptions.ConnectionClosed:
                            continue

                # Iniciando a tarefa de recebimento de mensagens
                receive_task = asyncio.create_task(receive_messages())
                INACTIVITY_TIMEOUT = 120 
                last_activity_time = time.time() # inicializando a última hora de atividade

                while self.running:
                    try:
                        # Aguardando a recepção de uma mensagem do servidor antes de enviar a próxima mensagem "3"
                        message_received = await asyncio.wait_for(message_queue.get(), timeout=7)
                        # Enviando mensagem "3"
                        await websocket.send("3")

                        # definindo a hora da última atividade para a hora atual
                        last_activity_time = time.time() 
                    except asyncio.TimeoutError:
                        # Enviando mensagem "3" caso o tempo de espera tenha expirado
                        await websocket.send("3")

                        if time.time() - last_activity_time > INACTIVITY_TIMEOUT:
                            await websocket.close()
                            break
                    except websockets.exceptions.ConnectionClosed:
                        break

                # Finalizando a tarefa de recebimento de mensagens
                receive_task.cancel()

        # Executando o loop de eventos do asyncio para enviar as mensagens
        asyncio.run(send_messages())

    def stop(self):
        self.running = False
