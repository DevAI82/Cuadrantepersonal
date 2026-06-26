# Script para enviar el informe global de cobertura por email via Outlook
$outlook = New-Object -ComObject Outlook.Application
$mail = $outlook.CreateItem(0)

$mail.To = "jm_olmeda@hotmail.com"
$mail.Subject = "Informe Cobertura Personal — 13/05/2026"
$mail.Body = ""

$attachmentPath = "C:\Users\JOSE\Documents\Claude\Projects\Calendarios de Personal\Informe_Global_2026-05-13.pdf"
$mail.Attachments.Add($attachmentPath)

$mail.Send()
Write-Host "Correo enviado correctamente con el informe adjunto."
