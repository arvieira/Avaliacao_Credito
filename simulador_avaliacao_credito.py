import streamlit as st
from joblib import load
import pandas as pd
from utils import Transformador


# As linhas #MainMenu e footer servem para esconder o menu do canto superior direito da página
# A última linha foi da aula e serve para mudar a cor do background dos combobox
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
div[role="listbox"] ul{background-color: #eee1f79e};
</style>

"""

# No Streamlit podemos modificar os estilos do css do html dele sem problemas. Basta
# usar o markdown que está a seguir.
# Cor de fundo do listbox
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Função que vai usar o modelo para avaliar as respostas do cliente e indicar
# se o crédito vai ser aprovado ou não.
def avaliar_mau(dict_respostas):
    # Carregando o modelo e as features (colunas) do dataframe
    # Observe que por mais que ele carregue o modelo do arquivo do dump, o pipeline
    # utilizava um transformador que era uma classe que a gente tinha criado. Nesse caso,
    # precisamos trazer aquela classe de lá para cá para poder importar no código. Observe que
    # as demais bibliotecas não precisamos importar, mas o transformador que é nosso, teremos.
    modelo = load('Objetos/modelo.joblib')
    features = load('Objetos/features.joblib')

    # Transformando o dicionário com as respostas do cliente em uma lista
    respostas = []
    for coluna in features:
        respostas.append(dict_respostas[coluna])

    # Tratando o problema do anos desempregados. No modelo, só tinha anos empregados.
    # O desemprego era tratado com valores positivos. Para a interface do usuário ficar mais 
    # intuitiva, dividiu-se os anos empregados em anos empregados e anos desempregados.
    # Nesse momento, terei de tratar essas duas variáveis passando a ter uma só positiva
    # ou negativa, conforme o modelo aprendeu.
    #
    # Se o cliente mexeu no anos desempregados, ele pega o valor desse slider, transforma
    # para negativo e coloca no anos empregado. Com isso, a partir daqui eu só preciso 
    # trabalhar com anos empregado.
    if dict_respostas['Anos_desempregado'] > 0:
        dict_respostas['Anos_empregado'] = dict_respostas['Anos_desempregado'] * -1

    # Estou criando um dataframe com as respostas para enviar para o modelo avaliar.
    # Nos dados do DataFrame() o panda espera uma lista. Então, precisamos passar uma 
    # lista com a variável resposta, mesmo a variável já sendo uma lista.
    df_novo_cliente = pd.DataFrame(data=[respostas], columns=features)

    # Realizando a previsão
    # Até o momento, só tínhamos passado para o predict dataframes com milhares de linhas,
    # mas observe que posso passar um dataframe com uma única resposta de um cliente e ele
    # realizar a previsão para mim. Também poderia passar a ele um dataframe com vários 
    # clientes e ele fazer um lote de previsões.
    # Como passamos 1 cliente, queremos a primeira e única resposta da lista que o predict
    # retorna.
    mau = modelo.predict(df_novo_cliente)[0]

    # Retorna a previsão de 1 ou 0 do modelo, que corresponde a verdadeiro ou falso para o python
    return mau



# Escrevendo uma imagem e um título
st.image('img/bytebank_logo.png')
st.write('# Simulador de Avaliação de crédito')

# Expanders são paineis que espandem e contraem
my_expander_1 = st.beta_expander('Trabalho')
my_expander_2 = st.beta_expander('Pessoal')
my_expander_3 = st.beta_expander('Família')

# Criando um dicionário para as respostas do cliente
dict_respostas = {}

# Carregando os dados que foram salvos pelo notebook
# As opções dos campos está aqui
lista_campos = load('Objetos/lista_campos.joblib')

# Esse with trata dos objetos que estarão no expander 1
with my_expander_1:
    # Criando duas colunas no painel de expander
    col1_form, col2_form = st.beta_columns(2)

    # Na coluna 1 estou colocando um combobox com as opções importadas do notebook
    # A seleção do usuário é colocada no retorno do combobox
    dict_respostas['Categoria_de_renda'] = col1_form.selectbox('Qual a categoria de renda ?', lista_campos['Categoria_de_renda'])

    dict_respostas['Ocupacao'] = col1_form.selectbox('Qual a ocupação ?', lista_campos['Ocupacao'])

     # Definindo uma variável categórica binária de sim e não mapeada em 1 e 0
    dict_respostas['Tem_telefone_trabalho'] = 1 if col1_form.selectbox('Tem um telefone do trabalho ?', ['Sim', 'Não']) == 'Sim' else 0


    # Slider é uma barra horizontal para selecionar um valor
    # No dataframe o salário era anual. Aqui pedimos o mensal que é mais comum para o usuário e multiplicamos por 12
    dict_respostas['Rendimento_Anual'] = col2_form.slider('Qual o salário mensal ?', help='Podemos mover a barra usando as setas do teclado', min_value=0, max_value=35000, step=500) * 12
    
    # Observe que o modelo que criamos utilizava anos empregado como positivo e desempregado como negativo. 
    # Nesse caso, teremos que posteriormente tratar esses campos para submeter ao modelo.
    dict_respostas['Anos_empregado'] = col2_form.slider('Quantos anos empregado ?', help='Podemos mover a barra usando as setas do teclado', min_value=0, max_value=50, step=1)
    dict_respostas['Anos_desempregado'] = col2_form.slider('Quantos anos desempregado ?', help='Podemos mover a barra usando as setas do teclado', min_value=0, max_value=50, step=1)
    
with my_expander_2:
    col3_form, col4_form = st.beta_columns(2)

    dict_respostas['Grau_Escolaridade'] = col3_form.selectbox('Qual o Grau de Escolaridade ?', lista_campos['Grau_Escolaridade'])
    dict_respostas['Estado_Civil'] = col3_form.selectbox('Qual o Estado Civil ?', lista_campos['Estado_Civil'])
    dict_respostas['Tem_Carro'] = 1 if col3_form.selectbox('Tem um Carro ?', ['Sim', 'Não']) == 'Sim' else 0
    
    dict_respostas['Tem_telefone_fixo'] = 1 if col4_form.selectbox('Tem um telefone fixo ?', ['Sim', 'Não']) == 'Sim' else 0
    dict_respostas['Tem_email'] = 1 if col4_form.selectbox('Tem um email ?', ['Sim', 'Não']) == 'Sim' else 0
    dict_respostas['Idade'] = col4_form.slider('Qual a idade ?', help='Podemos mover a barra usando as setas do teclado', min_value=0, max_value=100, step=1)

with my_expander_3:
    col5_form, col6_form = st.beta_columns(2)

    dict_respostas['Moradia'] = col5_form.selectbox('Qual o tipo de moradia ?', lista_campos['Moradia'])
    dict_respostas['Tem_Casa_Propria'] = 1 if col5_form.selectbox('Tem Casa Propria ?', ['Sim', 'Não']) == 'Sim' else 0
    
    dict_respostas['Tamanho_Familia'] = col6_form.slider('Qual o tamaho da família ?', help='Podemos mover a barra usando as setas do teclado', min_value=1, max_value=20, step=1)
    dict_respostas['Qtd_Filhos'] = col6_form.slider('Quantos filhos ?', help='Podemos mover a barra usando as setas do teclado', min_value=0, max_value=20, step=1)

# O button retorna dois valores True ou False. Retorna True se estiver pressionado
# e false caso não esteja. Por isso, eu posso colocar o button no if
if st.button('Avaliar Crédito'):
    # Função que passa as respostas para o modelo avaliar
    if avaliar_mau(dict_respostas):
        # Exibe uma msg padrão de erro com o texto que queremos
        st.error('Crédito negado')
    else:
        # Exibe uma mensagem padrão de sucesso com o texto que queremos
        st.success('Crédito aprovado')
