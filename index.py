import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO
import calendar
import locale
from babel.dates import format_date

from app import *

from dash import callback_context

from components import contadorgpt
# xhave chat gpt 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

# ========== Styles ============ #

template_theme1 = "flatly" 
template_theme2 = "vapor"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.VAPOR

tab_card = {'height': '100%'}

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor":"top", 
                "y":0.9, 
                "xanchor":"left",
                "x":0.1,
                "title": {"text": None},
                "font" :{"color":"black"},
                "bgcolor": "rgba(255,255,255,0.0)"}, 
    "margin": {"l":0, "r":0, "t":10, "b":0}
}

# ===== Reading n cleaning File ====== #
df_main = pd.read_csv("vitalfarma.csv")

df_main['preco'] = df_main['PRECO TOTAL'].copy()
df_store = df_main.to_dict()


# =========  Layout  =========== #
app.layout = dbc.Container(children=[
    dcc.Location(id="url"),
    # Armazenar o dataset
    dcc.Store(id='dataset', data=df_store),
    dcc.Store(id='dataset_fixed', data=df_store), #dataset fixo apenas para backup, caso algo dê errado
    

    # Layout
    # Row  1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("VitalFarma")
                        ], sm=8),
                        dbc.Col([
                            html.I(className='fa fa-chart-bar', style={'font-size': '400%'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend("Data Wealth Consultoria")
                        ])
                    ], style={'margin-top': '10px'}),
               
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Visite o Site", href="https://datawealth4.wordpress.com/", target="_blank")
                        ])
                    ], style={'margin-top': '10px'}),
                    
                   
                ])
            ], style=tab_card)
            
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Faturamento em 2022", className="card-text text-center"),
                         
                            dcc.Graph(id='faturamento_total', config={"displayModeBar": False, "showTips": False}, style={'margin-top': '30px'})
                        ])
                    ],style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=6, lg=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6("Mês de Análise"),
                            dcc.Dropdown(
                                id="select_mes",
                                value = df_main.at[df_main.index[1], 'MES'],
                                clearable = False,
                               # className='dbc',
                                options=[{"label": x, "value": x} for x in df_main.MES.unique()],style={'background-color': 'rgba(0, 0, 0, 0.3'}
                            ),
                            html.Legend("Faturamento Médio Mensal", className="card-text text-center"),
                            dcc.Graph(id='faturamento_mes', config={"displayModeBar": False, "showTips": False}, style={'margin-top': '30px'})
                        ])
                    ],style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=6, lg=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6("Produto"),
                            dcc.Dropdown(
                                id="select_produto",
                                value = df_main.at[df_main.index[1], 'PRODUTO'],
                                clearable = False,
                                #className='dbc',
                                options=[{"label": x, "value": x} for x in df_main.PRODUTO.unique()],style={'background-color': 'rgba(0, 0, 0, 0.3'}
                            ),
                            html.Legend("Faturamento por Produto", className="card-text text-center"),
                            dcc.Graph(id='faturamento_produto', config={"displayModeBar": False, "showTips": False}, style={'margin-top': '30px'})
                        ])
                    ],style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=6, lg=4)
    ], className='main_row g-2 my-auto', style={'margin-top': '7px'}),

    # ROW 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Comparar Vendas por Produto'),
                    html.H6("Selecione o Produto"),
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(
                                id="select_produto0",
                                value = df_main.at[df_main.index[1], 'PRODUTO'],
                                clearable = False,
                                #className='dbc',
                                multi = True,
                                options=[{"label": x, "value": x} for x in df_main.PRODUTO.unique()
                            ],style={'background-color': 'rgba(0, 0, 0, 0.3'})
                        ], sm=10),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='animation_graph', config={"displayModeBar": False, "showTips": False})
                        ])
                    ])
                ])
            ],style=tab_card)
        ], sm=12, md=6, lg=5),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("Quantidade Vendidas"),
                    html.H6("Comparação de quantidade vendidas de produtos em um dado período de tempo"),
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(
                                id="select_produto1",
                                value = df_main.at[df_main.index[1], 'PRODUTO'],
                                clearable = False,
                                #className='dbc',
                                options=[{"label": x, "value": x} for x in df_main.PRODUTO.unique()
                            ],style={'background-color': 'rgba(0, 0, 0, 0.3'}),
                        ], sm=10, md=5),
                        dbc.Col([
                            dcc.Dropdown(
                                id="select_produto2",
                                value = df_main.at[df_main.index[1], 'PRODUTO'],
                                clearable = False,
                                #className='dbc',
                                options=[{"label": x, "value": x} for x in df_main.PRODUTO.unique()
                            ],style={'background-color': 'rgba(0, 0, 0, 0.3'})
                        ], sm=10, md=6)
                    ], style={'margin-top': '20px'}, justify='center'),
                    dcc.Graph(id='direct_comparison_graph', config={"displayModeBar": False, "showTips": False}),
                    html.P(id='desc_comparison', style={'color': 'gray', 'font-size': '80%'}),

                ])
            ], style=tab_card)
        ], sm=12, md=6, lg=4),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='card_indicators', config={"displayModeBar": False, "showTips": False}, style={'margin-top': '30px'})
                        ])
                    ], style=tab_card)
                ])
            ], justify='center', style={'padding-bottom': '7px', 'height': '50%'}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='card2_indicators', config={"displayModeBar": False, "showTips": False}, style={'margin-top': '30px'})
                        ])
                    ], style=tab_card)
                ])
            ], justify='center', style={'height': '50%'})
        ], sm=12, lg=3, style={'height': '100%'})

    ], className='main_row g-2 my-auto'),

          dbc.Row([
              dbc.Col([
                  dbc.Button("ContadorGPT", href='/chatgpt', target="_blank")
                        ])
                        ], style={'margin-top': '10px'}),

        dbc.Row([
            dbc.Col([

            ]),
            ],id="page-content"),




], fluid=True, style={'height': '100%'})



