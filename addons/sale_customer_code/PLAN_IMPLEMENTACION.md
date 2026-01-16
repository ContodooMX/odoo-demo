# Habilitar Códigos de Producto Genéricos

## Descripción del Objetivo
Permitir el registro de códigos de producto "genéricos" que se apliquen a todos los clientes cuando no esté definido un código específico de cliente-producto. Esto optimiza la entrada de datos al eliminar la necesidad de registrar el mismo código para cada cliente.

## Revisión del Usuario Requerida
> [!IMPORTANT]
> - El campo `partner_id` en `product.customer.code` ya no será obligatorio (`required=False`).
> - Se agregará una nueva restricción de Python para evitar múltiples códigos genéricos para el mismo producto, ya que la restricción única de SQL permite múltiples valores NULL.

## Cambios Propuestos

### `addons/sale_customer_code`

#### [MODIFICAR] [product_customer_code.py](file:///c:/Users/alber/PycharmProjects/odoo19/addons/sale_customer_code/models/product_customer_code.py)
- Cambiar el atributo `required` del campo `partner_id` a `False`.
- Agregar `@api.constrains('partner_id', 'product_id')` para forzar la unicidad de registros genéricos (donde `partner_id` es False).

#### [MODIFICAR] [sale_order_line.py](file:///c:/Users/alber/PycharmProjects/odoo19/addons/sale_customer_code/models/sale_order_line.py)
- Actualizar `_compute_customer_product_code` y `_onchange_product_id_customer_code`.
- Actualización de la lógica:
    1. Intentar encontrar un código específico para el `order_id.partner_id`.
    2. Si no se encuentra, intentar encontrar un código genérico (donde `partner_id` es False).
    3. Usar el código encontrado o establecerlo en False.

## Plan de Verificación

### Pruebas Automatizadas
- Crear un script de reproducción `reproduce_issue.py` (o similar) usando `odoo-bin shell` para:
    1. Crear un producto "Manzana".
    2. Crear un código genérico "manzanarroja" (partner_id=False).
    3. Crear un código específico "manzanaverde" para el Partner "Cliente Especial".
    4. Simular `onchange` o `compute` para una nueva orden con un "partner aleatorio". Se espera "manzanarroja".
    5. Simular `onchange` o `compute` para "Cliente Especial". Se espera "manzanaverde".

### Verificación Manual
1. Abrir Odoo.
2. Ir a Ventas -> Configuración -> Códigos de Producto por Cliente.
3. Crear un registro: Producto "Test", Código "GENERICO", Cliente vacío.
4. Crear un registro: Producto "Test", Código "ESPECIFICO", Cliente "Azure Interior".
5. Crear una Cotización para "Gemini Furniture" (aleatorio). Agregar "Test". Verificar Código -> Debería ser "GENERICO".
6. Crear una Cotización para "Azure Interior". Agregar "Test". Verificar Código -> Debería ser "ESPECIFICO".
