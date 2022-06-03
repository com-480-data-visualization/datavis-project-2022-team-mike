import requests
from time import time
from util import save_dataframes, load_dataframes


def get_image(text):
    def getafter(text, substr):
        return text[text.find(substr) + len(substr):]

    def getbefore(text, substr):
        return text[:text.find(substr)]

    def test_is_valid_image(img, extension, name):
        res = getbefore(
            img, '.' + extension).split('/')[-1].replace('_', '').replace('-', '').replace(' ', '')
        for t in name.split(' '):
            if(t.replace('.', '') in res):
                res = res.replace(t, '')
            else:
                return False
        return len(res) == 0

    res = []
    for t in str(text).split(' '):
        if(t not in res):
            res.append(t)
    text = '+'.join(res)
    r = requests.get(
        f"http://logos.fandom.com/wiki/Special:Search?scope=internal&query={text}&ns%5B0%5D=6&filter=imageOnly")
    tmp = r.text

    text = tmp
    first = None
    while ((len(text) > 0) and ('"unified-search__result__header"' in text)):
        if('<i>No results found.</i>' in text):
            return None
        text = getafter(text, '"unified-search__result__header"')
        text = getafter(text, '<img')
        text = getafter(text, 'src="')
        res = getbefore(text, '"')
        for extension in ['svg', 'jpg', 'png', 'webp']:
            if(f'.{extension}' in res):
                res = getbefore(res, extension) + extension
                if(first is None):
                    first = res
                if test_is_valid_image(res, extension, text):
                    return res

    text = tmp
    if('"unified-search__community__image"' in text):
        text = getafter(text, '"unified-search__community__image"')
        text = getafter(text, 'data-thumbnail="')
        res = getbefore(text, '"')
        for extension in ['svg', 'jpg', 'png', 'webp']:
            if(f'.{extension}' in res):
                return res.replace("&amp;", "&")
    return first


def add_image(path, filename):
    df = load_dataframes(path)
    publisher = {}
    platform = {}

    for p in df["Publisher"].unique():
        publisher[p] = get_image(p)

    for p in df["Platform"].unique():
        platform[p] = ''#get_image(p)

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
