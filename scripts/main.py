from Read_Pdf import Read_Pdf
from NER_Algo import NER_Algo

# extract input
input_template=Read_Pdf("lexiscan-auto/data/raw/sample_contract.pdf")

#NER
output_party_names, output_dates, output_amounts, output_termination_clauses = NER_Algo(input_template)

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
