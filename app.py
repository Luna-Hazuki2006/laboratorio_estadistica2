import csv
import math
import random
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from pandas import DataFrame
from pprint import pprint

lista = []

def obtencion(lista, numero):
    fa = lista['fa']
    fi = lista['fi']
    clase = lista['clase']
    indice = 0
    for esto in fa: 
        if esto >= numero: 
            indice = fa.index(esto)
            break
    if indice == 0: fa_numero = 0
    else: fa_numero = fa[indice - 1]
    fi_numero = fi[indice]
    li = clase[indice]['minimo']
    amplitud = clase[0]['maximo'] - clase[0]['minimo']
    esto = li + ((numero - fa_numero) / fi_numero) * amplitud
    return esto

def mostrar_tabla(todo : dict): 
    total = len(todo['clase'])
    llaves = todo.keys()
    texto = '|'
    for esto in llaves: texto += f' {esto} |'
    print(len(texto) * '-')
    print(texto)
    for i in range(total): 
        texto = '|'
        for esto in llaves: 
            if esto == 'clase': 
                minimo = todo[esto][i]['minimo']
                maximo = todo[esto][i]['maximo']
                texto += f' {minimo}-{maximo} |'
            else: texto += f' {todo[esto][i]} |'
        print(len(texto) * '-')
        print(texto)
    print(len(texto) * '-')

def buscar_modales(fi : list): 
    lista = []
    maximo = max(fi)
    for i in range(len(fi)): 
        if fi[i] == maximo: 
            lista.append(i)
    return lista

def creacion(r : list): 
    minimo = min(r)
    maximo = max(r)
    n = len(r)
    rango = maximo - minimo 
    k = 1 + 3.3 * math.log(n, 10)
    amplitud = rango / k
    if amplitud > int(amplitud): 
        # amplitud += 1
        # amplitud = int(amplitud)
        amplitud = round(amplitud)
    lista = {}
    for esto in r: 
        try: lista[esto] += 1
        except: lista[esto] = 1
    real = []
    para = 0
    while True: 
        if minimo > maximo: break
        para = minimo + amplitud - 1
        clase = {
            'minimo': int(minimo), 
            'maximo': int(para + 1)
        }
        minimo = para + 1
        real.append(clase)
    oficial = [{'clase': real}]
    oficial[0]['fi'] = []
    for esto in real: 
        numero = sum(map(lambda x: lista[x], filter(lambda x: x >= esto['minimo'] and x < esto['maximo'], lista.keys())))
        oficial[0]['fi'].append(numero)
    parte = []
    for esto in oficial[0]['fi']: 
        if len(parte) >= 1: parte.append(esto + parte[-1])
        else: parte.append(esto)
    oficial[0]['fa'] = parte
    oficial[0]['xi'] = list(map(lambda x: (x['minimo'] + x['maximo']) / 2, oficial[0]['clase']))
    oficial[0]['fi.xi'] = [(xi * fi) for xi, fi in zip(oficial[0]['fi'], oficial[0]['xi'])]
    oficial[0]['fsr'] = list(map(lambda x: x / oficial[0]['fa'][-1], oficial[0]['fi']))
    oficial[0]['far'] = list(map(lambda x: x / oficial[0]['fa'][-1], oficial[0]['fa']))
    oficial[0]['fsr%'] = list(map(lambda x: x * 100, oficial[0]['fsr']))
    oficial[0]['far%'] = list(map(lambda x: x * 100, oficial[0]['far']))
    oficial[0]['fi.xi^2'] = [(xi * fixi) for xi, fixi in zip(oficial[0]['fi.xi'], oficial[0]['xi'])]
    return oficial

