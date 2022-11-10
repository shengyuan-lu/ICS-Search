from Reader import Reader, NoMoreFilesToReadException
from bs4 import BeautifulSoup
from tokenizer import compute_word_frequencies


# parse(json : str): -> (url : str, html_text : str, doc_id : int)
def parse(file: str) -> (str, str, int):
    """
    Parses the loaded html file, extracting the url and raw text
    """
    # Get the json from the loaded file, as a dict
    json = file[1]
    # Get the url
    url = json["url"]
    doc_id = file[0]

    # Get the raw html content
    content = json["content"]

    # Turn the raw html into tokenizable text
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text().strip()

    out = (url, text, doc_id)
    # Return the url, the raw text content, and the doc_id
    # In that order
    return out


if __name__ == '__main__':
    reader = Reader('DEV')

    # reader.print_not_processed_sub_folders()
    # reader.print_not_processed_files_in_current_sub_folder()

    try:
        while True:
            file = reader.get_next_file()
            url, raw_text, doc_id = parse(file)
            # break
            print(compute_word_frequencies(raw_text))

    except NoMoreFilesToReadException as e:
        print(e)
