import pandas as pd

from tabulate import tabulate

data = '[Кистоун Лоджистикс, 4179, 193, 37, Лэндинги, 79, 3, 0, Арбилегал, 2, 3, 3, AURORA, 6, 1, 1, Инженерное Дело, 8, 4, 0, Северо-западный битумный терминал, 3, 0, 1, Веселая улыбка, 18, 19, 4, ЭмСиЭнЭс Полеуретан РУС, 24, 19, 1, Симпейс, 3, 9, 0]'
data = data.replace("]", "")
data = data.replace("[", "")
data = data.replace(" ", "")
result = data.split(",")


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]


lists = split_list(result, wanted_parts=9)
lenght = len(lists)

table = {}

for i in range(lenght):
    pool = lists[i]
    table[i] = pool

headers = ["Название", "Заявки", "Сотрудников", "Регламентные работы"]

df = pd.DataFrame({
        'country': ['Kazakhstan', 'Russia', 'Belarus', 'Ukraine'],
        'population': [17.04, 143.5, 9.5, 45.5],
        'square': [2724902, 17125191, 207600, 603628]
})
print(df)


#print(tabulate([table[0], table[1], table[2], table[3], table[4], table[5], table[6], table[7], table[8]], headers))

