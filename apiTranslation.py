import requests
import json

ApiKey= 'OTI0MzFhYWMtMWJiMC00NzRjLTk2YzktNDcxNTUwYjBmYjQ0OjgzNmFjZWFhOGQ0ZDRiZWVhNTAxMDliNmU0NmJhZDdh'
url_param = 'https://developers.lingvolive.com/api/v1.1/authenticate'
header_params = {
    'Authorization': 'Basic OTI0MzFhYWMtMWJiMC00NzRjLTk2YzktNDcxNTUwYjBmYjQ0OjgzNmFjZWFhOGQ0ZDRiZWVhNTAxMDliNmU0NmJhZDdh'
}
response = requests.post(
    url_param,
    headers = header_params
)
if response.status_code != 200:
    print('Error occured')
token = response.text


def initiateTranslation(txt, srcLang, dstLang):
    header_params_new = {
        'Authorization': f'Bearer {token}'
    }
    params_new = {
        'text': str(txt),
        'srcLang': str(srcLang),
        'dstLang': str(dstLang),
    }
    url1 ='https://developers.lingvolive.com/api/v1/Minicard'
    response_new = requests.get(
        url=url1,
        params=params_new,
        headers=header_params_new
    )
    if response_new.status_code == 200:
        x = json.loads(response_new.text)
        return f"{x['Translation']['Heading']} => {x['Translation']['Translation']}"
    else:
        return 'Перевод не найдён'
def findSpelling(txt):
    fileName = txt+'.wav'
    dictionaryName = 'LingvoUniversal (En-Ru) 1033→1049'
    header_params_new = {
        'Authorization': f'Bearer {token}'
    }
    params_new = {
        'dictionaryName': dictionaryName,
        'fileName': fileName
    }
    response_new = requests.get(
        url='https://developers.lingvolive.com/api/v1/Sound',
        headers=header_params_new,
        params=params_new
    )
    if response_new.status_code == 200:
        return json.loads(response_new.text)
if __name__ == '__main__':
    word = input('Введите слово на англ для перевода ')
    bruh = findSpelling(word)
    print(bruh)
    print('Скрипт запущен мануально')