"""
exportar_backup_supabase.py
===========================
Descarga una copia de seguridad integral desde Supabase y la guarda en la carpeta 'backups/'.
USO: python exportar_backup_supabase.py
"""
import urllib.request, json, os
from datetime import datetime

SUPABASE_URL = "https://unrpssxvivjhehamkfoe.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVucnBzc3h2aXZqaGVoYW1rZm9lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAxMjI3MzAsImV4cCI6MjA5NTY5ODczMH0.xV8YS4uLxE3WDCjO2TNRxSfRgUUBczYzS0X0Z1F3Ufg"

def supa_get(endpoint):
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/{endpoint}",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def fetch_all_shifts():
    all_shifts = []
    limit = 1000
    offset = 0
    while True:
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/shifts?select=employee_id,date,shift_code&order=date.asc&limit={limit}&offset={offset}",
            headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if not data: break
            all_shifts.extend(data)
            print(f"  Cargando turnos: {len(all_shifts)} registros...")
            if len(data) < limit: break
            offset += limit
    return all_shifts

def main():
    print("Iniciando copia de seguridad desde Supabase...")
    emps = supa_get("employees?select=id,department_id,name,sort_order&order=department_id,sort_order")
    print(f"  Empleados recuperados: {len(emps)}")
    
    shifts = fetch_all_shifts()
    print(f"  Turnos recuperados: {len(shifts)}")

    try:
        custom_hours_data = supa_get("custom_hours?select=hour_key,time_in,time_out,break_min")
        custom_hours = {r["hour_key"]: {"in": r["time_in"], "out": r["time_out"], "break": r["break_min"]} for r in custom_hours_data}
    except Exception:
        custom_hours = {}

    try:
        comp_data = supa_get("festivo_compensaciones?select=comp_key,festivo_date")
        festivo_comp = {r["comp_key"]: r["festivo_date"] for r in comp_data}
    except Exception:
        festivo_comp = {}

    # Construir estructura DEPTS
    emp_map = {} # emp_id -> (dept, idx)
    depts = {}
    for e in emps:
        d = e["department_id"]
        depts.setdefault(d, {"employees": [], "raw": {}})
        idx = len(depts[d]["employees"])
        depts[d]["employees"].append(e["name"])
        emp_map[e["id"]] = (d, idx)

    for s in shifts:
        if s["employee_id"] not in emp_map: continue
        d, idx = emp_map[s["employee_id"]]
        dt = s["date"]
        if dt not in depts[d]["raw"]:
            depts[d]["raw"][dt] = ["0"] * len(depts[d]["employees"])
        while len(depts[d]["raw"][dt]) <= idx:
            depts[d]["raw"][dt].append("0")
        depts[d]["raw"][dt][idx] = s["shift_code"]

    now = datetime.now()
    backup = {
        "metadata": {
            "tipo": "COPIA_SEGURIDAD_CUADRANTE_2026",
            "fecha_backup": now.isoformat(),
            "version_app": "v2026.09.19-v13",
            "generado_por": "python_backup_cli",
            "total_empleados": len(emps),
            "total_turnos": len(shifts),
            "total_horarios_personalizados": len(custom_hours),
            "total_festivos_compensados": len(festivo_comp)
        },
        "departamentos": depts,
        "custom_hours": custom_hours,
        "festivo_compensaciones": festivo_comp
    }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    backups_dir = os.path.join(script_dir, "backups")
    os.makedirs(backups_dir, exist_ok=True)
    filename = os.path.join(backups_dir, f"Cuadrante_2026_Backup_{now.strftime('%Y-%m-%d_%H%M')}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(backup, f, ensure_ascii=False, indent=2)

    print(f"Copia de seguridad guardada con exito en: {filename}")

if __name__ == "__main__":
    main()
