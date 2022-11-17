# GOAL For Indexer

# Create an inverted index for the given corpus with data structures designed by you.

# Tokens: all alphanumeric sequences in the dataset.
# Stop words: do not use stopping, i.e. use all words, even the frequently occurring ones.
# Stemming: use stemming for better textual matches. Suggestion: Porter stemming.
# Important words: Words in bold, in headings (h1, h2, h3), and in titles should be treated as more important than the other words.


# IMPORT OTHER CLASSES HERE
from Reader import Reader, NoMoreFilesToReadException
from Memory import Memory
from Parser import parse
from Tokenizer import compute_word_frequencies
import os
import shutil


def run(base_folder):
    reader = Reader(base_folder)
    memory = Memory()

    path = 'Index'

    # Remove the folder and its content if already exist
    if os.path.exists(path):
        shutil.rmtree(path)

    # Create the folder
    os.mkdir(path)

    try:
        while True:
            file = reader.get_next_file()

            doc_id, url, raw_text = parse(file)

            frequencies = compute_word_frequencies(raw_text)

            memory.add_page(frequencies, doc_id)

    except NoMoreFilesToReadException as e:
        print(e)

    # Write index to disk
    memory.store_to_disk()

    # Print the stats
    memory.print_stats()

    # Write a doc_id : url dic on disk
    reader.write_doc_id_dict()

if __name__ == '__main__':
    run('DEV')
