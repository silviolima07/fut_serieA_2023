from PIL import Image
import numpy as np
import streamlit as st

import matplotlib.pyplot as plt

#from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#import nltk

#from bokeh.models.widgets import Div

import pandas as pd

from PIL import Image

#pd.set_option('precision',2)

#import base64

import sys

import glob

import re

import requests
from bs4 import BeautifulSoup

st.set_option('deprecation.showPyplotGlobalUse', False)
   
    

def main():

    """Futebol App """

   
    logo_seriea  = Image.open("Images/times/logo_seriea.png")
    campo  = Image.open("Images/times/campo.png")
    projeto  = Image.open("Images/projeto2.png")
    #tela  = Image.open("Images/tela1.png")
    
    
    botafogo = Image.open("Images/times/botafogo.png")
    santos = Image.open("Images/times/santos.png") 
    bahia = Image.open("Images/times/bahia.png")
    america = Image.open("Images/times/america-mineiro.png")
   
    athletico_pr    = Image.open("Images/times/athletico-paranaense.png")
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
    
    dict_times = {'botafogo': botafogo,
                   'flamengo': flamengo,
                   'red-bull-bragantino': bragantino,
                   'fluminense': fluminense,
                   'palmeiras': palmeiras,
                   'gremio': gremio,
                   'cuiaba': cuiaba,
                   'athletico-pr': athletico_pr,
                   'sao-paulo': saopaulo,
                   'cruzeiro': cruzeiro,
                   'atletico-mg': atletico_mg,
                   'internacional':internacional,
                   'fortaleza': fortaleza,
                   'corinthians': corinthians,
                   'goias': goias,
                   'bahia': bahia,
                   'santos': santos,
                   'coritiba': coritiba,
                   'vasco': vasco,
                   'america-mg': america}
    
    st.sidebar.image(logo_seriea,caption="", width=300)

    activities = ["Classificação Atual",'Campanhas 2012 a 2023',"Resumo", "Projeto", "Sobre"]
     
    
    

    choice = st.sidebar.selectbox("Selecione uma opção",activities)
    
    df = pd.read_csv("CSV/dados_2012_2023.csv")
    
    df_2023 = pd.read_csv("CSV/dados_2023.csv")

    # Definir a data da última atualização


    #st.write('Atualizacao:'+str(get_version()))      
    if choice == 'Classificação Atual':
        #st.sidebar.markdown('##   Última atualização dia: '+" "+str(get_version()))
        st.sidebar.markdown('## Atualizado às terças-feiras')
        
     
    
    
    if choice == activities[0]: # Classificação atual
        
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
    
        size_1= st.sidebar.slider('Primeiro', 80, 140, 80)
    
        size_2_20= st.sidebar.slider("Segundo ao Vigesimo", 30,90,30)
    
        extra = 20
        extra_reb = 10

        
        #df = pd.read_csv("CSV/dados_2012_2023.csv")
        #saldo_gols = df_2023['saldo_gols']
        #df['saldo_gols'] = saldo_gols
        
        df_2023 = df_2023.sort_values(by= ['pontos', 'vitorias', 'saldo_gols'], ascending=False)
        
        #df_2023['jogos'] = df_2023['vitorias']+df_2023['derrotas']+df_2023['empates']

        rodada_numero = df_2023['jogos'].max()
        
        st.subheader('Rodada: '+ str(rodada_numero)+(' de 38'))     
        
        l_posicao = list(df_2023.times)
       
        #     
        #st.dataframe(df_2023[['times', 'pontos', 'saldo_gols']])
        #df_2023['pontos'] = df_2023['pontos'].astype('int')
        pontuacao = df_2023['pontos'].to_list()
        
        col1, col2 = st.columns(2)
    
        col11, col22 = st.columns(2)
        
        col_teste1,col_teste2, col_teste3, col_teste4 = st.columns(4)
        
                
        #col_teste1.header(l_posicao[0])
        col_teste1.text("Primeiro - "+str(pontuacao[0]))
        col_teste1.image(dict_times.get(l_posicao[0]))
        
        
        #col_teste2.header(l_posicao[1])
        col_teste1.text("Segundo - "+str(pontuacao[1]))
        col_teste1.image(dict_times.get(l_posicao[1]), width=size_2_20+extra)

        #col_teste2.header(l_posicao[2])
        col_teste1.text("Terceiro - "+str(pontuacao[2]))
        col_teste1.image(dict_times.get(l_posicao[2]), width=size_2_20+extra)

        #col_teste2.header(l_posicao[3])
        col_teste1.text("Quarto - "+str(pontuacao[3]))
        col_teste1.image(dict_times.get(l_posicao[3]), width=size_2_20+extra)
        
        #col_teste2.header(l_posicao[4])
        col_teste1.text("Quinto - "+str(pontuacao[4]))
        col_teste1.image(dict_times.get(l_posicao[4]), width=size_2_20+extra)
        
        #col_teste2.header(l_posicao[5])
        col_teste1.text("Sexto - "+str(pontuacao[5]))
        col_teste1.image(dict_times.get(l_posicao[5]), width=size_2_20+extra)
        
        #col_teste2.header(l_posicao[6])
        col_teste2.text("Setimo - "+str(pontuacao[6]))
        col_teste2.image(dict_times.get(l_posicao[6]), width=size_2_20+extra)
        
        #col_teste2.header(l_posicao[7])
        col_teste2.text("Oitavo - "+str(pontuacao[7]))
        col_teste2.image(dict_times.get(l_posicao[7]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[8])
        col_teste2.text("Nono - "+str(pontuacao[8]))
        col_teste2.image(dict_times.get(l_posicao[8]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[9])
        col_teste2.text("Decimo - "+str(pontuacao[9]))
        col_teste2.image(dict_times.get(l_posicao[9]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[10])
        col_teste2.text("Decimo Primeiro - "+str(pontuacao[10]))
        col_teste2.image(dict_times.get(l_posicao[10]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[11])
        col_teste3.text("Decimo Segundo - "+str(pontuacao[11]))
        col_teste3.image(dict_times.get(l_posicao[11]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[12])
        col_teste3.text("Decimo Terceiro - "+str(pontuacao[12]))
        col_teste3.image(dict_times.get(l_posicao[12]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[13])
        col_teste3.text("Decimmo Quarto - "+str(pontuacao[13]))
        col_teste3.image(dict_times.get(l_posicao[13]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[14])
        col_teste3.text("Decimo Quinto - "+str(pontuacao[14]))
        col_teste3.image(dict_times.get(l_posicao[14]), width=size_2_20+extra)
        
        #col_teste3.header(l_posicao[15])
        col_teste3.text("Decimmo Sexto - "+str(pontuacao[15]))
        col_teste3.image(dict_times.get(l_posicao[15]), width=size_2_20+extra)
        
        
        # Ultimos 4 times
       
        #col_teste4.header('Zona de Rebaixamento: '+l_posicao[16])
        col_teste4.header('Zona de Rebaixamento: ')
        col_teste4.text("Decimmo Setimo - "+str(pontuacao[16]))
        col_teste4.image(dict_times.get(l_posicao[16]), width=size_2_20+extra_reb)
        
        
        #col_teste4.header(l_posicao[17])
        col_teste4.text("Decimmo Oitavo - "+str(pontuacao[17]))
        col_teste4.image(dict_times.get(l_posicao[17]), width=size_2_20+extra_reb)
        
        #col_teste4.header(l_posicao[18])
        col_teste4.text("Decimmo Nono - "+str(pontuacao[18]))
        col_teste4.image(dict_times.get(l_posicao[18]), width=size_2_20+extra_reb)
    
    
        #col_teste4.header(l_posicao[19])
        col_teste4.text("Vigesimo - "+str(pontuacao[19]))
        col_teste4.image(dict_times.get(l_posicao[19]), width=size_2_20+extra_reb)
    
        
    
    
    elif choice == activities[1]: # campanhas 2012  2023
    
        html_page_activiy_1 = """
    <div style="background-color:white;padding=30px">
        <p style='text-align:center;font-size:30px;font-weight:bold;color:red'>Campeonato Brasileiro de 2012 A 2022</p>
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
        
        # Remover 2023 da lista de season para escolha
        # Pois a base não é atualizada constantemente
        df_time = df_time.loc[df_time.season != 2023]
        
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
        vitorias = []
        derrotas = []
        empates = []
        total_gols = 0
        for time in lista_times:
            temp = df.loc[df.times == time]
            gols_pro = temp.gols_marcados.sum()
            gols_marcados.append(gols_pro)

            gols_levados = temp.gols_levados.sum()
            gols_tomados.append(gols_levados)
            
            total_v = temp.vitorias.sum()
            vitorias.append(total_v)
            
            total_d = temp.derrotas.sum()
            derrotas.append(total_d)
            
            total_e = temp.empates.sum()
            empates.append(total_e)
            
            
            total_gols = total_gols + gols_pro
            #print("\nTime:", time, "Gols marcados:", gols_pro)

        data = {'TIME': lista_times, 'GOLS_PRO':gols_marcados, 'GOLS_CONTRA': gols_tomados, 'VITORIAS':vitorias, 'DERROTAS':derrotas, 'EMPATES':empates}
        df_geral = pd.DataFrame(data).sort_values(by='GOLS_PRO', ascending=False)
        
        st.sidebar.markdown(" ## Total de Gols:    "+ str(total_gols))
    
        st.table(df_geral.reset_index(drop=True))
        
    elif choice == activities[3]:
        html_page_projeto = """
    <div style="background-color:white;padding=30px">
        <p style='text-align:left;font-size:30px;font-weight:bold;color:red'>Layout do Projeto</p>
    </div>
              """
        st.markdown(html_page_projeto, unsafe_allow_html=True)
        
        st.image(projeto, width = 800)
        #st.image(tela, use_column_width='auto')

        
    
    elif choice == 'Sobre':
        html_page_about = """
    <div style="background-color:white;padding=30px">
        <p style='text-align:left;font-size:30px;font-weight:bold;color:red'>Saiba mais...</p>
    </div>
              """
        st.markdown(html_page_about, unsafe_allow_html=True)
        
        st.subheader("Built with Streamlit")
        
        st.markdown("##### Dados coletados via scrap usando: request e BeautifulSoup.")
        
        st.markdown("##### Classificação considera a pontuação. Em caso de empate, total de vitórias e saldo de gols.")

        st.markdown("##### Fonte dos dados: ")
        st.markdown("##### https://www.football-data.co.uk/")
        st.markdown("##### As atualizações do campeonato atual ocorrem normalmente às terças-feiras, pois alguns times podem jogar na segunda-feira.")
        st.markdown("##### Um script Python é executado via Git Actions, esse script faz a leitura do dataset CSV no site da página football-data.")
        st.markdown("##### O script pode ser executado sob demanda ou agendamento.")
      
        st.subheader("Silvio Lima")
        
        st.markdown('#### https://www.linkedin.com/in/silviocesarlima/')
       
    
    
       

   
      
if __name__ == '__main__':
    main()




