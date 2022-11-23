from Reader import Reader, NoMoreFilesToReadException
from bs4 import BeautifulSoup
from Tokenizer import compute_word_frequencies


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

    # Turn the raw html into tokenizable text

    # title
    # h1
    # h2
    # h3
    # strong
    # b
    # em

    # body (not a tag)

    # Check if the html is valid
    if BeautifulSoup(content, 'html.parser').find():

        # Get a soup object with parsed content using html.parser
        soup = BeautifulSoup(content, 'html.parser')

        # A list of special tags
        special_tags = ['h1', 'h2', 'h3', 'strong', 'b', 'em']

        # Find all special tags
        tags = soup.find_all(special_tags)

        # print(tags)

        # Init strings contains special tags

        h1 = ''
        h2 = ''
        h3 = ''
        strong = ''
        b = ''
        em = ''

        # For each special tags, append the corresponding string
        for tag in tags:
            match tag.name:
                case 'h1':
                    h1 += tag.text.strip() + ' '
                case 'h2':
                    h2 += tag.text.strip() + ' '
                case 'h3':
                    h3 += tag.text.strip() + ' '
                case 'strong':
                    strong += tag.text.strip() + ' '
                case 'b':
                    b += tag.text.strip() + ' '
                case 'em':
                    em += tag.text.strip() + ' '

        # Get everything
        body = soup.get_text().strip()

        return doc_id, url, [h1.strip(), h2.strip(), h3.strip(), strong.strip(), b.strip(), em.strip(), body.strip()]

    else:

        # Return a list with empty strings if the content is not valid html
        return doc_id, url, ['', '', '', '', '', '', '', '']


if __name__ == '__main__':

    reader = Reader('DEV_SMALL')

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