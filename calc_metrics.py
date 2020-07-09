import pandas as pd
import seaborn as sn
from sklearn import preprocessing
import sklearn.metrics as metrics
import numpy as np
import matplotlib.pyplot as plt



path_labels = "Base\\Labels\\"
path_resultados = ""

path_resultados = "Resultados\\transf_output"

transformacoes = ["normal", 
                  "noise1", "noise2", "noise3", 
                  "blur1", "blur2", "blur3", 
                  "gamma1", "gamma2", "gamma3",
                  "rotacao1", "rotacao2", "rotacao3"]
lista_titulosGraficos = ["normal", 
                  "noise1", "noise2", "noise3", 
                  "blur1", "blur2", "blur3", 
                  "gamma1", "gamma2", "gamma3",
                  "rotacao1", "rotacao2", "rotacao3"]
#transformacoes = ["normal"]
numVideos = 2
numClasses = 5

le = preprocessing.LabelEncoder()

some_labels = pd.read_excel(path_labels + "label1.xlsx")["Labels"]
le.fit(some_labels)

resultados_metricas = {}

#Ler arquivos e calcular métricas
for transf in transformacoes:
    confusion_matrix = np.zeros((numClasses,numClasses))
    
    wa_precision = []
    wa_recall = []
    wa_f1 = []
    
    precision_class = np.zeros((1,numClasses))
    recall_class = np.zeros((1,numClasses))
    f1_class = np.zeros((1,numClasses))
    
    print(transf)
    for i in range(1,numVideos+1):
        print(i)
        print(path_labels + "label" + str(i) + ".xlsx")
        true_labels = pd.read_excel(path_labels + "label" + str(i) + ".xlsx")
        true_labels = le.transform(true_labels["Labels"])
        
        pred_labels = pd.read_csv(path_resultados + str(i) + "\\output" + str(i) + "_" + transf + ".csv", delimiter = ';')
        pred_labels = le.transform(pred_labels["Class"])
        
        result_classes = metrics.precision_recall_fscore_support(true_labels, pred_labels)
        precision_class = np.concatenate((precision_class, result_classes[0].reshape(1,numClasses)), axis=0)
        recall_class = np.concatenate((recall_class, result_classes[1].reshape(1,numClasses)), axis=0)
        f1_class = np.concatenate((f1_class, result_classes[1].reshape(1,numClasses)), axis=0)
        
        result_wa = metrics.precision_recall_fscore_support(true_labels, pred_labels, average='weighted')
        wa_precision.append(result_wa[0])
        wa_recall.append(result_wa[1])
        
        #print(wa_recall)
        wa_f1.append(result_wa[2])
        
        confusion_matrix = confusion_matrix + metrics.confusion_matrix(true_labels, pred_labels)
    
    resultados_metricas[transf + '_cm'] = confusion_matrix
    resultados_metricas[transf + '_waPrecision'] = wa_precision
    resultados_metricas[transf + '_waRecall'] = wa_recall
    resultados_metricas[transf + '_waF1'] = wa_f1
    
    resultados_metricas[transf + "_classPrecision"] = precision_class[1:]
    resultados_metricas[transf + "_classRecall"] = recall_class[1:]
    resultados_metricas[transf + "_classF1"] = f1_class[1:]
    
    
#Gerar gráficos
labels = list(le.classes_)

#Matriz de confusão
size_titulo, size_axis, size_annot = 30, 20, 20
fig_size = (8, 6)
rotation = 45

def saveConfusionMatrix(matrix, title):
    df_cm = pd.DataFrame(matrix, range(numClasses), range(numClasses))
    fig, ax1 = plt.subplots(figsize=fig_size)
    #fig, ax1 = plt.subplots(figsize=(8,6))
    sn.set(font_scale=1.4) # for label size
    sn.heatmap(df_cm, xticklabels=labels, yticklabels=labels, annot=True, annot_kws={"size": size_annot}, fmt='g', linewidths=0.8, linecolor='white') # font size
    plt.yticks(rotation=0, fontsize=size_axis) 
    plt.xticks(rotation=rotation, fontsize=size_axis) 
    ax1.set_title(title, fontsize=size_titulo)
    plt.savefig(title + '.png', bbox_inches='tight')

