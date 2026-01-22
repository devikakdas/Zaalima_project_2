import random
import json
from pathlib import Path
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Legal entity suffixes
LEGAL_SUFFIXES = [
    "Inc.", "Corp.", "Corporation", "LLC", "LLP",
    "Ltd.", "Limited", "Company", "Co.", "LP"
]

# Contract templates
TEMPLATES = [
    """SERVICE AGREEMENT

This Service Agreement is entered into as of {date1} by and between {party1} ("Client") and {party2} ("Service Provider").

SERVICES: Service Provider shall provide consulting services to Client.

COMPENSATION: Client agrees to pay Service Provider {amount1} for services rendered.

TERM: This Agreement commences on {date2} and continues until {date3}.

TERMINATION: Either party may terminate this Agreement upon thirty (30) days written notice. Upon termination, Client shall pay for all services completed through the termination date.""",

    """EMPLOYMENT AGREEMENT

This Employment Agreement is made on {date1} between {party1} ("Employer") and {party2} ("Employee").

POSITION: Employee is hired as Senior Consultant.

SALARY: Employee shall receive {amount1} per year, payable bi-weekly.

START DATE: Employment begins on {date2}.

TERMINATION: This employment may be terminated by either party with two weeks notice. Employer will pay all earned compensation through the termination date of {date3}.""",

    """VENDOR CONTRACT

Dated {date1}, this contract is between {party1} as purchaser and {party2} as vendor.

PRODUCTS: Vendor will supply office equipment as specified in Exhibit A.

PRICE: Total contract value is {amount1}, with {amount2} due upon signing.

DELIVERY: Products will be delivered by {date2}.

CANCELLATION: Contract may be cancelled with written notice. Cancellation after {date3} incurs a 25% fee."""
]


def generate_party_name():
    """Generate realistic company name"""
    company = fake.company()
    suffix = random.choice(LEGAL_SUFFIXES)
    return f"{company} {suffix}"


def generate_amount():
    """Generate monetary amount"""
    value = random.choice([
        random.randint(5000, 50000),
        random.randint(50000, 500000),
        random.randint(100000, 2000000)
    ])

    formats = [
        f"${value:,}",
        f"${value:,}.00",
        f"USD {value:,}",
    ]

    return random.choice(formats)


def generate_date():
    """Generate date in various formats"""
    date = fake.date_between(start_date='-2y', end_date='+1y')

    formats = [
        date.strftime("%B %d, %Y"),
        date.strftime("%m/%d/%Y"),
        date.strftime("%d %B %Y"),
    ]

    return random.choice(formats)


def create_training_sample(template):
    """Create one annotated training sample"""

    # Generate entities
    entities_data = {
        'party1': generate_party_name(),
        'party2': generate_party_name(),
        'amount1': generate_amount(),
        'amount2': generate_amount(),
        'date1': generate_date(),
        'date2': generate_date(),
        'date3': generate_date(),
    }

    # Fill template
    text = template.format(**entities_data)

    # Create annotations
    # Format: [start_char, end_char, entity_type]
    annotations = []

    # Find each entity in the text
    for key, value in entities_data.items():
        entity_type = None
        if 'party' in key:
            entity_type = "PARTY_NAME"
        elif 'amount' in key:
            entity_type = "AMOUNT"
        elif 'date' in key:
            entity_type = "DATE"

        # Find all occurrences
        start = 0
        while True:
            pos = text.find(value, start)
            if pos == -1:
                break
            annotations.append({
                'start': pos,
                'end': pos + len(value),
                'label': entity_type
            })
            start = pos + 1

    # Find termination clauses
    termination_keywords = ['terminate', 'termination', 'cancel', 'cancellation']
    sentences = text.split('.')

    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in termination_keywords):
            pos = text.find(sentence.strip())
            if pos != -1 and len(sentence.strip()) > 20:
                annotations.append({
                    'start': pos,
                    'end': pos + len(sentence.strip()),
                    'label': 'TERMINATION_CLAUSE'
                })

    return {
        'text': text,
        'annotations': annotations
    }


def generate_dataset(num_samples=100):
    """Generate complete dataset"""
    samples = []

    for i in range(num_samples):
        template = TEMPLATES[i % len(TEMPLATES)]
        sample = create_training_sample(template)
        samples.append(sample)
#-------------VERIFY LABELS-----------------------------------------------
if __name__ == "__main__":
    sample = create_training_sample(TEMPLATES[0])

    for ann in sample["annotations"]:
        entity_text = sample["text"][ann["start"]:ann["end"]]
        print(f"{ann['label']}: {entity_text}")

#--------------DEBUG LOGIC---------------------------------------------------
if __name__ == "__main__":
    sample = create_training_sample(TEMPLATES[0])

    print("\n===== GENERATED TEXT =====\n")
    print(sample["text"])

    print("\n===== ANNOTATIONS =====\n")
    for ann in sample["annotations"]:
        print(ann)