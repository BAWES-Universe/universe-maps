"""Rebuild the frozen concept review from composed pages; no character sheets needed."""
from pathlib import Path
from reportlab.pdfgen import canvas
D=Path(__file__).parent
c=canvas.Canvas(str(D/'Saltwind-Performance-r1-review.pdf'),pagesize=(1000,700),invariant=1)
c.setTitle('Saltwind Performance Courtyard - Concept review r1')
c.setAuthor('Universe map design')
for i in (1,2):
 c.drawImage(str(D/f'review-page-{i}.png'),0,0,width=1000,height=700)
 c.showPage()
c.save()
