-- Script SQL para habilitar todos los productos para todos los clientes
-- Esto crea registros en product_customer_code para todas las combinaciones

-- Primero, crear una tabla temporal con los productos únicos y sus códigos
WITH unique_products AS (
    SELECT DISTINCT ON (product_id)
        product_id,
        product_code,
        product_name
    FROM product_customer_code
    WHERE product_code IS NOT NULL
),
-- Obtener todos los clientes
all_customers AS (
    SELECT id as partner_id
    FROM res_partner
    WHERE customer_rank > 0
)
-- Insertar todas las combinaciones que no existan
INSERT INTO product_customer_code (partner_id, product_id, product_code, product_name, create_uid, create_date, write_uid, write_date)
SELECT 
    c.partner_id,
    p.product_id,
    p.product_code,
    p.product_name,
    1 as create_uid,
    NOW() as create_date,
    1 as write_uid,
    NOW() as write_date
FROM all_customers c
CROSS JOIN unique_products p
WHERE NOT EXISTS (
    SELECT 1 
    FROM product_customer_code pcc 
    WHERE pcc.partner_id = c.partner_id 
    AND pcc.product_id = p.product_id
);

-- Mostrar resumen
SELECT 
    COUNT(*) as total_registros,
    COUNT(DISTINCT partner_id) as total_clientes,
    COUNT(DISTINCT product_id) as total_productos
FROM product_customer_code;
