from pymongo import MongoClient
from datetime import datetime

# Conexión a MongoDB Atlas
client = MongoClient("mongodb+srv://cpaucar:Base123%21@cluster0.hiparqe.mongodb.net/?retryWrites=true&w=majority")
db = client["ComuniArte"]
coleccion = db["interacciones"]

# Insertar un comentario
comentario = {
    "tipo": "comentario",
    "usuario": "crisler",
    "mensaje": "¡Muy bueno este post!",
    "fecha": datetime.now(),
    "post_id": "post123"
}
coleccion.insert_one(comentario)

# Insertar un like
like = {
    "tipo": "like",
    "usuario": "crisler",
    "fecha": datetime.now(),
    "post_id": "post123"
}
coleccion.insert_one(like)

# Insertar una visualización
visualizacion = {
    "tipo": "visualizacion",
    "usuario": "crisler",
    "fecha": datetime.now(),
    "post_id": "post123"
}
coleccion.insert_one(visualizacion)

# Mostrar todos los comentarios
print("\nComentarios:")
for doc in coleccion.find({"tipo": "comentario"}):
    print(doc)

# Mostrar cantidad de likes
likes = coleccion.count_documents({"tipo": "like", "post_id": "post123"})
print("\nCantidad de likes:", likes)

# Mostrar cantidad de visualizaciones
vistas = coleccion.count_documents({"tipo": "visualizacion", "post_id": "post123"})
print("Cantidad de visualizaciones:", vistas)
