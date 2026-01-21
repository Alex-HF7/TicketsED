<p align="center">
  <img src="base/static/base/img/l-ivem.png" alt="Logo del IVEM" width="200"/>
</p>

<h1 align="center">Sistema de Tickets – Departamento de Informática (IVEM)</h1>

<p align="center">
  Aplicación web desarrollada con <strong>Django</strong> para la gestión de reportes y tickets
  de soporte técnico del Departamento de Informática del IVEM.
</p>

---

## 🎫 Descripción del Proyecto

Este sistema permite al **personal del IVEM** reportar incidencias técnicas mediante un sistema de **tickets**, facilitando la comunicación con el **Departamento de Informática** y el seguimiento del estado de cada solicitud.

Cada usuario cuenta con un **usuario y contraseña**, con los cuales puede:
- Crear reportes de soporte
- Consultar el estado de sus tickets
- Visualizar el historial de incidencias

Por su parte, el **personal de Informática** puede:
- Visualizar todos los tickets registrados
- Clasificarlos por **departamento** y **categoría**
- Actualizar el estado de los tickets
- Dar seguimiento y solución a los reportes

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django
- **Base de datos:** PostgreSQL / MySQL / SQLite
- **Frontend:** HTML, CSS, Bootstrap
- **Autenticación:** Django Authentication System
- **Servidor de aplicación:** Gunicorn
- **Control de versiones:** Git & GitHub

---

## 👥 Roles del Sistema

### 🧑‍💼 Usuario (Personal del IVEM)
- Inicio de sesión con credenciales
- Registro de tickets de soporte
- Selección de:
  - Departamento
  - Categoría del ticket
- Consulta del estado del ticket:
  - Pendiente
  - En proceso
  - Resuelto

### 🧑‍💻 Personal de Informática
- Acceso a todos los tickets del sistema
- Visualización por:
  - Departamento
  - Categoría
  - Estado
- Actualización del estado de los tickets
- Control y seguimiento de incidencias

---

## 🗂️ Clasificación de Tickets

Los tickets se organizan de la siguiente manera:

### 📍 Por Departamento
Ejemplos:
- Administración
- Recursos Humanos
- Finanzas
- Dirección
- Informática

### 🏷️ Por Categoría
- 🖨️ Impresoras
- 💻 Software
- 🧠 Hardware

---

## 🚀 Instalación

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/Alex-HF7/ivem-tickets.git
cd ivem-tickets
