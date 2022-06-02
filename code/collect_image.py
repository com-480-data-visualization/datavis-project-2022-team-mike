import requests
from util import save_dataframes, load_dataframes

def get_image(row):
    def getafter(text, substr):
        return text[text.find(substr) + len(substr):]

    def getbefore(text, substr):
        return text[:text.find(substr)]

    def test_is_valid_image(img, extension, row):
        res = getbefore(img, '.' + extension).split('/')[-1].replace('_', '').replace('-', '').replace(' ', '')
        for t in row['Name'].split(' '):
            if(t.replace('.', '') in res):
                res = res.replace(t,'')
            else:
                return False
        return len(res) == 0

    text = f"{row['Name']} {row['Platform']}"
    res = []
    for t in text.split(' '):
        if(t not in res):
            res.append(t)
    text = '+'.join(res)
    r = requests.get(f"http://logos.fandom.com/wiki/Special:Search?scope=internal&query={text}&ns%5B0%5D=6&filter=imageOnly")
    text = r.text
    first = None
    while ((len(text) > 0) and ('"unified-search__result__header"' in text)):
        if('<i>No results found.</i>' in text):
            return None
        text = getafter(text, '"unified-search__result__header"')
        text = getafter(text, '<img')
        text = getafter(text, 'src="')
        res = getbefore(text, '"')
        if(first is None):
            first = res
        for extension in ['svg', 'jpg', 'png', 'webp']:
            if(f'.{extension}' in res):
                res = getbefore(res, extension) + extension
                if test_is_valid_image(res, extension, row):
                    return res
    return first

def add_image(df):
    val = df.apply(lambda row: (f"{row['Name']} {row['Platform']} {row['Publisher']}", get_image(row)), axis=1)
    val.apply(lambda x : print(x))

df = load_dataframes("vgsales_cleand")
add_image(df.head(10))
#save_dataframes(df, "vgsales")