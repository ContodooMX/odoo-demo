# Script para ejecutar el código de agregar EAN codes
Write-Host "Ejecutando script para agregar códigos EAN..." -ForegroundColor Yellow

$env:PATH = "C:\Users\alber\PycharmProjects\odoo19\venv\Scripts;" + $env:PATH

# Leer el script Python
$pythonScript = Get-Content "c:\Users\alber\PycharmProjects\odoo19\addons\sale_customer_code\add_ean_codes.py" -Raw

# Ejecutar en el shell de Odoo
$command = @"
$env:PATH = "C:\Users\alber\PycharmProjects\odoo19\venv\Scripts;" + `$env:PATH
python c:\Users\alber\PycharmProjects\odoo19\odoo\odoo-bin shell -c odoo.conf --addons-path "c:\Users\alber\PycharmProjects\odoo19\odoo\addons,c:\Users\alber\PycharmProjects\odoo19\enterprise,c:\Users\alber\PycharmProjects\odoo19\addons" -d odoo19_v16 --no-http
"@

Write-Host "Conectando al shell de Odoo..." -ForegroundColor Cyan
Write-Host ""
Write-Host "INSTRUCCIONES:" -ForegroundColor Green
Write-Host "1. Espera a que aparezca el prompt >>>" -ForegroundColor White
Write-Host "2. Copia y pega el contenido del archivo add_ean_codes.py" -ForegroundColor White
Write-Host "3. Presiona Enter" -ForegroundColor White
Write-Host "4. Escribe 'exit()' para salir" -ForegroundColor White
Write-Host ""

Invoke-Expression $command
