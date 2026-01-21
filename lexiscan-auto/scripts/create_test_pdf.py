from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def create_sample_contract():
    """Create a simple test contract PDF"""
    pdf_path = "data/raw/sample_contract.pdf"

    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "SERVICE AGREEMENT")

    # Contract text
    c.setFont("Helvetica", 12)
    text = [
        "",
        "This Agreement is made on January 15, 2024",
        "between Acme Corporation Inc. (Client)",
        "and Tech Solutions LLC (Service Provider).",
        "",
        "The Client agrees to pay $50,000.00 for consulting services.",
        "",
        "This contract may be terminated by either party with",
        "30 days written notice.",
    ]


    y = 700
    for line in text :
        c.drawString(100, y, line)
        y -= 20



if __name__ == "__main__":
    create_sample_contract()