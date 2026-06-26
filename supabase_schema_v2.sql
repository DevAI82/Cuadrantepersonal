-- ============================================================
-- CUADRANTE PERSONAL 2026 — Esquema v2
-- Ejecutar en: Supabase Dashboard → SQL Editor
-- ============================================================

-- 1. SESIONES DE USUARIO
CREATE TABLE IF NOT EXISTS user_sessions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  username TEXT NOT NULL,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  ended_at TIMESTAMPTZ,
  duration_seconds INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(username);
CREATE INDEX IF NOT EXISTS idx_sessions_start ON user_sessions(started_at DESC);

ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Acceso público sessions" ON user_sessions FOR ALL USING (true);

-- 2. CONTROL DE CAMBIOS
CREATE TABLE IF NOT EXISTS change_log (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  username     TEXT        NOT NULL,
  changed_at   TIMESTAMPTZ DEFAULT NOW(),
  department   TEXT        NOT NULL,
  employee     TEXT        NOT NULL,
  date         DATE        NOT NULL,
  old_value    TEXT,
  new_value    TEXT,
  change_type  TEXT        -- 'turno', 'vacaciones', 'libre', 'baja', etc.
);

CREATE INDEX IF NOT EXISTS idx_changelog_user ON change_log(username);
CREATE INDEX IF NOT EXISTS idx_changelog_date ON change_log(changed_at DESC);
CREATE INDEX IF NOT EXISTS idx_changelog_emp  ON change_log(employee);

ALTER TABLE change_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Acceso público change_log" ON change_log FOR ALL USING (true);

-- Activar Realtime en change_log (opcional, para ver cambios en vivo)
ALTER PUBLICATION supabase_realtime ADD TABLE change_log;
ALTER PUBLICATION supabase_realtime ADD TABLE user_sessions;
