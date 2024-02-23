import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path
import os


def generate(invoices_path, pdfs_path, image_path, product_id,
             product_name, amount, price_per_unit, total_price):
    """

    :param invoices_path:
    :param pdfs_path:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount:
    :param price_per_unit:
    :param total_price:
    :return:
    """
    # get data from excel files
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:
        # get invoice # and date
        filename = Path(filepath).stem
        invoice_nr, invoice_date = filename.split('-')
        total_cost = 0

        # format invoice page
        pdf = FPDF(orientation="P", unit="mm",format="Letter")
        pdf.add_page()
        pdf.set_text_color(0, 0, 0)

        # write invoice nr.
        pdf.set_font(family="Times", style="B", size=20)
        pdf.cell(w=50, h=8, txt=f"Invoice #{invoice_nr}", ln=1)

        # write invoice date
        pdf.set_font(family="Times", style="I", size=16)
        pdf.cell(w=50, h=8, txt=f"Invoice Date: {invoice_date}", ln=1)

        # read data from Excel file
        df = pd.read_excel(filepath, sheet_name='Sheet 1')

        #create headers
        headers = df.columns
        headers = [item.replace("_", " ").title() for item in headers]
        pdf.set_font(family="Times", size=12, style="B")
        pdf.cell(w=25, h=8, txt=headers[0], align="C", border=1)
        pdf.cell(w=60, h=8, txt=headers[1], align="C", border=1)
        pdf.cell(w=40, h=8, txt=headers[2], align="C", border=1)
        pdf.cell(w=30, h=8, txt=headers[3], align="C", border=1)
        pdf.cell(w=30, h=8, txt=headers[4], align="C", border=1, ln=1)

        #populate the data
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=12)
            pdf.cell(w=25, h=8, txt=str(row[product_id]), align="C", border=1)
            pdf.cell(w=60, h=8, txt=str(row[product_name]), align="C", border=1)
            pdf.cell(w=40, h=8, txt=str(row[amount]), align="C", border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), align="C", border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), align="C", border=1, ln=1)

        # calculate total cost
        total_cost = df['total_price'].sum()

        # print invoice TOTAL row
        pdf.set_font(family="Times", size=12, style="B")
        pdf.cell(w=25, h=8, txt="TOTAL", align="C", border=1)
        pdf.cell(w=60, h=8, txt="", border=1)
        pdf.cell(w=40, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=str(total_cost), align="C", border=1, ln=1)

        # Print the invoice total and thank you
        pdf.cell(w=0, h=8, txt="", ln=1)
        pdf.set_font(family="Times", size=16)
        pdf.cell(w=0, h=8, txt=f"The total cost is ${total_cost}.", ln=1)
        pdf.cell(w=30, h=8, txt="PythonHow")
        pdf.image(image_path, w=10)

        # create pdf file
        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")





