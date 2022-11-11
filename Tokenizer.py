import re

def tokenize(content: 'str') -> 'list':

    pattern = "[a-zA-Z0-9]+'?’?[a-zA-Z0-9]*"
    result = re.findall(pattern, content.lower())
    return result


# textContent = processed text from HTML
# returns (token : {position (str) : int, occurrence (str) : int})
def compute_word_frequencies(textContent:str) -> 'dict':

    token_map = dict();
    token_list = tokenize(textContent);
    stop_word_set = {'should', 'between', 'both', 'or', 'you’ve', 'all', 'let’s', "wouldn't", 'he’s', 'she’d',
                         'his', 'my', 'had', 'they’ll', 'but', 'for', "she'd", "we're", 'how’s', 'they’ve', 'about',
                         'wasn’t', 'such', "they'd", 'be', 'most', 'mustn’t', 'own', 'we’ve', 'why’s', 'again', "it's",
                         "haven't", 'we’d', 'herself', 'up', 'we’ll', 'itself', "you'd", 'if', 'not', 'shan’t', 'each',
                         'couldn’t', 'than', 'can’t', 'she’ll', "they'll", 'here', "i've", 'any', 'as', 'it’s',
                         'there’s', "you've", 'further', 'you', 'where’s', 'him', 'you’ll', 'before', 'himself',
                         'here’s', 'were', "won't", 'when’s', 'above', "shouldn't", 'cannot', 'only', "couldn't",
                         "what's", 'its', "they're", 'he’d', "there's", 'which', "who's", 'i’d', 'don’t', 'down',
                         'after', 'they’re', 'myself', "how's", "she's", 'the', 'under', 'ours', 'aren’t', "weren't",
                         'whom', 'because', 'with', 'what’s', 'didn’t', 'weren’t', "mustn't", 'that', 'some', "i'll",
                         'doing', 'haven’t', 'nor', 'them', 'they', "you'll", "that's", 'same', "aren't", 'he',
                         'hadn’t', 'so', 'i', 'me', 'when', 'having', 'yourselves', 'then', 'once', 'they’d', "he'll",
                         'will', 'their', 'we’re', 'she’s', 'has', "shan't", 'there', 'while', 'to', "she'll", 'few',
                         "he'd", 'off', 'no', 'ourselves', 'it', 'that’s', "hasn't", 'what', 'i’m', "you're", 'are',
                         'a', 'yourself', 'at', 'an', "i'd", "doesn't", 'from', 'he’ll', 'these', 'do', "can't",
                         "here's", 'did', "don't", 'ought', 'how', 'very', "i'm", 'shouldn’t', 'against', 'until',
                         'you’re', "they've", "didn't", 'have', 'would', 'over', 'theirs', 'into', 'isn’t', 'she',
                         'out', 'through', 'could', 'where', 'i’ll', 'why', 'we', 'i’ve', "he's", 'won’t', "isn't",
                         "we've", 'below', 'on', "hadn't", 'your', 'by', 'been', 'of', 'during', "why's", 'this',
                         'more', "we'd", 'doesn’t', 'is', 'does', 'in', 'our', 'being', "where's", 'am', 'was',
                         'wouldn’t', 'you’d', 'her', "when's", 'themselves', "let's", 'hers', 'those', 'hasn’t', 'who',
                         'yours', "wasn't", 'other', 'and', 'who’s', 'too', "we'll"}

    for idx, token in enumerate(token_list):
        if token in stop_word_set or len(token) < 2:
            continue
        if token in token_map.keys():
            token_map[token]["freq"] += 1
            token_map[token]["pos"].add(idx)
        else:
            init_dict = dict()
            init_dict["freq"] = 1
            init_dict["pos"] =set();
            init_dict["pos"].add(idx)
            token_map[token] = init_dict

    return token_map
