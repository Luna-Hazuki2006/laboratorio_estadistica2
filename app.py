import csv
import math
import random
import seaborn as sns
# import matplotlib as mpl
import scipy.stats as st
import matplotlib.pyplot as plt
from pandas import DataFrame
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from pprint import pprint

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")

templates = Jinja2Templates(directory="./templates")

tablas = []

diagramas = []

razas_sexos = []

horas_años = []

lista = []

salarios = []
edades = []
horarios = []

probabilidades = []

hipotesis_salarios = []

hipotesis_edades = []

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
            else: texto += f' {round(todo[esto][i], 4)} |'
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
    # print(f'mínimo: {minimo}')
    maximo = max(r)
    # print(f'máximo: {maximo}')
    n = len(r)
    rango = maximo - minimo 
    # print(f'Rango: {rango}')
    k = 1 + 3.3 * math.log(n, 10)
    amplitud = rango / k
    if amplitud > int(amplitud): 
        # amplitud += 1
        # amplitud = int(amplitud)
        amplitud = math.ceil(amplitud)
    # print(f'amplitud: {amplitud}')
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
    # print(f'Clases: {len(real)}')
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
    resultados = []
    # mostrar_tabla(todo[0])
    total = todo[0]['fa'][-1]
    # print(f'Total {total}')
    a = todo[0]['clase'][0]['maximo'] - todo[0]['clase'][0]['minimo'] 
    # print(f"Sum: {sum(todo[0]['fi.xi'])}")
    parte = []
    titulo = 'Variables de posición: '
    print('Variables de posición: ')
    cuartiles = []
    for i in range(1, 5): 
        q = obtencion(todo[0], ((25 * i) / 100) * total)
        parte.append(f'Q{i}: {round(q, 4)}')
        print(f'Q{i}: {round(q, 4)}')
        cuartiles.append(q)
    resultados.append((titulo, parte))
    titulo = 'Variables de centralización: '
    parte = []
    print('Variables de centralización: ')
    media = sum(todo[0]['fi.xi']) / total
    parte.append(f'Media aritmética: {round(media, 4)}')
    print(f'Media aritmética: {round(media, 4)}')
    calculo = total / 2
    fa = 0
    for esto in todo[0]['fa']: 
        if esto >= calculo: 
            fa = esto
            break
    # print(f'fa: {fa}')
    indice = todo[0]['fa'].index(fa)
    # print(f'índice: {indice}')
    li = todo[0]['clase'][indice]['minimo']
    # print(f'li: {li}')
    fi_menos = todo[0]['fa'][indice - 1] if indice != 0 else 0
    # print(f'fi menos: {fi_menos}')
    fi = todo[0]['fi'][indice]
    # print(f'fi: {fi}')
    mediana = li + ((calculo - fi_menos) / fi) * a
    parte.append(f'Mediana: {round(mediana, 4)}')
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
    parte.append(f'Modales: {modales}')
    print(f'Modales: {modales}')
    resultados.append((titulo, parte))
    titulo = 'Variables de variabilidad: '
    parte = []
    print('Variables de variabilidad: ')
    varianza = (sum(todo[0]['fi.xi^2']) / total) - (media**2)
    parte.append(f'Varianza: {round(varianza, 4)}')
    print(f'Varianza: {round(varianza, 4)}')
    desviacion = math.sqrt(varianza)
    parte.append(f'Desviación estándar: {round(desviacion, 4)}')
    print(f'Desviación estándar: {round(desviacion, 4)}')
    intercuartil = cuartiles[2] - cuartiles[0]
    p75 = obtencion(todo[0], (75 / 100) * total)
    p25 = obtencion(todo[0], (25 / 100) * total)
    p90 = obtencion(todo[0], (90 / 100) * total)
    p10 = obtencion(todo[0], (10 / 100) * total)
    curtosis = ((p75 - p25) / (p90 - p10)) * 0.5
    coeficiente = (desviacion / media) * 100
    parte.append(f'Coeficiente de variación: {round(coeficiente, 4)}%')
    print(f'Coeficiente de variación: {round(coeficiente, 4)}%')
    parte.append(f'Rango intercuartil: {round(intercuartil, 4)}')
    print(f'Rango intercuartil: {round(intercuartil, 4)}')
    resultados.append((titulo, parte))
    parte = []
    titulo = 'Variables de forma: '
    print('Variables de forma: ')
    indice = (3 * (media - mediana)) / desviacion
    if curtosis == 0: apuntamiento = 'Es mesocúrtica como la normal'
    elif curtosis > 0: apuntamiento = 'Es leptocúrtica apuntada'
    elif curtosis < 0: apuntamiento = 'Es platicúrtica aplanada'
    parte.append(f'Curtosis: {round(curtosis, 4)} ({apuntamiento})')
    print(f'Curtosis: {round(curtosis, 4)} ({apuntamiento})')
    if indice == 0: simetria = 'Es simétrica'
    elif indice > 0: simetria = 'Es asimétrica positiva con sesgo a la derecha'
    elif indice < 0: simetria = 'Es asimétrica negativa con sesgo a la izquierda'
    parte.append(f'Índice de asimetría: {round(indice, 4)} ({simetria})')
    print(f'Índice de asimetría: {round(indice, 4)} ({simetria})')
    resultados.append((titulo, parte))
    f, ax = plt.subplots(figsize=(7, 5))
    sns.despine(f)
    plt.pie(todo[0]['fi'], labels=list(map(lambda x: f'{x["minimo"]}-{x["maximo"]}', todo[0]['clase'])), autopct='%.0f%%')
    plt.title(nombre)
    diagramas.append(f'./static/{nombre}-pie.png')
    plt.savefig(f'./static/{nombre}-pie.png')
    # plt.show()
    print('++++++++++++++++++++++++++++++++++++++++++++')
    print('**********************************************')
    if nombre == 'Income': 
        data = (1 - st.norm.cdf((44 - media) / desviacion)) * 100
        salarios.append(data)
        data = (st.norm.cdf((49 - media) / desviacion) - st.norm.cdf((47 - media) / desviacion)) * 100
        salarios.append(data)
    elif nombre == 'Age': 
        data = st.norm.cdf((49 - media) / desviacion) * 100
        edades.append(data)
        data = (st.norm.cdf((50 - media) / desviacion) - st.norm.cdf((46 - media) / desviacion)) * 100
        edades.append(data)
    elif nombre == 'HoursWk':
        data = (1 - st.norm.cdf((29.5 - media) / desviacion)) * 100
        horarios.append(data)
        data = st.norm.cdf((26.5 - media) / desviacion) * 100
        horarios.append(data)
    return resultados

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
        if data[1] == '1': return (data[0], 'Ciudadano')
        elif data[1] == '0': return (data[0], 'No ciudadano')
    elif data[0] == 'HealthInsurance': 
        if data[1] == '1': return (data[0], 'Tiene seguro médico')
        elif data[1] == '0': return (data[0], 'Sin seguro médico')
    elif data[0] == 'Language': 
        if data[1] == '1': return (data[0], 'Inglés')
        elif data[1] == '0': return (data[0], 'Otro')
    return data

