-- ============================================================
-- SCRIPT DE INICIALIZACIÓN: CRUD Didáctico con Supabase
-- Proyecto: app_prueba_prompts
-- Fecha: 2025-12-23
-- ============================================================
-- 
-- INSTRUCCIONES DE USO:
-- 1. Ir a Supabase Dashboard > SQL Editor
-- 2. Crear un "New Query"
-- 3. Pegar todo este contenido
-- 4. Ejecutar con "Run"
--
-- ============================================================

-- ============================================================
-- SECCIÓN 1: LIMPIEZA (Solo para desarrollo/reset)
-- ============================================================
-- ADVERTENCIA: Descomentar solo si quieres borrar todo y empezar de cero
-- DROP TABLE IF EXISTS public.notas CASCADE;
-- DROP FUNCTION IF EXISTS public.handle_updated_at CASCADE;

-- ============================================================
-- SECCIÓN 2: CREAR TABLA NOTAS
-- ============================================================

CREATE TABLE IF NOT EXISTS public.notas (
    -- Clave primaria con UUID autogenerado
    -- POR QUÉ UUID: Evita colisiones en sistemas distribuidos,
    -- no expone cantidad de registros (vs. autoincrement)
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Relación con usuario de Supabase Auth
    -- POR QUÉ CASCADE: Si se elimina el usuario, se eliminan sus notas
    -- (evita huérfanos y cumple con GDPR/derecho al olvido)
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Campos de contenido
    -- POR QUÉ TEXT y no VARCHAR: PostgreSQL trata igual ambos,
    -- TEXT es más flexible y no tiene límite artificial
    title TEXT NOT NULL,
    content TEXT,  -- Nullable: el contenido es opcional
    
    -- Timestamps con zona horaria
    -- POR QUÉ TIMESTAMPTZ: Almacena en UTC, convierte automáticamente
    -- según la zona del cliente (evita bugs de horario)
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Comentario en la tabla para documentación
COMMENT ON TABLE public.notas IS 'Notas personales de usuarios - CRUD didáctico';
COMMENT ON COLUMN public.notas.user_id IS 'FK a auth.users, propietario de la nota';
COMMENT ON COLUMN public.notas.title IS 'Título obligatorio de la nota';
COMMENT ON COLUMN public.notas.content IS 'Contenido opcional de la nota';

-- ============================================================
-- SECCIÓN 3: ÍNDICES PARA OPTIMIZACIÓN
-- ============================================================

-- Índice para búsquedas por usuario (usado por RLS)
-- POR QUÉ: Acelera el filtro WHERE user_id = X que RLS aplica en cada query
CREATE INDEX IF NOT EXISTS idx_notas_user_id 
    ON public.notas(user_id);

-- Índice para ordenamiento por fecha
-- POR QUÉ DESC: Las notas más recientes primero es el caso de uso principal
CREATE INDEX IF NOT EXISTS idx_notas_created_at 
    ON public.notas(created_at DESC);

-- ============================================================
-- SECCIÓN 4: ROW LEVEL SECURITY (RLS) - CRÍTICO
-- ============================================================

-- Habilitar RLS en la tabla
-- POR QUÉ: Sin esto, cualquier usuario autenticado ve TODAS las notas
ALTER TABLE public.notas ENABLE ROW LEVEL SECURITY;

-- Política SELECT: Usuarios solo ven sus propias notas
CREATE POLICY "Users can view own notas" 
    ON public.notas
    FOR SELECT
    USING (auth.uid() = user_id);

-- Política INSERT: Usuarios solo pueden crear notas con su user_id
-- POR QUÉ WITH CHECK: Valida el user_id del nuevo registro
CREATE POLICY "Users can insert own notas" 
    ON public.notas
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Política UPDATE: Usuarios solo pueden editar sus notas
-- POR QUÉ USING + WITH CHECK: 
--   USING valida que la nota existente sea del usuario
--   WITH CHECK valida que no cambie el user_id
CREATE POLICY "Users can update own notas" 
    ON public.notas
    FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Política DELETE: Usuarios solo pueden eliminar sus notas
CREATE POLICY "Users can delete own notas" 
    ON public.notas
    FOR DELETE
    USING (auth.uid() = user_id);

-- ============================================================
-- SECCIÓN 5: TRIGGER PARA UPDATED_AT AUTOMÁTICO
-- ============================================================

-- Función que actualiza updated_at
-- POR QUÉ FUNCTION + TRIGGER: Garantiza que updated_at siempre 
-- refleje la última modificación, sin depender del cliente
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    -- POR QUÉ now(): Usa el timestamp del servidor (confiable)
    -- en lugar del cliente (manipulable)
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que ejecuta la función antes de cada UPDATE
CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON public.notas
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_updated_at();

-- ============================================================
-- SECCIÓN 6: VERIFICACIÓN
-- ============================================================

-- Verificar que la tabla existe
SELECT 
    table_name, 
    (SELECT COUNT(*) FROM public.notas) as row_count
FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name = 'notas';

-- Verificar que RLS está activo
SELECT 
    tablename, 
    rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' AND tablename = 'notas';

-- Listar políticas RLS
SELECT 
    policyname, 
    cmd as operation,
    permissive
FROM pg_policies 
WHERE tablename = 'notas';

-- ============================================================
-- FIN DEL SCRIPT
-- ============================================================
-- 
-- PRÓXIMOS PASOS:
-- 1. Verificar que las 4 políticas aparecen en la salida
-- 2. Ir a Table Editor > notas para ver la tabla
-- 3. Probar insertando un registro desde el dashboard
--    (fallará sin autenticación, eso es correcto por RLS)
--
-- ============================================================
