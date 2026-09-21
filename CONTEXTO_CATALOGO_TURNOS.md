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
- `J`: Libre anual por exceso de horas del **año en curso** (0.0 h; **equivalente a un día libre ordinario del año en curso, computa como 0 horas**)
- `JA`: Libre anual con cargo a horas debidas del **año anterior** (presencia física: 0.0 h; **para el cómputo y balance anual de horas SÍ se suman a la jornada**)
- `E` / `AH`: Baja médica por Incapacidad Temporal / Ausencia médica (0.0 h)

### Regla Canónica de Cómputo: Distinción entre Códigos JA y J
1. **Código `J` (Exceso del Año en Curso)**:
   - Supone una libranza concedida por horas de exceso generadas dentro del **año en curso (2026)**.
   - Es **estrictamente equivalente a un día libre (`L`) del año en curso** y computa como **0,0 horas trabajadas**.
2. **Código `JA` (Horas Debidas del Año Anterior)**:
   - Supone horas debidas por exceso de jornada generado en el **ejercicio anterior (2025)** que el trabajador disfruta durante el año en curso.
   - **En tienda / presencia física**: El empleado no asiste (0,0 h de presencia física en cuadrante diario).
   - **En el cómputo y balance anual de horas (exceso / déficit)**: **SÍ se suman a las horas del año en curso**, valorándose según la jornada diaria habitual de cada trabajador (obtenida de `HORARIOS_DEF`, `OPER_H` o turno predominante; por ejemplo, 7,25 h en turno `T3J`, 8,0 h en `ZTV`, o media contractual). Esto garantiza que el exceso real de jornada quede fielmente reflejado sin distorsiones.
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

---

## 5. Caso Específico y Auditoría Oficial: Carlos Lapeña Carnicero

- **Empleado**: 66108861 - CARLOS LAPEÑA CARNICERO (Operaciones)
- **Jornada Teórica Contractual Oficial (RH / Nexo)**: **1.693,33 horas** (1.693 h 20 min) debido a la reducción de jornada aplicada.
- **Días de presencia programados en 2026**: 248 días.
- **Horas de presencia efectiva**:
  - Calendario a 14.09: **1.709,12 horas** (1.709 h 7 min).
  - Calendario actualizado a 21.09: **1.709,87 horas** (1.709 h 52 min, tras el ajuste de septiembre: 8 días pasan de V5J a T3J +2h y el 17/09 pasa de T3J a V7U -1,25h).
- **Cómputo de Días JA (Horas debidas de 2025 disfrutadas en 2026)**:
  - 3 días: 5, 6 y 25 de marzo.
  - Valorados a su turno habitual T3J (7,25 h): $3 \times 7,25\text{ h} = \mathbf{+21,75\text{ horas}}$.
- **Cómputo de Días J (Exceso de 2026 disfrutado en 2026)**:
  - 1 día: 7 de marzo $\rightarrow \mathbf{0,0\text{ horas}}$ (día libre ordinario del año en curso).
- **Jornada Anual Proyectada**:
  $$\text{Horas Proyectadas} = 1.709,12\text{ h} + 21,75\text{ h} = \mathbf{1.730,87\text{ horas}}\quad (\approx 1.730,9\text{ h})$$
- **Balance Oficial de Exceso**:
  $$\text{Exceso de Jornada} = 1.730,87\text{ h} - 1.693,33\text{ h} = \mathbf{+37,54\text{ horas}}$$
*(Con la actualización del 21.09, las horas proyectadas ascienden a 1.731,62 h con un exceso de +38,29 h).*

---

## 6. Caso Específico y Auditoría Oficial: Elena Ródenas Cebrián

- **Empleado**: 78714821 - ELENA RÓDENAS CEBRIÁN (Operaciones / Caja)
- **Jornada Teórica Contractual Oficial (RH / Nexo)**: **1.721,00 horas** (equivalente al 97,23% de jornada anual de 1.770 h).
- **Desglose de Horas Presenciales y Proyectadas**:
  - **Horas presenciales computadas en cuadrante base (sin Z)**: $1.628,50\text{ horas}$.
  - **1 día JA (30 de enero)**: $+6,50\text{ horas}$ (horas debidas de 2025 libradas en 2026, turno habitual V7W/VQL de 6,5 h).
  - **12 días laborables con Código Z (Período de transición Caja $\rightarrow$ Operaciones)**:
    - *22 al 30 de abril (8 días laborables en Caja, turno P9D de 6,25 h; domingo 26 libre)*: $8 \times 6,25\text{ h} = \mathbf{+50,00\text{ horas}}$.
    - *1 al 4 de junio (3 días laborables en Operaciones; jueves 4 festivo de cierre Corpus Christi)*: $3 \times 8,833\text{ h} = \mathbf{+26,50\text{ horas}}$.
    - **Total días Z**: $\mathbf{+76,50\text{ horas}}$.
- **Jornada Anual Proyectada Oficial (Nexo)**:
  $$\text{Jornada Proyectada} = 1.628,50\text{ h} + 6,50\text{ h} + 76,50\text{ h} = \mathbf{1.711,50\text{ horas}}\quad (\approx 1.711\text{ h})$$
- **Balance Oficial de Jornada**:
  $$\text{Balance / Diferencia} = 1.711,50\text{ h} - 1.721,00\text{ h} = \mathbf{-9,50\text{ horas}}\quad \text{(le faltan 9,5 h por trabajar)}$$
- **Origen de la Discrepancia Previa en la Aplicación (-57,1 h vs -9,5 h = 47,6 h)**:
  1. **Omisión de los días con turno Z (+76,5 h)**: En la versión inicial de la aplicación, el código `Z` no tenía asignación horaria explícita (`0,0 h`), computando los 12 días laborables como si fueran descansos.
  2. **Divergencia en la Jornada Teórica Contractual (+28,9 h)**: En la app se había estimado provisionalmente una teórica de 1.696,7 h, y además el motor restaba 4,6 h por 1 día de ausencia médica aislada `AH` (13 de abril), situando el máximo exigible en $1.692,1\text{ h}$ frente a los **$1.721,0\text{ h}$** oficiales de Nexo.
  3. **Cuadratura matemática exacta**:
     $$(1.635,0\text{ h} - 1.692,1\text{ h}) = -57,1\text{ h} \quad\text{frente a}\quad (1.711,5\text{ h} - 1.721,0\text{ h}) = -9,5\text{ h}$$
     $$\text{Diferencia explicada} = -9,5\text{ h} - (-57,1\text{ h}) = \mathbf{+47,6\text{ horas}}.$$