def primero(): 
    with open('Datos proyecto 2024.csv', 'r') as archivo: 
        lista = list(map(lambda x: dict(map(lambda y: (y[0], float(y[1])) if prueba(y[1], y[0]) else seleccion(y), x.items())), csv.DictReader(archivo)))
    datos = DataFrame(data=lista)
    sns.set_theme(style='whitegrid')
    for esto in lista[0].keys(): 
        if esto not in grande: 
            f, ax = plt.subplots(figsize=(7, 5))
            sns.despine(f)
            sns.histplot(
                datos,
                x=esto,
                multiple="layer", 
                # hue=esto, 
                edgecolor=".3",
                linewidth=.5,
                log_scale=True,
            )
            # ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
            diagramas.append(f'./static/{esto}-histplot.png')
            f.savefig(f'./static/{esto}-histplot.png')
            # ax.set_xticks([500, 1000, 2000, 5000, 10000])
            # plt.show()
            continue
        datos = DataFrame(data=list(map(lambda x: dict(map(lambda y: (y[0], 0.5) if y[0] == esto and y[1] <= 0 else y, x.items())), lista)))
        print('*' * 30)
        print(f'[{esto}]')
        print('*' * 30)
        data = list(map(lambda x: x[esto], lista))
        todo = creacion(data)
        f, ax = plt.subplots(figsize=(7, 5))
        sns.despine(f)
        sns.histplot(
            datos,
            x=esto,
            multiple="layer", 
            # hue='Sex', 
            edgecolor=".3",
            linewidth=.5,
            log_scale=True, 
            kde=True
        )
        # ax.set_xticks(list(map(lambda x: x['minimo'], todo[0]['clase'])))
        diagramas.append(f'./static/{esto}-histplot.png')
        f.savefig(f'./static/{esto}-histplot.png')
        # ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
        # pprint(todo)
        # ax.set_xticks(list(map(lambda x: x['minimo'], todo[0]['clase'])))
        # plt.show()
        f, ax = plt.subplots(figsize=(7, 5))
        sns.despine(f)
        sns.ecdfplot(datos, x=esto)
        diagramas.append(f'./static/{esto}-ecdfplot.png')
        f.savefig(f'./static/{esto}-ecdfplot.png')
        # plt.show()
        resultados = proceso(todo, esto)
        tablas.append((esto, todo, resultados))
    mostar_resultados(lista)

