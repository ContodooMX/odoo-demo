-- Script SQL para Validación de REP Multi-Factura
-- Ejecutar en PostgreSQL para verificar vinculación de facturas

-- ============================================================================
-- CONSULTA 1: Ver facturas vinculadas a un REP específico
-- ============================================================================
-- Reemplazar '[REP_UUID]' con el UUID del REP a validar
-- Ejemplo: '06397D69-B74D-4407-BF72-617CECFE73D4'

SELECT 
    d.id as documento_id,
    d.state as estado_documento,
    d.attachment_uuid as rep_uuid,
    COUNT(r.invoice_id) as total_facturas_vinculadas,
    STRING_AGG(m.name, ', ') as facturas,
    STRING_AGG(m.l10n_mx_edi_cfdi_uuid, ', ') as facturas_uuids,
    SUM(m.amount_total) as total_facturas,
    SUM(m.amount_residual) as saldo_pendiente
FROM l10n_mx_edi_document d
LEFT JOIN l10n_mx_edi_invoice_document_ids_rel r ON r.document_id = d.id
LEFT JOIN account_move m ON m.id = r.invoice_id
WHERE d.attachment_uuid = '[REP_UUID]'
GROUP BY d.id, d.state, d.attachment_uuid;

-- Resultado esperado para REP con 2 facturas:
-- total_facturas_vinculadas = 2
-- saldo_pendiente = 0.00


-- ============================================================================
-- CONSULTA 2: Detalle de cada factura vinculada
-- ============================================================================

SELECT 
    d.id as documento_id,
    d.attachment_uuid as rep_uuid,
    m.name as factura,
    m.l10n_mx_edi_cfdi_uuid as factura_uuid,
    m.amount_total as monto_factura,
    m.amount_residual as saldo_pendiente,
    m.state as estado_factura,
    CASE 
        WHEN m.amount_residual = 0 THEN '✅ Pagada'
        ELSE '❌ Con saldo'
    END as status_pago
FROM l10n_mx_edi_document d
JOIN l10n_mx_edi_invoice_document_ids_rel r ON r.document_id = d.id
JOIN account_move m ON m.id = r.invoice_id
WHERE d.attachment_uuid = '[REP_UUID]'
ORDER BY m.name;

-- Resultado esperado:
-- Cada fila = una factura vinculada
-- status_pago = '✅ Pagada' para todas


-- ============================================================================
-- CONSULTA 3: Verificar que NO haya duplicados
-- ============================================================================

SELECT 
    d.attachment_uuid as rep_uuid,
    m.l10n_mx_edi_cfdi_uuid as factura_uuid,
    COUNT(*) as veces_vinculada
FROM l10n_mx_edi_document d
JOIN l10n_mx_edi_invoice_document_ids_rel r ON r.document_id = d.id
JOIN account_move m ON m.id = r.invoice_id
WHERE d.attachment_uuid = '[REP_UUID]'
GROUP BY d.attachment_uuid, m.l10n_mx_edi_cfdi_uuid
HAVING COUNT(*) > 1;

-- Resultado esperado: 0 filas (sin duplicados)


-- ============================================================================
-- CONSULTA 4: Buscar facturas por UUID (para validar existencia)
-- ============================================================================

SELECT 
    id,
    name as factura,
    l10n_mx_edi_cfdi_uuid as uuid,
    amount_total,
    amount_residual,
    state,
    company_id
FROM account_move
WHERE l10n_mx_edi_cfdi_uuid IN (
    '7CFA835C-1CFF-4DA7-B5BC-9E2854209F0F',
    'C5863DB6-B06E-4DD3-99B9-253B424399BF'
)
ORDER BY name;

-- Resultado esperado: 2 filas (las facturas existen)


-- ============================================================================
-- CONSULTA 5: Ver todos los documentos de pago recientes
-- ============================================================================

SELECT 
    d.id,
    d.state,
    d.attachment_uuid,
    d.datetime,
    COUNT(r.invoice_id) as facturas_vinculadas
FROM l10n_mx_edi_document d
LEFT JOIN l10n_mx_edi_invoice_document_ids_rel r ON r.document_id = d.id
WHERE d.state IN ('payment_sent', 'payment_received')
  AND d.datetime >= NOW() - INTERVAL '7 days'
GROUP BY d.id, d.state, d.attachment_uuid, d.datetime
ORDER BY d.datetime DESC
LIMIT 10;

-- Muestra los últimos 10 documentos de pago


-- ============================================================================
-- CONSULTA 6: Comparar montos (REP vs Facturas)
-- ============================================================================

WITH rep_data AS (
    SELECT 
        d.id as doc_id,
        d.attachment_uuid,
        SUM(m.amount_total) as total_facturas
    FROM l10n_mx_edi_document d
    JOIN l10n_mx_edi_invoice_document_ids_rel r ON r.document_id = d.id
    JOIN account_move m ON m.id = r.invoice_id
    WHERE d.attachment_uuid = '[REP_UUID]'
    GROUP BY d.id, d.attachment_uuid
)
SELECT 
    attachment_uuid as rep_uuid,
    total_facturas,
    CASE 
        WHEN total_facturas = 69138.78 THEN '✅ Correcto'
        ELSE '❌ Incorrecto'
    END as validacion_monto
FROM rep_data;

-- Para el caso del usuario:
-- total_facturas debe ser 69138.78
-- validacion_monto = '✅ Correcto'


-- ============================================================================
-- INSTRUCCIONES DE USO
-- ============================================================================

/*
1. Conectarse a la base de datos de Odoo:
   psql -U odoo -d nombre_base_datos

2. Reemplazar '[REP_UUID]' con el UUID real del REP

3. Ejecutar las consultas una por una

4. Documentar los resultados en reporte_validacion.md

5. Ejemplos de UUIDs para pruebas:
   - REP Usuario: 06397D69-B74D-4407-BF72-617CECFE73D4
   - Factura 1: 7CFA835C-1CFF-4DA7-B5BC-9E2854209F0F
   - Factura 2: C5863DB6-B06E-4DD3-99B9-253B424399BF
*/
