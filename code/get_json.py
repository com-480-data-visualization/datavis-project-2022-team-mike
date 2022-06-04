from time import time
from util import save_dataframes, load_dataframes
import ast


def get_idx(param, key):
    for i in range(len(param['children'])):
        if(param['children'][i]['Name'] == key):
            return i
    return -1


def add_json(path, filename):
    global i, d, t, param, map_
    param = {}
    param["name"] = ""
    param["color"] = "rgb(255,255,255)"
    param["img"] = ""
    df = load_dataframes(path)
    i = 0
    d = 0
    n = len(df)
    t = time()

    f = open("../data/img.py", "r")

    map_ = ast.literal_eval(f.read())
    f.close()

    def json(row):
        global i, d, t, param, map_

        Meta_score = float(row['Meta_score'])
        User_score = float(row['User_score'])
        NA_Sales = float(row['NA_Sales'])
        EU_Sales = float(row['EU_Sales'])
        JP_Sales = float(row['JP_Sales'])
        Other_Sales = float(row['Other_Sales'])
        Global_Sales = float(row['Global_Sales'])

        if(Meta_score != Meta_score):
            Meta_score = -1
        if(User_score != User_score):
            User_score = -1
        if(NA_Sales != NA_Sales):
            NA_Sales = -1
        if(EU_Sales != EU_Sales):
            EU_Sales = -1
        if(JP_Sales != JP_Sales):
            JP_Sales = -1
        if(Other_Sales != Other_Sales):
            Other_Sales = -1
        if(Global_Sales != Global_Sales):
            Global_Sales = -1

        c = param

        if('children' not in c):
            c['children'] = []

        idx = get_idx(c, str(row['Platform']))
        if(idx < 0):
            idx = len(c['children'])
            c['children'].append({})

        c = c['children'][idx]
        if('Name' not in c):
            c['Name'] = str(row['Platform']).replace(
                "\"", "'").replace("'", "\\\"")
            c['Meta_score'] = max(0,  Meta_score)
            c['User_score'] = max(0,  User_score)
            c['NA_Sales'] = max(0,  NA_Sales)
            c['EU_Sales'] = max(0,  EU_Sales)
            c['JP_Sales'] = max(0,  JP_Sales)
            c['Other_Sales'] = max(0,  Other_Sales)
            c['Global_Sales'] = max(0,  Global_Sales)
            c['NB'] = 1
            c['color'] = 'rgb(255,255,255)'
            c['img'] = map_['Platform'][row['Platform']] if((
                row['Platform'] in map_['Platform']) and (map_['Platform'][row['Platform']] is not None)) else ""
        else:
            c['Meta_score'] += max(0, Meta_score)
            c['User_score'] += max(0, User_score)
            c['NA_Sales'] += max(0, NA_Sales)
            c['EU_Sales'] += max(0, EU_Sales)
            c['JP_Sales'] += max(0, JP_Sales)
            c['Other_Sales'] += max(0, Other_Sales)
            c['Global_Sales'] += max(0, Global_Sales)
            c['NB'] += 1

        if('children' not in c):
            c['children'] = []

        idx = get_idx(c, str(row['Publisher']))
        if(idx < 0):
            idx = len(c['children'])
            c['children'].append({})

        c = c['children'][idx]
        if('Name' not in c):
            c['Name'] = str(row['Publisher']).replace(
                "\"", "'").replace("'", "\\\"")
            c['Meta_score'] = max(0, Meta_score)
            c['User_score'] = max(0, User_score)
            c['NA_Sales'] = max(0, NA_Sales)
            c['EU_Sales'] = max(0, EU_Sales)
            c['JP_Sales'] = max(0, JP_Sales)
            c['Other_Sales'] = max(0, Other_Sales)
            c['Global_Sales'] = max(0, Global_Sales)
            c['NB'] = 1
            c['color'] = 'rgb(255,255,255)'
            c['img'] = map_['Publisher'][row['Publisher']] if((
                row['Publisher'] in map_['Publisher']) and (map_['Publisher'][row['Publisher']] is not None)) else ""
            while((len(c['img']) > 0) and not(
                    c['img'].endswith(".jpg") or
                    c['img'].endswith(".png") or
                    c['img'].endswith(".svg"))):
                c['img'] = c['img'][:-1]
        else:
            c['Meta_score'] += max(0, Meta_score)
            c['User_score'] += max(0, User_score)
            c['NA_Sales'] += max(0, NA_Sales)
            c['EU_Sales'] += max(0, EU_Sales)
            c['JP_Sales'] += max(0, JP_Sales)
            c['Other_Sales'] += max(0, Other_Sales)
            c['Global_Sales'] += max(0, Global_Sales)
            c['NB'] += 1

        if('children' not in c):
            c['children'] = []

        idx = len(c['children'])
        c['children'].append({})
        c = c['children'][idx]

        c['Name'] = str(row['Name']).replace("\"", "'").replace("'", "\\\"")
        c['Meta_score'] = Meta_score
        c['User_score'] = User_score
        c['NA_Sales'] = NA_Sales
        c['EU_Sales'] = EU_Sales
        c['JP_Sales'] = JP_Sales
        c['Other_Sales'] = Other_Sales
        c['Global_Sales'] = Global_Sales
        c['color'] = 'rgb(255,255,255)'
        if(row['img'] != row['img']):
            c['img'] = ''
        else:
            c['img'] = str(row['img'])

        i += 1
        dt = time() - t
        if(i-d > 0):
            print(f'{((i-d)*1000 // (n-d))/10 }% ({round(dt, 2)}s : {round(((n-d) - (i-d)) * dt / (i-d), 2)}s = {round((n-d) * dt / (i-d), 2)}s)         ', end='\r')
        pass

    df.apply(json, axis=1)

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

    file = file.replace("'", '"').replace(
        "\\\\\"", "'").replace('"Name": nan', '"Name": ""')
    f = open(filename, "w", encoding="utf8")
    f.write(file)
    f.close()


add_json("merged_sales_ratings_img", "../data/bubble.json")
