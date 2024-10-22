import json
import re

with open('utils/json/editions_keywords.json', 'r') as json_file:
    edition_keywords = json.load(json_file)

with open('utils/json/detailed_keywords.json', 'r') as json_file:
    detailed_keywords = json.load(json_file)

def classify_items(df):
    """
    Classifies items into subcategories based on provided keywords,
    ignoring case differences, using regular expressions.

    :param df: DataFrame containing item data.
    :param detailed_keywords: Detailed dictionary with categories, subcategories, and keywords.
    :return: Updated DataFrame with a new column 'SUBCATEGORY'.
    """
    # Flattening the detailed keywords into a single dictionary mapping subcategory names to keywords
    flat_keywords = {}
    for category, subcategories in detailed_keywords.items():
        for subcategory, words in subcategories.items():
            flat_subcategory = f"{category}-{subcategory}"
            if flat_subcategory not in flat_keywords:
                flat_keywords[flat_subcategory] = []
            flat_keywords[flat_subcategory].extend(words)

    # Function to classify a single item
    def classify_item(item):
        if isinstance(item, str):
            item_lower = item.lower()
            matched_subcategories = []
            
            # Check each subcategory's keywords
            for subcategory, words in flat_keywords.items():
                # Create a pattern that ensures we are matching whole words
                pattern = r'\b(?:' + '|'.join(re.escape(word.lower()) for word in words) + r')\b'  # Match whole words
                if re.search(pattern, item_lower):
                    matched_subcategories.append(subcategory)

            # If matches were found, return the most specific match
            if matched_subcategories:
                # Here you can choose how to determine the "most specific" match.
                # For example, you could sort by length of subcategory name.
                return max(matched_subcategories, key=len)

        return "Outros"  # Return "Outros" if no keywords match

    # Applying the classification function to the 'TITLE' column
    df['SUBCATEGORY'] = df['TITLE'].apply(classify_item)

    return df


def classify_editions(df):
    """
    Classifies items into editions based on provided keywords.

    :param df: DataFrame containing item data.
    :param edition_keywords: Dictionary with edition keywords.
    :return: Updated DataFrame with a new column 'EDITION'.
    """
    # Flattening the edition keywords into a single dictionary
    flat_keywords = {}
    for edition, words in edition_keywords.items():
        flat_keywords[edition] = words

    # Function to classify a single item
    def classify_edition(item):
        if isinstance(item, str):
            item_lower = item.lower()
            for edition, words in flat_keywords.items():
                pattern = '|'.join(re.escape(word.lower()) for word in words)  # Escape special characters
                if re.search(pattern, item_lower):
                    return edition.upper()  # Return the edition ID in uppercase
        return "Outros"  # Return "OUTROS" if no keywords match

    # Applying the classification function to the 'TITLE' column
    df['EDITION'] = df['TITLE'].apply(classify_edition)
    
    return df

