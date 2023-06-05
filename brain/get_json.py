import json as j


def update(word: str, number_of_tag: int):
    number_of_tag -= 1
    f = open('brain/all_data/intents.json', 'r+', encoding='utf-8')

    d = j.load(f)
    d['intents'][number_of_tag]['patterns'].append(word)
    print(d['intents'][number_of_tag])
    f.seek(0)
    j.dump(d, f, indent=2, ensure_ascii=False)
    f.truncate()
    print('Тамом, ку барои санчиш ябори дига бугу')


def list_of_tags() -> list:
    f = open('brain/all_data/intents.json', 'r+', encoding='utf-8')
    d = j.load(f)
    f = d['intents']
    z = []
    for i in range(len(f)):
        z.append(f[i]['tag'])
    return z

