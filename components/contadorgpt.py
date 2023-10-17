from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

from dotenv import load_dotenv
import openai
import os
from app import *
load_dotenv()
from dash_bootstrap_templates import ThemeSwitchAIO


template_theme1 = "flatly" 
template_theme2 = "vapor"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.VAPOR


# Carregue a chave da API da OpenAI das variáveis de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    df_historico_msgs = pd.read_csv('historical_msgs.csv', index_col=0)
except:
    df_historico_msgs = pd.DataFrame(columns=['user', 'chatGPT'])
    df_historico_msgs.to_csv('historical_msgs.csv')

try:
    df_df = pd.read_csv('vitalfarma01.csv')
except:
    df_df = pd.read_csv('vitalfarma01.csv')


def generate_card_gpt(pesquisa):
    cardNovo = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.H5([html.I(className='fa fa-desktop', style={"fontSize": '85%'}), "StocksGPT"], className='dbc'),
                                    html.H5(str(pesquisa), className='dbc')
                                ], md=2, style={'text-align': 'left'}),
                            ])
                        ])
                    ])
                ])
            ], class_name='card_chatgpt_gpt')
        ])
    ], className='g-2 my-auto')
    
    return cardNovo 


def generate_card_user(pesquisa):
    cardNovo = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.H5([html.I(className='fa fa-user-circle', style={"fontSize": '85%'}), "User"], className='dbc'),
                                    html.H5(str(pesquisa), className='dbc')
                                ], md=2, style={'text-align': 'left'}),
                            ])
                        ])
                    ])
                ])
            ], class_name='card_chatgpt_user')
        ])
    ], className='g-2 my-auto')
    
    return cardNovo 

def clusterCards(df_msg_store):

    df_historical_msg = pd.DataFrame(df_msg_store)
    cardList = []

    for line in df_historical_msg.iterrows():
        card_pergunta = generate_card_user(line[1]['user'])
        card_resposta = generate_card_gpt(line[1]['chatGPT'])

        cardList.append(card_pergunta)
        cardList.append(card_resposta)

    return cardList


def gerar_resposta(mensagem):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=mensagem,
            max_tokens=1024,
            temperature=1,
        )
        retorno = response.choices[0].message.content
    except:
        retorno = "Não foi possível pesquisar. DW Contador fora do ar"
    return retorno

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col("", className='dbc', style={'margin-top': '10px','font-size': '60px'}, md=12)
            ], className='g-2 my-auto'),

            dbc.Row([
                dbc.Col([
                    dbc.Input(id="msg_user_wallet",type="text", placeholder="Olá, tudo bem? Sou o seu Contador Consultor. Como posso ajudar você hoje?")
                ], md=10),
                dbc.Col([
                    dbc.Button("Enviar", id="botao_search_wallet")
                ], md=2)
            ], className='g-2 my-auto'),

            dbc.Row([
                dbc.Col([

                ], md=12, id='cards_respostas_wallet', style={"height": "100%", "maxHeight": "25rem", "overflow-y": "auto"})
            ], className='g-2 my-auto')
        ], md=9)
    ], className='g-2 my-auto')
], fluid=True)


@app.callback(
    Output('cards_respostas_wallet', 'children'),
    State('msg_user_wallet', 'value'),
    Input('botao_search_wallet', 'n_clicks'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def add_msg(msg_user, n, toggle):
    template = template_theme1 if toggle else template_theme2

    df_historical_msgs = pd.read_csv('historical_msgs.csv', index_col=0)

    if msg_user == None:
        lista_cards = clusterCards(df_historical_msgs)
        return lista_cards
    if 'produto'.lower() in msg_user or 'produto'.lower() in msg_user:
        mensagem = f'{df_df}, considerando todos os dados existentes no dataframe, desde a primeira linha até a última linha, qual é a resposta exata de um Consultor para a pergunta: ' + msg_user
    else:
        mensagem = 'qual é a resposta exata de um consultor para a pergunta: ' + msg_user

    mensagens = []
    mensagens.append({"role": "user", "content": str(mensagem)})

    pergunta_user = mensagens[0]['content']

    resposta_chatgpt = gerar_resposta(mensagens)

    if pergunta_user == None or pergunta_user == '':
        lista_cards = clusterCards(df_historical_msgs)
        return lista_cards
    
    new_line = pd.DataFrame([[pergunta_user, resposta_chatgpt]], columns= ['user', 'chatGPT'])

    new_line['user'] = new_line['user'].str.split(':')
    new_line['user'] = new_line['user'][0][-1]
    df_historical_msgs = pd.concat([new_line, df_historical_msgs], ignore_index=True)

    df_historical_msgs.to_csv('historical_msgs.csv')

    lista_cards = clusterCards(df_historical_msgs)

    return lista_cards
