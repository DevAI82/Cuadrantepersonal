# 📁 Copias de Seguridad del Cuadrante 2026 (Backups)

Esta carpeta almacena el historial de copias de seguridad periódicas del Cuadrante Personal 2026 extraídas directamente de **Supabase**.

---

## 📌 Historial de Copias

| Archivo | Fecha de Extracción | Turnos Consolidados | Trabajadores | Generado Por |
| :--- | :--- | :--- | :--- | :--- |
| [`Cuadrante_2026_Backup_2026-09-19_1438.json`](./Cuadrante_2026_Backup_2026-09-19_1438.json) | 19 de septiembre de 2026 (14:38) | 13.214 | 45 (5 dptos.) | CLI Backup |

---

## 🛠️ ¿Cómo Restaurar una Copia de Seguridad?

### Opción A: Desde la Aplicación Web
1. Abre la aplicación web del Cuadrante en tu navegador.
2. En la barra superior, haz clic en el botón verde **`💾 Copia de Seguridad`**.
3. En la sección naranja, haz clic en **`📂 Seleccionar Archivo JSON de Respaldo`** y selecciona el archivo `.json` deseado de esta carpeta.
4. Revisa el resumen de seguridad y pulsa **`⚠️ Confirmar y Restaurar en Supabase`**.
5. Toda la base de datos se actualizará al estado de esa fecha y los demás usuarios conectados se sincronizarán al instante.

### Opción B: Exportar una Nueva Copia
Para añadir una nueva copia a esta carpeta, ejecuta:
```bash
python exportar_backup_supabase.py
```
El archivo se creará automáticamente con la fecha y hora actual en esta misma carpeta.
