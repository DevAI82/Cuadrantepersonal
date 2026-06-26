---
name: informe-cobertura-diario
description: Genera el PDF del Informe Global del cuadrante y lo envía adjunto por email a jm_olmeda@hotmail.com
---

Genera el PDF del Informe Global del cuadrante de personal y envíalo adjunto por email a jm_olmeda@hotmail.com. Sin texto en el cuerpo del correo, solo el PDF adjunto.

## Paso 1 — Instalar Playwright (si no está instalado)

```bash
pip install playwright --break-system-packages -q 2>&1 | tail -3
python3 -m playwright install chromium --with-deps 2>&1 | tail -5
```

## Paso 2 — Generar el PDF con Playwright

Ejecuta este script Python en bash (usa rutas Linux del sandbox):

```python
import asyncio, os
from datetime import date
from playwright.async_api import async_playwright

HTML_LINUX = '/sessions/gallant-stoic-goldberg/mnt/Calendarios de Personal/Cuadrante_Personal_2026.html'
today_str  = date.today().isoformat()
PDF_LINUX  = f'/sessions/gallant-stoic-goldberg/mnt/Calendarios de Personal/Informe_Global_{today_str}.pdf'
PDF_WIN    = rf'C:\Users\JOSE\Documents\Claude\Projects\Calendarios de Personal\Informe_Global_{today_str}.pdf'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page    = await browser.new_page()
        await page.goto('file://' + HTML_LINUX)
        await page.wait_for_load_state('networkidle')
        # Activar vista Global (Informe Global - todos los departamentos)
        await page.click('#btn-global')
        await page.wait_for_timeout(1500)
        # Ocultar los botones que no deben aparecer en el PDF
        await page.evaluate("document.querySelectorAll('.no-print').forEach(el => el.style.display='none')")
        # Exportar a PDF
        await page.pdf(
            path=PDF_LINUX,
            format='A4',
            print_background=True,
            margin={'top':'12mm','bottom':'12mm','left':'10mm','right':'10mm'}
        )
        await browser.close()
    print(f'PDF generado: {PDF_LINUX}')
    print(f'PDF_WIN:{PDF_WIN}')

asyncio.run(main())
```

Captura la ruta Windows del PDF de la línea que empieza con `PDF_WIN:`.

## Paso 3 — Enviar el email con el PDF adjunto por Outlook

1. Solicita acceso: `request_access(apps=["Outlook"], clipboardWrite=True)`
2. Abre Outlook: `open_application("Outlook")`
3. Haz clic en **Correo nuevo**
4. En el campo **Para** escribe `jm_olmeda@hotmail.com` y pulsa Tab
5. En el campo **Asunto** escribe `Informe Cobertura Personal — DD/MM/YYYY` (fecha de hoy en formato español)
6. **No escribas nada en el cuerpo** del correo
7. Haz clic en el icono de adjuntar archivo (clip) en la barra de herramientas del mensaje
8. En el diálogo de archivos, navega a:
   `C:\Users\JOSE\Documents\Claude\Projects\Calendarios de Personal\`
   y selecciona el archivo `Informe_Global_YYYY-MM-DD.pdf`
9. Espera a que aparezca el adjunto en el email
10. Haz clic en **Enviar**

## Paso 4 — Confirmación

Confirma si el email se envió correctamente con el PDF adjunto, o describe el error encontrado.
