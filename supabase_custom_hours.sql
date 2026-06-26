-- ============================================================
-- CUADRANTE PERSONAL 2026 — Horarios personalizados persistentes
-- Ejecutar en: Supabase Dashboard → SQL Editor
-- ============================================================

-- Tabla para horarios personalizados de jornada
-- Reemplaza el almacenamiento en localStorage por persistencia real en BD
CREATE TABLE IF NOT EXISTS custom_hours (
  id          UUID    DEFAULT gen_random_uuid() PRIMARY KEY,
  hour_key    TEXT    UNIQUE NOT NULL,   -- formato: 'dept|empIdx|YYYY-MM-DD'
  time_in     TEXT    NOT NULL,          -- ej: '07:10'
  time_out    TEXT    NOT NULL,          -- ej: '15:30'
  break_min   INTEGER DEFAULT 30,        -- minutos de descanso
  updated_by  TEXT,
  updated_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_custom_hours_key ON custom_hours(hour_key);

ALTER TABLE custom_hours ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Acceso público custom_hours" ON custom_hours FOR ALL USING (true);

-- Activar Realtime para sincronización instantánea entre usuarios
ALTER PUBLICATION supabase_realtime ADD TABLE custom_hours;
