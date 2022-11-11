from Reader import Reader, NoMoreFilesToReadException
from bs4 import BeautifulSoup


# parse(file : (int, json_dict)): -> (url : str, html_text : str, doc_id : int)
def parse(file: (int, dict)) -> (int, str, str):
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
        # The html parser *should* handle errors in the html.
        # Any errors BeautifulSoup decided were worth throwing
        # Probably are
    text = soup.get_text().strip()

    out = (doc_id, url, text)
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
            print(parse(file))
            # break
            # print()

    except NoMoreFilesToReadException as e:
        print(e)
