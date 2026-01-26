
from create_sample_data import create_training_sample, TEMPLATES
from NER_Algo import NER_Algo

#INPUT DATA

# Generate one sample contract text from your sample data
sample_data = create_training_sample(TEMPLATES[0])
Input_text = sample_data["text"]

# Process text with spaCy
doc = nlp(Input_text)

# Create matcher for termination clauses
matcher = Matcher(nlp.vocab)
termination_pattern = [{"LOWER": "termination"}, {"IS_PUNCT": True, "OP": "?"}, {"IS_ALPHA": True, "OP": "*"}]
matcher.add("TERMINATION_CLAUSE", [termination_pattern])

matches = matcher(doc)

# Containers for extracted info
party_names = []
amounts = []
dates = []
termination_clauses = []

# Extract using spaCy entities
for ent in doc.ents:
    if ent.label_ in ["ORG"]:
        party_names.append(ent.text)
    elif ent.label_ in ["MONEY"]:
        amounts.append(ent.text)
    elif ent.label_ in ["DATE"]:
        dates.append(ent.text)

# Extract termination clauses using matcher
for match_id, start, end in matches:
    span = doc[start:end].sent  # capture full sentence
    termination_clauses.append(span.text.strip())

# Remove duplicates
inputdata_party_names = list(set(party_names))
inputdata_dates = list(set(dates))
inputdata_amounts = list(set(amounts))
inputdata_termination_clauses = list(set(termination_clauses))

# Print extracted annotations
print("===== GENERATED TEXT =====")
print(Input_text)
print("\n===== EXTRACTED ANNOTATIONS =====")
for name in inputdata_party_names:
    print(f"INPUT PARTY_NAME: {name}")
for amt in inputdata_amounts:
    print(f"INPUT AMOUNT: {amt}")
for date in inputdata_dates:
    print(f"INPUT DATE: {date}")
for clause in inputdata_termination_clauses:
    print(f"INPUT TERMINATION_CLAUSE: {clause}")


#NER

output_party_names, output_dates, output_amounts, output_termination_clauses = NER_Algo(Input_text)



#OUTPUT

# Print extracted annotations
print("Annotations:")
for name in output_party_names:
    print(f"OUTPUT PARTY_NAME: {name}")
for amt in output_amounts:
    print(f"OUTPUT AMOUNT: {amt}")
for date in output_dates:
    print(f"OUTPUT DATE: {date}")
for clause in output_termination_clauses:
    print(f"OUTPUT TERMINATION_CLAUSE: {clause}")
