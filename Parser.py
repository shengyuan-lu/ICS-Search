from Reader import Reader, NoMoreFilesToReadException
from bs4 import BeautifulSoup
from Tokenizer import compute_word_frequencies


# parse(file : (int, json_dict)): -> (url : str, html_text : str, doc_id : int)
def parse(file: (int, dict)) -> (int, str, str):
    """
    Parses the loaded html file, extracting the url and raw text
    """
    # Get the doc id from file
    doc_id = file[0]

    # Get the json from the loaded file, as a dict
    json = file[1]

    # Get the url
    url = json["url"]

    # Get the raw html content
    content = json["content"]

    # Turn the raw html into tokenizable text

    # Check if the html is valid
    if BeautifulSoup(content, "html.parser").find():

        soup = BeautifulSoup(content, "html.parser")

        text = soup.get_text().strip()

        # Return the doc_id, url, the raw text content
        out = (doc_id, url, text)

        return out

    else:
        out = (doc_id, url, '')

        return out


if __name__ == '__main__':
    reader = Reader('DEV')

    # reader.print_not_processed_sub_folders()
    # reader.print_not_processed_files_in_current_sub_folder()

    try:
        while True:
            file = reader.get_next_file()
            doc_id, url, raw_text = parse(file)
            print("url:", url)
            print(compute_word_frequencies(raw_text))

    except NoMoreFilesToReadException as e:
        print(e)