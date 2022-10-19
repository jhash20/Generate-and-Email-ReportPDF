#!/usr/bin/env python3

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.units import inch
from car_report import format_car

def generate(filename, title, additional_info, table_data, sorted_data):
    styles = getSampleStyleSheet()
    reports = SimpleDocTemplate(filename)
    report_title = Paragraph(title, styles["h1"])
    table_style = [('GRID', (0,0), (-1.-1), 1, colors.black), ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('ALIGN', (0,0), (-1,-1) 'CENTER')]
    report_table = Table(data = table_data, style = table_style, hAlighn = "LEFT")
    # Creates a Pie Chart
    report_pie = Pie(width=3*inch, height=3*inch)
    report_pie.data = []
    report_pie.labels = []
    for item in sorted_data:
        car_info = format_car(sorted_data)
        report_pie.data.append(item["total_sales"])
        report_pie.labels.append(car_info)
    print(report_pie.labels)
    print(report_pie.data)
    report_chart = Drawing()
    report_chart.add(report_pie)
    # build pdf
    empty_line = Spacer(1,20)
    report.build([report_title, empty_line, report_info, empty_line, report_table, empty_line, report_chart])
    
