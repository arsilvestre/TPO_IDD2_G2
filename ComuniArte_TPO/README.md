TPO Ingeniería de Datos II – ComuniArte

Descripción general

**ComuniArte** es una plataforma cultural distribuida que integra múltiples tecnologías NoSQL para modelar relaciones sociales, gestionar usuarios, registrar interacciones y simular eventos en tiempo real.

El sistema se compone de:

* 🔵 **Neo4j** para relaciones sociales, contenidos y colaboraciones.
* 🟢 **MongoDB** para perfiles, likes, comentarios y visualizaciones.
* 🔴 **Redis** para transmisión en tiempo real (comentarios en vivo).



## 📁 Estructura del repositorio

```
ComuniArte_TPO/
├── neo4j_relaciones/            # Relaciones entre creadores y seguidores
├── mongodb_usuarios/           # Gestión de usuarios (GUI y conexión MongoDB)
├── comentarios_eventos/        # Comentarios y eventos en vivo con Redis
├── likes_vistas/               # Likes y visualizaciones (MongoDB)
├── capturas/                   # Imágenes del grafo y GUI
├── connect.env                 # Variables de conexión
├── requerimientos.txt          # Librerías necesarias
└── README.md                   # Documentación general
```


##  Requisitos

### 1. Dependencias de Python

Crear entorno virtual (opcional) y ejecutar:

```bash
pip install -r requerimientos.txt
```

### 2. Tecnologías necesarias

* Python 3.10+
* Neo4j Desktop corriendo
* MongoDB Atlas o local
* Redis local o remoto



## Ejecución de cada módulo

### 🔹 Neo4j – Relaciones

```bash
cd neo4j_relaciones
python crear_grafo_neo4j.py
```

### 🔹 MongoDB – Gestión de usuarios

```bash
cd mongodb_usuarios
python crud_usuarios_gui.py
```

### 🔹 Redis – Comentarios en vivo

```bash
cd comentarios_eventos
python redis_eventos.py
```

### 🔹 Likes y visualizaciones

```bash
cd likes_vistas
python simulador_likes.py
```

---

División del trabajo
* Valentin – Comentarios en tiempo real con Redis + MongoDB
* Ariel – Gestión de usuarios con MongoDB y GUI en Python
* Pau  – Simulación de likes y visualizaciones con MongoDB
* Valentina – Modelado de relaciones entre usuarios y contenidos con Neo4j



 Conclusión final

Si bien al principio pensamos que sería sencillo, nos enfrentamos a varios desafíos técnicos y de organización. Pero fue justamente eso lo que nos permitió aprender mucho más. Trabajar en equipo, compartir errores y ayudarnos entre nosotros fue clave para que el proyecto funcione. Más allá de lo técnico, nos llevamos una experiencia de verdadero compañerismo.
