-- Verificar estado actual
SELECT 
    'Códigos actuales' as descripcion,
    COUNT(*) as total,
    COUNT(DISTINCT partner_id) as clientes,
    COUNT(DISTINCT product_id) as productos
FROM product_customer_code;

-- Ver productos únicos con códigos
SELECT DISTINCT ON (product_id)
    product_id,
    product_code,
    product_name
FROM product_customer_code
WHERE product_code IS NOT NULL
ORDER BY product_id;

-- Ver total de clientes
SELECT COUNT(*) as total_clientes
FROM res_partner
WHERE customer_rank > 0;
