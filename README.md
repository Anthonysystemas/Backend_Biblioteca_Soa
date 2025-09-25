# 📚 SOA Biblioteca Digital - Backend

Sistema de biblioteca digital basado en arquitectura SOA (Service-Oriented Architecture) desarrollado con FastAPI y Docker.

## 🏗️ Arquitectura

El sistema está compuesto por dos microservicios independientes:

- **auth-service** (Puerto 8000): Servicio de autenticación y gestión de usuarios
- **catalog-service** (Puerto 8001): Servicio de catálogo de libros y categorías

## 🚀 Tecnologías

- **FastAPI**: Framework web moderno para APIs
- **Python 3.9**: Lenguaje de programación
- **Docker & Docker Compose**: Containerización y orquestación
- **JWT**: Autenticación basada en tokens
- **bcrypt**: Hashing seguro de contraseñas
- **Pydantic**: Validación de datos
- **JSON**: Persistencia de datos

## 📦 Estructura del Proyecto

```
SOA-BIBLIOTECA/
├── auth-service/
│   ├── main.py              # Endpoints de autenticación
│   ├── models.py            # Modelos Pydantic
│   ├── database.py          # Operaciones de base de datos
│   ├── auth_utils.py        # Utilidades JWT y bcrypt
│   ├── config.py            # Configuraciones
│   ├── users.json           # Datos de usuarios
│   ├── requirements.txt     # Dependencias
│   └── Dockerfile           # Imagen Docker
├── catalog-service/
│   ├── main.py              # Endpoints de catálogo
│   ├── models.py            # Modelos Pydantic
│   ├── database.py          # Operaciones de base de datos
│   ├── config.py            # Configuraciones
│   ├── books.json           # Datos de libros
│   ├── categories.json      # Datos de categorías
│   ├── requirements.txt     # Dependencias
│   └── Dockerfile           # Imagen Docker
├── docker-compose.yml       # Orquestación de servicios
├── insomnia_auth_collection.json    # Colección API auth
├── insomnia_catalog_collection.json # Colección API catalog
└── README.md
```

## 🔧 Instalación y Ejecución

### Prerrequisitos
- Docker
- Docker Compose

### Ejecutar el Sistema

1. **Clonar el repositorio:**
```bash
git clone https://github.com/Anthonysystemas/Backend_Biblioteca_Soa.git
cd Backend_Biblioteca_Soa
```

2. **Construir las imágenes:**
```bash
docker-compose build
```

3. **Ejecutar los servicios:**
```bash
docker-compose up -d
```

4. **Verificar que los servicios estén corriendo:**
```bash
docker-compose ps
```

## 🌐 Endpoints Disponibles

### Auth Service (Puerto 8000)
- `GET /` - Health check
- `POST /register` - Registrar usuario
- `POST /login` - Iniciar sesión
- `POST /verify` - Verificar token JWT

### Catalog Service (Puerto 8001)
- `GET /` - Health check
- `GET /categories` - Obtener categorías
- `POST /categories` - Crear categoría (requiere auth)
- `GET /books` - Obtener libros
- `GET /books/{id}` - Obtener libro por ID
- `GET /books?category_id={id}` - Filtrar libros por categoría
- `POST /books` - Crear libro (requiere auth)
- `PUT /books/{id}` - Actualizar libro (requiere auth)

## 🧪 Pruebas con Insomnia

El proyecto incluye colecciones de Insomnia listas para usar:
- `insomnia_auth_collection.json` - Endpoints de autenticación
- `insomnia_catalog_collection.json` - Endpoints de catálogo

### Importar en Insomnia:
1. Abrir Insomnia
2. Import/Export → Import Data → From File
3. Seleccionar los archivos JSON

## 🔐 Flujo de Autenticación

1. **Registrar usuario:** `POST /register`
2. **Hacer login:** `POST /login` → Obtener JWT token
3. **Usar token:** Incluir token en requests autenticados del catalog-service

## 🏛️ Arquitectura SOA

- **Servicios independientes:** Cada servicio puede ejecutarse y escalarse por separado
- **Comunicación HTTP:** Los servicios se comunican vía REST API
- **Autenticación distribuida:** El catalog-service valida tokens con el auth-service
- **Persistencia independiente:** Cada servicio maneja sus propios datos

## 📊 Datos de Ejemplo

El sistema viene con datos de ejemplo pre-cargados:
- Usuarios de prueba en `auth-service/users.json`
- Categorías de libros en `catalog-service/categories.json`
- Libros de muestra en `catalog-service/books.json`

## 🐳 Docker

Cada servicio tiene su propia imagen Docker optimizada:
- Base: `python:3.9-slim`
- Dependencias cacheadas para builds rápidos
- Volúmenes para persistencia de datos

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 👨‍💻 Autor

**Anthony** - [@Anthonysystemas](https://github.com/Anthonysystemas)

---

⭐ ¡Dale una estrella si te gustó el proyecto!