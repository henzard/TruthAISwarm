import pandas as pd
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import json

class ExportService:
    @staticmethod
    def export_verifications(verifications, format: str):
        # Convert verifications to DataFrame
        df = pd.DataFrame(verifications)
        
        if format == "CSV":
            output = BytesIO()
            df.to_csv(output, index=False)
            return output.getvalue()
            
        elif format == "Excel":
            output = BytesIO()
            df.to_excel(output, index=False)
            return output.getvalue()
            
        elif format == "PDF":
            output = BytesIO()
            doc = SimpleDocTemplate(output, pagesize=letter)
            elements = []
            
            # Convert DataFrame to table data
            table_data = [df.columns.tolist()] + df.values.tolist()
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            doc.build(elements)
            return output.getvalue()
            
        elif format == "JSON":
            return json.dumps(df.to_dict('records'), indent=2)
            
        return None 