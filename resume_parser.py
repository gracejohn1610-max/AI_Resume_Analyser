from pypdf import PdfReader
from docx import Document


def extract_pdf_text(file):
    """Extract text from all pages of a PDF."""

    reader = PdfReader(file)

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


def extract_docx_text(file):
    """Extract text from all paragraphs of a DOCX file."""

    document = Document(file)

    text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    return "\n".join(text)


def extract_text(file):
    """Automatically extract text based on file type."""

    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_pdf_text(file)

    elif file_name.endswith(".docx"):
        return extract_docx_text(file)

    else:
        raise ValueError(
            "Unsupported file format. Please upload a PDF or DOCX file."
        )