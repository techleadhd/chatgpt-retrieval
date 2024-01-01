import os
import json
from PyPDF2 import PdfFileReader



def simple_search(query, data):
    query = query.lower()
    best_match = None
    highest_count = 0

    for file_name, text in data.items():
        text_lower = text.lower()
        count = text_lower.count(query)
        if count > highest_count:
            highest_count = count
            best_match = text

    if best_match:
        start_index = best_match.lower().find(query)
        end_index = start_index + len(query)
        snippet = best_match[max(0, start_index-30):min(end_index+30, len(best_match))]
        return snippet

    return "No relevant information found."

