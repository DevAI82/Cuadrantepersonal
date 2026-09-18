# Catálogo Determinista de Turnos, Horarios y Descansos 2026
**Centro:** 0864 - ALBACETE II (El Corte Inglés, S.A.)  
**Año:** 2026  
**Fichero de datos:** [`catalogo_turnos_completo.json`](./catalogo_turnos_completo.json)  
**Fichero JavaScript:** [`catalogo_turnos_completo.js`](./catalogo_turnos_completo.js)

---

## 1. Propósito y Contexto del Catálogo

Este catálogo consolida y unifica de manera **100% determinista** la información oficial de turnos de trabajo, pausas reglamentarias de descanso/comida y tiempos de trabajo efectivo extraídos directamente de los **49 calendarios individuales en formato PDF** del personal de tienda de El Corte Inglés Albacete II.

Su objetivo es eliminar ambigüedades, estimaciones heurísticas o cálculos erróneos en la aplicación **Cuadrante Personal**, sirviendo como **fuente de verdad canónica** para:
1. Cálculo exacto del cómputo de horas trabajadas (diarias, semanales y anuales).
2. Tramos horarios de presencia física (horas de entrada y salida reales).
3. Tramos de descanso no retribuido / desconexión (ej. comida de 12:00 a 15:00 o pausas de 15 a 180 minutos).
4. Cobertura de franjas de 30 minutos (slot coverage) en los informes diarios y semanales de Caja, SAC, Omnicanal, Muelle y Operaciones.
5. Determinación de sábados de calidad, libranzas y compensatorios.

---

## 2. Estructura de Datos (`catalogo_turnos_completo.json`)

Cada entrada del catálogo contiene los siguientes campos deterministas:

| Campo | Tipo | Descripción | Ejemplo (`ZG6`) |
| :--- | :--- | :--- | :--- |
| `codigo` | `string` | Clave identificativa del turno según el sistema de personal | `"ZG6"` |
| `tipo` | `string` | Categoría macro: `TRABAJO`, `DESCANSO`, `VACACIONES`, `AUSENCIA`, `PERMISO`, `FORMACION`, `FESTIVO` | `"TRABAJO"` |
| `clasificacion` | `string` | Código de turno: `MAN` (Mañana), `TAR` (Tarde), `PAR` (Partido), `LIB`, `VAC`, `COM`, etc. | `"PAR"` |
| `clasificacion_descripcion` | `string` | Descripción legible de la jornada | `"Partido"` |
| `horario` | `string` | Franja completa de presencia en tienda | `"09:30 - 20:30"` |
| `hora_entrada` | `string` | Hora de inicio (formato `HH:MM`) | `"09:30"` |
| `hora_salida` | `string` | Hora de fin (formato `HH:MM`) | `"20:30"` |
| `duracion_total_minutos` | `number` | Minutos transcurridos entre entrada y salida | `660` |
| `horas_brutas` | `number` | Horas brutas de permanencia en tienda | `11.0` |
| `minutos_descanso` | `number` | Minutos de pausa/comida no computables como trabajo | `180` |
| `horas_descanso` | `number` | Horas de descanso | `3.0` |
| `pausas_horario` | `string \| null` | Horario de la pausa si está especificado en el cuadrante | `"12:00 - 15:00"` |
| `pausa_inicio` | `string \| null` | Inicio del intervalo de descanso (`HH:MM`) | `"12:00"` |
| `pausa_fin` | `string \| null` | Fin del intervalo de descanso (`HH:MM`) | `"15:00"` |
| `tiempo_teorico` | `string` | Tiempo efectivo de jornada en formato `HH:MM` | `"08:00"` |
| `horas_trabajo_efectivo` | `number` | Horas efectivas netas a computar en el cuadrante | `8.0` |
| `trabajadores` | `array<string>` | Empleados que tienen asignado este código en sus cuadrantes | `["JOSE MIGUEL OLMEDA PASCUAL"]` |

### Ejemplo JSON
```json
{
  "ZG6": {
    "codigo": "ZG6",
    "tipo": "TRABAJO",
    "clasificacion": "PAR",
    "clasificacion_descripcion": "Partido",
    "horario": "09:30 - 20:30",
    "hora_entrada": "09:30",
    "hora_salida": "20:30",
    "duracion_total_minutos": 660,
    "horas_brutas": 11.0,
    "minutos_descanso": 180,
    "horas_descanso": 3.0,
    "pausas_horario": "12:00 - 15:00",
    "pausa_inicio": "12:00",
    "pausa_fin": "15:00",
    "tiempo_teorico": "08:00",
    "horas_trabajo_efectivo": 8.0,
    "trabajadores": [
      "JOSE MIGUEL OLMEDA PASCUAL"
    ]
  }
}
```

---

## 3. Resumen Global de Códigos Identificados

- **Total global de códigos**: **195**
  - **Turnos de trabajo efectivos**: **180 códigos**
  - **Códigos especiales / no laborables**: **15 códigos**

### Códigos Especiales y de Ausencia
- `L` / `DL`: Descanso semanal / Día libre (0.0 h)
- `V` / `VA`: Vacaciones anuales reglamentarias (0.0 h)
- `C`: Compensatorio por festivo trabajado (0.0 h)
- `J` / `JA`: Libre anual con cargo a exceso de horas (0.0 h)
- `E` / `AH`: Baja médica por Incapacidad Temporal / Ausencia médica (0.0 h)
- `PER` / `PM`: Permiso retribuido / Asuntos propios (0.0 h)
- `FOR`: Jornada de formación interna (8.0 h)
- `SPS`: Sin prestación de servicios / contrato inactivo (0.0 h)
- `TRASLADO`: Prestación de servicios en otro centro/departamento (0.0 h)
- `FES` / `FF`: Festivo de cierre oficial (0.0 h)

---

## 4. Uso en la Aplicación Web

### En el navegador (`index.html`)
El catálogo se encuentra disponible de forma nativa a través de:
```html
<script src="catalogo_turnos_completo.js"></script>
```
Se expone en el objeto global:
```javascript
window.CATALOGO_TURNOS_OFICIAL_2026.codigos["ZG6"]
```
Y nutre automáticamente el objeto `CATALOGO_TURNOS` utilizado por los motores de renderizado y cálculo de coberturas.

### Para scripts y automatizaciones futuras (Node.js / Python)
Cualquier script que necesite comprobar horarios o calcular horas puede importar directamente:
```python
import json

with open("catalogo_turnos_completo.json", "r", encoding="utf-8") as f:
    catalogo = json.load(f)

info = catalogo["codigos"]["ZG6"]
print(f"Turno: {info['codigo']}, Horario: {info['horario']}, Horas: {info['horas_trabajo_efectivo']}")
```
