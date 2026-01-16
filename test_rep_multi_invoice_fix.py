#!/usr/bin/env python3
"""
Script de prueba para validar la corrección del bug REP Multi-Facturas.

Este script crea un XML de prueba con múltiples DoctoRelacionado y verifica
que el método _get_payment_cfdi_invoice_uuids extraiga correctamente todos los UUIDs.

Ejecutar desde la carpeta odoo19:
  python test_rep_multi_invoice_fix.py
"""

from lxml import etree

# Simular el método de extracción de UUIDs
def get_payment_cfdi_invoice_uuids(cfdi_data):
    """Extraer todos los UUIDs de factura de un CFDI de pago."""
    if not cfdi_data:
        return []

    try:
        cfdi_node = etree.fromstring(cfdi_data)
    except (etree.XMLSyntaxError, AttributeError):
        return []

    # Extraer TODOS los DoctoRelacionado de TODOS los nodos Pago
    uuids = []
    for docto_node in cfdi_node.xpath("//*[local-name()='DoctoRelacionado']"):
        uuid = docto_node.get('IdDocumento')
        if uuid:
            uuids.append(uuid.upper())  # Normalizar a mayúsculas

    return uuids


# XML de prueba: REP con múltiples nodos Pago (estructura C&Z)
TEST_XML_MULTIPLE_PAGO = b"""<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" xmlns:pago20="http://www.sat.gob.mx/Pagos20" TipoDeComprobante="P">
    <cfdi:Complemento>
        <pago20:Pagos>
            <pago20:Totales MontoTotalPagos="69138.78"/>
            <pago20:Pago FechaPago="2025-03-14T12:00:00" Monto="40030.85">
                <pago20:DoctoRelacionado IdDocumento="7CFA835C-1CFF-4DA7-B5BC-9E2854209F0F" ImpPagado="40030.85" ImpSaldoInsoluto="0.00"/>
            </pago20:Pago>
            <pago20:Pago FechaPago="2025-03-14T12:00:00" Monto="29107.93">
                <pago20:DoctoRelacionado IdDocumento="C5863DB6-B06E-4DD3-99B9-253B424399BF" ImpPagado="29107.93" ImpSaldoInsoluto="0.00"/>
            </pago20:Pago>
        </pago20:Pagos>
    </cfdi:Complemento>
</cfdi:Comprobante>
"""

# XML de prueba: REP con un solo Pago y múltiples DoctoRelacionado (estructura alternativa)
TEST_XML_SINGLE_PAGO = b"""<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" xmlns:pago20="http://www.sat.gob.mx/Pagos20" TipoDeComprobante="P">
    <cfdi:Complemento>
        <pago20:Pagos>
            <pago20:Totales MontoTotalPagos="69138.78"/>
            <pago20:Pago FechaPago="2025-03-14T12:00:00" Monto="69138.78">
                <pago20:DoctoRelacionado IdDocumento="7cfa835c-1cff-4da7-b5bc-9e2854209f0f" ImpPagado="40030.85" ImpSaldoInsoluto="0.00"/>
                <pago20:DoctoRelacionado IdDocumento="c5863db6-b06e-4dd3-99b9-253b424399bf" ImpPagado="29107.93" ImpSaldoInsoluto="0.00"/>
            </pago20:Pago>
        </pago20:Pagos>
    </cfdi:Complemento>
</cfdi:Comprobante>
"""

# XML de prueba: REP con una sola factura
TEST_XML_SINGLE_INVOICE = b"""<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" xmlns:pago20="http://www.sat.gob.mx/Pagos20" TipoDeComprobante="P">
    <cfdi:Complemento>
        <pago20:Pagos>
            <pago20:Totales MontoTotalPagos="40030.85"/>
            <pago20:Pago FechaPago="2025-03-14T12:00:00" Monto="40030.85">
                <pago20:DoctoRelacionado IdDocumento="7CFA835C-1CFF-4DA7-B5BC-9E2854209F0F" ImpPagado="40030.85" ImpSaldoInsoluto="0.00"/>
            </pago20:Pago>
        </pago20:Pagos>
    </cfdi:Complemento>
</cfdi:Comprobante>
"""


