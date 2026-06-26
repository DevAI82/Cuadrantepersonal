@echo off
echo ================================================
echo  Enviando newsletter de cobertura por Outlook
echo ================================================
powershell -ExecutionPolicy Bypass -Command ^
  "$outlook = New-Object -ComObject Outlook.Application; ^
   $mail = $outlook.CreateItem(0); ^
   $mail.To = 'jm_olmeda@hotmail.com'; ^
   $mail.Subject = '=?UTF-8?B?8J+Tuq==?= Cobertura Personal - Semana 18/05/2026 al 24/05/2026'; ^
   $mail.HTMLBody = '<html><body style=""font-family:Arial,sans-serif;color:#333""><h2 style=""color:#1565c0"">Informe de Cobertura Personal</h2><p>Generado el 24/05/2026. Adjunto encontras el informe PDF con incidencias de cobertura, mapa de calor semanal y alertas de personal.</p><p style=""color:#888;font-size:12px"">Este correo se genera desde el sistema de Cuadrante Personal 2026.</p></body></html>'; ^
   $pdf = 'C:\Users\JOSE\Documents\Claude\Projects\Calendarios de Personal\Informe_Cobertura_2026-05-18.pdf'; ^
   $mail.Attachments.Add($pdf) | Out-Null; ^
   $mail.Send(); ^
   Write-Host 'Correo enviado correctamente a jm_olmeda@hotmail.com'"

echo.
if %errorlevel%==0 (
    echo [OK] Correo enviado correctamente.
) else (
    echo [ERROR] Algo ha fallado al enviar el correo.
)
echo.
pause
