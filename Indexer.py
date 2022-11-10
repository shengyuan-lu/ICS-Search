# GOAL For Indexer

# Create an inverted index for the given corpus with data structures designed by you.

# Tokens: all alphanumeric sequences in the dataset.
# Stop words: do not use stopping, i.e. use all words, even the frequently occurring ones.
# Stemming: use stemming for better textual matches. Suggestion: Porter stemming.
# Important words: Words in bold, in headings (h1, h2, h3), and in titles should be treated as more important than the other words.


# IMPORT OTHER CLASSES HERE
from Reader import Reader

if __name__ == '__main__':
    reader = Reader('DEV')
