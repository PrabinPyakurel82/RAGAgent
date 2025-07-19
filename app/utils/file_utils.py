import fitz

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.file.read(),filetype='pdf')
    return "\n".join([page.get_text() for page in doc])


def extract_text_from_txt(file):
    return file.file.read().decode('utf-8')