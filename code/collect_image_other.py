import requests
from time import time
from util import save_dataframes, load_dataframes


def get_image(text):
    def getafter(text, substr):
        return text[text.find(substr) + len(substr):]

    def getbefore(text, substr):
        return text[:text.find(substr)]

    text.replace(" ", "_")
    r = requests.get(
        f"http://fr.wikipedia.org/wiki/{text}")
    text = r.text
    if("Wikipédia ne possède pas d'article avec ce nom." in text):
        return ''

    text = getafter(text, 'class="infobox infobox_v2"')
    text = getafter(text, '<img')
    text = getafter(text, 'src="')
    res = getbefore(text, '"')
    if(res.startswith('//upload.wikimedia.org')):
        return f"https:{res}"
    return ''


def add_image(path, filename):
    df = load_dataframes(path)
    publisher = {}
    platform = {}

    val = df["Publisher"].unique()
    i = 0
    n = len(val)
    for p in val:
        publisher[str(p)] = get_image(str(p))
        i += 1
        print(f'{i*1000 // n/10 }%', end = '\r')

    val = df["Platform"].unique()
    i = 0
    n = len(val)
    for p in val:
        platform[str(p)] = get_image(str(p))
        i += 1
        print(f'{i*1000 // n/10 }%', end = '\r')

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
