import re
from nltk.stem import PorterStemmer


def tokenize(content: 'str') -> 'list':

    content = content.lower()

    pattern = "[a-zA-Z0-9]+'?’?[a-zA-Z0-9]*"
    email_pattern = r"([a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+)"
    tel_pattern = r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))"

    result = re.findall(pattern, content)
    emails = re.findall(email_pattern, content)
    tels = re.findall(tel_pattern, content)

    return result + emails + tels


# textContent = processed text from HTML
# returns (token : {position (str) : int, occurrence (str) : int})
def compute_word_frequencies(text_content: list) -> 'dict':
    ps = PorterStemmer()
    token_map = dict()
    special_map = dict() # word: freq
    weight_map = {0:10, 1:5, 2:4, 3:3, 4:2, 5:2, 6:2, 7:1}

    for index, text in enumerate(text_content):
        token_list = tokenize(text)

        for idx, token in enumerate(token_list):
            if len(token) > 3:
                token = ps.stem(token)

            if token in token_map.keys():
                token_map[token]['freq'] += weight_map[index]
                token_map[token]['pos'].add(idx)

                if index != 7:
                    special_map[token] += 1
            else:
                init_dict = dict()
                init_dict['freq'] = weight_map[index]
                init_dict['pos'] = set()
                init_dict['pos'].add(idx)
                token_map[token] = init_dict

                if index != 7:
                    special_map[token] = 1

    for key, val in special_map.items():
        token_map[key]['freq'] -= val

    return token_map
