from neo4j import GraphDatabase
from pymongo import MongoClient

# === CONEXIÓN A NEO4J ===
uri = "bolt://localhost:7687"
user = "neo4j"
password = "valentina"
driver = GraphDatabase.driver(uri, auth=(user, password))

# === CONEXIÓN A MONGODB ATLAS ===
mongo_client = MongoClient("mongodb+srv://valentin:ValentinCampillo@clusterasilvestre.zlkahyz.mongodb.net/?retryWrites=true&w=majority&appName=ClusteraSilvestre")
db = mongo_client["ComuniArte"]
coleccion = db["usuarios"]

# === FUNCIÓN PARA CREAR GRAFO EN NEO4J ===
def crear_grafo_comuniarte(tx):
    # Crear usuarios
    tx.run("""
        CREATE
          (juana:User {id: "u1", nombre: "Juana", tipo: "CREADOR", region: "NOA", intereses: ["poesía", "arte urbano"]}),
          (carlos:User {id: "u2", nombre: "Carlos", tipo: "ESPECTADOR", region: "Cuyo", intereses: ["folklore"]}),
          (mar:User {id: "u3", nombre: "Mar", tipo: "CREADOR", region: "NOA", intereses: ["arte urbano"]}),
          (lara:User {id: "u4", nombre: "Lara", tipo: "CREADOR", region: "Patagonia", intereses: ["audiovisual", "radio"]})
    """)

    # Relaciones de seguimiento
    tx.run("""
        MATCH (carlos:User {nombre: "Carlos"}), (juana:User {nombre: "Juana"}),
              (mar:User {nombre: "Mar"}), (lara:User {nombre: "Lara"})
        CREATE
          (carlos)-[:SIGUE_A]->(juana),
          (carlos)-[:SIGUE_A]->(mar),
          (juana)-[:SIGUE_A]->(lara)
    """)

    # Crear contenidos
    tx.run("""
        CREATE
          (obra1:Content {id: "c1", titulo: "Versos en el viento", tipo: "poesía", fecha_subida: date("2024-10-12")}),
          (obra2:Content {id: "c2", titulo: "Resistencia sonora", tipo: "audio", fecha_subida: date("2024-11-01")})
    """)

    # Relación CREÓ
    tx.run("""
        MATCH (juana:User {nombre: "Juana"}), (lara:User {nombre: "Lara"}),
              (obra1:Content {id: "c1"}), (obra2:Content {id: "c2"})
        CREATE
          (juana)-[:CREÓ]->(obra1),
          (lara)-[:CREÓ]->(obra2)
    """)

    # Reproducciones
    tx.run("""
        MATCH (carlos:User {nombre: "Carlos"}),
              (obra1:Content {id: "c1"}), (obra2:Content {id: "c2"})
        CREATE
          (carlos)-[:REPRODUJO]->(obra1),
          (carlos)-[:REPRODUJO]->(obra2)
    """)

    # Colaboraciones
    tx.run("""
        MATCH (juana:User {nombre: "Juana"}),
              (mar:User {nombre: "Mar"}),
              (lara:User {nombre: "Lara"})
        CREATE
          (juana)-[:COLABORÓ_CON]->(mar),
          (mar)-[:COLABORÓ_CON]->(lara)
    """)

# === FUNCION PARA CARGAR USUARIOS EN MONGODB (si no existen) ===
usuarios = [
    {"id": "u1", "nombre": "Juana", "tipo": "CREADOR", "region": "NOA", "intereses": ["poesía", "arte urbano"]},
    {"id": "u2", "nombre": "Carlos", "tipo": "ESPECTADOR", "region": "Cuyo", "intereses": ["folklore"]},
    {"id": "u3", "nombre": "Mar", "tipo": "CREADOR", "region": "NOA", "intereses": ["arte urbano"]},
    {"id": "u4", "nombre": "Lara", "tipo": "CREADOR", "region": "Patagonia", "intereses": ["audiovisual", "radio"]}
]

for u in usuarios:
    if coleccion.count_documents({"id": u["id"]}) == 0:
        coleccion.insert_one(u)
        print(f"📥 Usuario insertado en MongoDB: {u['nombre']}")
    else:
        print(f"⚠️ Ya existe en MongoDB: {u['nombre']}")

# === EJECUTAR NEO4J ===
with driver.session() as session:
    session.write_transaction(crear_grafo_comuniarte)

print("✅ Grafo creado en Neo4j.")
driver.close()