def informacion(lista : list): 
    total = lista[0]['fa'][-1]
    media = sum(lista[0]['fi.xi']) / total
    varianza = (sum(lista[0]['fi.xi^2']) / total) - (media**2)
    desviacion = math.sqrt(varianza)
    return total, media, desviacion

def mostar_resultados(lista : list): 
    probabilidades.append(f'La probabilidad de que el salario sea mayor que 44 es de {round(salarios[0], 4)}%')
    probabilidades.append(f'La probabilidad de que el salario de una persona se encuentre entre 47 y 49 es de {round(salarios[1], 4)}%')
    probabilidades.append(f'La probabilidad de que se encuentre una persona con una edad menor de 49 años es de {round(edades[0], 4)}%')
    probabilidades.append(f'La probabilidad de que se encuentre una persona con una edad entre 46 y 50 años es de {round(edades[1], 4)}%')
    probabilidades.append(f'La probabilidad de que las horas trabajadas sea mayor que 29,5 horas es de {round(horarios[0], 4)}%')
    probabilidades.append(f'La probabilidad de que las horas trabajadas sea menor que 26,5 horas es de {round(horarios[1], 4)}%')
    # sns.set_theme()
    # Load the example flights dataset and convert to long-form
    # sns.relplot(data=datos, x="Income", y="Age")
    # plt.show()
    razas = {}
    sexos = {}
    fusion = {}
    horas = []
    años = []
    encuentro = {}
    pase = 0
    while pase <= 59: 
        actual = pase + 19
        horas.append((pase, actual))
        pase = actual + 1
    horas.append((59, 2000))
    pase = 14
    actual = 24
    while pase <= 94: 
        años.append([pase, actual])
        pase = actual + 1
        actual = pase + 9 
    años[-1][1] = 95
    for esto in lista: 
        try: razas[esto['Race']] += 1
        except: razas[esto['Race']] = 1
        try: sexos[esto['Sex']] += 1
        except: sexos[esto['Sex']] = 1
        esta = f'{esto["Race"]}-{esto["Sex"]}'
        try: fusion[esta] += 1
        except: fusion[esta] = 1
    # "cada" significa un rango de años
    for cada in años: 
        # "este" significa un rango de horas
        for este in horas: 
            parte = f'{cada[0]}-{cada[1]}/{este[0]}-{este[1]}'
            encuentro[parte] = len(list(filter(lambda y: round(y['Age']) >= cada[0] and round(y['Age']) <= cada[1] and round(y['HoursWk']) >= este[0] and round(y['HoursWk']) <= este[1], lista)))

    filas = []
    columnas = []
    titulo = '| Categorías\t |'
    columnas.append('Sexo\\Razas')
    for esto in razas.keys(): 
        columnas.append(esto)
        titulo += f' {esto} |'
    titulo += ' Total |'
    columnas.append('Total')
    filas.append(columnas)
    techo = '-' * len(titulo)
    print(techo)
    print(titulo)
    for esto in sexos.keys(): 
        columnas = []
        columnas.append(esto)
        titulo = f'| {esto}\t |'
        for esta in razas.keys(): 
            columnas.append(fusion[f"{esta}-{esto}"])
            titulo += f' {fusion[f"{esta}-{esto}"]}\t |'
        columnas.append(sexos[esto])
        filas.append(columnas)
        titulo += f' {sexos[esto]}\t |'
        techo = '-' * len(titulo)
        print(techo)
        print(titulo)
    columnas = []
    columnas.append('Total')
    titulo = '| Total\t\t |'
    for esto in razas.values(): 
        columnas.append(esto)
        titulo += f' {esto}\t |'
    columnas.append((sum(sexos.values()) + sum(razas.values())) / 2)
    filas.append(columnas)
    # pprint(filas)
    titulo += f' {(sum(sexos.values()) + sum(razas.values())) / 2}\t |'
    techo = '-' * len(titulo)
    print(techo)
    print(titulo)
    print(techo)
    mayor = max(fusion.values())
    categoria = list(filter(lambda x: x[1] == mayor, fusion.items()))[0]
    hablas = categoria[0].split('-')
    porcentaje = (100 * mayor) / sum(fusion.values())
    explicacion = f'''
Gracias a esta tabla se puede notar que la mayor parte de fuerza laboral está compuesta de {mayor} personas 
que son de raza "{hablas[0]}" y sexo "{hablas[1]}", esta siendo el {round(porcentaje, 2)}% de la muestra la mayoría.
'''
    print(explicacion)
    razas_sexos.append(filas)
    razas_sexos.append(explicacion)
    print('/' * 50)
    filas = []
    columnas = []
    columnas.append('Edad\\Horas')
    titulo = '| Categorías\t |'
    for esto in horas: 
        if esto == horas[-1]: 
            columnas.append('Más horas')
            titulo += ' Más horas |'
            break
        columnas.append(f'{esto[0]}-{esto[1]}')
        titulo += f' {esto[0]}-{esto[1]} |'
    filas.append(columnas)
    columnas = []
    techo = '-' * len(titulo)
    print(techo)
    print(titulo)
    for esto in años: 
        columnas = []
        columnas.append(f'{esto[0]}-{esto[1]}')
        titulo = f'| {esto[0]}-{esto[1]}\t\t |'
        for esta in horas: 
            columnas.append(f'{encuentro[f"{esto[0]}-{esto[1]}/{esta[0]}-{esta[1]}"]}')
            titulo += f' {int(encuentro[f"{esto[0]}-{esto[1]}/{esta[0]}-{esta[1]}"])}\t |'
        techo = '-' * len(titulo)
        filas.append(columnas)
        print(techo)
        print(titulo)
    print(techo)
    mayor = max(encuentro.values())
    categoria = list(filter(lambda x: x[1] == mayor, encuentro.items()))[0]
    hablas = categoria[0].split('/')
    porcentaje = (mayor * 100) / sum(encuentro.values())
    explicacion = f'''
Gracias a esta tabla se puede notar que la mayor parte de fuerza laboral está compuesta de {mayor} personas 
que tienen de {hablas[0]} años y trabajan de {hablas[1]} horas, esta siendo el {round(porcentaje, 2)}% de la muestra.
'''
    print(explicacion)
    horas_años.append(filas)
    horas_años.append(explicacion)
    filas = []
    columnas = []
    print('/' * 50)
    pagos = list(map(lambda x: x['Income'], lista))
    grupo1 = random.sample(pagos, 500)
    grupo2 = random.sample(pagos, 500)
    grupo3 = random.sample(pagos, 600)
    grupos = [['Grupo 1', grupo1], ['Grupo 2', grupo2], ['Grupo 3', grupo3]]
    titulo = '| Nombre | Cantidad | Media aritmética | Desviación típica |'
    columnas.append('Muestras de salarios')
    columnas.append('Cantidad')
    columnas.append('Media aritmética')
    columnas.append('Desviación típica')
    filas.append(columnas)
    techo = '-' * len(titulo)
    print(techo)
    print(titulo)
    print(techo)
    for grupo in grupos: 
        columnas = []
        mejorado = creacion(grupo[1])
        total, media, desviacion = informacion(mejorado)
        grupo.append((total, media, desviacion))
        columnas.append(grupo[0])
        columnas.append(total)
        columnas.append(round(media, 4))
        columnas.append(round(desviacion, 4))
        titulo = f'| {grupo[0]} | {total} | {round(media, 4)} | {round(desviacion, 4)} |'
        techo = '-' * len(titulo)
        filas.append(columnas)
        print(titulo)
        print(techo)
    explicacion = []
    zcal = (grupos[0][2][1] - grupos[1][2][1]) / math.sqrt(((grupos[0][2][2] ** 2) / grupos[0][2][0]) + ((grupos[1][2][2] ** 2) / grupos[1][2][0]))
    ztab = 1.65
    if -ztab < zcal < ztab: 
        explicacion.append(f'Ho (hipótesis nula) fue aceptada, ya que {-ztab} < {round(zcal, 2)} < {ztab} eso quiere decir que entre las primeras muestras de salarios no hay variabilidad.')
    else: 
        texto = f'(zcal) {round(zcal, 2)} > (ztab) {ztab}' if zcal > ztab else f'(zcal) {round(zcal, 2)} < (ztab) {-ztab}'
        explicacion.append(f'Ha (hipótesis alterna) fue aceptada, ya que {texto} esto quiere decir que entre las dos primeras muestras de salarios hay una gran variabilidad.')
    zcal = (grupos[1][2][1] - grupos[2][2][1]) / math.sqrt(((grupos[1][2][2] ** 2) / grupos[1][2][0]) + ((grupos[2][2][2] ** 2) / grupos[2][2][0]))
    ztab = 2.33
    if -ztab < zcal < ztab: 
        explicacion.append(f'Ho (hipótesis nula) fue aceptada, ya que {-ztab} < {round(zcal, 2)} < {ztab} esto quiere decir que entre las dos últimas muestras de salario no hay variabilidad.')
    else: 
        texto = f'(zcal) {round(zcal, 2)} > (ztab) {ztab}' if zcal > ztab else f'(zcal) {round(zcal, 2)} < (ztab) {-ztab}'
        explicacion.append(f'Ha (hipótesis alterna) fue aceptada, ya que {texto} esto quiere decir que entre las dos últimas muestras de salarios hay una gran variabilidad.')
    print('/' * 50)
    hipotesis_salarios.append(filas)
    hipotesis_salarios.append(explicacion)
    filas = []
    columnas = []
    años = list(map(lambda x: x['Age'], lista))
    edad1 = random.sample(años, 300)
    edad2 = random.sample(años, 400)
    partes =[[edad1], [edad2]]
    grupos = [['Grupo 1', edad1], ['Grupo 2', edad2]]
    titulo = '| Nombre | Cantidad | Media aritmética | Desviación típica |'
    columnas.append('Muestras de edades')
    columnas.append('Cantidad')
    columnas.append('Media aritmética')
    columnas.append('Desviación típica')
    filas.append(columnas)
    techo = '-' * len(titulo)
    print(techo)
    print(titulo)
    print(techo)
    for grupo in grupos: 
        columnas = []
        mejorado = creacion(grupo[1])
        total, media, desviacion = informacion(mejorado)
        grupo.append((total, media, desviacion))
        columnas.append(grupo[0])
        columnas.append(total)
        columnas.append(round(media, 4))
        columnas.append(round(desviacion, 4))
        titulo = f'| {grupo[0]} | {total} | {round(media, 4)} | {round(desviacion, 4)} |'
        techo = '-' * len(titulo)
        print(titulo)
        print(techo)
        filas.append(columnas)
    explicacion = []
    for edad in partes: 
        mejorado = creacion(edad[0])
        total, media, desviacion = informacion(mejorado)
        edad.append((total, media, desviacion))
    zcal = (partes[0][1][1] - partes[1][1][1]) / math.sqrt(((partes[0][1][2] ** 2) / partes[0][1][0]) + ((partes[1][1][2] ** 2) / partes[1][1][0]))
    ztab = 1.29
    if -ztab < zcal < ztab: 
        explicacion.append(f'Ho (hipótesis nula) fue aceptada, ya que {-ztab} < {round(zcal, 2)} < {ztab} esto quiere decir que entre las dos muestras edades no se encuentra variabilidad.')
    else: 
        texto = f'(zcal) {round(zcal, 2)} > (ztab) {ztab}' if zcal > ztab else f'(zcal) {round(zcal, 2)} < (ztab) {-ztab}'
        explicacion.append(f'Ha (hipótesis alterna) fue aceptada, ya que {texto} esto quiere decir que entre las dos muestas de edades hay una gran variabilidad.')
    hipotesis_edades.append(filas)
    hipotesis_edades.append(explicacion)


# def main(): 
#     primero()

# Cuz I always kill the things I love :(

primero() 

@app.get('/')
def mostrar(request : Request):
    return templates.TemplateResponse('index.html', {
        'request': request, 'tablas': tablas, 'diagramas': diagramas, 'probabilidades': probabilidades, 
        'razas_sexos': razas_sexos, 'horas_años': horas_años, 'hipotesis_edades': hipotesis_edades, 
        'hipotesis_salarios': hipotesis_salarios})

# if __name__ == '__main__': 
#     main()