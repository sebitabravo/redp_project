# REDP: Registro de Experiencias y Descubrimientos Personales

REDP (Registro de Experiencias y Descubrimientos Personales) es una aplicación construida con Django que permite a los usuarios registrar y compartir experiencias únicas, como lugares interesantes, habilidades aprendidas, o momentos memorables. También incluye funcionalidades como registro de usuarios, autenticación JWT y exportación de datos a CSV.

## 🚀 Funcionalidades Principales
- **Gestión de Experiencias:**
  - CRUD completo para experiencias categorizadas como descubrimientos culinarios, hitos personales y recomendaciones culturales.
- **Comentarios y Favoritos:**
  - Añadir comentarios a experiencias y marcarlas como favoritas.
- **Exportación de Datos:**
  - Descargar experiencias filtradas en formato CSV.
- **Autenticación JWT:**
  - Autenticación segura utilizando JSON Web Tokens.
- **Registro de Usuarios:**
  - Sistema de signup integrado con validación de integridad.

---

## 🛠️ Tecnologías Usadas
- **Backend:** Django, Django REST Framework
- **Base de Datos:** PostgreSQL (con soporte para SQLite en desarrollo)
- **Autenticación:** Django SimpleJWT
- **Frontend:** Templates HTML de Django
- **Despliegue (opcional):** Compatible con Railway y Heroku

---

## 📦 Instalación y Configuración

### **Requisitos Previos**
- Python 3.11+
- PostgreSQL (para producción)
- Pip (Administrador de paquetes de Python)
- Virtualenv (opcional, pero recomendado)

### **1. Clonar el Repositorio**
```bash
git clone <URL-del-repositorio>
cd redp_project
```

### **2. Crear un Entorno Virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### **3. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **4. Configurar Variables de Entorno**
Crea un archivo .env en el directorio raíz del proyecto y añade lo siguiente:
```bash
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3  # Cambiar a la configuración de PostgreSQL en producción
SECRET_KEY=tu-secreto-aqui # Crea una clave original y larga que sea por lo menos 10 caracteres
```

### **5. Aplicar Migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **6. Crear un Superusuario**
```bash
python manage.py createsuperuser
```

### **7. Iniciar el Servidor de Desarrollo**
```bash
python manage.py runserver
```
Visita http://127.0.0.1:8000/ para acceder a la aplicación.

