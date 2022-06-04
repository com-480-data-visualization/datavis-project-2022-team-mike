import requests
from util import load_dataframes

def get_image(row):
    """
    Returns the URL of the most likely image
    """
    def getafter(text, substr):
        """
        Returns the string after the substr
        """
        return text[text.find(substr) + len(substr):]

    def getbefore(text, substr):
        """
        Returns the string before the substr
        """
        return text[:text.find(substr)]

    #Get html
    text.replace(" ", "_")
    r = requests.get(
        f"http://fr.wikipedia.org/wiki/{text}")
    text = r.text
    if("Wikipédia ne possède pas d'article avec ce nom." in text):
        return ''

    #Get image URL
    text = getafter(text, 'class="infobox infobox_v2"')
    text = getafter(text, '<img')
    text = getafter(text, 'src="')
    res = getbefore(text, '"')
    if(res.startswith('//upload.wikimedia.org')):
        return f"https:{res}"
    return ''


def add_image(path, filename):
    """
    Add image from the dataframe in the given path to the given filename
    """
    df = load_dataframes(path)
    publisher = {}
    platform = {}

    #Get image of Publisher
    val = df["Publisher"].unique()
    i = 0
    n = len(val)
    for p in val:
        publisher[str(p)] = get_image(str(p))
        i += 1
        print(f'{i*1000 // n/10 }%', end = '\r')

    #Get image of Platform
    val = df["Platform"].unique()
    i = 0
    n = len(val)
    for p in val:
        platform[str(p)] = get_image(str(p))
        i += 1
        print(f'{i*1000 // n/10 }%', end = '\r')

    #Save the results in file
    param = {
        "Publisher": publisher,
        "Platform": platform
    }

    result = (str(param)
              .replace('], ', '],\n')
              .replace('}', '\n}')
              .replace('}, ', '},\n')
              .replace("[[", "[\n[")
              .replace("[{", "[\n{")
              .replace("]]", "]\n]")
              .replace("}]", "}\n]")
              .replace("['", "[\n'")
              .replace("{'", "{\n'")
              .replace(" '", "\n'")
              .replace('\n\n', '\n')
              .replace(':\n', ':')
              ).split('\n')

    file = ""
    i = 0
    for l in result:
        if(l.endswith('}') or l.endswith(']') or l.endswith('},') or l.endswith('],')):
            i -= 1
        if(l.startswith('[') and (l.endswith(']') or l.endswith('],'))):
            i += 1
        file += ('\t' * i) + l + '\n'
        if(l.startswith('[') and (l.endswith(']') or l.endswith('],'))):
            i -= 1
        if((l.startswith('{') or l.startswith('[') or l.endswith('{') or l.endswith('['))):
            i += 1

    f = open(filename, "w", encoding="utf8")
    f.write(file)
    f.close()


add_image("merged_sales_ratings_img", "../data/img.py")