cm_sum = np.zeros((numClasses, numClasses))
for i, transf in enumerate(transformacoes):
    cm_sum = cm_sum + resultados_metricas[transf + '_cm']
    titulo = "Confusion Matrix - " + lista_titulosGraficos[i]
    saveConfusionMatrix(resultados_metricas[transf + '_cm'], titulo)

saveConfusionMatrix(cm_sum, "Confusion Matrix")

#WA recall, precision, F1

def saveBoxPlot(prefix_key, title):
    matrix = np.zeros((numVideos, 1))
    for transf in transformacoes:
        m = np.array(resultados_metricas[transf + prefix_key]).reshape((numVideos, 1))
        matrix = np.concatenate((matrix, m), axis=1)
        
    matrix = matrix[:, 1:]
    fig, ax1 = plt.subplots(figsize=(20, 6))
    bp = plt.boxplot(matrix, notch=0, sym='+', vert=1, whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')
    #    ax1.boxplot(acc_matrix2)
    ax1.set_title(title, fontsize=25)
    #ax1.set_ylabel('Weighted Average Recall', fontsize=20)
    plt.xticks(list(range(1,len(lista_titulosGraficos)+1)), lista_titulosGraficos, fontsize=20)
    
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    plt.savefig(title + '.png' )
    np.save(title, matrix)
    

saveBoxPlot('_waRecall', 'Weighted Average Recall')
saveBoxPlot('_waPrecision', 'Weighted Average Precision')
saveBoxPlot('_waF1', 'Weighted Average F1 Score')

#Construir planilha com métricas em um csv
f_csv_tabela = open("resultados_metricas.csv", 'w')

f_csv_tabela.write('Transformação;')
for c in labels:
    f_csv_tabela.write(c)
    f_csv_tabela.write(';;;')
f_csv_tabela.write('\n')

f_csv_tabela.write(';')
for i in range(len(labels)):
    f_csv_tabela.write('Precision;Recall;F1 Measure;')
f_csv_tabela.write('\n')


for i, transf in enumerate(transformacoes):
    f_csv_tabela.write(lista_titulosGraficos[i] + ';')
    print(lista_titulosGraficos[i])
    mean_precision = np.around(np.mean(resultados_metricas[transf + "_classPrecision"], axis=0), decimals=4)
    mean_recall = np.around(np.mean(resultados_metricas[transf + "_classRecall"], axis=0), decimals=4)
    mean_f1 = np.around(np.mean(resultados_metricas[transf + "_classF1"], axis=0), decimals=4)
    
    std_precision = np.around(np.std(resultados_metricas[transf + "_classPrecision"], axis=0), decimals=4)
    std_recall = np.around(np.mean(resultados_metricas[transf + "_classRecall"], axis=0), decimals=4)
    std_f1 = np.around(np.mean(resultados_metricas[transf + "_classF1"], axis=0), decimals=4)
    
    print(mean_precision)
    assert len(labels) == mean_precision.shape[0] == mean_recall.shape[0] == mean_f1.shape[0]
    for i in range(len(labels)):
        f_csv_tabela.write(str(mean_precision[i]).replace('.', ',') + ' (' + str(std_precision[i]).replace('.', ',') + ');')
        f_csv_tabela.write(str(mean_recall[i]).replace('.', ',') + ' (' + str(std_recall[i]).replace('.', ',') + ');')
        f_csv_tabela.write(str(mean_f1[i]).replace('.', ',') + ' (' + str(std_f1[i]).replace('.', ',') + ');')
              
    f_csv_tabela.write('\n')
    

f_csv_tabela.close()

#Graficos F1 Measure por transformação

def saveBoxPlot2(matrix, title):
    fig, ax1 = plt.subplots(figsize=(20, 6))
    bp = plt.boxplot(matrix, notch=0, sym='+', vert=1, whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')
    #    ax1.boxplot(acc_matrix2)
    ax1.set_title(title, fontsize=25)
    #ax1.set_ylabel('Weighted Average Recall', fontsize=20)
    plt.xticks(list(range(1,len(labels)+1)), labels, fontsize=20)
    
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    plt.savefig(title + '.png' )
    np.save(title, matrix)

for i, transf in enumerate(transformacoes):
    saveBoxPlot2(resultados_metricas[transf + "_classF1"], 'F1 Score - ' + lista_titulosGraficos[i])
