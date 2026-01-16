#!/usr/bin/env python3
"""
Script de Validación - REP Multi-Factura
Genera XMLs de prueba y valida la extracción de UUIDs
"""

import os
from datetime import datetime

# Plantilla base para REP
REP_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" 
                  xmlns:pago20="http://www.sat.gob.mx/Pagos20"
                  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                  Version="4.0"
                  Fecha="{fecha}"
                  Folio="{folio}"
                  Serie="REP"
                  TipoDeComprobante="P"
                  SubTotal="0"
                  Moneda="XXX"
                  Total="0"
                  LugarExpedicion="64000">
    <cfdi:Emisor Rfc="AAA010101AAA" Nombre="EMPRESA PRUEBA" RegimenFiscal="601"/>
    <cfdi:Receptor Rfc="XAXX010101000" Nombre="CLIENTE PRUEBA" UsoCFDI="CP01" 
                   DomicilioFiscalReceptor="64000" RegimenFiscalReceptor="616"/>
    <cfdi:Conceptos>
        <cfdi:Concepto ClaveProdServ="84111506" Cantidad="1" ClaveUnidad="ACT" 
                       Descripcion="Pago" ValorUnitario="0" Importe="0" ObjetoImp="01"/>
    </cfdi:Conceptos>
    <cfdi:Complemento>
        <pago20:Pagos Version="2.0">
            <pago20:Totales MontoTotalPagos="{total}"/>
{pagos}
        </pago20:Pagos>
    </cfdi:Complemento>
</cfdi:Comprobante>
"""

def generar_caso1_multiples_pago():
    """Caso 1: Múltiples nodos <Pago> (estructura del usuario)"""
    pagos = """            <pago20:Pago FechaPago="2026-01-14T12:00:00" FormaDePagoP="03" 
                         MonedaP="MXN" Monto="40030.85">
                <pago20:DoctoRelacionado IdDocumento="7CFA835C-1CFF-4DA7-B5BC-9E2854209F0F" 
                                         Serie="CZ" Folio="1693"
                                         MonedaDR="MXN" NumParcialidad="1"
                                         ImpSaldoAnt="40030.85" ImpPagado="40030.85" 
                                         ImpSaldoInsoluto="0.00" ObjetoImpDR="02"/>
            </pago20:Pago>
            <pago20:Pago FechaPago="2026-01-14T12:00:00" FormaDePagoP="03" 
                         MonedaP="MXN" Monto="29107.93">
                <pago20:DoctoRelacionado IdDocumento="C5863DB6-B06E-4DD3-99B9-253B424399BF" 
                                         Serie="CZ" Folio="1694"
                                         MonedaDR="MXN" NumParcialidad="1"
                                         ImpSaldoAnt="29107.93" ImpPagado="29107.93" 
                                         ImpSaldoInsoluto="0.00" ObjetoImpDR="02"/>
            </pago20:Pago>"""
    
    xml = REP_TEMPLATE.format(
        fecha=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        folio="TEST-001",
        total="69138.78",
        pagos=pagos
    )
    
    filename = "caso1_multiples_pago.xml"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(xml)
    
    print(f"✅ Generado: {filename}")
    print(f"   Estructura: 2 nodos <Pago> separados")
    print(f"   Facturas esperadas: 2")
    print(f"   UUIDs: 7CFA835C-... y C5863DB6-...")
    return filename

def generar_caso2_un_pago_multiples_doctos():
    """Caso 2: Un nodo <Pago> con múltiples <DoctoRelacionado>"""
    pagos = """            <pago20:Pago FechaPago="2026-01-14T12:00:00" FormaDePagoP="03" 
                         MonedaP="MXN" Monto="1500.00">
                <pago20:DoctoRelacionado IdDocumento="11111111-1111-1111-1111-111111111111" 
                                         Serie="TEST" Folio="A001"
                                         MonedaDR="MXN" NumParcialidad="1"
                                         ImpSaldoAnt="1000.00" ImpPagado="1000.00" 
                                         ImpSaldoInsoluto="0.00" ObjetoImpDR="02"/>
                <pago20:DoctoRelacionado IdDocumento="22222222-2222-2222-2222-222222222222" 
                                         Serie="TEST" Folio="A002"
                                         MonedaDR="MXN" NumParcialidad="1"
                                         ImpSaldoAnt="500.00" ImpPagado="500.00" 
                                         ImpSaldoInsoluto="0.00" ObjetoImpDR="02"/>
            </pago20:Pago>"""
    
    xml = REP_TEMPLATE.format(
        fecha=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        folio="TEST-002",
        total="1500.00",
        pagos=pagos
    )
    
    filename = "caso2_un_pago_multiples_doctos.xml"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(xml)
    
    print(f"✅ Generado: {filename}")
    print(f"   Estructura: 1 nodo <Pago> con 2 <DoctoRelacionado>")
    print(f"   Facturas esperadas: 2")
    print(f"   UUIDs: 11111111-... y 22222222-...")
    return filename

def generar_caso3_una_factura():
    """Caso 3: Una sola factura"""
    pagos = """            <pago20:Pago FechaPago="2026-01-14T12:00:00" FormaDePagoP="03" 
                         MonedaP="MXN" Monto="2000.00">
                <pago20:DoctoRelacionado IdDocumento="33333333-3333-3333-3333-333333333333" 
                                         Serie="TEST" Folio="C001"
                                         MonedaDR="MXN" NumParcialidad="1"
                                         ImpSaldoAnt="2000.00" ImpPagado="2000.00" 
                                         ImpSaldoInsoluto="0.00" ObjetoImpDR="02"/>
            </pago20:Pago>"""
    
    xml = REP_TEMPLATE.format(
        fecha=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        folio="TEST-003",
        total="2000.00",
        pagos=pagos
    )
    
    filename = "caso3_una_factura.xml"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(xml)
    
    print(f"✅ Generado: {filename}")
    print(f"   Estructura: 1 nodo <Pago> con 1 <DoctoRelacionado>")
    print(f"   Facturas esperadas: 1")
    print(f"   UUID: 33333333-...")
    return filename

def generar_caso4_uuids_minusculas():
    """Caso 4: UUIDs en minúsculas (normalización)"""
    pagos = """            <pago20:Pago FechaPago="2026-01-14T12:00:00" FormaDePagoP="03" 
                         MonedaP="MXN" Monto="1000.00">
                <pago20:DoctoRelacionado IdDocumento="7cfa835c-1cff-4da7-b5bc-9e2854209f0f" 
                                         Serie="CZ" Folio="1693"
                                         MonedaDR="MXN" NumParcialidad="1"
                                         ImpSaldoAnt="1000.00" ImpPagado="1000.00" 
                                         ImpSaldoInsoluto="0.00" ObjetoImpDR="02"/>
            </pago20:Pago>"""
    
    xml = REP_TEMPLATE.format(
        fecha=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        folio="TEST-004",
        total="1000.00",
        pagos=pagos
    )
    
    filename = "caso4_uuids_minusculas.xml"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(xml)
    
    print(f"✅ Generado: {filename}")
    print(f"   Estructura: UUID en MINÚSCULAS")
    print(f"   Facturas esperadas: 1 (si existe CZ-1693)")
    print(f"   UUID: 7cfa835c-... (minúsculas)")
    return filename

def generar_reporte_template():
    """Genera plantilla para reporte de resultados"""
    template = """# Reporte de Validación - REP Multi-Factura
