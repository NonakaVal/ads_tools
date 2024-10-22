import re

keywords = {
    'sony': {
        'playstation': [
            'playstation', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'psp', 'vita', 'sony'
        ],
        'controllers': [
            'dualshock', 'remote', 'joystick', 
             'controle', 'controller'
        ],
        'accessories': [
            'memory', 'camera', 'charger', 'adapter', 'stand', 'cover', 'bundle', 'skin',
            'cable', 'charging', 'dock', 'strap', 'headset', 'faceplate', 'vertical'
        ]
    },
    'nintendo': {
        'items': [
            'nintendo', 'famicom','gameboy', 'gamecube', 'cube'
        ],
        'games': [
            'mario', 'zelda', 'kirby', 'pokemon', 'metroid', 'link', 'yoshi', 'smash', 'bros',
            'donkey', 'kong', 'animal', 'crossing', 'splatoon', 'star', 'fox', 'fire', 'emblem',
            'luigi', 'tetris', 'bayonetta', 'xenoblade', 'paper', 'warioware', 'punch-out',
            'super', 'kart', 'advance', 'world'
        ],
        'accessories': [
            'amiibo', 'charger', 'dock', 'strap', 'screen', 'protector', 'bag', 'adapter',
            'stand', 'battery', 'card', 'memory', 'case', 'cable', 'pad', 'pak'
        ]
    },
    'sega': {
        'items': [
            'sega', 'saturn', 'genesis', 'dreamcast', 'megadrive', 'master', 'system', 
            'game', 'gear', 'sega cd', '32x'
        ],
        'controllers': [
            'controller', 'joystick', 'arcade', 'pad', 'stick', 'gamepad', 'remote'
        ],
        'games': [
            'sonic', 'virtua', 'fighter', 'streets', 'of', 'rage', 'golden', 'axe', 'shining',
            'force', 'yakuza', 'shenmue', 'phantasy', 'star', 'jet', 'set', 'radio', 'house',
            'dead', 'crazy', 'taxi', 'space', 'channel', 'nights', 'rez'
        ],
        'accessories': [
            'memory', 'cd', 'adapter', 'charger', 'battery', 'case', 'cable', 'cartridge',
            'stand'
        ]
    },
    'microsoft': {
        'games-': [
            'xbox', '360', 'xbox360', 'xbox one', 'xbox series', 'one s', 'one x', 'series s', 'series x', 
            'microsoft','Halo 4 Limited Edition Xbox 360 Versão Japonesa'
        ],
        'controllers': [
            'controller', 'remote', 'elite', 'gamepad', 'wireless', 'arcade', 'stick', 'adaptive',
            'charge', 'kit', 'wired', 'thumbstick'
        ],
        'accessories': [
            'headset', 'battery', 'charger', 'dock', 'case', 'skin', 'stand', 'camera', 
            'kinect', 'cable', 'adapter', 'stereo', 'chat', 'keyboard'
        ]
    }
}

        # Dicionário de palavras-chave para as edições
edicoes_keywords = {
    'standart': [
        'standard', 'standart', 'normal', 'regular'
    ],
    'limited': [
        'limited', 'edição limitada', 'limitada',
    ],
    '': [
        'japonesa', 'japan', 'limited edition japonesa','jp'
    ],
    'Collectors Edition': ['collectors edition','collectors',]
}

def classify_editions(df, edition_keywords):
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
        return "OUTROS"  # Return "OUTROS" if no keywords match

    # Applying the classification function to the 'TITLE' column
    df['EDITION'] = df['TITLE'].apply(classify_edition)
    
    return df

def classify_items(df, detailed_keywords):
    """
    Classifies items into subcategories based on provided keywords,
    ignoring case differences, using regular expressions.

    :param df: DataFrame containing item data.
    :param detailed_keywords: Detailed dictionary with categories, subcategories, and keywords.
    :return: Updated DataFrame with a new column 'Subcategoria'.
    """
    # Flattening the detailed keywords into a single dictionary mapping subcategory names to keywords
    flat_keywords = {}
    for category, subcategories in detailed_keywords.items():
        for subcategory, words in subcategories.items():
            flat_subcategory = f"{category}_{subcategory}"
            if flat_subcategory not in flat_keywords:
                flat_keywords[flat_subcategory] = []
            flat_keywords[flat_subcategory].extend(words)
    
    # Function to classify a single item
    def classify_item(item):
        # Check if the item is a string and convert to lowercase
        if isinstance(item, str):
            item_lower = item.lower()
            for subcategory, words in flat_keywords.items():
                # Build a regex pattern for each subcategory
                pattern = '|'.join(re.escape(word.lower()) for word in words)  # Escape special characters
                if re.search(pattern, item_lower):  # Search for the regex pattern in the item
                    return subcategory
        return "Outros"  # Return "Outros" if no keywords match

    # Applying the classification function to the 'TITLE' column
    df['SUBCATEGORY'] = df['TITLE'].apply(classify_item)
    
    return df

