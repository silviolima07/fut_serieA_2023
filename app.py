from PIL import Image
import numpy as np
import streamlit as st

import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import nltk

#from bokeh.models.widgets import Div

import pandas as pd

from PIL import Image

#pd.set_option('precision',2)

import base64

import sys

import glob

import re

import requests
from bs4 import BeautifulSoup



st.set_option('deprecation.showPyplotGlobalUse', False)


def clean_desc(df):
    desc = []
    for line in df.Descrição:
        words = line.replace('Postado', '').replace('há','').replace(',','').replace('dias','').replace('+ ','').replace('·','').lower().replace('(','').replace(')','')
        line = re.sub("\d+", "", words).replace('employerativa','').replace('atrás','').replace(';','').replace('–…','').replace('…','').strip().replace('.','')
        temp = "".join(line)
        desc.append(temp)   
    return desc

# Python3 code to find frequency of each word
# function for calculating the frequency

def freq(str):
    word = []
    count_word  = []
  
    # break the string into list of words
    str_list = str.split()
  
    # gives set of unique words
    unique_words = set(str_list)

    # Lib de palavras stopwords
    nltk.download('stopwords')
    #
    stopwords = nltk.corpus.stopwords.words('portuguese')
    #stopwords = ['a','de']
    
    # Eliminar de lista unique_words as palavras irrelevantes tipo: de, a, em
    dataset = unique_words
    lista_sem_stopwords = [word for word in dataset if word not in stopwords]
    
    for words in lista_sem_stopwords :
        count = str_list.count(words)
        #print('Frequency of ', words , 'is :', count)
        word.append(words)
        count_word.append(count)
    return word, count_word      


def download_link(df):
    if isinstance(df,pd.DataFrame):
        object_to_download = df.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{texto1}">{texto2}</a>'

def get_table_download_link(df,file):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download= "{file}" >Download csv</a>'
    return href
    

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link
    return f'<a target="_blank" href="{link}">Link da vaga</a>' # ou {text} e irá mostrar o link clicável


def wc(df):
        
        # Remover caracteres, palavras indesejados na coluna Descrição do dataset lido
        desc = clean_desc(df)
        #

        # Une todos itens/palavras da lista com a descrição numa linha unica
        string_desc = ' '.join([str(item) for item in desc])

        # Cria duas listas, uma lista word com todas palavras e uma lista com a frequencia dessas palavras na descrição
        word, count_word = freq(string_desc)
        #

        # Converter para dict, sendo chave a word e valor a frequencia da palavra
        data = dict(zip(word, count_word ))
        #print(data)
        #
        

        # Cria a wordcloud baseada nos valores no dicionario gerado
        wc = WordCloud(width=300, height=300, max_words=200).generate_from_frequencies(data)
        
        #plt.figure(figsize=(100,100))
        #plt.imshow(wc)
        
        # Titulo do web app
        html_wordcloud = """
    <div style="background-color:blue;padding=25px">
        <p style='text-align:center;font-size:25px;font-weight:bold;color:white'>Termos mais frequentes na Descrição</p>
    </div>
              """
        st.markdown(html_wordcloud, unsafe_allow_html=True)
        
        # Plota a wordcloud gerada
        fig = plt.figure(figsize=(12,12), dpi=100)
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        #plt.show()
        st.pyplot(fig)
        


def get_version():
    """
    Funcao get_version retorna a data de criacao do arquivo csv.
    Return: data
    """
    URL = "https://www.football-data.co.uk/brazil.php"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all("i")
    for link in links:
        #print(link, "-",link.text)
        version_data = str(link).replace('<i>Last updated:','').replace('</i>', '').strip()
    #print('Última atualização:',version_data)
    return version_data
    
