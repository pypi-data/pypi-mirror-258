import re
import obeliks

def collapse_whitespace(text):
    collapsed_text = re.sub(r'\s+', ' ', text)
    return collapsed_text

def spacePunctCleanup(text):
    i = -1
    j = -1
    out = ""
    for char in text:
        i+=1
        j+=1
        if char in punct and i > 0 and i < len(text) - 1: 
            # remove space before punctuation
            if out[j-1] == " ":
                j-=1
            out[j] = char

            # skip duplicate punctuation
            while text[i+1] == char:
                i += 1

            # force space after punctuation
            if (text[i+1] != " "):
                j+=1
                out[j] = " "
        else:
            out[j] = char

    return out



punct = "!\"$,…-.:;?"       

allowed_chars_all = " !\"#$'()*+,…-.:;?@0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzČčŠšŽžÉÍÜßàáèéíñóôöøüē"

allowed_chars_normalized = " !\",…-.:?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzČčŠšŽžÉÍÜßàáèéíñóôöøüē"

allowed_chars_min = " !\",…-.:?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzČčŠšŽž"

char_map = {
    "'": "\"",
    '–': '-',
    "'": "\"",
    "«": "\"",
    "»": "\"",
    "...": "…",
    '‚': ',',
    "›": "\"",
    "‹": "\"",
    "“": "\"",
    "”": "\"",
    "‘": "\"",
    "’": "\"",
    "–": "-",
    "—": "-",
    "Ć": "Č",
    "ć": "č",
    "ç": "c",
    "‚": "\"",
    "=": " je ",
    " ": "",
    "♥": "love",
    "●": "-",
    "": "",
    "ȇ‌": "e",
    "đ": "dž",
    '_': '-',
    "/": '-',
    'ȇ': 'e'
}



def unify_chars(text, type = 'all'):
    text = collapse_whitespace(text)
    for key, val in char_map.items():
        text = text.strip().replace(key, val)

    allowed_chars = allowed_chars_all
    if type == 'normalized':
        allowed_chars = allowed_chars_normalized
    elif type == 'min':
        allowed_chars = allowed_chars_min

    illegal = []
    for char in text:
        if char not in allowed_chars:
            print(f"illegal char: {char}")
            illegal.append(char)

    for char in illegal:
        text = text.replace(char, "")

    text = spacePunctCleanup()

    return text

def tokenize_sentences(text):
    result = obeliks.run(text, object_output=True)
    sentences = []
    for paragraph in result:
        for sentence in paragraph:
            meta = sentence["metadata"].trim().split('\n')
            for m in meta:
                parts = m.trim().split('=')
                if len(parts) == 2 and parts[0].trim() == 'text':
                    sentences.append(parts[1].trim())

    return sentences

def tokenize_word(text):
    result = obeliks.run(text, object_output=True)
    return result
    
def tokenize_char(text):
    return unify_chars(text)