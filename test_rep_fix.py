#!/usr/bin/env python3
"""
Test script to validate the REP multi-invoice linking fix.
This script tests the _get_payment_cfdi_invoice_uuids method with different XML structures.
"""

from lxml import etree

def test_get_payment_cfdi_invoice_uuids(cfdi_data):
    """
    Simulates the _get_payment_cfdi_invoice_uuids method.
    
    :param cfdi_data: The CFDI data as bytes or string.
    :return: A list of invoice UUIDs (uppercase).
    """
    if not cfdi_data:
        return []
    
    try:
        if isinstance(cfdi_data, str):
            cfdi_data = cfdi_data.encode('utf-8')
        cfdi_node = etree.fromstring(cfdi_data)
    except (etree.XMLSyntaxError, AttributeError) as e:
        print(f"Error parsing XML: {e}")
        return []
    
    # Extract ALL DoctoRelacionado from ALL Pago nodes
    uuids = []
    for docto_node in cfdi_node.xpath("//*[local-name()='DoctoRelacionado']"):
        if uuid := docto_node.get('IdDocumento'):
            uuids.append(uuid.upper())  # Normalize to uppercase
    
    return uuids


# Test Case 1: Multiple <Pago> nodes (user's problematic structure)
test_xml_multiple_pago = """<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" 
                  xmlns:pago20="http://www.sat.gob.mx/Pagos20"
                  TipoDeComprobante="P">
    <cfdi:Complemento>
        <pago20:Pagos Version="2.0">
            <pago20:Totales MontoTotalPagos="69138.78"/>
            <pago20:Pago FechaPago="2025-03-14T12:00:00" Monto="40030.85">
                <pago20:DoctoRelacionado IdDocumento="7CFA835C-1CFF-4DA7-B5BC-9E2854209F0F" 
                                         ImpPagado="40030.85" 
                                         ImpSaldoInsoluto="0.00"/>
            </pago20:Pago>
            <pago20:Pago FechaPago="2025-03-14T12:00:00" Monto="29107.93">
                <pago20:DoctoRelacionado IdDocumento="C5863DB6-B06E-4DD3-99B9-253B424399BF" 
                                         ImpPagado="29107.93" 
                                         ImpSaldoInsoluto="0.00"/>
            </pago20:Pago>
        </pago20:Pagos>
    </cfdi:Complemento>
</cfdi:Comprobante>
"""

# Test Case 2: Single <Pago> with multiple <DoctoRelacionado>
test_xml_single_pago = """<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" 
                  xmlns:pago20="http://www.sat.gob.mx/Pagos20"
                  TipoDeComprobante="P">
    <cfdi:Complemento>
        <pago20:Pagos Version="2.0">
            <pago20:Totales MontoTotalPagos="69138.78"/>
            <pago20:Pago FechaPago="2025-03-14T12:00:00" Monto="69138.78">
                <pago20:DoctoRelacionado IdDocumento="7cfa835c-1cff-4da7-b5bc-9e2854209f0f" 
                                         ImpPagado="40030.85" 
                                         ImpSaldoInsoluto="0.00"/>
                <pago20:DoctoRelacionado IdDocumento="c5863db6-b06e-4dd3-99b9-253b424399bf" 
                                         ImpPagado="29107.93" 
                                         ImpSaldoInsoluto="0.00"/>
            </pago20:Pago>
        </pago20:Pagos>
    </cfdi:Complemento>
</cfdi:Comprobante>
"""

# Test Case 3: Single invoice
test_xml_single_invoice = """<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" 
                  xmlns:pago20="http://www.sat.gob.mx/Pagos20"
                  TipoDeComprobante="P">
    <cfdi:Complemento>
        <pago20:Pagos Version="2.0">
            <pago20:Totales MontoTotalPagos="40030.85"/>
            <pago20:Pago FechaPago="2025-03-14T12:00:00" Monto="40030.85">
                <pago20:DoctoRelacionado IdDocumento="7CFA835C-1CFF-4DA7-B5BC-9E2854209F0F" 
                                         ImpPagado="40030.85" 
                                         ImpSaldoInsoluto="0.00"/>
            </pago20:Pago>
        </pago20:Pagos>
    </cfdi:Complemento>
</cfdi:Comprobante>
"""

def run_tests():
    print("=" * 80)
    print("REP Multi-Invoice Linking Fix - Test Suite")
    print("=" * 80)
    print()
    
    # Test 1: Multiple Pago nodes (user's problematic case)
    print("Test 1: Multiple <Pago> nodes (each with one <DoctoRelacionado>)")
    print("-" * 80)
    uuids = test_get_payment_cfdi_invoice_uuids(test_xml_multiple_pago)
    print(f"Found {len(uuids)} invoice(s):")
    for i, uuid in enumerate(uuids, 1):
        print(f"  {i}. {uuid}")
    expected = 2
    status = "✅ PASS" if len(uuids) == expected else f"❌ FAIL (expected {expected}, got {len(uuids)})"
    print(f"Status: {status}")
    print()
    
    # Test 2: Single Pago with multiple DoctoRelacionado
    print("Test 2: Single <Pago> node (with multiple <DoctoRelacionado>)")
    print("-" * 80)
    uuids = test_get_payment_cfdi_invoice_uuids(test_xml_single_pago)
    print(f"Found {len(uuids)} invoice(s):")
    for i, uuid in enumerate(uuids, 1):
        print(f"  {i}. {uuid}")
    expected = 2
    status = "✅ PASS" if len(uuids) == expected else f"❌ FAIL (expected {expected}, got {len(uuids)})"
    print(f"Status: {status}")
    print()
    
    # Test 3: Single invoice
    print("Test 3: Single invoice")
    print("-" * 80)
    uuids = test_get_payment_cfdi_invoice_uuids(test_xml_single_invoice)
    print(f"Found {len(uuids)} invoice(s):")
    for i, uuid in enumerate(uuids, 1):
        print(f"  {i}. {uuid}")
    expected = 1
    status = "✅ PASS" if len(uuids) == expected else f"❌ FAIL (expected {expected}, got {len(uuids)})"
    print(f"Status: {status}")
    print()
    
    # Verify UUID normalization (uppercase)
    print("Test 4: UUID Normalization (lowercase → uppercase)")
    print("-" * 80)
    uuids = test_get_payment_cfdi_invoice_uuids(test_xml_single_pago)
    all_uppercase = all(uuid == uuid.upper() for uuid in uuids)
    status = "✅ PASS" if all_uppercase else "❌ FAIL"
    print(f"All UUIDs normalized to uppercase: {status}")
    print()
    
    print("=" * 80)
    print("Test Suite Complete")
    print("=" * 80)


if __name__ == "__main__":
    run_tests()