def get_data():
    """
    Funcao get_data traz o dataset csv.
    Return: csv
    """
    URL = "https://www.football-data.co.uk/brazil.php"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    # Extrair a linha que tem a string CSV, exatamente onde tem a url para baixar o arquivo csv.
    links = soup.find_all("a")
    for link in links:
        if link.text == 'CSV':
            #print(link, "-",link.text)
            link_csv = str(link).replace('<a href="','').replace('">CSV</a>', '')
    #print(link_csv)

    url = 'https://www.football-data.co.uk/'

    url_csv = url+link_csv

    df = pd.read_csv(url_csv)
    return df

def get_gols(time, df):
    """
      Funcao get_gols o total de gols que um time fez ou levou.
      input: time (string), df (dataframe)
      return: int
    """
    gols_marcados = 0
    gols_levados = 0
    #print("\nSeason:", season)
    for index, row in df.iterrows():
        if row['Home'] == time:
            gols_marcados    = int(gols_marcados + row['HG'])
            gols_levados = int(gols_levados + row['AG'])
        elif row['Away'] == time:
            gols_marcados    = int(gols_marcados + row['AG'])
            gols_levados = int(gols_levados + row['HG'])
    #print(time.upper())
    print("\tTotal gols marcados:",int(gols_marcados))
    print("\tTotal gols levados:",int(gols_levados))
    return (gols_marcados, gols_levados)

def get_resultados(time, df):
    """
      Funcao get_resultados retorna o total de vitorias, derrotas e empates de um time.
      Traz também os times que ele enfrentou e a pontuação no momento.
      Input: time (string), df (dataframe)
      Return: int e string
    """
    jogo = 1
    vitorias = 0
    lista_v = []
    empates = 0
    lista_e = []
    derrotas = 0
    lista_d = []
    lista_placar_v = []
    lista_placar_d = []
    lista_placar_e = []
    for index, row in df.iterrows():
        #print("\n\nAno:", row['Season'])
        # VITORIAS
        if row['Home'] == time and row['HG'] > row['AG']:
            # Jogo em casa
            vitorias    = int(vitorias + 1)
            placar = row['Home']+'-'+str(row['HG'])+'X'+str(row['AG'])+'-'+(row['Away'])
            print("\n",row['Season'],"- VITORIA em CASA -->", placar)
            lista_placar_v.append(placar) # Placar da vitoria em  casa
            lista_v.append(row['Away']) # Time visitante que perdeu
        elif row['Away'] == time and row['AG'] > row['HG']:
            # Jogo visitante
            vitorias    = int(vitorias + 1)
            lista_v.append(row['Home']) # Time da casa que perdeu
            placar = row['Home']+'-'+str(row['HG'])+'X'+str(row['AG'])+'-'+(row['Away'])
            print("\n",row['Season'],"- VITORIA FORA de CASA -->", placar)
            lista_placar_v.append(placar) # Placar da vitoria como visitane

        # DERROTAS
        elif row['Home'] == time and row['HG'] < row['AG']:
            # Jogo em casa
            derrotas     = int(derrotas + 1)
            lista_d.append(row['Away'])
            placar = row['Home']+'-'+str(row['HG'])+'X'+str(row['AG'])+'-'+(row['Away'])
            print("\n",row['Season'],"- DERROTA em CASA -->", placar)
            lista_placar_d.append(placar) # Placar da derrota em casa
        elif row['Away'] == time and row['AG'] < row['HG']:
            # Jogo como visitante
            derrotas     = int(derrotas + 1)
            lista_d.append(row['Home'])# Time da casa que ganhou
            placar = row['Home']+'-'+str(row['HG'])+'X'+str(row['AG'])+'-'+(row['Away'])
            print("\n",row['Season'],"- DERROTA FORA de  CASA -->", placar)
            lista_placar_d.append(placar)

        # EMPATES
        elif row['Home'] == time and row['HG'] == row['AG'] and row['Res'] == 'D':
            # Jogo em casa
            empates = int(empates +1)
            lista_e.append(row['Away']) # Time visitante com quem empatou
            placar = row['Home']+'-'+str(row['HG'])+'X'+str(row['AG'])+'-'+(row['Away'])
            print("\n",row['Season'],"- EMPATE em CASA -->", placar)
            lista_placar_e.append(placar) # Placar do empate em casa

        elif row['Away'] == time and row['HG'] == row['AG'] and row['Res'] == 'D':
            # Jogo como visitante
            empates = int(empates +1)
            lista_e.append(row['Home']) # Time da casa com quem empatou
            placar = row['Home']+'-'+str(row['HG'])+'X'+str(row['AG'])+'-'+(row['Away'])
            print("\n",row['Season'],"- EMPATE FORA de CASA -->", placar)
            lista_placar_e.append(placar)

        jogo = jogo +1


    pontos = vitorias*3 + empates
    #print(time.upper())
    print("\tTotal vitorias",int(vitorias))
    lista_v = str(lista_v).replace("'",'').replace('[','').replace(']','')
    print("\tVitoria contra:", lista_v)

    print("\tTotal derrotas:",derrotas)
    lista_d = str(lista_d).replace("'",'').replace('[','').replace(']','')
    print("\tDerrota para:",lista_d)

    print("\tTotal empates:",empates)
    lista_e = str(lista_e).replace("'",'').replace('[','').replace(']','')
    print("\tEmpate com:",lista_e)
    #placar = row['Home']+'-'+str(row['HG'])+'X'+str(row['AG'])+'-'+(row['Away'])
    #lista_placar_e.append(placar)

    print("\tPontos:", pontos)
    return (vitorias, derrotas, empates, pontos, lista_v, lista_d, lista_e, lista_placar_v, lista_placar_d, lista_placar_e)

    
    

