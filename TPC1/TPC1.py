
'''
Modelo:
    => Informaçao: idade,sexo,tensão,colesterol,batimento,temDoença
    => Dict:
        -> (Keys) Tem Doença ou Nao tem Doença
        -> (Values) Dict
            - (Keys) Gender, Age, Cholesterol
            - (Values) List (Tamanho depende da Key: Gender(2), Age(11), Cholesterol(61);
                            Cada posiçao tera um valor inteiro que incrementa sempre que um paciente novo comparece e que se encaixe naquela posiçao, 
                                isto e, caso um paciente pretença ao sexo masculino vai para a casa 0, ou se a idade esta entre o 40-44 vai para a casa 3, ou se o 
                                seu cholesterol estiver entre os 300 e os 309 vai para a casa 31)

'''

import matplotlib.pyplot as plt
import numpy as np

def read_file():
    f = open("myheart.csv", "rt")
    f.readline()
    content = f.read()
    f.close()
    return content.split()

def break_text(content):
    list_content = []
    for linha in content:
        aux = str(linha).split(',')
        list_content.append(aux)
    return list_content

def init_list_of_details(list, size):
    i = 0
    while i < size:
        list.append(0)
        i += 1

def init_details(dict):
    dict['Gender'] = []
    dict['Age'] = []
    dict['Cholesterol'] = []
    init_list_of_details(dict['Gender'],2)
    init_list_of_details(dict['Age'],11)
    init_list_of_details(dict['Cholesterol'], 61)

def init_module():
    info = dict()
    info['0'] = dict()
    info['1'] = dict()
    init_details(info['0'])
    init_details(info['1'])
    return info

def load_Gender(gender, list):
    if gender == 'M':
        temp = list[0]
        temp += 1
        list[0] = temp
    else:
        temp = list[1]
        temp += 1
        list[1] = temp

def load_Age(age, list):
    min = 25
    max = 29
    added = False
    i = 0
    while i < len(list) and not added:
        if age >= min and age <= max:
            tmp = list[i]
            tmp += 1
            list[i] = tmp
            added = True
        else:
            min += 5
            max += 5
            i += 1

def load_Cholesterol(cholesterol, list):
    min = 0
    max = 9
    added = False
    i = 0
    while i < len(list) and not added:
        if cholesterol >= min and cholesterol <= max:
            tmp = list[i]
            tmp += 1
            list[i] = tmp
            added = True
        else:
            min += 10
            max += 10
            i += 1

def load_patient(linha, dict):
    load_Gender(linha[1], dict['Gender'])
    load_Age(int(linha[0]), dict['Age'])
    load_Cholesterol(int(linha[3]), dict['Cholesterol'])

def load_data_to_module(list_content, info):
    for linha in list_content:
        sick_or_not = int(linha[5])
        if sick_or_not == 1:
            load_patient(linha, info['1'])
        else:
            load_patient(linha, info['0'])
            
def get_distribution_Gender(info):
    male_sick = info['1']['Gender'][0]
    total_male_sick = info['0']['Gender'][0]
    total_male_sick += male_sick

    female_sick = info['1']['Gender'][1]
    total_female_sick = info['0']['Gender'][1]
    total_female_sick += female_sick

    gender_dict = dict()
    gender_dict['M'] = round(male_sick / total_male_sick,3) * 100
    gender_dict['F'] = round(female_sick / total_female_sick,3) * 100

    return gender_dict

def get_distribution_Age(info):
    min_age = 25
    max_age = 29
    age_dict = dict()
    i = 0
    while i < len(info['1']['Age']):
        sick = info['1']['Age'][i]
        total_sick = info['0']['Age'][i] + sick
        aux = "[" + str(min_age) + "-" + str(max_age) + "]"
        if total_sick != 0:
            age_dict[aux] = (round(sick / total_sick,3) * 100)
        else:
            age_dict[aux] = 0
        i += 1
        min_age += 5
        max_age += 5
    return age_dict

def get_distribution_Cholesterol(info):
    min_ch = 0
    max_ch = 9
    cholesterol_dict = dict()
    i = 0
    while i < len(info['1']['Cholesterol']):
        sick = info['1']['Cholesterol'][i]
        total_sick = info['0']['Cholesterol'][i] + sick
        aux = "[" + str(min_ch) + "-" + str(max_ch) + "]"
        if total_sick != 0:
            cholesterol_dict[aux] = (round(sick / total_sick, 3) * 100)
        else : 
            cholesterol_dict[aux] = 0
        i += 1
        min_ch += 10
        max_ch += 10

    return cholesterol_dict

def dict_to_table(dict):
    keys = dict.keys()
    print("----------- ---------------")
    for key in keys:
        aux = str(key)
        while(len(aux) < 12):
            aux += " "
        print(aux + str(dict[key]))
    print("----------- ---------------")

def dict_to_graph(dict, type):
    keys = dict.keys()

    y_pos = np.arange(len(keys))
    distribution = dict.values()

    plt.bar(y_pos, distribution, align='center', alpha=0.75)
    plt.xticks(y_pos, keys)
    plt.ylabel('Percentagem de Distribuicao')
    plt.title('Distribuicao por ' + type)

    plt.show()



def menu():

    print("--------------------------------------------------")
    print("|           1 -> Distribuicao por sexo           |")
    print("|           2 -> Distribuica0 por idade          |")
    print("|           3 -> Distribuicao por colesterol     |")
    print("--------------------------------------------------")

    return int(input("Escolha uma distribuicao: "))


content = read_file()
list_content = break_text(content)

info_module = init_module()
load_data_to_module(list_content, info_module)

opcao = menu()

if opcao == 1:
    gender_dict = get_distribution_Gender(info_module)
    dict_to_table(gender_dict)
    #dict_to_graph(gender_dict, "Sexo")
elif opcao == 2:
    age_dict = get_distribution_Age(info_module)
    dict_to_table(age_dict)
    #dict_to_graph(age_dict, "Idade")
elif opcao == 3:
    cholesterol_dict = get_distribution_Cholesterol(info_module)
    dict_to_table(cholesterol_dict)
    #dict_to_graph(cholesterol_dict, "Colesterol")
else:
    print("Opcao Invalida")




