"""
Este script simula un sistema de donaciones en tiempo real en el contexto de una transmisión en vivo.
Utiliza una base de datos MongoDB para obtener dos grupos de usuarios: presentadores (filtrando por "rol": "creador")
y donadores (todos los usuarios con email válido). Cada tres segundos, el sistema selecciona aleatoriamente un donador, presentador, mensaje y monto
Luego, construye un objeto con toda esta información y lo publica en un canal de Redis Pub/Sub cuyo nombre coincide con el email del presentador.
"""

import redis
import json
import time
import random
from datetime import datetime
from pymongo import MongoClient

#Conexión a Redis Cloud
r = redis.Redis(
    host='redis-15684.c321.us-east-1-2.ec2.redns.redis-cloud.com',
    port=15684,
    username="default",
    password="ydxscnfNilAKtgf0X06AdMDpDPoE7tZf",
    decode_responses=True
)

# --- Configuración MongoDB ---
mongo_client = MongoClient("mongodb+srv://valentin:ValentinCampillo@clusterasilvestre.zlkahyz.mongodb.net/?retryWrites=true&w=majority&appName=ClusteraSilvestre")
db = mongo_client["ComuniArte"]
coleccion = db["usuarios"]

#Presentadores, donadores y mensajes
presentadores = []
for user_document in coleccion.find({"rol": "creador"}, {"email": 1, "_id": 0}):
    if "email" in user_document:
        presentadores.append(user_document["email"])

donadores = []
for user_document in coleccion.find({}, {"email": 1, "_id": 0}):
    if "email" in user_document:
        donadores.append(user_document["email"])

mensajes = ['¡Saludo grande!', 'Gracias por el contenido', 'Sos crack', 'Seguí asi']

while True:
    presentador = random.choice(presentadores)
    donador = random.choice(donadores)
    mensaje = random.choice(mensajes)
    monto = random.randrange(0, 200)

    canal = f"{presentador}"
    donacion = {
        "donador": donador,
        "monto": monto,
        "mensaje": mensaje,
        "presentador": presentador,
        "timestamp": time.time()
    }

    #Convertir a Json
    donacion_json = json.dumps(donacion)

    #Publicar por Pub
    r.publish(canal, donacion_json)

    #Guardar en una lista en Redis para visualización/persistencia
    r.rpush("log:donaciones", donacion_json)

    timestamp = datetime.now().timestamp()
    fecha_hora = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    print("\n", fecha_hora, "- DONACION", f"\n{canal} → {donacion_json}\n")
    time.sleep(3)