# ======== Callbacks ========== #

# Atualiza a página 
@app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
)
def render_page(pathname):
    if pathname == '/' or pathname =='/chatgpt':
        
        return contadorgpt.layout

# Faturamento Total
@app.callback(
    Output("faturamento_total", "figure"),
    Input('dataset', 'data'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def fat_total(data, toggle):
    template = template_theme1 if toggle else template_theme2

    dft = pd.DataFrame(data)
    dft1 = dft.groupby('MES')['PRECO TOTAL'].sum().reset_index()
    # Verificar os dados após o agrupamento
    #print(f'Data after grouping:\n{dft1.head()}')
    # Obter o nome do mês
    # Mapeie os números dos meses para os nomes dos meses em português
    dft1['MES'] = dft1['MES'].map({1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto', 
                                   9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'})
    

    fig = go.Figure(go.Bar(x=dft1['MES'], y=dft1['PRECO TOTAL'], textposition='auto', text=dft1['PRECO TOTAL'],
))
    
    fig.update_layout(main_config, height=300, template=template)
    
    return fig

# Faturamento por Mês
@app.callback(
    Output('faturamento_mes', 'figure'),
    [Input('dataset', 'data'),
     Input('select_mes', 'value'),
     Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
def graph_mes(data, mes, toggle):
    template = template_theme1 if toggle else template_theme2

    df = pd.DataFrame(data)
    
    # Filtrar o DataFrame para o mês selecionado
    df_filtered = df[df['MES'] == mes]
    
    # Calcular o faturamento total para o mês
    faturamento_mensal = df_filtered['PRECO TOTAL'].mean()

    # Obter o nome do mês
    meses_pt_br = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto', 
                   9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
    nome_mes = meses_pt_br[int(mes)]


    # Criar o gráfico
    fig1 = go.Figure(go.Indicator(
        mode="number+delta",
        title={"text": f"<span style='size:60%'>Faturamento Médio em {nome_mes}</span><br><span style='font-size:0.7em'></span>"},
        value=faturamento_mensal,
        number={'prefix': "R$", 'valueformat': '.2f'},
    ))
    
    
    # Atualizar o layout do gráfico
    fig1.update_layout(main_config, height=200, template=template)
    
    return fig1


# Faturamento por Produto
@app.callback(
    Output('faturamento_produto', 'figure'),
    [Input('dataset', 'data'),
     Input('select_produto', 'value'),
     Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
def graph_produto(data, produtos_selecionados, toggle):
    template = template_theme1 if toggle else template_theme2

    df_p = pd.DataFrame(data)

    # Criar um gráfico go.Indicator para o produto selecionado
    faturamento_produto = df_p[df_p['PRODUTO'] == produtos_selecionados]['PRECO TOTAL'].sum()

    # Calcular a porcentagem em relação ao faturamento total de 2022
    faturamento_total = df_p['PRECO TOTAL'].sum()
    percentual_produto = (faturamento_produto / faturamento_total) * 100

    fig2 = go.Figure()

    fig2.add_trace(go.Indicator(
        mode = "number+delta",
        title = {"text": f"<span style='size:60%'>Vendas de {produtos_selecionados} em 2022</span><br><span style='font-size:0.7em'></span>"},
        value = faturamento_produto,
        number = {'prefix': "R$", 'valueformat': '.2f'},
        
       
    ))

    

    # Criar o layout do gráfico

    fig2.update_layout(main_config, height=200, template=template)

    return fig2


import plotly.graph_objects as go

@app.callback(
    Output('animation_graph', 'figure'),
    Input('dataset', 'data'),
    Input('select_produto0', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), 'value')
) 
def animation(data, produto0, toggle):
    template = template_theme1 if toggle else template_theme2

    df_comp = pd.DataFrame(data)

    # Garantir que produtos_selecionados seja uma lista
    if isinstance(produto0, str):
        produto0 = [produto0]

    df_selected_products = df_comp[df_comp['PRODUTO'].isin(produto0)]

    # Colocar os meses em pt-br no eixo x
    meses_pt_br = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
        7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }

    fig3 = go.Figure()

    for produto in produto0:
        df_produto = df_selected_products[df_selected_products['PRODUTO'] == produto]
        fig3.add_trace(go.Scatter(x=df_produto['MES'], y=df_produto['preco'], mode='lines+markers', name=produto, showlegend=True,
                                  hovertemplate="<b>%{text}</b><br>Faturamento: R$%{y:.2f}<br>Mês: %{x}<extra></extra>",
            text=df_produto['preco']))

    # Ajuste nas configurações de cor e legenda
    fig3.update_layout(template=template, height=500, xaxis_title=None, yaxis_title='Faturamento R$', xaxis=dict(
        tickmode='array',
        tickvals=list(meses_pt_br.keys()),
        ticktext=list(meses_pt_br.values())
    ))
   # fig3.update_layout(hoverlabel=dict(bgcolor='white', font=dict(color='black')))

    return fig3



# Callback para o gráfico de comparação de quantidade vendida
@app.callback(
    [Output('direct_comparison_graph', 'figure'),
     Output('desc_comparison', 'children')],
    [Input('dataset', 'data'),
     Input('select_produto1', 'value'),
     Input('select_produto2', 'value'),
     Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
def compare_quantities(data, produto1, produto2, toggle):
    template = template_theme1 if toggle else template_theme2

    df_comp = pd.DataFrame(data)

    # Filtrar o DataFrame para os produtos selecionados
    df_selected_products = df_comp[df_comp['PRODUTO'].isin([produto1, produto2])]

    # Colocar os meses em pt-br no eixo x
    meses_pt_br = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
        7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }

    # Criar um gráfico de dispersão com linha e marcadores comparando as quantidades vendidas ao longo do tempo
    fig4 = go.Figure()

    for produto in [produto1, produto2]:
        df_produto = df_selected_products[df_selected_products['PRODUTO'] == produto]
        fig4.add_trace(go.Scatter(x=df_produto['MES'], y=df_produto['QUANTIDADE VENDIDA'], mode='lines+markers', name=produto, showlegend=True,
                                  hovertemplate="<b>%{text}</b><br>Quantidade Vendida: %{y}<br>Mês: %{x}<extra></extra>",
                                  text=df_produto['QUANTIDADE VENDIDA']))


    # Atualizar o layout do gráfico
    fig4.update_layout(template=template,height=495,xaxis_title=None, xaxis=dict(
            tickmode='array',
            tickvals=list(meses_pt_br.keys()),
            ticktext=list(meses_pt_br.values())
        ))

    # Calcular a diferença percentual entre as quantidades vendidas
    quantity1 = df_selected_products[df_selected_products['PRODUTO'] == produto1]['QUANTIDADE VENDIDA'].iloc[0]
    quantity2 = df_selected_products[df_selected_products['PRODUTO'] == produto2]['QUANTIDADE VENDIDA'].iloc[0]
    percent_diff = ((quantity2 - quantity1) / quantity1) * 100

    # Criar a descrição para exibir a diferença percentual
    desc_comparison = f"A diferença percentual entre {produto1} e {produto2} é de {percent_diff:.2f}%."

    return fig4, html.P(desc_comparison, style={'text-align': 'center'})



@app.callback(
    Output("card_indicators", "figure"),
    [Input('dataset', 'data'),
     Input('select_produto', 'value'),
     Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
def card(data, produto, toggle):
    template = template_theme1 if toggle else template_theme2

    dff = pd.DataFrame(data)

    # Filtrar o DataFrame para o produto selecionado
    df_produto = dff[dff['PRODUTO'] == produto]

    # Calcular o faturamento médio por produto
    faturamento_medio = df_produto['PRECO TOTAL'].mean()

    # Calcular o faturamento total em 2022
    faturamento_total_2022 = dff['PRECO TOTAL'].sum()

    # Calcular a porcentagem relativa ao faturamento total
    percentual_faturamento = (faturamento_medio / faturamento_total_2022) * 100

    dd = dff.groupby('PRODUTO')['QUANTIDADE VENDIDA'].sum().reset_index()
    dd = dd.reset_index()

    # Calculate the reference value (total sum of 'PRECO TOTAL' for all products)
    reference_value = dd['QUANTIDADE VENDIDA'].count()

    # Criar um gráfico de indicadores para o faturamento médio por produto
    fig_card2 = go.Figure()

    fig_card2.add_trace(go.Indicator(
        mode="number+delta",
        title={"text": f"<span style='size:60%'>Faturamento Médio de {produto} em 2022</span><br><span style='font-size:0.7em'></span>"},
        value=faturamento_medio,
        number={'prefix': "R$", 'valueformat': '.2f'},
        #delta = {'relative': True, 'valueformat': '.1%', 'reference':reference_value}
        
    ))

    # Atualizar o layout do gráfico
    fig_card2.update_layout(main_config, height=255, template=template)

    return fig_card2


# Callback para o indicador de quantidade vendida por produto
@app.callback(
    Output("card2_indicators", "figure"),
    [Input('dataset', 'data'),
     Input('select_produto1', 'value'),
     Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
def card2(data, produto, toggle):
    template = template_theme1 if toggle else template_theme2

    dff = pd.DataFrame(data)

    # Filtrar o DataFrame para o produto selecionado
    df_produto = dff[dff['PRODUTO'] == produto]

    # Calcular a quantidade total vendida do produto
    quantidade_total = df_produto['QUANTIDADE VENDIDA'].sum()

    # Calcular a porcentagem relativa à quantidade total vendida
    percentual_quantidade = (df_produto['QUANTIDADE VENDIDA'] / 12) * 100

    # Calcular a referência (média da porcentagem)
    reference_value = percentual_quantidade.mean()

    # Criar um gráfico de indicadores para a quantidade vendida por produto
    fig_card3 = go.Figure()

    fig_card3.add_trace(go.Indicator(
        mode="number+delta",
        title={"text": f"<span style='size:60%'>Quantidade Vendida de {produto} em 2022</span><br><span style='font-size:0.7em'></span>"},
        value=df_produto['QUANTIDADE VENDIDA'].sum(),
        #delta = {'relative': True, 'valueformat': '.1%', 'reference': percentual_quantidade}
        
        
    ))

    # Atualizar o layout do gráfico
    fig_card3.update_layout(main_config, height=295, template=template)

    # Ajustar o texto do delta para mostrar a porcentagem


    return fig_card3


if __name__ == '__main__':
    app.run_server(debug=True)