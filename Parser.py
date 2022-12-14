from Reader import Reader
from bs4 import BeautifulSoup


# parse(file : (int, json_dict)): -> (doc_id : int, url : str, tag_list : list)
def parse(file: (int, dict)) -> (int, str, list):
    """
    Parses the loaded html file, extracting the url and raw text
    """
    # Get the doc id from file
    doc_id = file[0]

    # Get the json from the loaded file, as a dict
    json = file[1]

    # Get the url
    url = json['url']

    # Get the raw html content
    content = json['content']

    # Check if the html is valid
    if BeautifulSoup(content, 'html.parser').find():

        # Get a soup object with parsed content using html.parser
        soup = BeautifulSoup(content, 'html.parser')

        # A list of special tags
        special_tags = ['title', 'h1', 'h2', 'h3', 'strong', 'b', 'em']

        # Find all special tags
        tags = soup.find_all(special_tags)

        # print(tags)

        # Init strings contains special tags

        # Turn the raw html into tokenizable text

        # title
        # h1
        # h2
        # h3
        # strong
        # b
        # em

        # body (not a tag)

        title = ''
        h1 = ''
        h2 = ''
        h3 = ''
        strong = ''
        b = ''
        em = ''

        # For each special tags, append the corresponding string
        for tag in tags:

            text = text_processing(tag.text)

            if tag.name == 'title':
                title += text + ' '
            elif tag.name == 'h1':
                h1 += text + ' '
            elif tag.name == 'h2':
                h2 += text + ' '
            elif tag.name == 'h3':
                h3 += text + ' '
            elif tag.name == 'strong':
                strong += text + ' '
            elif tag.name == 'b':
                b += text + ' '
            elif tag.name == 'em':
                em += text + ' '

        # Get everything
        body = text_processing(soup.get_text().strip())

        return doc_id, url, [title.strip(), h1.strip(), h2.strip(), h3.strip(), strong.strip(), b.strip(), em.strip(), body.strip()]

    else:
        # Return a list with empty strings if the content is not valid html
        return doc_id, url, ['', '', '', '', '', '', '', '', '']


def text_processing(text: str) -> str:
    text = text.strip()
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    text = text.replace('\u00a0', '')
    text = text.replace('\u2019', '')

    return text


if __name__ == '__main__':

    reader = Reader('TEST')

    """
    # reader.print_not_processed_sub_folders()
    # reader.print_not_processed_files_in_current_sub_folder()

    try:
        while True:
            file = reader.get_next_file()
            doc_id, url, raw_text = parse(file)
            print('url:', url)
            print(compute_word_frequencies(raw_text))

    except NoMoreFilesToReadException as e:
        print(e)
        
    """

    print(parse(reader.get_next_file()))