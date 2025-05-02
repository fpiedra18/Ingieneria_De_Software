# NaturaClick

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](#) [![Python](https://img.shields.io/badge/python-3.9+-blue)](#) [![Django](https://img.shields.io/badge/django-4.x-green)](#)

---

## 📋 Descripción

NaturaClick es una plataforma web integral diseñada para **Clínica Natura** que facilita el agendamiento de tratamientos estéticos de forma rápida y profesional. Los usuarios pueden:

* Visualizar el catálogo de tratamientos en un carrusel interactivo.
* Consultar detalles de cada tratamiento (duración, precio, imagen y descripción).
* Agendar citas según disponibilidad de especialistas.
* Recibir confirmaciones automáticas por WhatsApp.
* Sincronizar sus citas con Google Calendar.

El panel de administración permite a los encargados de la clínica gestionar tratamientos, especialistas, horarios y citas, garantizando una experiencia fluida tanto para el cliente como para el equipo.

---

## 🚀 Funcionalidades principales

1. **Catálogo de tratamientos**: Carrusel responsive con Swiper.js.
2. **Detalles de tratamiento**: Vista individual con información completa y botón de consulta.
3. **Agendamiento de citas**:

   * Asignación automática de especialistas según disponibilidad.
   * Prevención de conflictos de horario y doble reserva.
4. **Integraciones**:

   * **Google Calendar API** para sincronizar eventos.
   * **WhatsApp API (Twilio)** para confirmaciones y recordatorios.
5. **Panel administrativo**: CRUD de tratamientos, especialistas, horarios y citas.

---

## 🛠️ Tecnologías

* **Backend**: Python 3.9+, Django 4.x
* **Frontend**: Django Templates, HTML5, CSS3 (Tailwind CSS), JavaScript (Swiper.js)
* **Base de datos**: SQL Server
* **Integraciones**:

  * Google Calendar API
  * WhatsApp (Twilio)
* **Control de versiones**: Git & GitHub
* **Despliegue**: Docker / Heroku / AWS (opcional)

---

## 📂 Estructura del proyecto

```bash
Ingieneria_De_Software/       # Repositorio y proyecto Django principal
├── citas/                    # Aplicación principal para gestión de citas
│   ├── __pycache__/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── calendar_sync.py     # Sincronización con Google Calendar
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── credentials/              # Credenciales de APIs (no subir a repo público)
│   ├── credentials.json      # Google Calendar
│   └── token.json            # Token OAuth generado
├── media/                    # Archivos subidos por usuarios
├── proyecto/                 # Configuración global de Django
│   ├── __pycache__/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/                   # Activos estáticos
│   ├── css/
│   │   ├── agendar_protegido.css
│   │   ├── agendar.css
│   │   ├── base.css
│   │   ├── clases.css
│   │   ├── detalle_tratamiento.css
│   │   ├── estilo.css
│   │   └── gracias.css
│   ├── img/                  # Imágenes de UI (logo, hero, placeholders)
│   └── js/
│       └── agendar_protegido.js
├── templates/                # Plantillas HTML
│   ├── includes/             # Componentes parciales (header, footer, etc.)
│   └── [varias vistas .html]
├── db.sqlite3                # Base de datos SQLite (db.sqlite3)
├── google_auth.py            # Lógica de autenticación OAuth con Google
├── manage.py                 # Comandos de gestión Django
└── .gitignore                # Ignora archivos sensibles y __pycache__
```

---

## ⚙️ Configuración del proyecto en Visual Studio Code

A continuación se describe cómo clonar el repositorio, abrirlo en VS Code y manejar commits y ramas desde el IDE.

1. **Clonar desde GitHub y abrir en VS Code**:

   ```bash
   git clone https://github.com/tu-usuario/Ingieneria_De_Software.git
   cd Ingieneria_De_Software
   code .                   # Abre el proyecto en Visual Studio Code
   ```

2. **Instalar dependencias (si las hubiera)**:

   * Este proyecto utiliza únicamente Python  y Django; no hay `requirements.txt`. Si agregas paquetes, recuerda instalarlos con:

     ```bash
     pip install <paquete>
     ```

3. **Configurar la base de datos**:

   * Se usa **SQLite** por defecto. El archivo está en `db.sqlite3`. No se requieren ajustes adicionales.

4. **Ejecutar servidor de desarrollo**:

   * En VS Code, abre una terminal integrada y ejecuta:

     ```bash
     python manage.py migrate
     python manage.py runserver
     ```
   * Accede en tu navegador a `http://localhost:8000`.

5. **Versionado y ramas en Git desde VS Code**:

   * **Commit directo en `main`**:

     1. Haz cambios en archivos.
     2. Ve a la sección Source Control (ícono de rama o Ctrl+Shift+G).
     3. Escribe un mensaje descriptivo y pulsa el icono ✓ para hacer commit.
     4. Haz click en el icono de los tres puntos (…) y selecciona **Push** para subir a `main`.

   * **Trabajo en ramas**:

     1. En VS Code, selecciona la rama actual (`main`) en la barra inferior.
     2. Elige **Create new branch** y nómbrala, por ejemplo, `feature/mi-nueva-funcionalidad`.
     3. Realiza commits en esa rama (igual que en main).
     4. Para subir la rama al repositorio remoto, ve a Source Control, haz click en **Publish Branch**.
     5. Desde GitHub, podrás abrir un Pull Request para revisar e integrar a `main`.

6. **Integración posterior**:

   * **Merge desde GitHub**: Una vez aprobado el Pull Request, GitHub integra la rama en `main`.
   * **Actualizar tu copia local**:

     ```bash
     git checkout main
     git pull origin main
     ```

---



