"""
newsletter_cobertura.py
=======================
Genera el informe semanal de cobertura en PDF (datos desde Supabase)
y lo envía por correo via Gmail SMTP.

Uso:
    python newsletter_cobertura.py            # genera + envía
    python newsletter_cobertura.py --solo-pdf # solo genera el PDF
    python newsletter_cobertura.py --solo-email ruta\archivo.pdf  # solo envía

Requisitos:
    pip install supabase reportlab
"""

import smtplib, ssl, sys, os, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from supabase import create_client
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                 Paragraph, Spacer, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

# ──────────────────────────────────────────────
# CONFIGURACIÓN
# ──────────────────────────────────────────────

# Ruta del directorio donde está este script (funciona en Windows y en el sandbox Linux)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEST_EMAIL = "jmolmeda@gmail.com"

# Gmail SMTP
GMAIL_USER     = "jmolmeda@gmail.com"
GMAIL_PASSWORD = "zrgcndeaoomzzrwp"   # contraseña de aplicación Google

# Supabase
SUPA_URL = "https://unrpssxvivjhehamkfoe.supabase.co"
SUPA_KEY = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVucnBzc3h2aXZqaGVoYW1rZm9lIiwi"
            "cm9sZSI6ImFub24iLCJpYXQiOjE3ODAxMjI3MzAsImV4cCI6MjA5NTY5ODczMH0"
            ".xV8YS4uLxE3WDCjO2TNRxSfRgUUBczYzS0X0Z1F3Ufg")

# ──────────────────────────────────────────────
# CONSTANTES DE FORMATO
# ──────────────────────────────────────────────

