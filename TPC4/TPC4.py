
import re
import json


regex_cabeçalho = r'(?P<numero>[^\d,]+),(?P<nome>\w+),(?P<curso>\w+\b),?((?P<notas>\w+)(?P<notas_size>({.+}))?(::)?(?P<func>(\w+))?)?'
regex = r'(?P<numero>\d+),(?P<nome>[^\d,]+),(?P<curso>[^\d,]+\b),?(?P<notas>.+)?'
regex_ints = r'(\d+)'

re1_cabeçalho = re.compile(regex_cabeçalho)
re1 = re.compile(regex)


list_of_objects = []
f = open("alunos1.csv")

cabeçalho = re1_cabeçalho.search(f.readline())

for line in f:
    temp = re1.search(line).groupdict()
    print(temp)
    if 'notas_size' in cabeçalho.groupdict().keys() and cabeçalho.group('notas_size') is not None:
        list_size = re.findall(regex_ints, cabeçalho.group('notas_size'))
        list_size = list(map(int, list_size))
        list_of_values = list(map(int,re.findall(regex_ints, temp['notas'])))
        if len(list_size) == 2 and len(list_of_values) >= list_size[0] and len(list_of_values) <= list_size[1]:
            temp['notas'] = list_of_values
        elif len(list_of_values) == list_size[0]:
            temp['notas'] = list_of_values
        else:
            temp['notas'] = []

    list_of_objects.append(temp)

func = cabeçalho.group('func')

objects = []

if func is not None and func == "sum":
    for l in list_of_objects:
        if l:
            sum_list = sum(l['notas'])
            l['notas'] = sum_list
elif func is not None and func == "media":
    for l in list_of_objects:
        if l:
            media_list = sum(l['notas'])/len(l['notas'])
            l['notas'] = media_list

for obj in list_of_objects:
    i = 1
    temp = dict()
    for key in obj.keys():
        if key == 'notas':
            if obj[key] is not None:
                if func is not None:
                    new_key = "Notas" + "_" + str(cabeçalho.group('func'))
                    temp[new_key] = obj[key]
                else:
                    temp[str(cabeçalho.group('notas'))] = obj[key]
        else:
            temp[str(cabeçalho.group(i))] = obj[key]
        i += 1
    objects.append(temp)
    
f_output = open("alunos1.json", "w")

json_dict = json.dumps(objects, indent=4, ensure_ascii=False)

f_output.write(json_dict)
print(json_dict)


