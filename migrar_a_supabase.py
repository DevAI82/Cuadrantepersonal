"""
migrar_a_supabase.py
====================
Extrae los datos del Cuadrante_Personal_2026.html y los carga en Supabase.

USO:
  1. pip install supabase
  2. Rellena SUPABASE_URL y SUPABASE_KEY con tus credenciales
  3. Asegúrate de haber ejecutado supabase_schema.sql primero
  4. Ejecuta: python migrar_a_supabase.py
"""

import re, json, sys
from pathlib import Path

# ─── CONFIGURACIÓN ───────────────────────────────────────────────────────────
SUPABASE_URL = "https://unrpssxvivjhehamkfoe.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVucnBzc3h2aXZqaGVoYW1rZm9lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAxMjI3MzAsImV4cCI6MjA5NTY5ODczMH0.xV8YS4uLxE3WDCjO2TNRxSfRgUUBczYzS0X0Z1F3Ufg"

HTML_PATH = Path(__file__).parent / "Cuadrante_Personal_2026.html"
BATCH_SIZE = 500   # registros por lote al insertar
# ─────────────────────────────────────────────────────────────────────────────

def parse_html(path: Path) -> dict:
    """Extrae el objeto DEPTS del HTML."""
    content = path.read_text(encoding="utf-8")
    idx_start = content.find("const DEPTS = {")
    idx_end   = content.find("\nconst ", idx_start + 10)
    depts_js  = content[idx_start + len("const DEPTS = "):idx_end].strip().rstrip(";")

    # Convertir claves JS no entrecomilladas a JSON válido
    depts_json = re.sub(r'(?<!["\w])(\b[a-zA-Z_]\w*\b)\s*:', r'"\1":', depts_js)
    return json.loads(depts_json)


def build_records(data: dict) -> tuple[list, list, list]:
    """Construye las listas de employees y shifts a insertar."""
    DEPT_ORDER = {"operaciones": 1, "omnicanal": 2, "cajasac": 3, "muelle": 4}

    employees = []
    emp_index = {}  # (dept, name) -> sort_order
    shifts_raw = []  # (dept, emp_name, date, shift_code)

    for dept, info in data.items():
        for i, name in enumerate(info["employees"]):
            employees.append({
                "department_id": dept,
                "name": name,
                "sort_order": i
            })
            emp_index[(dept, name)] = i

        for date_str, codes in info["raw"].items():
            for emp_i, code in enumerate(codes):
                emp_name = info["employees"][emp_i]
                shifts_raw.append((dept, emp_name, date_str, code))

    return employees, shifts_raw


def chunked(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


def main():
    print("⏳ Cargando datos del HTML...")
    data = parse_html(HTML_PATH)
    employees, shifts_raw = build_records(data)
    print(f"   → {len(employees)} empleados, {len(shifts_raw)} turnos")

    # Importar supabase aquí para que el error sea claro
    try:
        from supabase import create_client
    except ImportError:
        print("\n❌ Falta la librería: pip install supabase")
        sys.exit(1)

    if "XXXXXXXX" in SUPABASE_URL:
        print("\n❌ Rellena SUPABASE_URL y SUPABASE_KEY en el script antes de ejecutar.")
        sys.exit(1)

    print(f"\n🔗 Conectando a {SUPABASE_URL}...")
    sb = create_client(SUPABASE_URL, SUPABASE_KEY)

    # ── Insertar empleados ──────────────────────────────────────────────────
    print("📥 Insertando empleados...")
    for batch in chunked(employees, BATCH_SIZE):
        sb.table("employees").upsert(batch, on_conflict="department_id,name").execute()
    print(f"   ✅ {len(employees)} empleados cargados")

    # ── Recuperar IDs de empleados ──────────────────────────────────────────
    print("🔍 Recuperando IDs de empleados...")
    resp = sb.table("employees").select("id, department_id, name").execute()
    emp_id_map = {(r["department_id"], r["name"]): r["id"] for r in resp.data}

    # ── Insertar turnos ─────────────────────────────────────────────────────
    print("📥 Insertando turnos (puede tardar ~1 minuto)...")
    shift_records = [
        {
            "employee_id": emp_id_map[(dept, name)],
            "date": date_str,
            "shift_code": code,
            "updated_by": "migracion_inicial"
        }
        for dept, name, date_str, code in shifts_raw
        if (dept, name) in emp_id_map
    ]

    total = len(shift_records)
    for i, batch in enumerate(chunked(shift_records, BATCH_SIZE)):
        sb.table("shifts").upsert(batch, on_conflict="employee_id,date").execute()
        pct = min(100, int((i + 1) * BATCH_SIZE / total * 100))
        print(f"   {pct}% ({min((i+1)*BATCH_SIZE, total)}/{total})", end="\r")

    print(f"\n   ✅ {total} turnos cargados")
    print("\n🎉 ¡Migración completada con éxito!")
    print("   Ya puedes abrir el HTML conectado a Supabase.")


if __name__ == "__main__":
    main()
