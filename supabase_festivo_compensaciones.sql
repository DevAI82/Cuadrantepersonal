-- ============================================================
-- CUADRANTE PERSONAL 2026 — Vinculación Festivo Trabajado <-> Día Compensado
-- Ejecutar en: Supabase Dashboard → SQL Editor
-- ============================================================

CREATE TABLE IF NOT EXISTS festivo_compensaciones (
  id           UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
  comp_key     TEXT        UNIQUE NOT NULL, -- formato: 'dept|empIdx|YYYY-MM-DD' (fecha del día C)
  employee_id  UUID        REFERENCES employees(id) ON DELETE CASCADE,
  department   TEXT        NOT NULL,
  comp_date    DATE        NOT NULL,        -- Fecha en que el trabajador libra (código C)
  festivo_date DATE        NOT NULL,        -- Fecha del festivo de apertura que genera la compensación
  updated_by   TEXT        DEFAULT 'usuario',
  updated_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_festivo_comp_key ON festivo_compensaciones(comp_key);
CREATE INDEX IF NOT EXISTS idx_festivo_comp_emp ON festivo_compensaciones(employee_id);
CREATE INDEX IF NOT EXISTS idx_festivo_comp_date ON festivo_compensaciones(comp_date);

ALTER TABLE festivo_compensaciones ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Acceso público festivo_compensaciones" ON festivo_compensaciones FOR ALL USING (true);

ALTER PUBLICATION supabase_realtime ADD TABLE festivo_compensaciones;
