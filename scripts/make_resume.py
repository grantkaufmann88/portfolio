"""Optional PDF regeneration: requires reportlab. The finished PDF is already included."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
FONT_DIR=Path(__file__).resolve().parent / "fonts"
pdfmetrics.registerFont(TTFont("PortfolioSans", str(FONT_DIR / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("PortfolioSansBold", str(FONT_DIR / "DejaVuSans-Bold.ttf")))
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/downloads/Grant-Kaufmann-Resume.pdf'
c=canvas.Canvas(str(OUT),pagesize=(612,792))
c.setTitle('Grant Kaufmann | Engineering Resume');c.setAuthor('Grant Kaufmann')
INK=HexColor('#242a27');MUTED=HexColor('#555e55');ACCENT=HexColor('#a34127')
y=743

def text(s,size=9.5,font='PortfolioSans',color=INK,x=46,leading=13,maxwidth=520):
 global y
 c.setFont(font,size);c.setFillColor(color)
 for line in simpleSplit(s,font,size,maxwidth):c.drawString(x,y,line);y-=leading

def section(s):
 global y
 y-=11;text(s.upper(),8.5,'PortfolioSansBold',ACCENT,leading=13)
 c.setStrokeColor(HexColor('#d9dcd3'));c.line(46,y+5,566,y+5);y-=5

def role(title,org,period,body=None):
 global y
 text(title+' | '+org,10,'PortfolioSansBold',leading=13)
 text(period,8.5,color=MUTED,leading=12)
 if body:text(body,9,leading=12)
 y-=4

text('GRANT KAUFMANN',26,'PortfolioSansBold',leading=30)
text('Mechanical Engineering  /  Harvard College, Class of 2028',11,color=MUTED,leading=18)
text('Cambridge, MA  |  kaufmann.grant@gmail.com  |  +1 (617) 851-7057',9,leading=14)
text('linkedin.com/in/grant-kaufmann-harvard  |  youtube.com/@grantkprojects',9,leading=13)
c.linkURL('mailto:kaufmann.grant@gmail.com',(119,688,302,702),relative=0)
c.linkURL('https://www.linkedin.com/in/grant-kaufmann-harvard/',(46,674,312,688),relative=0)
section('Education')
text('Harvard College - Mechanical Engineering',10,'PortfolioSansBold',leading=14)
text('Class of 2028 | Third-year undergraduate',9,color=MUTED,leading=13)
text('Cambridge Rindge and Latin School | Class of 2024',9,leading=13)
section('Experience & leadership')
role('Research Assistant','Harvard Rowland Institute','Part-time; began during senior year of high school', 'Undergraduate research in the electrical engineering laboratory of Winfield Hill and Professor Paul Horowitz.')
role('Engineering Intern','SpaceX','Fall 2025')
role('Vice President','Harvard Undergraduate Robotics Club','Harvard College','Student robotics leadership; project portfolio includes the HURC Mars rover.')
role('Midshipman','BU-MIT NROTC Consortium','Alongside Harvard undergraduate studies')
role('Captain of Mechanical Design','CRLS FIRST Robotics','2023-2024','Taught and mentored a group of 25 students working toward a competition robot. Also served as an engineering teaching assistant, including project-based instruction for six students.')
section('Selected engineering projects')
role('Budget e-bike conversion kit','Independent project','2023-2024','Designed custom brushless motor-control electronics, Bluetooth interface, and a printed enclosure. Iterated through 50+ PCB attempts; tested an experimental printed motor and identified thermal limitations.')
role('Desktop CNC / PCB mill','Independent project','2021-2023','Designed and built a low-cost machine for PCB fabrication. Produced double-sided boards and learned the limits of in-house manufacturing for dense electronics.')
role('Mini Cybertruck go-kart','Independent project','2017-2024','Developed a steel-frame vehicle with electronic steering and remote-control capability. Designed a starter-generator transmission with printed components and one-way bearings.')
section('Technical skills & interests')
text('Design & fabrication: Onshape, Fusion 360, FDM/SLA printing, CNC milling, welding, carpentry.',9,leading=13)
text('Electronics & software: PCB design, soldering, Arduino, motor control, C/C++, Python.',9,leading=13)
text('Languages & interests: English and Spanish; violin, hiking, canoeing, and running.',9,leading=13)
c.setFont('PortfolioSans',7.5);c.setFillColor(MUTED);c.drawString(46,30,'September 2026')
assert y>45, f'Resume overflow: {y}'
c.save();print(OUT,'bottom=',round(y))
