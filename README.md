# Cuadrante Personal 2026

Aplicación web progresiva (PWA / SPA) para la gestión integral y consulta de turnos, horarios, coberturas y libranzas del personal de tienda de **El Corte Inglés, Centro 0864 - Albacete II** para el año 2026.

---

## 🚀 Características Principales

- **Gestión Multi-Departamento**: Cuadrantes de Operaciones, Omnicanal, Caja / SAC, Muelle y Postventa.
- **Sincronización en Tiempo Real**: Conectado a base de datos Supabase con suscripción `postgres_changes` para reflejar modificaciones en vivo en todos los dispositivos.
- **Vistas Adaptadas**:
  - **Semanal**: Matriz de turnos por empleado y día de la semana.
  - **Día**: Desglose y cobertura horaria por franjas de 30 minutos (slot coverage).
  - **Plantilla Efectiva y Estudio**: Análisis de dotación y balance de personal.
  - **Informe Global**: Vista consolidada multi-departamento para seguimiento de centro.
- **Catálogo Determinista de Turnos**: Integración con el catálogo oficial de códigos de turno, horarios, minutos de descanso y pausas de comida.

---

## 📚 Catálogo Determinista de Turnos y Descansos

Toda la información horaria de los 49 trabajadores del centro ha sido estandarizada en un catálogo canónico:

- **JSON de datos**: [`catalogo_turnos_completo.json`](./catalogo_turnos_completo.json) (195 códigos con horas de entrada, salida, minutos de descanso, intervalos de pausa y horas netas).
- **Biblioteca JavaScript**: [`catalogo_turnos_completo.js`](./catalogo_turnos_completo.js) (expone `window.CATALOGO_TURNOS_OFICIAL_2026`).
- **Guía de referencia y esquema**: Consulta [`CONTEXTO_CATALOGO_TURNOS.md`](./CONTEXTO_CATALOGO_TURNOS.md) para conocer el formato detallado de cada campo y ejemplos de uso.

---

## 🛠️ Tecnologías

- **Frontend**: HTML5, CSS3 moderno (variables CSS, responsive design), Vanilla JavaScript (ES6+).
- **Gráficos**: Chart.js.
- **Backend / Datos**: Supabase (PostgreSQL + REST API + Realtime Channels).
- **PWA**: Manifest y Service Worker para soporte offline e instalación móvil.