def main():

    """Futebol App """

    # Titulo do web app
    #html_indeed = """
    #<div style="background-color:blue;padding=30px">
    #    <p style='text-align:center;font-size:30px;font-weight:bold;color:red'>Futebol</p>
    #</div>
    #          """
    #st.markdown(html_indeed, unsafe_allow_html=True)
   
    #html_page = """
    #<div style="background-color:white;padding=30px">
    #    <p style='text-align:center;font-size:30px;font-weight:bold;color:red'>Campeonato Brasileiro de 2012 a 2023</p>
    #</div>
    #          """
    #st.markdown(html_page, unsafe_allow_html=True)

   
    
    
   
    logo_seriea  = Image.open("Images/times/logo_seriea.png")
    campo  = Image.open("Images/times/campo.png")
    
    
    botafogo = Image.open("Images/times/botafogo.png")
    santos = Image.open("Images/times/santos.png") 
    bahia = Image.open("Images/times/bahia.png")
    america = Image.open("Images/times/america-mineiro.png")
   
    atletico_pr    = Image.open("Images/times/athletico-paranaense.png")
    atletico_mg    = Image.open("Images/times/atletico-mineiro.png")
    
    corinthians    = Image.open("Images/times/corinthians.png")
    coritiba    = Image.open("Images/times/coritiba.png")
    cruzeiro    = Image.open("Images/times/cruzeiro.png")
    cuiaba    = Image.open("Images/times/cuiaba.png")
    flamengo    = Image.open("Images/times/flamengo.png")
    
    fluminense    = Image.open("Images/times/fluminense.png")
    fortaleza    = Image.open("Images/times/fortaleza.png")
    goias    = Image.open("Images/times/goias-esporte-clube.png")
    gremio    = Image.open("Images/times/gremio.png")
    internacional    = Image.open("Images/times/internacional.png")
    
    palmeiras    = Image.open("Images/times/palmeiras.png")
    bragantino    = Image.open("Images/times/red-bull-bragantino.png")
    saopaulo    = Image.open("Images/times/sao-paulo.png")
    vasco    = Image.open("Images/times/vasco-da-gama.png")
    
    dict_times = {'Botafogo RJ': botafogo,
                   'Flamengo RJ': flamengo,
                   'Bragantino': bragantino,
                   'Fluminense': fluminense,
                   'Palmeiras': palmeiras,
                   'Gremio': gremio,
                   'Cuiaba': cuiaba,
                   'Athletico-PR': atletico_pr,
                   'Sao Paulo': saopaulo,
                   'Cruzeiro': cruzeiro,
                   'Atletico-MG': atletico_mg,
                   'Internacional':internacional,
                   'Fortaleza': fortaleza,
                   'Corinthians': corinthians,
                   'Goias': goias,
                   'Bahia': bahia,
                   'Santos': santos,
                   'Coritiba': coritiba,
                   'Vasco': vasco,
                   'America MG': america}
    
    st.sidebar.image(logo_seriea,caption="", width=300)

    activities = ["Classificação Atual",'Campanhas 2012 a 2023',"Resumo","Sobre"]
    lista_CD= []
    lista_AD=[]
    lista_EML=[]
    lista_ED=[]
    lista_intervalo = []
    
    
    for f in glob.iglob("CSV/*.csv"): # generator, search immediate subdirectories
        #st.write(f)

        if str(f).startswith('CSV/indeed_CD'):
            lista_CD.append(f)
            temp = f.replace('indeed_CD_','').replace('.csv','').replace('CSV/','')
            lista_CD.append(temp)
         
        if f.startswith('CSV/indeed_AD'):
            lista_AD.append(f)
            temp = f.replace('indeed_AD_','').replace('.csv','').replace('CSV/','')
            lista_AD.append(temp)

        if f.startswith('CSV/indeed_EML'):
            lista_EML.append(f)
            temp = f.replace('indeed_EML_','').replace('.csv','').replace('CSV/','')
            lista_EML.append(temp)

        if f.startswith('CSV/indeed_ED'):
            lista_ED.append(f)
            temp = f.replace('indeed_ED_','').replace('.csv','').replace('CSV/','')
            lista_ED.append(temp)


    choice = st.sidebar.selectbox("Selecione uma opção",activities)
    
    df = pd.read_csv("CSV/dados_2012_2023.csv")

    # Definir a data da última atualização


    #st.write('Atualizacao:'+str(get_version()))      
    if choice == 'Classificação Atual':
        st.sidebar.markdown('##   Última atualização dia: '+" "+str(get_version()))

        

    
    
  
    
    
    if choice == activities[0]:
        
        html_page_activiy_0 = """
    <div style="background-color:white;padding=30px">
        <p style='text-align:center;font-size:30px;font-weight:bold;color:red'>Classificação Atual</p>
    </div>
              """
        st.markdown(html_page_activiy_0, unsafe_allow_html=True)
        
        #width = 100
        #width0 = 140
        #width1 = 120
        #width2 = 120
        #width_reb = 90
    
        size_1= st.sidebar.slider('Primeiro', 80, 110, 80)
    
        size_2_20= st.sidebar.slider("2 a 20", 50,80)
    
        extra = 20
        extra_reb = 10

        
        #df = pd.read_csv("CSV/dados_2012_2023.csv")
        saldo_gols = df['gols_marcados'] - df['gols_levados']
        df['saldo_gols'] = saldo_gols
        df_2023 = df.loc[df.season == 2023].sort_values(by= ['pontos','saldo_gols'], ascending=False)
        l_posicao = list(df_2023.times)
        
        #st.dataframe(df_2023[['times', 'pontos', 'saldo_gols']])

       
        col1, col2 = st.columns(2)
    
        col11, col22 = st.columns(2)
        
        col_teste1,col_teste2, col_teste3, col_teste4 = st.columns(4)
        
        
        #col_teste1.header(l_posicao[0])
        col_teste1.text("Primeiro")
        col_teste1.image(dict_times.get(l_posicao[0]), width=size_1+extra)
        
        #col_teste2.header(l_posicao[1])
        col_teste1.text("Segundo")
        col_teste1.image(dict_times.get(l_posicao[1]), width=size_2_20+extra)

        #col_teste2.header(l_posicao[2])
        col_teste1.text("Terceiro")
        col_teste1.image(dict_times.get(l_posicao[2]), width=size_2_20+extra)

        #col_teste2.header(l_posicao[3])
        col_teste1.text("Quarto")
        col_teste1.image(dict_times.get(l_posicao[3]), width=size_2_20+extra)
        
        #col_teste2.header(l_posicao[4])
        col_teste1.text("Quinto")
        col_teste1.image(dict_times.get(l_posicao[4]), width=size_2_20+extra)
        
        #col_teste2.header(l_posicao[5])
        col_teste1.text("Sexto")
        col_teste1.image(dict_times.get(l_posicao[5]), width=size_2_20+extra)
        
        #col_teste2.header(l_posicao[6])
        col_teste2.text("Setimo")
        col_teste2.image(dict_times.get(l_posicao[6]), width=size_2_20+extra)
        
        #col_teste2.header(l_posicao[7])
        col_teste2.text("Oitavo")
        col_teste2.image(dict_times.get(l_posicao[7]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[8])
        col_teste2.text("Nono")
        col_teste2.image(dict_times.get(l_posicao[8]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[9])
        col_teste2.text("Decimo")
        col_teste2.image(dict_times.get(l_posicao[9]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[10])
        col_teste2.text("Decimo Primeiro")
        col_teste2.image(dict_times.get(l_posicao[10]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[11])
        col_teste3.text("Decimo Segundo")
        col_teste3.image(dict_times.get(l_posicao[11]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[12])
        col_teste3.text("Decimo Terceiro")
        col_teste3.image(dict_times.get(l_posicao[12]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[13])
        col_teste3.text("Decimmo Quarto")
        col_teste3.image(dict_times.get(l_posicao[13]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[14])
        col_teste3.text("Decimo Quinto")
        col_teste3.image(dict_times.get(l_posicao[14]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[15])
        col_teste3.text("Decimmo Sexto")
        col_teste3.image(dict_times.get(l_posicao[15]), width=size_2_20+extra)
        
        
        # Ultimos 4 times
       
        #col_teste4.header('Zona de Rebaixamento: '+l_posicao[16])
        col_teste4.header('Zona de Rebaixamento: ')
        col_teste4.text("Decimmo Setimo")
        col_teste4.image(dict_times.get(l_posicao[16]), width=size_2_20+extra_reb)
        
        
        #col_teste4.header(l_posicao[17])
        col_teste4.text("Decimmo Oitavo")
        col_teste4.image(dict_times.get(l_posicao[17]), width=size_2_20+extra_reb)
        
        #col_teste4.header(l_posicao[18])
        col_teste4.text("Decimmo Nono")
        col_teste4.image(dict_times.get(l_posicao[18]), width=size_2_20+extra_reb)
    
    
        #col_teste4.header(l_posicao[19])
        col_teste4.text("Vigesimo")
        col_teste4.image(dict_times.get(l_posicao[19]), width=size_2_20+extra_reb)
    
        
    
    
    elif choice == activities[1]: # campanhas 2012  2023
    
        html_page_activiy_1 = """
    <div style="background-color:white;padding=30px">
        <p style='text-align:center;font-size:30px;font-weight:bold;color:red'>Campeonato Brasileiro de 2012 A 2023</p>
    </div>
              """
        st.markdown(html_page_activiy_1, unsafe_allow_html=True)
                
        usecols = ['season', 'times', 'pontos', 'gols_marcados', 'gols_levados', 'vitorias', 'derrotas', 'empates',
                   'time_ganhou', 'time_derrota', 'time_empate', 'placar_vitoria', 'placar_derrota', 'placar_empate']
        #df = pd.read_csv("CSV/dados_2012_2023.csv", usecols = usecols)
        #l_seasons = sorted(set(df['season']))
        l_times = sorted(set(df['times']))
        
        choice_time = st.sidebar.selectbox("Time",l_times)
        df_time = df.loc[df.times == choice_time]
        
        
        
        l_seasons = sorted(set(df_time['season']))
        
        choice_ano = st.sidebar.selectbox("Ano",l_seasons)
        
        st.sidebar.image(campo,caption="",width=300)
        
        #st.subheader(str(choice_ano)+'/'+choice_time)
        st.subheader(choice_time+' / '+str(choice_ano))
        
        df = df.loc[(df.season == choice_ano)& (df.times == choice_time)]
        colunas = ['season','pontos', 'gols_marcados', 'gols_levados', 'vitorias', 'derrotas', 'empates','time_ganhou', 'time_derrota', 'time_empate', 'placar_vitoria', 'placar_derrota', 'placar_empate']
        df = df[colunas]
        colunas_tela = ['pontos', 'gols_marcados', 'gols_levados', 'vitorias', 'derrotas', 'empates']
        temp = df[colunas_tela]
        temp.rename(columns={'pontos':'PONTOS', 'gols_marcados':'GOLS_MARCADOS', 'gols_levados':'GOLS_TOMADDOS', 'vitorias': 'VITORIAS', 'derrotas':'DERROTAS', 'empates': 'EMPATES'}, inplace=True)
        
        temp = temp.reset_index(drop=True)
        temp = temp.set_index(df['season'])
        st.dataframe(temp)
        
        flag_vitoria = False
        flag_empate = False
        flag_derrota = False
        
        flag_lista_derrotas = False
        flag_lista_empates = False
        flag_lista_vitorias = False
        
        flag_placar_derrota  = False
        flag_placar_empate = False
        flag_placar_vitoria = False
        
        
        col1,   col2,   col3   = st.columns(3)
        col11,  col22,  col33  = st.columns(3)
        col111, col222, col333 = st.columns(3)
        
        col1111, col2222, col3333 = st.columns(3)
        

        res = ['Vitoria', 'Derrota', 'Empate', 
                'Lista Vitorias', 'Lista_Derrotas', 'Lista_Empates', 
                'Placar_Vitoria', 'Placar_Derrota', 'Placar_Empate']
        key = [1,2,3,4,5,6,7,8,9]
                
        with col1:
          if(st.button(res[0], key=f'{0}')):
            flag_vitoria = True
            
        with col2:
          if(st.button(res[1], key=key[1])):
            flag_derrota = True
            
        with col3:
          if(st.button(res[2], key=key[2])):
            flag_empate = True
            
        #with col11:
        #  if(st.button(res[3], key=key[3])):
        #    flag_lista_vitorias = True
            
        #with col22:
        #  if(st.button(res[4], key=key[4])):
        #    flag_lista_derrotas = True 
         
        #with col33:
        #  if(st.button(res[5], key=key[5])):
        #    flag_lista_empates = True 

        with col111:
          if(st.button(res[6], key=key[6])):
            flag_placar_vitoria = True

        with col222:
          if(st.button(res[7], key=key[7])):
            flag_placar_derrota = True

        with col333:
          if(st.button(res[8], key=key[8])):
            flag_placar_empate = True            
                            
       
        if (flag_vitoria):
            vitorias = df['time_ganhou']
          
            temp = pd.DataFrame(vitorias)
            temp2 = temp.time_ganhou.str.split(',')
            lista = []
            for i in temp2:
              for x in i:
                x = x.replace('[','').replace(']','').replace('\\"','').replace("'",'')
                st.subheader(x)
           
        if (flag_derrota):
            derrotas = df['time_derrota']
            
            temp = pd.DataFrame(derrotas)
            temp2 = temp.time_derrota.str.split(',')
            lista = []
            
            for i in temp2:
              for x in i:
                x = x.replace('[','').replace(']','').replace('\\"','').replace("'",'')
                st.subheader(x)
               

             
        if (flag_empate):
            #st.write(df['time_empate'])
            empates = df['time_empate']
          
            temp = pd.DataFrame(empates)
            temp2 = temp.time_empate.str.split(',')
            lista = []
            for i in temp2:
              for x in i:
                x = x.replace('[','').replace(']','').replace('\\"','').replace("'",'')
                st.subheader(x)
               
            
            
        if (flag_placar_vitoria):
            vitorias = df['placar_vitoria']
            #print('TIPO:', type(empates))
            #for item in empates:
            temp = pd.DataFrame(vitorias)
            temp2 = temp.placar_vitoria.str.split(',')
            lista = []
            for i in temp2:
              for x in i:
                x = x.replace('[','').replace(']','').replace('\\"','').replace("'",'')
                st.subheader(x)   
        
        if (flag_placar_derrota):
            derrota = df['placar_derrota']
            temp = pd.DataFrame(derrota)
            temp2 = temp.placar_derrota.str.split(',')
            lista = []
            for i in temp2:
              for x in i:
                x = x.replace('[','').replace(']','').replace('\\"','').replace("'",'')
                st.subheader(x) 
                
        if (flag_placar_empate):
            empates = df['placar_empate']
            temp = pd.DataFrame(empates)
            temp2 = temp.placar_empate.str.split(',')
            lista = []
            for i in temp2:
              for x in i:
                x = x.replace('[','').replace(']','').replace('\\"','').replace("'",'')
                st.subheader(x)         
        
        if (flag_vitoria):
          col2222.header('Vitórias')    
          
        if (flag_derrota):
          col2222.header('Derrotas')   

        if (flag_empate):
          col2222.header('Empates')  

        if (flag_placar_vitoria):
          col2222.header('Placar Vitórias')  

        if (flag_placar_derrota):
          col2222.header('Placar Derrotas')  

        if (flag_placar_empate):
          col2222.header('Placar Empates')            
        
    elif choice == activities[2]:
        html_page_resumo = """
    <div style="background-color:white;padding=30px">
        <p style='text-align:left;font-size:30px;font-weight:bold;color:red'>Resumo de Participações (2012 a 2023)</p>
    </div>
              """
        st.markdown(html_page_resumo, unsafe_allow_html=True)
        
        lista_times = list(set(df['times']))
        gols_marcados = []
        gols_tomados = []
        total_gols = 0
        for time in lista_times:
            temp = df.loc[df.times == time]
            gols_pro = temp.gols_marcados.sum()
            gols_marcados.append(gols_pro)

            gols_levados = temp.gols_levados.sum()
            gols_tomados.append(gols_levados)

            total_gols = total_gols + gols_pro
            #print("\nTime:", time, "Gols marcados:", gols_pro)

        data = {'TIME': lista_times, 'GOLS_MARCADOS':gols_marcados, 'GOLS_TOMADOS': gols_tomados}
        df_geral = pd.DataFrame(data).sort_values(by='GOLS_MARCADOS', ascending=False)
        
        st.sidebar.markdown(" ## Total de Gols:    "+ str(total_gols))
    
        st.table(df_geral.reset_index(drop=True))
    
    elif choice == 'Sobre':
        html_page_about = """
    <div style="background-color:white;padding=30px">
        <p style='text-align:left;font-size:30px;font-weight:bold;color:red'>Saiba mais...</p>
    </div>
              """
        st.markdown(html_page_about, unsafe_allow_html=True)
        
        st.subheader("Built with Streamlit")
        
        st.markdown("#### Dados coletados via scrap usando: request e BeautifulSoup.")

        st.markdown("#### Fonte dos dados: ")
        st.markdown("#### https://www.football-data.co.uk/")
        st.markdown("#### As atualizações do campeonato atual ocorrem normalmente às terças-feiras, pois estão agendados jogos na segunda-feira.")
      
        st.subheader("Silvio Lima")
        
        st.markdown('#### https://www.linkedin.com/in/silviocesarlima/')
       
    
    
       

   
      
if __name__ == '__main__':
    main()




