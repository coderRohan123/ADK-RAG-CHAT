from pypdf import PdfReader
import pandas as pd

# -----------------------------
# PDF Extraction
# -----------------------------
def extract_pdf_text(file_path):

    reader = PdfReader(file_path)

    documents = []

    for page_num, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text:

            documents.append({
                "text": text,
                "page": page_num
            })

    return documents


# -----------------------------
# Excel Extraction
# -----------------------------
def extract_excel_text(file_path):

    excel_data = pd.read_excel(
        file_path,
        sheet_name=None
    )

    documents = []

    for sheet_name, df in excel_data.items():

        text = df.astype(str).to_string()

        documents.append({
            "text": text,
            "sheet": sheet_name
        })

    return documents