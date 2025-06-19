"""
Este script simula la interacción de usuarios en una transmisión en vivo.
Cada 3 segundos, selecciona al azar un usuario (a partir de los emails almacenados en una base de datos MongoDB)
y una pregunta predefinida. Luego, esa pregunta es enviada a un stream en Redis (simulando una transmisión en tiempo real)
y también se guarda en el campo "preguntas" del documento correspondiente al usuario en MongoDB,
permitiendo registrar el historial de preguntas realizadas por cada participante, para su analisis y seguimiento en caso de ser necesario.
"""

import redis
import time
import random
from datetime import datetime
from pymongo import MongoClient

# --- Conexión a Redis Cloud ---
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

# --- Stream de Redis ---
stream_id = "transmision:140318:preguntas"

# --- Preguntas posibles ---
preguntas_posibles = [
    "¿Qué opinás del contenido hasta ahora?",
    "¿Recomendás algún recurso para seguir aprendiendo?",
    "¿Dónde puedo ver tus trabajos anteriores?",
    "¿Tenés algún consejo práctico para aplicar hoy?"
]

# --- Obtener lista de emails desde Mongo ---
emails = []
for user_document in coleccion.find({}, {"email": 1, "_id": 0}):
    if "email" in user_document:
        emails.append(user_document["email"])

# --- Validación previa ---
if not emails:
    print("❌ No se encontraron emails en la base.")
else:
    print(f"✅ {len(emails)} usuarios encontrados. Iniciando transmisión...\n")

    # --- Loop de transmisión cada 3 segundos ---
    while True:
        # Elegimos usuario y pregunta random
        email_random = random.choice(emails)
        pregunta_random = random.choice(preguntas_posibles)

        # 1. Enviar a Redis
        r.xadd(stream_id, {
            "usuario": email_random,
            "pregunta": pregunta_random
        })

        # 2. Guardar en Mongo
        coleccion.update_one(
            {"email": email_random},
            {"$push": {"preguntas": pregunta_random}}
        )

        # 3. Log en consola
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{fecha_hora} - ENVIADO")
        print(f"{email_random} → {pregunta_random}\n")

        time.sleep(3)