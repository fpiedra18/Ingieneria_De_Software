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
NaturaClick/
├── config/                 # Configuración de Django (settings, urls)
├── treatments/             # App principal: modelos, vistas, plantillas y URLs
│   ├── migrations/
│   ├── templates/
│   │   ├── tratamientos.html
│   │   └── detalle_tratamiento.html
│   └── static/
│       ├── css/
│       │   └── tratamientos.css
│       └── js/
│           └── swiper-init.js
├── specialists/            # Gestión de especialistas y horarios
├── appointments/           # Lógica de citas y bloqueos de horario
├── requirements.txt        # Dependencias de Python
├── Procfile                # Configuración de despliegue (Heroku)
├── Dockerfile              # Contenedor Docker
└── README.md               # Documentación del proyecto
```

---

## ⚙️ Instalación y ejecución

1. **Clonar repositorio**:

   ```bash
   git clone https://github.com/tu-usuario/NaturaClick.git
   cd NaturaClick
   ```

2. **Configurar entorno**:

   * Crear un entorno virtual e instalar dependencias:

     ```bash
     python -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

3. **Variables de entorno**:

   * Copiar `.env.example` a `.env` y completar:

     ```env
     SECRET_KEY=tu_secret_key
     DEBUG=True
     DATABASE_URL=sqlserver://usuario:pass@host:port/dbname
     GOOGLE_CALENDAR_CREDENTIALS=path/to/credentials.json
     TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
     TWILIO_AUTH_TOKEN=your_token
     ```

4. **Migraciones y datos iniciales**:

   ```bash
   python manage.py migrate
   python manage.py loaddata initial_data.json
   ```

5. **Ejecutar servidor de desarrollo**:

   ```bash
   python manage.py runserver
   ```

   Accede a `http://localhost:8000`.

---

## 🛡️ Buenas prácticas y contribución

* Sigue el estilo PEP8 para Python y principios SOLID.
* Mantén el frontend organizado con componentes reutilizables.
* Crea ramas por cada feature o bugfix (`feature/nueva-funcionalidad`).
* Abre Pull Requests bien descritos y referenciando issues.
* Aceptamos contribuciones: crea un issue antes de implementar cambios relevantes.

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

> Creado con ❤️ por el equipo de **Clínica Natura**. ¡Bienvenido/a!



