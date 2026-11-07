def writer_agent(question, search_result, db_result):
    if not search_result.get("found"):
        return "I don't know. No matching loan rule was found."
    cibil = db_result.get("cibil_score", 680)
    has_statement = db_result.get("has_one_year_statement")
    if cibil >= 720:
        decision = "Eligible"
    elif cibil >= 690 and has_statement:
        decision = "Offer with conditions"
    elif cibil >= 680 and has_statement:
        decision = "Offer with conditions (exception rule)"
    else:
        decision = "Not Eligible"
    return f"Question: {question}\nFirst check: CIBIL {cibil} vs required 720.\nBank statement (1 year): {'YES' if has_statement else 'NO'}.\nFinal decision: {decision}."
