import requests
from time import time
from util import save_dataframes, load_dataframes

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

    def test_is_valid_image(img, extension, row):
        """
        Returns if the image is valid
        """
        res = getbefore(
            img, '.' + extension).split('/')[-1].replace('_', '').replace('-', '').replace(' ', '')
        for t in row['Name'].split(' '):
            if(t.replace('.', '') in res):
                res = res.replace(t, '')
            else:
                return False
        return len(res) == 0

    text = f"{row['Name']} {row['Platform']}"
    res = []
    for t in text.split(' '):
        if(t not in res):
            res.append(t)
    text = '+'.join(res)

    #Get html 
    r = requests.get(
        f"http://logos.fandom.com/wiki/Special:Search?scope=internal&query={text}&ns%5B0%5D=6&filter=imageOnly")
    text = r.text

    first = None
    while ((len(text) > 0) and ('"unified-search__result__header"' in text)):
        if('<i>No results found.</i>' in text):
            return None
        #Get Link
        text = getafter(text, '"unified-search__result__header"')
        text = getafter(text, '<img')
        text = getafter(text, 'src="')
        res = getbefore(text, '"')

        #Check if Link is valid
        for extension in ['svg', 'jpg', 'png', 'webp']:
            if(f'.{extension}' in res):
                res = getbefore(res, extension) + extension
                if(first is None):
                    first = res
                if test_is_valid_image(res, extension, row):
                    return res
    return first


def add_image(path):
    """
    Add image to the dataframe in the given path
    """
    global i, d, t, df
    df = load_dataframes(path)
    i = 0
    d = 0
    n = len(df)
    t = time()

    def img(row):
        """
        Add image for a given row
        """
        global i, d, t, df
        if((df["img"][i] is None) or (df["img"][i] != df["img"][i])):
            df["img"][i] = get_image(row)
            if(i % 100 == 0):
                save_dataframes(df, path + '.tmp')
                save_dataframes(df, path)
        else:
            d += 1
            t = time()
        i += 1
        dt = time() - t
        if(i-d > 0):
            print(f'{((i-d)*1000 // (n-d))/10 }% ({round(dt, 2)}s : {round(((n-d) - (i-d)) * dt / (i-d), 2)}s = {round((n-d) * dt / (i-d), 2)}s)         ', end='\r')
        pass

    df.apply(img, axis=1)


add_image("merged_sales_ratings_img")
