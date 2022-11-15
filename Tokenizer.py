import re
from nltk.stem import PorterStemmer
def tokenize(content: 'str') -> 'list':

    pattern = "[a-zA-Z0-9]+'?’?[a-zA-Z0-9]*"
    result = re.findall(pattern, content.lower())
    return result


# textContent = processed text from HTML
# returns (token : {position (str) : int, occurrence (str) : int})
def compute_word_frequencies(textContent:str) -> 'dict':
    ps = PorterStemmer()
    token_map = dict()
    token_list = tokenize(textContent)

    for idx, token in enumerate(token_list):
        token = ps.stem(token)

        if token in token_map.keys():
            token_map[token]["freq"] += 1
            token_map[token]["pos"].add(idx)
        else:
            init_dict = dict()
            init_dict["freq"] = 1
            init_dict["pos"] = set()
            init_dict["pos"].add(idx)
            token_map[token] = init_dict

    return token_map
