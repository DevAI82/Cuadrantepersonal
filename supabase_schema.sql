-- ============================================================
-- CUADRANTE PERSONAL 2026 — Esquema Supabase
-- Ejecutar en: Supabase Dashboard → SQL Editor
-- ============================================================

-- 1. DEPARTAMENTOS
CREATE TABLE IF NOT EXISTS departments (
  id TEXT PRIMARY KEY,           -- 'operaciones', 'omnicanal', 'cajasac', 'muelle'
  label TEXT NOT NULL,           -- Nombre para mostrar en la UI
  sort_order INTEGER NOT NULL DEFAULT 0
);

-- 2. EMPLEADOS
CREATE TABLE IF NOT EXISTS employees (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  department_id TEXT NOT NULL REFERENCES departments(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  sort_order INTEGER NOT NULL DEFAULT 0,
  UNIQUE(department_id, name)
);

-- 3. TURNOS (una fila por empleado+fecha)
CREATE TABLE IF NOT EXISTS shifts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  shift_code TEXT NOT NULL DEFAULT '0',   -- 'M(AM)', 'T(TC)', 'L', 'VAC', '0', etc.
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  updated_by TEXT DEFAULT 'sistema',
  UNIQUE(employee_id, date)
);

-- Índice para consultas rápidas por fecha
CREATE INDEX IF NOT EXISTS idx_shifts_date ON shifts(date);
CREATE INDEX IF NOT EXISTS idx_shifts_employee ON shifts(employee_id);

-- ============================================================
-- REALTIME: activar para la tabla shifts
-- ============================================================
ALTER PUBLICATION supabase_realtime ADD TABLE shifts;

-- ============================================================
-- ROW LEVEL SECURITY (RLS)
-- Política simple: todos pueden leer y escribir (sin auth)
-- Si en el futuro quieres añadir autenticación, modifica aquí
-- ============================================================
ALTER TABLE departments ENABLE ROW LEVEL SECURITY;
ALTER TABLE employees ENABLE ROW LEVEL SECURITY;
ALTER TABLE shifts ENABLE ROW LEVEL SECURITY;

-- Lectura pública
CREATE POLICY "Lectura pública departments" ON departments FOR SELECT USING (true);
CREATE POLICY "Lectura pública employees"   ON employees   FOR SELECT USING (true);
CREATE POLICY "Lectura pública shifts"      ON shifts      FOR SELECT USING (true);

-- Escritura pública (cualquiera puede editar)
CREATE POLICY "Escritura pública shifts"    ON shifts      FOR ALL    USING (true);

-- ============================================================
-- DATOS INICIALES — Departamentos
-- ============================================================
INSERT INTO departments (id, label, sort_order) VALUES
  ('operaciones', 'Operaciones',  1),
  ('omnicanal',   'Omnicanal',    2),
  ('cajasac',     'Caja / SAC',   3),
  ('muelle',      'Muelle',       4)
ON CONFLICT (id) DO NOTHING;