DIAS_ES  = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
MESES_ES = ['', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
            'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

SHIFT_COLORS = {
    'M':      ('#e8f5e9', '#2e7d32'),
    'MAN':    ('#e8f5e9', '#2e7d32'),
    'M(AM)':  ('#e8f5e9', '#2e7d32'),
    'T':      ('#e3f2fd', '#1565c0'),
    'TAR':    ('#e3f2fd', '#1565c0'),
    'PAR':    ('#fff3e0', '#e65100'),
    'COM':    ('#fce4ec', '#c2185b'),
    'L':      ('#f5f5f5', '#9e9e9e'),
    'LIB':    ('#f5f5f5', '#9e9e9e'),
    'VAC':    ('#e8eaf6', '#3f51b5'),
    'C':      ('#fafafa', '#bdbdbd'),
    'BAJ':    ('#ffebee', '#c62828'),
    'SPS':    ('#ffebee', '#c62828'),
    'FOR':    ('#f3e5f5', '#6a1b9a'),
    'AP':     ('#fff8e1', '#f57f17'),
}

DEPT_BG = {
    'operaciones': '#e65100',
    'omnicanal':   '#1565c0',
    'cajasac':     '#2e7d32',
    'muelle':      '#4e342e',
}

LEGEND = [
    ('M/MAN/M(AM)', '#e8f5e9', '#2e7d32', 'Mañana'),
    ('T / TAR',     '#e3f2fd', '#1565c0', 'Tarde'),
    ('PAR',         '#fff3e0', '#e65100', 'Partido'),
    ('COM',         '#fce4ec', '#c2185b', 'Complemento'),
    ('L / LIB',     '#f5f5f5', '#9e9e9e', 'Libre'),
    ('VAC',         '#e8eaf6', '#3f51b5', 'Vacaciones'),
    ('BAJ / SPS',   '#ffebee', '#c62828', 'Baja'),
    ('FOR',         '#f3e5f5', '#6a1b9a', 'Formación'),
    ('C',           '#fafafa', '#bdbdbd', 'Compensación'),
]

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

def get_week_range(offset_weeks=0):
    today = datetime.date.today()
    mon   = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(weeks=offset_weeks)
    sun   = mon + datetime.timedelta(days=6)
    return mon, sun

def fmt(d):
    return d.strftime("%d/%m/%Y")

def fmt_file(d):
    return d.strftime("%Y-%m-%d")

def fmt_short(d):
    return f"{d.day:02d}/{d.month:02d}"

def fmt_long(d):
    return f"{d.day} {MESES_ES[d.month]}"

def shift_color(code):
    code = (code or '').strip().upper()
    for k, v in SHIFT_COLORS.items():
        if code == k or code.startswith(k):
            return v
    return ('#ffffff', '#333333')

# ──────────────────────────────────────────────
# OBTENER DATOS DE SUPABASE
# ──────────────────────────────────────────────

def fetch_data(mon0, sun1):
    print("[DATA] Conectando a Supabase…", flush=True)
    sb = create_client(SUPA_URL, SUPA_KEY)

    depts_raw  = sb.table('departments').select('*').order('sort_order').execute().data
    depts      = {d['id']: d['label'] for d in depts_raw}

    emps_raw   = sb.table('employees').select('*').order('sort_order').execute().data

    shifts_raw = (sb.table('shifts').select('*')
                    .gte('date', str(mon0))
                    .lte('date', str(sun1))
                    .execute().data)

    shifts_map = {}
    for s in shifts_raw:
        shifts_map.setdefault(s['employee_id'], {})[s['date']] = s['shift_code']

    print(f"[DATA] {len(emps_raw)} empleados · {len(shifts_raw)} turnos", flush=True)
    return depts, emps_raw, shifts_map, len(shifts_raw)

# ──────────────────────────────────────────────
# GENERAR PDF CON REPORTLAB
# ──────────────────────────────────────────────

def generar_pdf(pdf_path, mon0, sun1):
    depts, emps_raw, shifts_map, n_shifts = fetch_data(mon0, sun1)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(A4),
        leftMargin=10*mm, rightMargin=10*mm,
        topMargin=12*mm,  bottomMargin=12*mm,
    )

    s_title = ParagraphStyle('T', fontSize=13, fontName='Helvetica-Bold',
                              textColor=colors.HexColor('#1a237e'), spaceAfter=2)
    s_sub   = ParagraphStyle('S', fontSize=8, fontName='Helvetica',
                              textColor=colors.HexColor('#546e7a'), spaceAfter=6)

    story = []

    # Cabecera
    mon1, sun1b = get_week_range(1)
    wk = mon0.isocalendar()[1]
    sun0 = mon0 + datetime.timedelta(days=6)

    story.append(Paragraph(
        "Cuadrante de Personal 2026 — Informe de Cobertura Semanal", s_title))
    story.append(Paragraph(
        f"Semana {wk}: {fmt_long(mon0)} – {fmt_long(sun0)}  ·  "
        f"Semana {wk+1}: {fmt_long(mon1)} – {fmt_long(sun1b)}  ·  "
        f"Generado: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}",
        s_sub))
    story.append(HRFlowable(width="100%", thickness=1,
                             color=colors.HexColor('#c5cae9'), spaceAfter=8))

    # Días Lun–Sáb de las 2 semanas
    week_days = [
        mon0 + datetime.timedelta(days=i)
        for i in range(14)
        if (mon0 + datetime.timedelta(days=i)).weekday() < 6
    ]
    n_days  = len(week_days)
    col_emp = 34*mm
    col_day = max(9*mm, (doc.width - col_emp) / n_days)

    for dept_id, dept_label in depts.items():
        dept_emps = [e for e in emps_raw if e['department_id'] == dept_id]
        if not dept_emps:
            continue

        bg_dept = DEPT_BG.get(dept_id, '#37474f')

        # Fila 0: etiqueta dpto + separadores de semana
        row0 = [dept_label.upper()]
        row0 += [f"◀ Semana {wk}" if i == 0 else
                 (f"◀ Semana {wk+1}" if i == 6 else '')
                 for i in range(n_days)]

        # Fila 1: cabecera días
        row1 = ['Empleado']
        row1 += [f"{DIAS_ES[d.weekday()]}\n{fmt_short(d)}" for d in week_days]

        data = [row0, row1]
        for emp in dept_emps:
            row = [emp['name']]
            for d in week_days:
                row.append(shifts_map.get(emp['id'], {}).get(str(d), '—'))
            data.append(row)

        col_widths = [col_emp] + [col_day] * n_days
        t = Table(data, colWidths=col_widths, repeatRows=2)

        ts = TableStyle([
            ('BACKGROUND',    (0, 0), (-1, 0), colors.HexColor(bg_dept)),
            ('TEXTCOLOR',     (0, 0), (-1, 0), colors.white),
            ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE',      (0, 0), (-1, 0), 8),
            ('ALIGN',         (0, 0), (0, 0),  'LEFT'),
            ('ALIGN',         (1, 0), (-1, 0), 'CENTER'),
            ('SPAN',          (0, 0), (5, 0)),
            ('BACKGROUND',    (0, 1), (-1, 1), colors.HexColor('#37474f')),
            ('TEXTCOLOR',     (0, 1), (-1, 1), colors.white),
            ('FONTNAME',      (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE',      (0, 1), (-1, 1), 7),
            ('ALIGN',         (0, 1), (-1, 1), 'CENTER'),
            ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE',      (0, 2), (-1, -1), 7.5),
            ('FONTNAME',      (0, 2), (0, -1),  'Helvetica-Bold'),
            ('ALIGN',         (1, 2), (-1, -1), 'CENTER'),
            ('ROWBACKGROUNDS',(0, 2), (-1, -1),
             [colors.white, colors.HexColor('#f5f5f5')]),
            ('GRID',          (0, 1), (-1, -1), 0.3, colors.HexColor('#e0e0e0')),
            ('LINEBELOW',     (0, 1), (-1, 1),  0.8, colors.HexColor('#bdbdbd')),
            ('LINEAFTER',     (6, 0), (6, -1),  1.5, colors.HexColor('#9e9e9e')),
            ('LEFTPADDING',   (0, 0), (-1, -1), 3),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 3),
            ('TOPPADDING',    (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ])

        for ri, emp in enumerate(dept_emps):
            for ci, d in enumerate(week_days):
                code = shifts_map.get(emp['id'], {}).get(str(d), '')
                if code and code != '—':
                    bg_h, fg_h = shift_color(code)
                    r, c = ri + 2, ci + 1
                    ts.add('BACKGROUND', (c, r), (c, r), colors.HexColor(bg_h))
                    ts.add('TEXTCOLOR',  (c, r), (c, r), colors.HexColor(fg_h))
                    ts.add('FONTNAME',   (c, r), (c, r), 'Helvetica-Bold')

        t.setStyle(ts)
        story.append(Spacer(1, 4*mm))
        story.append(t)

    # Leyenda
    story.append(Spacer(1, 5*mm))
    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor('#e0e0e0'), spaceAfter=4))

    leg_data = [['Leyenda:'] + [f"{code} = {desc}" for code, _, _, desc in LEGEND]]
    leg_widths = [20*mm] + [28*mm] * len(LEGEND)
    leg_t = Table(leg_data, colWidths=leg_widths)
    leg_ts = TableStyle([
        ('FONTNAME',      (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE',      (0, 0), (-1, -1), 6.5),
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING',    (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ])
    for i, (_, bg, fg, _) in enumerate(LEGEND):
        c = i + 1
        leg_ts.add('BACKGROUND', (c, 0), (c, 0), colors.HexColor(bg))
        leg_ts.add('TEXTCOLOR',  (c, 0), (c, 0), colors.HexColor(fg))
        leg_ts.add('FONTNAME',   (c, 0), (c, 0), 'Helvetica-Bold')
    leg_t.setStyle(leg_ts)
    story.append(leg_t)

    doc.build(story)
    size_kb = os.path.getsize(pdf_path) // 1024
    print(f"[PDF] Generado: {pdf_path}  ({size_kb} KB)", flush=True)
    return n_shifts

# ──────────────────────────────────────────────
# ENVIAR EMAIL VIA GMAIL SMTP
# ──────────────────────────────────────────────

def enviar_email(pdf_path, mon0, n_shifts=None):
    mon1, sun1 = get_week_range(1)
    wk   = mon0.isocalendar()[1]
    sun0 = mon0 + datetime.timedelta(days=6)

    subject = f"Cuadrante Personal — S.{wk}: {fmt(mon0)}-{fmt(sun0)}"
    extra   = f"<br>{n_shifts} registros procesados desde Supabase." if n_shifts else ""

    body_html = f"""
<html><body style="font-family:Arial,sans-serif;color:#333;max-width:620px">
<h2 style="color:#1565c0;margin-bottom:4px">Informe de Cobertura Personal</h2>
<p style="color:#546e7a;margin-top:0">Generado automáticamente · {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
<hr style="border:none;border-top:1px solid #e0e0e0">
<table style="width:100%;border-collapse:collapse;margin:16px 0">
  <tr style="background:#e3f2fd">
    <td style="padding:8px 12px;font-weight:bold;color:#1a237e">Esta semana (S.{wk})</td>
    <td style="padding:8px 12px">{fmt(mon0)} – {fmt(sun0)}</td>
  </tr>
  <tr style="background:#f5f5f5">
    <td style="padding:8px 12px;font-weight:bold;color:#1a237e">Semana siguiente (S.{wk+1})</td>
    <td style="padding:8px 12px">{fmt(mon1)} – {fmt(sun1)}</td>
  </tr>
</table>
<p>Adjunto encontrarás el informe PDF con todos los turnos de los 4 departamentos
(Operaciones, Omnicanal, Caja/SAC y Muelle) para las dos semanas.</p>
<p style="margin-top:24px;color:#888;font-size:12px">
  Datos obtenidos de Supabase en tiempo real.{extra}<br>
  Para ver el cuadrante completo abre <strong>Cuadrante_Personal_2026.html</strong>.
</p>
</body></html>
"""

    msg = MIMEMultipart()
    msg['From']    = GMAIL_USER
    msg['To']      = DEST_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body_html, 'html', 'utf-8'))

    pdf_filename = os.path.basename(pdf_path)
    with open(pdf_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{pdf_filename}"')
    msg.attach(part)

    print("[EMAIL] Conectando a Gmail SMTP…", flush=True)
    ctx = ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls(context=ctx)
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, DEST_EMAIL, msg.as_bytes())

    print(f"[EMAIL] Enviado correctamente a {DEST_EMAIL}", flush=True)

# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main():
    args       = sys.argv[1:]
    solo_pdf   = '--solo-pdf'   in args
    solo_email = '--solo-email' in args

    mon0, sun0 = get_week_range(0)
    _,    sun1 = get_week_range(1)

    if solo_email:
        idx = args.index('--solo-email')
        if idx + 1 >= len(args):
            print("Uso: python newsletter_cobertura.py --solo-email <ruta_pdf>")
            sys.exit(1)
        pdf_path = args[idx + 1]
        if not os.path.isfile(pdf_path):
            print(f"Error: no se encuentra el PDF '{pdf_path}'")
            sys.exit(1)
        enviar_email(pdf_path, mon0)
        return

    pdf_name = f"Informe_Cobertura_{fmt_file(mon0)}.pdf"
    pdf_path = os.path.join(BASE_DIR, pdf_name)

    n_shifts = generar_pdf(pdf_path, mon0, sun1)

    if not solo_pdf:
        enviar_email(pdf_path, mon0, n_shifts)

    print(f"\n✓ Proceso completado. PDF: {pdf_path}", flush=True)


if __name__ == '__main__':
    main()
