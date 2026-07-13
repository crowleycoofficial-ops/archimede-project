"""Report generation using reportlab (skeleton)."""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_report(pdf_path, summary: dict, plots: list = None):
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica", 16)
    c.drawString(30, height - 50, "Archimède Demo — One Command Report")
    c.setFont("Helvetica", 10)
    y = height - 80
    for k, v in summary.items():
        c.drawString(30, y, f"{k}: {v}")
        y -= 14
    c.showPage()
    c.save()
