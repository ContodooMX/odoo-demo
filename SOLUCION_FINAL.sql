-- Script SQL DEFINITIVO para habilitar todos los productos para todos los clientes
-- Ejecutar con: psql -U odoo19user -d odoo19_v16 -f SOLUCION_FINAL.sql

\echo '================================================================================'
\echo 'HABILITANDO TODOS LOS PRODUCTOS PARA TODOS LOS CLIENTES'
\echo '================================================================================'

-- Insertar todas las combinaciones que no existan
INSERT INTO product_customer_code (partner_id, product_id, product_code, product_name, create_uid, create_date, write_uid, write_date)
SELECT 
    c.id as partner_id,
    p.product_id,
    p.product_code,
    p.product_name,
    1 as create_uid,
    NOW() as create_date,
    1 as write_uid,
    NOW() as write_date
FROM 
    res_partner c,
    (SELECT DISTINCT ON (product_id) product_id, product_code, product_name 
     FROM product_customer_code 
     WHERE product_code IS NOT NULL) p
WHERE 
    c.customer_rank > 0
    AND NOT EXISTS (
        SELECT 1 
        FROM product_customer_code pcc 
        WHERE pcc.partner_id = c.id 
        AND pcc.product_id = p.product_id
    );

-- Mostrar resumen
\echo ''
\echo '================================================================================'
\echo 'RESUMEN FINAL:'
\echo '================================================================================'

SELECT 
    COUNT(DISTINCT partner_id) as "Total Clientes",
    COUNT(DISTINCT product_id) as "Total Productos",
    COUNT(*) as "Total Registros"
FROM product_customer_code;

\echo ''
\echo 'COMPLETADO! Todos los clientes ahora tienen acceso a todos los productos.'
\echo ''