def proceso(todo : list, nombre : str): 
    mostrar_tabla(todo[0])
    total = todo[0]['fa'][-1]
    # print(f'Total {total}')
    a = todo[0]['clase'][0]['maximo'] - todo[0]['clase'][0]['minimo'] 
    # print(f"Sum: {sum(todo[0]['fi.xi'])}")
    print('Variables de posición: ')
    cuartiles = []
    for i in range(1, 5): 
        q = obtencion(todo[0], ((25 * i) / 100) * total)
        print(f'Q{i}: {round(q, 4)}')
        cuartiles.append(q)
    print('Variables de centralización: ')
    media = sum(todo[0]['fi.xi']) / total
    print(f'Media aritmética: {round(media, 4)}')
    calculo = total / 2
    fa = 0
    for esto in todo[0]['fa']: 
        if esto >= calculo: 
            fa = esto
            break
    indice = todo[0]['fa'].index(fa)
    li = todo[0]['clase'][indice]['minimo']
    fi_menos = todo[0]['fa'][indice - 1]
    fi = todo[0]['fi'][indice]
    mediana = li + ((calculo - fi_menos) / fi) * a
    print(f'Mediana: {round(mediana, 4)}')
    lugares_modales = buscar_modales(todo[0]['fi'])
    modales = []
    for esto in lugares_modales: 
        li = todo[0]['clase'][esto]['minimo']
        fi = todo[0]['fi'][esto]
        try: fi_menos = todo[0]['fi'][esto - 1]
        except: fi_menos = 0
        try: fi_mas = todo[0]['fi'][esto + 1]
        except: fi_mas = 0
        d1 = fi - fi_menos
        d2 = fi - fi_mas
        try: modal = li + (d1 / (d1 + d2)) * a
        except: 
            print(f'''"
En la {lugares_modales.index(esto) + 1}° moda hubo una excepción que ameritó cambiar (d1 / (d1 + d2)) 
porque daba una división de 0 sobre 0 que no está definida en matemática
"''')
            modal = li + a
        modales.append(round(modal, 4))
    print(f'Modales: {modales}')
    print('Variables de variabilidad: ')
    varianza = (sum(todo[0]['fi.xi^2']) / total) - (media**2)
    print(f'Varianza: {round(varianza, 4)}')
    desviacion = math.sqrt(varianza)
    print(f'Desviación estándar: {round(desviacion, 4)}')
    intercuartil = cuartiles[2] - cuartiles[0]
    p75 = obtencion(todo[0], (75 / 100) * total)
    p25 = obtencion(todo[0], (25 / 100) * total)
    p90 = obtencion(todo[0], (90 / 100) * total)
    p10 = obtencion(todo[0], (10 / 100) * total)
    curtosis = ((p75 - p25) / (p90 - p10)) * 0.5
    coeficiente = (desviacion / media) * 100
    print(f'Coeficiente de variación: {round(coeficiente, 4)}')
    print(f'Rango intercuartil: {round(intercuartil, 4)}')
    print('variables de forma: ')
    indice = (3 * (media - mediana)) / desviacion
    if curtosis == 0: apuntamiento = 'Es mesocúrtica como la normal'
    elif curtosis > 0: apuntamiento = 'Es leptocúrtica apuntada'
    elif curtosis < 0: apuntamiento = 'Es platicúrtica aplanada'
    print(f'Curtosis: {round(curtosis, 4)} ({apuntamiento})')
    if indice == 0: simetria = 'Es simétrica'
    elif indice > 0: simetria = 'Es asimétrica positiva con sesgo a la derecha'
    elif indice < 0: simetria = 'Es asimétrica negativa con sesgo a la izquierda'
    print(f'Índice de asimetría: {round(indice, 4)} ({simetria})')
    plt.pie(todo[0]['fi'], labels=list(map(lambda x: f'{x["minimo"]}-{x["maximo"]}', todo[0]['clase'])), autopct='%.0f%%')
    plt.title(nombre)
    plt.show()
    print('++++++++++++++++++++++++++++++++++++++++++++')
    print('**********************************************')

grande = ['Age', 'Income', 'HoursWk']

def prueba(esto, lugar): 
    if lugar not in grande: return False
    try: 
        float(esto)
        return True
    except: return False

def seleccion(data): 
    if data[0] == 'Sex': 
        if data[1] == '0': return (data[0], 'Femenino')
        elif data[1] == '1': return (data[0], 'Masculino')
    elif data[0] == 'Married': 
        if data[1] == '0': return (data[0], 'Soltero')
        elif data[1] == '1': return (data[0], 'Casado') 
    elif data[0] == 'USCitizen': 
        if data[1] == '0': return (data[0], 'Ciudadano')
        elif data[1] == '1': return (data[0], 'No ciudadano')
    elif data[0] == 'HealthInsurance': 
        if data[1] == '0': return (data[0], 'Tiene seguro médico')
        elif data[1] == '1': return (data[0], 'Sin seguro médico')
    elif data[0] == 'Language': 
        if data[1] == '0': return (data[0], 'Inglés')
        elif data[1] == '1': return (data[0], 'Otro')
    return data

def primero(): 
    with open('Datos proyecto 2024.csv', 'r') as archivo: 
        lista = list(map(lambda x: dict(map(lambda y: (y[0], float(y[1])) if prueba(y[1], y[0]) else seleccion(y), x.items())), csv.DictReader(archivo)))
    datos = DataFrame(data=lista)
    sns.set_theme(style="ticks")
    f, ax = plt.subplots(figsize=(7, 5))
    sns.despine(f)
    for esto in lista[0].keys(): 
        if esto not in grande: 
            sns.histplot(
                datos,
                x=esto,
                multiple="stack",
                edgecolor=".3",
                linewidth=.5,
                log_scale=True,
            )
            ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
            # ax.set_xticks([500, 1000, 2000, 5000, 10000])
            plt.show()
            continue
        datos = DataFrame(data=list(map(lambda x: dict(map(lambda y: (y[0], 0.5) if y[0] == esto and y[1] <= 0 else y, x.items())), lista)))
        sns.histplot(
            datos,
            x=esto,
            multiple="stack",
            edgecolor=".3",
            linewidth=.5,
            log_scale=True, 
            kde=True
        )
        ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
        # ax.set_xticks([500, 1000, 2000, 5000, 10000])
        plt.show()
        sns.displot(datos, x=esto, kind="ecdf")
        plt.show()
        print('*' * 30)
        print(f'[{esto}]')
        print('*' * 30)
        data = list(map(lambda x: x[esto], lista))
        todo = creacion(data)
        proceso(todo, esto)

def main(): 
    primero()

if __name__ == '__main__': 
    main()