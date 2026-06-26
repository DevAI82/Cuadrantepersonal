Set objOutlook = CreateObject("Outlook.Application")
Set objMail = objOutlook.CreateItem(0)

objMail.To = "jm_olmeda@hotmail.com"
objMail.Subject = "Informe Cobertura Personal " & Chr(8212) & " 13/05/2026"
objMail.Body = ""
objMail.Attachments.Add "C:\Users\JOSE\Documents\Claude\Projects\Calendarios de Personal\Informe_Global_2026-05-13.pdf"
objMail.Send

MsgBox "Email enviado correctamente con el PDF adjunto.", vbInformation, "OK"

Set objMail = Nothing
Set objOutlook = Nothing
