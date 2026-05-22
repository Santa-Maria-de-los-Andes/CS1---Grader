-- =============================================================
-- PYTHON QUEST — Supabase Schema
-- Ejecuta este script en el SQL Editor de tu proyecto Supabase
-- =============================================================

-- ── submissions: historial completo de intentos ──────────────
CREATE TABLE IF NOT EXISTS public.submissions (
  id               uuid        DEFAULT gen_random_uuid() PRIMARY KEY,
  email            text        NOT NULL DEFAULT '',
  dni              text,
  nombre           text,
  grado            text,
  notebook         text        NOT NULL DEFAULT 'nb1',
  earned           integer     NOT NULL,
  possible         integer     NOT NULL,
  pct              integer     NOT NULL,
  level_num        integer     NOT NULL,
  level_name       text        NOT NULL,
  achievements     text[]      DEFAULT '{}',
  streak           integer     DEFAULT 0,
  score_breakdown  jsonb       DEFAULT '{}',
  submitted_at     timestamptz DEFAULT now()
);

-- Si la tabla ya existe, agrega las nuevas columnas:
ALTER TABLE public.submissions ADD COLUMN IF NOT EXISTS dni    text;
ALTER TABLE public.submissions ADD COLUMN IF NOT EXISTS nombre text;
ALTER TABLE public.submissions ADD COLUMN IF NOT EXISTS grado  text;
ALTER TABLE public.submissions ALTER COLUMN email SET DEFAULT '';

-- Indice para consultas del leaderboard por DNI
CREATE INDEX IF NOT EXISTS idx_submissions_dni_pct
  ON public.submissions (dni, pct DESC, submitted_at DESC);

-- ── Row Level Security ───────────────────────────────────────
ALTER TABLE public.submissions ENABLE ROW LEVEL SECURITY;

-- Anon puede INSERT (autograder de los alumnos)
CREATE POLICY "anon_insert" ON public.submissions
  FOR INSERT TO anon
  WITH CHECK (true);

-- Anon puede SELECT (leaderboard publico en GitHub Pages)
CREATE POLICY "anon_select" ON public.submissions
  FOR SELECT TO anon
  USING (true);

-- Nota: si quieres restringir lecturas individuales, elimina la
-- politica anon_select y crea en su lugar una funcion
-- SECURITY DEFINER que devuelva solo los mejores por email.

-- ── students: vincula email con nombre real y grado ──────────
-- Llena esta tabla manualmente o con un CSV import
CREATE TABLE IF NOT EXISTS public.students (
  email       text PRIMARY KEY,
  full_name   text,
  grade       text,   -- ej: "3ro A", "4to B"
  created_at  timestamptz DEFAULT now()
);

ALTER TABLE public.students ENABLE ROW LEVEL SECURITY;

-- Solo el service_role (admin) puede leer/escribir students
-- anon NO tiene acceso

-- ── Consulta rapida: mejor puntaje por alumno ────────────────
-- Ejecuta esto en el SQL Editor para ver el leaderboard actual:
--
-- SELECT DISTINCT ON (s.email)
--   s.email,
--   st.full_name,
--   st.grade,
--   s.pct,
--   s.earned,
--   s.possible,
--   s.level_name,
--   array_length(s.achievements, 1) AS num_logros,
--   s.streak,
--   s.submitted_at
-- FROM public.submissions s
-- LEFT JOIN public.students st ON st.email = s.email
-- ORDER BY s.email, s.pct DESC, s.submitted_at DESC
-- ORDER BY pct DESC;
