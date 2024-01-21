import requests
from bs4 import BeautifulSoup
import re
import json
user_agent = {'User-agent': 'Mozilla/7.0'} #сайт думает что запрос от юзера а не от бота
def get_and_verify_url(url): 
    regx = re.compile(r'(?:https:\/\/)?(?:www\.)?dotabuff\.com\/players\/(\d+)(?:\/matches)?')
    res = re.match(regx, url)
    try:
        fixed_url = f"https://www.dotabuff.com/players/{res.group(1)}/matches"
    except:
        return (-1, throw_error('Invalid link'))
    page = get_page(fixed_url)
    soup = BeautifulSoup(page.text, features='html.parser')
    if soup.find('i', class_='fa fa-lock') and soup.find('i', class_='fa fa-lock')['title'] == 'This profile is private':
        return (-1, throw_error('This profile is private'))
    elif res.group(1) == '':
        return (-1, throw_error('Invalid link'))
    else:
        return (0, soup)
def throw_error(stroka):
    return f"The error has occured: {stroka}"
def format_the_string(stroka):
    if stroka[0] == 'x':
        return stroka[2:]
    return stroka
def get_page(url):
    page = requests.get(url, headers = user_agent)
    return page
def get_matches(Soupp):
    soup = Soupp[1]
    arr = []
    for elem in soup.find_all('td', class_='cell-large'):
        arr.append(
            [
            f"www.dotabuff.com{elem.find('a').get('href')}",
            elem.find('a').get_text(),
            elem.find('div', class_='subtext').get_text(),
            ]
        )
    k=0
    for elem in soup.find_all('td', class_=''):
        x = elem.find('a', class_=re.compile("won|lost|abandoned"))
        reg_duration = re.compile(r'(\d)?\d:\d\d(:\d\d)?')
        reg_kda = re.compile(r'(\d){1,3}\/(\d){1,3}\/(\d){1,3}')
        y = elem.get_text()
        kda = re.match(reg_kda, y)
        duration = re.match(reg_duration, y)
        if kda != None:
            arr[k-1].append(kda[0])
        if duration != None:
            arr[k].append(duration[0])
            k+=1
        if x is not None and k<=49:
            arr[k].append(x.get_text())
    k=0
    for elem in soup.find('tbody').find_all('td', class_='r-none-mobile'):
        if 'Ranked' in elem.get_text():
            arr[k].append('Ranked') 
            arr[k].append(format_the_string(elem.get_text().split('Ranked')[1]))
            k+=1
        elif 'Normal' in elem.get_text():
            arr[k].append('Normal') 
            arr[k].append(format_the_string(elem.get_text().split('Normal')[1]))
            k+=1
        elif 'Battle Cup' in elem.get_text():
            arr[k].append('Ranked') 
            arr[k].append(format_the_string(elem.get_text().split('Battle Cup')[1]))
            k+=1
    return arr
def load_data(filepath):
    try:
        with open(filepath, "r") as f:
            database = json.load(f)
            return database
    except:
        return {}
def save_data(filepath, db):
    with open(filepath, "w") as f:
        json.dump(db, f)
def match_info(arr_of_str):
    link, character, rank, WorL, duration, KDA, normranked, regime = arr_of_str
    #'link', 'Lion', 'Immortal', 'Won Match', '27:18', '5/3/14', 'Ranked', 'All Pick'
    return f"<b>{character}</b>\n{WorL} {KDA} <i>{duration}</i> \n{normranked} {regime} <b>{rank}</b> \n<u>{link}</u>"
if __name__ == '__main__':
    arr = get_matches(get_and_verify_url())
    for elem in arr:
        print(elem)