**Fecha**: {fecha}
**Ejecutado por**: [Tu Nombre]

---

## Caso 1: Múltiples Nodos <Pago>
**Archivo**: caso1_multiples_pago.xml
**Resultado**: [ ] ✅ EXITOSO / [ ] ❌ FALLIDO

**Detalles**:
- Facturas vinculadas: ___
- UUIDs encontrados: ___
- Montos correctos: [ ] Sí / [ ] No
- Saldos = $0.00: [ ] Sí / [ ] No

**Observaciones**:
___

---

## Caso 2: Un <Pago> con Múltiples <DoctoRelacionado>
**Archivo**: caso2_un_pago_multiples_doctos.xml
**Resultado**: [ ] ✅ EXITOSO / [ ] ❌ FALLIDO

**Detalles**:
- Facturas vinculadas: ___
- UUIDs encontrados: ___
- Montos correctos: [ ] Sí / [ ] No

**Observaciones**:
___

---

## Caso 3: Una Sola Factura
**Archivo**: caso3_una_factura.xml
**Resultado**: [ ] ✅ EXITOSO / [ ] ❌ FALLIDO

**Detalles**:
- Facturas vinculadas: ___
- UUID encontrado: ___

**Observaciones**:
___

---

## Caso 4: UUIDs en Minúsculas
**Archivo**: caso4_uuids_minusculas.xml
**Resultado**: [ ] ✅ EXITOSO / [ ] ❌ FALLIDO

**Detalles**:
- Normalización funcionó: [ ] Sí / [ ] No
- Factura vinculada: ___

**Observaciones**:
___

---

## Resumen General

**Total casos ejecutados**: ___
**Casos exitosos**: ___
**Casos fallidos**: ___

**Conclusión**: [ ] APROBADO / [ ] REQUIERE CORRECCIONES

**Próximos pasos**:
___
"""
    
    filename = "reporte_validacion.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(template.format(fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    print(f"✅ Generado: {filename}")
    return filename

def main():
    print("=" * 80)
    print("Generador de Casos de Prueba - REP Multi-Factura")
    print("=" * 80)
    print()
    
    archivos = []
    
    print("📝 Generando XMLs de prueba...")
    print()
    archivos.append(generar_caso1_multiples_pago())
    print()
    archivos.append(generar_caso2_un_pago_multiples_doctos())
    print()
    archivos.append(generar_caso3_una_factura())
    print()
    archivos.append(generar_caso4_uuids_minusculas())
    print()
    
    print("📋 Generando plantilla de reporte...")
    print()
    reporte = generar_reporte_template()
    print()
    
    print("=" * 80)
    print("✅ Generación Completada")
    print("=" * 80)
    print()
    print("Archivos generados:")
    for archivo in archivos:
        print(f"  • {archivo}")
    print(f"  • {reporte}")
    print()
    print("📌 Próximos pasos:")
    print("  1. Reiniciar Odoo: .\\restart_odoo.ps1")
    print("  2. Subir cada XML a Odoo como REP")
    print("  3. Documentar resultados en reporte_validacion.md")
    print("  4. Capturar screenshots como evidencia")
    print()

if __name__ == "__main__":
    main()
