def NER_Algo(Input_text):

    import spacy
    from spacy.matcher import Matcher
    
    # Sample contract text
    text = Input_text
    
    # Load English model
    nlp = spacy.load("en_core_web_sm")

    # Process text
    doc = nlp(text)

    # Create matcher for custom rules
    matcher = Matcher(nlp.vocab)

    # Rule to detect termination clauses (lines starting with TERMINATION)
    termination_pattern = [{"LOWER": "termination"}, {"IS_PUNCT": True, "OP": "?"}, {"IS_ALPHA": True, "OP": "*"}]
    matcher.add("TERMINATION_CLAUSE", [termination_pattern])

    matches = matcher(doc)

    # Extracted info
    party_names = []
    amounts = []
    dates = []
    termination_clauses = []

    # Extract using spaCy entities
    for ent in doc.ents:
        if ent.label_ in ["ORG"]:  # Organization names
            party_names.append(ent.text)
        elif ent.label_ in ["MONEY"]:
            amounts.append(ent.text)
        elif ent.label_ in ["DATE"]:
            dates.append(ent.text)

    # Extract termination clauses using matcher
    for match_id, start, end in matches:
        span = doc[start:end].sent  # capture the full sentence
        termination_clauses.append(span.text.strip())

    # Remove duplicates
    output_party_names = list(set(party_names))
    output_dates = list(set(dates))
    output_amounts = list(set(amounts))
    output_termination_clauses = list(set(termination_clauses))

    return output_party_names, output_dates, output_amounts, output_termination_clauses