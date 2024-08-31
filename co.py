import websocket
import ssl
websocket.enableTrace(True)
# Desativando a verificação do certificado SSL para fins de teste.
ssl_opts = {"cert_reqs": ssl.CERT_NONE}

# Crie a conexão com o WebSocket
ws = websocket.WebSocket(sslopt=ssl_opts)
ws.connect("wss://api.inout.games/io/?operatorId=fca2a331-fbf1-4dff-9f56-a8f91c68b4f9&Authorization=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIyMzk4MTcwIiwibmlja25hbWUiOiJyYWlhbnBic3R1ZGlvIzE3NDIiLCJiYWxhbmNlIjoiOS45MyIsImN1cnJlbmN5IjoiQlJMIiwib3BlcmF0b3IiOiJmY2EyYTMzMS1mYmYxLTRkZmYtOWY1Ni1hOGY5MWM2OGI0ZjkiLCJvcGVyYXRvcklkIjoiZmNhMmEzMzEtZmJmMS00ZGZmLTlmNTYtYThmOTFjNjhiNGY5IiwibWV0YSI6bnVsbCwiZ2FtZUF2YXRhciI6bnVsbCwiaWF0IjoxNjgyMDQ0NDI3LCJleHAiOjE2ODIxMzA4Mjd9.od0QQTaZ9kHBCWcXjy9fyRaPyU6odUXqOxdlJbYfyZM&gameMode=new-double&EIO=4&transport=websocket")

# Enviar uma mensagem para o servidor
ws.send("40")
