ipa = {
    '!',
    '\"',
    '(', ')', ',', '…',
    '-', '.', ':', ';', '?',

    'a', 'b', 'd', 'e', 'f',
    'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 's',
    't', 'u', 'w', 'x', 'y',
    'z', 'ß', 'ñ', 'ö', 'ø',
    'ü', 'ē', 'ŋ', 'ɔ', 'ə',
    'ɛ', 'ɡ', 'ɣ', 'ɪ', 'ɱ',
    'ɾ', 'ʃ', 'ʋ', 'ʍ', 'ʒ',
    'ʣ', 'ʤ', 'ʦ', 'ʧ', 'ʲ',
    'ʷ', 'ˡ', 'ⁿ',

    'ˈ', 'ː',
}

ipa_to_simpleipa = {
    'ʦ': 'c',
    'ʧ': 'č',
    'x': 'h',
    'ɪ': 'r',
    'ʋ': 'v',
    'ʃ': 'š',
    'ʒ': 'ž',
    'g': 'ɡ'
}

simple_ipa = {
    'a', 'b', 'c', 'č', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 'š',
    't', 'u', 'w', 'y', 'z', 'ž', 
    'ß', 'ñ', 'ö', 'ø', 'ü', 'ē', 'ŋ', 'ɔ', 'ə',
    'ɛ', 'ɣ', 'ɱ', 'ɾ', 'ʋ', 'ʍ',
    'ʣ', 'ʤ', 'ʲ', 'ʷ', 'ˡ', 'ⁿ',

    'ˈ', 'ː',
}

simple_punct = { '.', '!', '?', ',', '"', ':'}

simple_ipa_allowed_tokens = simple_ipa + simple_punct
simple_ipa_allowed_tokens_no_stress = simple_ipa[:-2] + simple_punct

def simplify_punct(text):
    return text.replace('(', ',').replace(')', ',').replace('', '...').replace(';', ',').replace('-', ',')


def ipa_to_simpleipa(text):
    res = ""
    for char in simplify_punct(text):
        res += ipa_to_simpleipa[char] if char in ipa_to_simpleipa else char
    return res

def ipa_extract_stress_markers(text: str):
    new_text = ""  # Initialize the new string without ":" and "'"
    stress = []  # Initialize the tones array

    i = 0  # Initialize index to walk through the text
    while i < len(text):
        if text[i] == ':':
            # If ":" is found, mark the previous character with a tone of 1
            # Assumes that ":" always follows a character in the context
            stress[-1] = 1
        elif text[i] == "'":
            # If "'" is found, prepare to mark the next character with a tone of 2
            # This is handled by inserting 2 in the tones array after the character is added
            pass
        else:
            # For normal characters, add them to the new_text
            new_text += text[i]
            # If the next character is a "'", mark this character with 2 in tones
            if i+1 < len(text) and text[i+1] == "'":
                stress.append(2)
            else:
                # Otherwise, mark it as 0
                stress.append(0)
        i += 1  # Move to the next character

    return new_text, stress

def distribute_phone(n_phone, n_word):
    phones_per_word = [0] * n_word
    for _ in range(n_phone):
        min_tasks = min(phones_per_word)
        min_index = phones_per_word.index(min_tasks)
        phones_per_word[min_index] += 1
    return phones_per_word

def ipa_calculate_length_ratio(text: str, phonetized_text: str) -> float:
    """
    Calculate the ratio of the length of the original text to its phonetized representation.

    Parameters:
    - text (str): The original text.
    - phonetized_text (str): The phonetized representation of the text.

    Returns:
    - float: The ratio of the length of the original text to its phonetized representation.
    """
    # Split both strings into lists of words
    text_words = text.split()
    phonetized_words = phonetized_text.split()

    # Ensure there is a one-to-one correspondence between the two lists of words
    if len(text_words) != len(phonetized_words):
        raise ValueError("The two strings must contain the same number of words.")

    word2ph = []
    for w, pw in zip(text_words, phonetized_words):
        word_len = len(w)
        phonetized_len = len(pw)

        aaa = distribute_phone(phonetized_len, word_len)
        word2ph += aaa

    return word2ph