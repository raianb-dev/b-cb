import asyncio
import json
import websockets
from reqoperator import operator
from sessionID import TOKEN
from auth_inout import auth_wss
import time
import ssl
import random

op, auth = operator(TOKEN)
token = auth_wss(TOKEN)

# Config bets
initial_bet = 0.02
fibonacci_sequence = [1, 1]  # Início da sequência de Fibonacci
current_index = 0
current_bet = initial_bet * fibonacci_sequence[current_index]
last_result = []
currency = 'BRL'
max_fibonacci_index = 10  # Limite de índice para a sequência de Fibonacci
last_colors = []  # Histórico das últimas cores
change_threshold = 6  # Mudar a cor após esta sequência de mesma cor

async def send_messages():
    # Url do websocket
    uri = f"wss://api.inout.games/io/?gameMode=platform-mines&operatorId={op}&Authorization={token}&EIO=4&transport=websocket"
  
    # Desabilitando a verificação do certificado SSL
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    while True:
        try:
            async with websockets.connect(uri, ssl=ssl_context) as websocket:
                # Enviando mensagem "40" ao iniciar
                await websocket.send("40")
                await asyncio.sleep(10)
                # Enviando mensagem "420["gameService",{"action":"get-game-state","payload":{}}]" após "40"
                await websocket.send('420["gameService",{"action":"get-game-state","payload":{}}]')

                # Iniciando uma tarefa para receber mensagens do servidor
                async def receive_messages():
                    global current_bet, current_index, fibonacci_sequence, last_colors
                    while True:
                        try:
                            # Recebendo mensagens do WebSocket
                            message = await websocket.recv()
                            print(message)

                            if '430[null]' in message or '"isFinished":true' in message:
                                is_win = '"isWin":true' in message

                                if is_win:
                                    # Voltar dois passos na sequência de Fibonacci após uma vitória
                                    current_index = max(0, current_index - 2)
                                else:
                                    # Avançar um passo na sequência de Fibonacci após uma perda
                                    current_index += 1
                                    if current_index >= len(fibonacci_sequence):
                                        if current_index <= max_fibonacci_index:
                                            fibonacci_sequence.append(fibonacci_sequence[-1] + fibonacci_sequence[-2])
                                        else:
                                            current_index = max_fibonacci_index

                                current_bet = initial_bet * fibonacci_sequence[current_index]
                                print(f"Aposta atual: {current_bet} (Índice Fibonacci: {current_index})")

                                # Enviando mensagem de aposta com a aposta atual
                                bet_message = f'423["gameService",{{"action":"bet","payload":{{"betAmount":"{current_bet}","minesCount":{random.randint(5, 7)},"currency":"{currency}"}}}}]'
                                await websocket.send(bet_message)
                                print(f'Sending message: {bet_message}')
                                await asyncio.sleep(5)
                                # Enviando mensagem de passo (step)
                                random_cell_position = random.randint(0, 19)
                                step_message = f'426["gameService",{{"action":"step","payload":{{"cellPosition":{random_cell_position}}}}}]'
                                await websocket.send(step_message)
                                print(f'Sending message: {step_message}')
                                await asyncio.sleep(5)
                                # Enviando mensagem de retirada
                                withdrawal_message = '427["gameService",{"action":"withdraw"}]'
                                await websocket.send(withdrawal_message)
                                print(f'Sending message: {withdrawal_message}')
                                
                        except websockets.exceptions.ConnectionClosedError:
                            print("Conexão encerrada. Tentando reconectar...")
                            break
                        except Exception as e:
                            print(f"Erro ao receber mensagem: {e}")
                            break
                                
                # Iniciando a tarefa de recebimento de mensagens
                receive_task = asyncio.create_task(receive_messages())

                # Mantendo o loop principal aberto
                while True:
                    try:
                        await asyncio.sleep(15)
                        await websocket.send("3")
                    except asyncio.CancelledError:
                        break
                    except Exception as e:
                        print(f"Erro ao enviar mensagem: {e}")

                receive_task.cancel()

        except Exception as e:
            print(f"Erro na conexão: {e}")

        await asyncio.sleep(5)

asyncio.run(send_messages())
