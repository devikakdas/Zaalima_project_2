from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_sample_contract():
    """Create a realistic service agreement PDF for OCR + NER testing"""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    pdf_path = os.path.join(BASE_DIR, "data", "raw", "sample_contract.pdf")

    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "SERVICE AGREEMENT")

    # Body text
    c.setFont("Helvetica", 11)
    text = [
        "",
        "This Service Agreement (\"Agreement\") is made and entered into on",
        "January 15, 2024 (\"Effective Date\"),",
        "",
        "BETWEEN:",
        "Acme Corporation Inc., a corporation incorporated under the laws of",
        "the State of Delaware, having its registered office at",
        "123 Market Street, San Francisco, CA 94105 (\"Client\"),",
        "",
        "AND:",
        "Tech Solutions LLC, a limited liability company registered in",
        "the State of Texas, with its principal place of business at",
        "789 Innovation Drive, Austin, TX 73301 (\"Service Provider\").",
        "",
        "1. SERVICES",
        "The Service Provider agrees to provide professional consulting,",
        "software development, and technical advisory services to the Client",
        "in accordance with the terms and conditions of this Agreement.",
        "",
        "2. PAYMENT TERMS",
        "The Client agrees to pay the Service Provider a total fee of",
        "USD $50,000.00 (Fifty Thousand United States Dollars) for the Services.",
        "Payment shall be made within thirty (30) days of receipt of invoice.",
        "",
        "3. CONFIDENTIALITY",
        "Each party agrees to maintain the confidentiality of all proprietary",
        "and confidential information disclosed under this Agreement.",
        "This obligation shall survive termination of the Agreement.",
        "",
        "4. TERM AND TERMINATION",
        "This Agreement shall commence on the Effective Date and shall",
        "remain in force for a period of twelve (12) months.",
        "Either party may terminate this Agreement by providing",
        "thirty (30) days written notice to the other party.",
        "",
        "5. GOVERNING LAW",
        "This Agreement shall be governed by and construed in accordance",
        "with the laws of the State of California, without regard to",
        "its conflict of laws principles.",
        "",
        "IN WITNESS WHEREOF, the parties have executed this Agreement",
        "as of the date first written above.",
    ]

    y = 710
    for line in text:
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = 750
        c.drawString(100, y, line)
        y -= 18

    c.save()
    print(f"✓ Created sample contract: {pdf_path}")

if __name__ == "__main__":
    create_sample_contract()



