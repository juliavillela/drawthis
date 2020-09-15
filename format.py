import re

#takes in a string formated as array
#and returns clean array of strings
def str_arr(str_arr):
    if str_arr:
        csv = str_arr
        for c in ["'", "[", "]"]:
            csv = csv.replace(c, "")
        array = csv.split(",")
        return array
    else:
        return []

#joins an array of strings in db format
def join(array):
    if array:
        s = "%"
        return s.join(array)
    else:
        return ""

#splits db string into array of strings
def split(string):
    if string:
        array = string.split("%")
        return array
    else:
        return []

def cards_imd(imd):
    cards =[]
    for item in imd:
        if re.search("card", item):
            card = imd.get(item);
            if len(card) > 0 :
                cards.append(card)
    string = join(cards)
    return string

def filter_in_text(string):
    for old, new in [("'", "''")]:
        string.replace(old, new)

def filter_out_text(string):
    for old, new in [("'", "''")]:
        string.replace(old, new)