def test_uuid_extraction():
    """Probar extracción de UUIDs de diferentes estructuras XML."""
    print("=" * 70)
    print("PRUEBA DE EXTRACCIÓN DE UUIDS - REP MULTI-FACTURAS")
    print("=" * 70)
    
    # Test 1: Múltiples nodos Pago
    print("\n[Test 1] REP con múltiples nodos <pago20:Pago>:")
    uuids = get_payment_cfdi_invoice_uuids(TEST_XML_MULTIPLE_PAGO)
    print(f"  UUIDs extraídos: {len(uuids)}")
    for uuid in uuids:
        print(f"    - {uuid}")
    assert len(uuids) == 2, f"ERROR: Se esperaban 2 UUIDs, se obtuvieron {len(uuids)}"
    print("  ✅ PASÓ - Extraídos 2 UUIDs correctamente")
    
    # Test 2: Un solo nodo Pago con múltiples DoctoRelacionado
    print("\n[Test 2] REP con un <pago20:Pago> y múltiples <DoctoRelacionado>:")
    uuids = get_payment_cfdi_invoice_uuids(TEST_XML_SINGLE_PAGO)
    print(f"  UUIDs extraídos: {len(uuids)}")
    for uuid in uuids:
        print(f"    - {uuid}")
    assert len(uuids) == 2, f"ERROR: Se esperaban 2 UUIDs, se obtuvieron {len(uuids)}"
    print("  ✅ PASÓ - Extraídos 2 UUIDs correctamente")
    
    # Test 3: Una sola factura
    print("\n[Test 3] REP con una sola factura:")
    uuids = get_payment_cfdi_invoice_uuids(TEST_XML_SINGLE_INVOICE)
    print(f"  UUIDs extraídos: {len(uuids)}")
    for uuid in uuids:
        print(f"    - {uuid}")
    assert len(uuids) == 1, f"ERROR: Se esperaba 1 UUID, se obtuvieron {len(uuids)}"
    print("  ✅ PASÓ - Extraído 1 UUID correctamente")
    
    # Test 4: Normalización a mayúsculas
    print("\n[Test 4] Prueba de normalización a mayúsculas:")
    uuids = get_payment_cfdi_invoice_uuids(TEST_XML_SINGLE_PAGO)
    all_uppercase = all(uuid == uuid.upper() for uuid in uuids)
    print(f"  Todos los UUIDs en mayúsculas: {all_uppercase}")
    assert all_uppercase, "ERROR: Los UUIDs no se normalizaron a mayúsculas"
    print("  ✅ PASÓ - UUIDs normalizados a mayúsculas")
    
    print("\n" + "=" * 70)
    print("TODOS LOS TESTS PASARON ✅")
    print("=" * 70)


def test_case_insensitive_search():
    """Simular búsqueda case-insensitive en base de datos."""
    print("\n" + "=" * 70)
    print("PRUEBA DE BÚSQUEDA CASE-INSENSITIVE")
    print("=" * 70)
    
    # Simular UUIDs en base de datos (algunos en minúsculas)
    db_invoices = {
        '7cfa835c-1cff-4da7-b5bc-9e2854209f0f': 'Factura CZ-1693',
        'C5863DB6-B06E-4DD3-99B9-253B424399BF': 'Factura CZ-1694',
    }
    
    # Extraer UUIDs del REP
    uuids = get_payment_cfdi_invoice_uuids(TEST_XML_MULTIPLE_PAGO)
    print(f"\nUUIDs en el REP (normalizados a mayúsculas):")
    for uuid in uuids:
        print(f"  - {uuid}")
    
    # Crear variantes de búsqueda (mayúsculas y minúsculas)
    all_uuid_variants = []
    for uuid in uuids:
        all_uuid_variants.append(uuid.upper())
        all_uuid_variants.append(uuid.lower())
    
    print(f"\nVariantes de búsqueda generadas:")
    for variant in all_uuid_variants:
        print(f"  - {variant}")
    
    # Simular búsqueda
    found_invoices = []
    for db_uuid, invoice_name in db_invoices.items():
        if db_uuid in all_uuid_variants:
            found_invoices.append(invoice_name)
    
    print(f"\nFacturas encontradas: {len(found_invoices)}")
    for inv in found_invoices:
        print(f"  - {inv}")
    
    assert len(found_invoices) == 2, f"ERROR: Se esperaban 2 facturas, se encontraron {len(found_invoices)}"
    
    print("\n" + "=" * 70)
    print("BÚSQUEDA CASE-INSENSITIVE FUNCIONANDO ✅")
    print("=" * 70)


if __name__ == '__main__':
    test_uuid_extraction()
    test_case_insensitive_search()
    
    print("\n\n📋 INSTRUCCIONES PARA PRUEBA EN ODOO:")
    print("-" * 50)
    print("1. Iniciar Odoo con: .\\start_odoo.ps1")
    print("2. Ir a Contabilidad > Pagos")
    print("3. Subir un REP que tenga múltiples facturas")
    print("4. Verificar en los logs:")
    print("   - 'REP Multi-Invoice Fix: Extracted X invoice UUIDs'")
    print("   - 'REP Multi-Invoice Fix: Found X invoices'")
    print("5. Verificar que el pago muestre todas las facturas vinculadas")
