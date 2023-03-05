
import re

regex = r"(?P<pasta>\d+)::(?P<data>\d\d\d\d-\d\d-\d\d)::(?P<nome>[a-zA-z,. ]+)::(?P<pai>[a-zA-z,(). ]*)::(?P<mae>[a-zA-z(),. ]*)::(?P<extra>.*)::"
regex_date = r"(?P<ano>\d\d\d\d)-(?P<mes>\d\d)-(?P<dia>\d\d)"
regex_century = r"(?P<seculo>\d\d)\d\d"
regex_name = r"(?P<primeiro_nome>\w*)(.*) (?P<last_nome>\w*)"


def freq_year(year):

    f = open("processos.txt")
    re1 = re.compile(regex)
    re2 = re.compile(regex_date)
    info = dict()

    for line in f:
        take_date = re1.match(line)
        if take_date is not None:
            date = re2.match(take_date.group('data')).group('ano')
            if date not in info.keys():
                info[date] = 1
            else:
                info[date] = info[date] + 1

    f.close()

    return (info[year] / sum(info.values())) * 100

def get_top_names(flag, names, seculo):

    names_len = len(names)
    max_names = []

    for name in names:
        count = names.count(name)
        i = 0
        while i < count:
            names.remove(name)
            i += 1
        aux = (name, count)
        if len(max_names) == 0:
            max_names.append(aux)

        i = 0
        for _, c in max_names:
            if c > count:
                i += 1
            else:
                max_names.insert(i, aux)
                break

    print(f"Seculo: {seculo}:")
    i = 0
    for n,c in max_names:
        print(f"\t{flag}: {n}, Freq: {c/names_len:<0.3%};")
        i += 1
        if i == 5:
            break
    
def freq_name(seculo_arg):

    f = open("processos.txt")
    re1 = re.compile(regex)
    re2 = re.compile(regex_date)
    re3 = re.compile(regex_name)
    info = dict()

    for line in f:
        take_name = re1.match(line)
        if take_name is not None:
            year = re2.match(take_name.group('data')).group('ano')
            name = re3.match(take_name.group('nome'))
            if year is not None:
                seculo = re.match(regex_century, year).group('seculo')
                if seculo is not None:
                    if not (int(year) % 100) == 0:
                        seculo = int(str(seculo)) + 1
                    else:
                        seculo = int(str(seculo))
                    if seculo not in info.keys():
                        info[seculo] = ([],[])
                
                    if name is not None:
                        f_n, l_n = info[seculo]
                        f_n.append(name.group('primeiro_nome'))
                        l_n.append(name.group('last_nome'))
                        info[seculo] = (f_n, l_n)
    
    (n_list, s_list) = info[seculo_arg]
    get_top_names("Nome", n_list, seculo_arg)
    get_top_names("Sobrenome", s_list, seculo_arg)

    f.close()


def txt_to_Json():

    f_input = open("processos.txt")
    f_output = open("processos.json", "w")

    re1 = re.compile(regex)

    i = 0
    f_output.write("[\n")
    while i < 20:
        f_output.write("\t{\n")
        i += 1
        content = f_input.readline()
        info = re1.match(content).groupdict()
        for key in info.keys():
            if key == "extra":
                f_output.write(f"\t\t\"{str(key)}\": \"{str(info[key])}\"\n")
            else:
                f_output.write(f"\t\t\"{str(key)}\": \"{str(info[key])}\",\n")
        if i < 20:
            f_output.write("\t},\n")
        else:
            f_output.write("\t}\n")

    f_output.write("]")

    f_output.close()

txt_to_Json()