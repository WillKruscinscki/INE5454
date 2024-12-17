from branalysis.colorizador import CORES
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import ListedColormap
from sklearn.decomposition import PCA
from statistics import mean, median
import json
import numpy as np
import os

DADOS_PATH = './Json'
AIR_QUALITY_SCORES = {
    'Excelente': 100,
    'Bom': 95,
    'Satisfatorio': 95,
    'Good': 95,
    'Razoavel': 70,
    'Moderado': 40,
    'Moderate': 40,
    'Unhealthy for Sensitive Groups': 20,
    'Forte': 20,
    'Mau': 0,
    'Unhealthy': 0,
    'Pobre': 0,
}

def rescale(x, a, b):
   return (x - a) / (b - a)

def makeint(dict, key):
    try:
        dict[key] = int(dict[key])

    except:
        del dict[key]

def convert_info(info):
    makeint(info, 'temperatura')
    makeint(info, 'umidade')
    makeint(info, 'sensacao_termica')
    info['qualidade_do_ar'] = AIR_QUALITY_SCORES.get(info['qualidade_do_ar'], 50)

    try:
        a, b = info['vento'].split(' - ')
        info['vento'] = (int(a) + int(b)) / 2.0

    except:
        makeint(info, 'vento')

    return info

def load_data():
    data = {}

    for filename in os.listdir(DADOS_PATH):
        with open(f'{DADOS_PATH}/{filename}', "r", encoding="utf-8") as f:
            for id, info in json.load(f).items():
                name, source = id.split('_')

                data.setdefault(name, {}).setdefault(source, []).append(convert_info(info))

    return data

def get_info(sources, info):
    return list(list(entry.get(info) for entry in source) for source in sources.values())

def filter_not_none(data):
    return filter(lambda x: x is not None, data)

def calculate_means(data):
    for _, sources in data.items():
        sources['Media'] = {
            'temperatura': list(mean(filter_not_none(x)) for x in zip(*get_info(sources, 'temperatura'))),
            'umidade': list(mean(filter_not_none(x)) for x in zip(*get_info(sources, 'umidade'))),
            'sensacao_termica': list(mean(filter_not_none(x)) for x in zip(*get_info(sources, 'sensacao_termica'))),
            'qualidade_do_ar': list(mean(filter_not_none(x)) for x in zip(*get_info(sources, 'qualidade_do_ar'))),
            'vento': list(mean(filter_not_none(x)) for x in zip(*get_info(sources, 'vento'))),
        }

    return data

def dimension_matrix(cities):
    matrix = []

    for _, sources in cities:
        matrix.append([
            rescale(median(sources['Media']['temperatura']), 10, 50),
            rescale(median(sources['Media']['umidade']), 0, 100),
            rescale(median(sources['Media']['sensacao_termica']), 10, 50),
            rescale(median(sources['Media']['vento']), 0, 70),
            rescale(median(sources['Media']['qualidade_do_ar']), 0, 100)
        ])

    return np.array(matrix)

data = load_data()
data = calculate_means(data)

with PdfPages('meuoutput.pdf') as pdf:
    cities = list(data.items())
    cities.sort(key=lambda x: x[0])
    cities_names = [name for name, _ in cities]


    fit = PCA(n_components=2).fit_transform(dimension_matrix(cities))
    colors = [i for i, _ in enumerate(cities)]

    fig, ax = plt.subplots(figsize=(12, 9), dpi=150)
    grafico = ax.scatter(fit[:, 0], fit[:, 1], c=colors, cmap=ListedColormap(CORES))

    cores_legenda = grafico.legend_elements(num=colors)[0]

    ax.legend(cores_legenda, cities_names, fontsize=6, ncol=2)
    ax.set_title('Proximidade climática entre capitais brasileiras')
    ax.set_xlabel('Considerando temperatura, umidade, sensação térmica, vento e qualidade do ar.')
    fig.gca().set_xticks([])
    fig.gca().set_yticks([])
    pdf.savefig(fig)


    def plot_metric(metric, axis_label):
        fig, ax = plt.subplots(figsize=(12, 9), dpi=150)
        cities2 = list(data.items())
        cities2.sort(key=lambda x: median(x[1]['Media'][metric]))
        ax.boxplot(list(sources['Media'][metric] for _, sources in cities2),
                    patch_artist=True,
                    tick_labels=list(name for name, _ in cities2))
        ax.set_ylabel(axis_label)
        plt.xticks(rotation=-45, ha='left')
        pdf.savefig(fig)

    plot_metric('temperatura', 'Temperatura (C°)')
    plot_metric('sensacao_termica', 'Sensação térmica (C°)')
    plot_metric('umidade', 'Umidade (%)')
    plot_metric('vento', 'Vento (km/h)')


    fig, ax = plt.subplots(figsize=(12, 9), dpi=150)
    qualidade_do_ar_media = [(name, mean(sources['Media']['qualidade_do_ar'])) for name, sources in cities]
    qualidade_do_ar_media.sort(key=lambda x: x[1])
    barras = ax.bar(*zip(*qualidade_do_ar_media))

    ax.bar_label(barras, fmt=lambda x: f'{x:.1f}', label_type='edge', fontsize=8)
    plt.ylabel('Qualidade do ar média (%)')
    plt.xticks(rotation=-45, ha='left')
    plt.ylim(40, 100)
    pdf.savefig(fig)