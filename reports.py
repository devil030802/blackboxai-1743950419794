import pandas as pd
from database import get_connection
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ReportGenerator:
    @staticmethod
    def export_daily_entries_to_excel():
        """Export daily entries to Excel."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT entry_date, (SELECT name FROM Customers WHERE id = customer_id) AS customer,
                   (SELECT name FROM Products WHERE id = product_id) AS product, quantity
            FROM DailyEntries
        ''')
        rows = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(rows, columns=["Date", "Customer", "Product", "Quantity"])
        df.to_excel('daily_entries.xlsx', index=False)

    @staticmethod
    def export_daily_entries_to_pdf():
        """Export daily entries to PDF."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT entry_date, (SELECT name FROM Customers WHERE id = customer_id) AS customer,
                   (SELECT name FROM Products WHERE id = product_id) AS product, quantity
            FROM DailyEntries
        ''')
        rows = cursor.fetchall()
        conn.close()

        pdf_file = 'daily_entries.pdf'
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.drawString(100, 750, "Daily Entries Report")
        c.drawString(100, 730, "Date")
        c.drawString(200, 730, "Customer")
        c.drawString(300, 730, "Product")
        c.drawString(400, 730, "Quantity")

        y = 710
        for row in rows:
            c.drawString(100, y, str(row[0]))
            c.drawString(200, y, row[1])
            c.drawString(300, y, row[2])
            c.drawString(400, y, str(row[3]))
            y -= 20

        c.save()