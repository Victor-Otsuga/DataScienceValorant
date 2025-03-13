import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm, poisson

# Configuração da página
st.set_page_config(page_title="Análise de Dados - Valorant", layout="wide")

# Título da página
st.title("Análise de Dados: Armas do Valorant")

# Carregar os dados do arquivo CSV
@st.cache_data  
def load_data():
    try:
        df = pd.read_csv("./valorant-stats.csv")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return pd.DataFrame() 

df = load_data()


if df.empty:
    st.stop()  

# Criar abas
tab1, tab2, tab3 = st.tabs(["📊 Análise Inicial", "📈 Medidas e Correlação", "🎲 Distribuições Probabilísticas"])

# Aba 1: Análise Inicial
with tab1:
    st.header("1. Apresentação dos Dados")
    st.write("""
    Este conjunto de dados contém informações sobre as armas disponíveis no jogo Valorant. 
    Cada arma possui atributos como tipo, preço, taxa de disparo, penetração em paredes, 
    capacidade do carregador e danos em diferentes distâncias (curta, média e longa).
    """)
    st.write("Amostra dos dados:")
    st.write(df.head())

    # Classificação das variáveis
    st.subheader("Classificação das Variáveis")
    st.write("""
    Abaixo está a classificação de cada variável do conjunto de dados:
    """)

    # Dicionário com a classificação das variáveis
    variable_types = {
        "Name": "Qualitativa Nominal",
        "Weapon Type": "Qualitativa Nominal",
        "Price": "Quantitativa Discreta",
        "Fire Rate": "Quantitativa Contínua",
        "Wall Penetration": "Qualitativa Ordinal",  
        "Magazine Capacity": "Quantitativa Discreta",
        "HDMG_0": "Quantitativa Contínua",
        "BDMG_0": "Quantitativa Contínua",
        "LDMG_0": "Quantitativa Contínua",
        "HDMG_1": "Quantitativa Contínua",
        "BDMG_1": "Quantitativa Contínua",
        "LDMG_1": "Quantitativa Contínua",
        "HDMG_2": "Quantitativa Contínua",
        "BDMG_2": "Quantitativa Contínua",
        "LDMG_2": "Quantitativa Contínua"
    }

    # Exibir a classificação em uma tabela
    classification_df = pd.DataFrame({
        "Variável": list(variable_types.keys()),
        "Tipo": list(variable_types.values())
    })
    st.write(classification_df)

    # Explicação dos tipos de variáveis
    st.subheader("Explicação dos Tipos de Variáveis")
    st.write("""
    - **Qualitativa Nominal**: Variáveis que representam categorias sem ordem específica (ex: nome da arma, tipo de arma).
    - **Qualitativa Ordinal**: Variáveis categóricas que possuem uma ordem ou hierarquia específica (ex: nível de penetração em paredes: Baixo, Médio, Alto).
    - **Quantitativa Discreta**: Variáveis numéricas que assumem valores inteiros (ex: preço, capacidade do carregador).
    - **Quantitativa Contínua**: Variáveis numéricas que assumem valores decimais (ex: taxa de disparo, dano em diferentes distâncias).
    """)

    # Perguntas de análise
    st.subheader("Perguntas de Análise")
    st.write("""
    1. Qual é a distribuição de preços das armas por tipo?
    2. Qual arma tem o maior dano em curta distância (HDMG_0)?
    3. Como a taxa de disparo (Fire Rate) varia entre os tipos de armas?
    4. Qual é a relação entre o preço da arma e seu dano em diferentes distâncias?
    5. Quais armas oferecem o melhor custo-benefício em termos de dano por preço?
    """)

    # Análise 1: Distribuição de preços por tipo de arma
    st.header("2. Distribuição de Preços por Tipo de Arma")
    fig1 = px.box(df, x="Weapon Type", y="Price", title="Distribuição de Preços por Tipo de Arma")
    st.plotly_chart(fig1)
    st.write("""
    - **Observação**: As armas do tipo Sniper e Heavy tendem a ser as mais caras, enquanto as Sidearms são as mais baratas.
    """)

    # Análise 2: Arma com maior dano em curta distância
    st.header("3. Arma com Maior Dano em Curta Distância (HDMG_0)")
    max_damage_weapon = df.loc[df["HDMG_0"].idxmax()]
    st.write(f"A arma com maior dano em curta distância é **{max_damage_weapon['Name']}** com **{max_damage_weapon['HDMG_0']}** de dano.")

    # Análise 3: Taxa de disparo por tipo de arma
    st.header("4. Taxa de Disparo por Tipo de Arma")
    fig2 = px.bar(df, x="Weapon Type", y="Fire Rate", title="Taxa de Disparo por Tipo de Arma", color="Weapon Type")
    st.plotly_chart(fig2)
    st.write("""
    - **Observação**: As SMGs têm a maior taxa de disparo, enquanto as Snipers têm a menor.
    """)

    # Análise 4: Relação entre preço e dano
    st.header("5. Relação entre Preço e Dano")
    st.subheader("Dano em Curta Distância (HDMG_0) vs Preço")
    fig3 = px.scatter(df, x="Price", y="HDMG_0", color="Weapon Type", title="Relação entre Preço e Dano em Curta Distância")
    st.plotly_chart(fig3)
    st.write("""
    - **Observação**: Em geral, armas mais caras tendem a causar mais dano, mas há exceções, como a Sheriff, que é relativamente barata e causa alto dano.
    """)

    # Análise 5: Custo-benefício (Dano por Preço)
    st.header("6. Custo-Benefício: Dano por Preço")
    df["Damage per Price"] = df["HDMG_0"] / df["Price"]
    fig4 = px.bar(df, x="Name", y="Damage per Price", title="Dano por Preço (Custo-Benefício)", color="Weapon Type")
    st.plotly_chart(fig4)
    st.write("""
    - **Observação**: A **Shorty** oferece o melhor custo-benefício em termos de dano por preço, enquanto a **Operator** tem o pior.
    """)

# Aba 2: Medidas e Correlação
with tab2:
    st.header("2. Medidas Centrais, Dispersão e Correlação")

    # Cálculo de medidas centrais
    st.subheader("Medidas Centrais")
    st.write("""
    Aqui estão as medidas centrais (média, mediana e moda) para as variáveis numéricas:
    """)

    # Selecionar colunas numéricas
    numeric_columns = df.select_dtypes(include=[np.number]).columns

    # Calcular média, mediana e moda
    mean_values = df[numeric_columns].mean()
    median_values = df[numeric_columns].median()
    mode_values = df[numeric_columns].mode().iloc[0]  # Pega a primeira moda, caso haja múltiplas

    # Exibir em uma tabela
    measures_df = pd.DataFrame({
        "Média": mean_values,
        "Mediana": median_values,
        "Moda": mode_values
    })
    st.write(measures_df)

    # Discussão sobre a distribuição dos dados
    st.subheader("Distribuição dos Dados")
    st.write("""
    A distribuição dos dados pode ser visualizada através de histogramas. Abaixo estão os histogramas para algumas variáveis numéricas:
    """)

    # Selecionar variáveis para histogramas
    selected_columns = st.multiselect(
        "Selecione as variáveis para visualizar a distribuição:",
        numeric_columns,
        default=["Price", "Fire Rate", "HDMG_0"]
    )

    # Plotar histogramas
    for col in selected_columns:
        fig = px.histogram(df, x=col, title=f"Distribuição de {col}", nbins=20)
        st.plotly_chart(fig)
        st.write(f"**{col}**: Média = {mean_values[col]:.2f}, Mediana = {median_values[col]:.2f}, Moda = {mode_values[col]}")

    # Medidas de dispersão
    st.subheader("Medidas de Dispersão")
    st.write("""
    A dispersão dos dados pode ser medida através do desvio padrão e da variância. Abaixo estão os valores para as variáveis numéricas:
    """)

    # Calcular desvio padrão e variância
    std_values = df[numeric_columns].std()
    var_values = df[numeric_columns].var()

    # Exibir em uma tabela
    dispersion_df = pd.DataFrame({
        "Desvio Padrão": std_values,
        "Variância": var_values
    })
    st.write(dispersion_df)

    # Correlação entre variáveis
    st.subheader("Correlação entre Variáveis")
    st.write("""
    A correlação entre as variáveis numéricas pode ser visualizada através de uma matriz de correlação. 
    Valores próximos de 1 ou -1 indicam uma forte correlação positiva ou negativa, respectivamente.
    """)

    # Calcular matriz de correlação
    corr_matrix = df[numeric_columns].corr()

    # Exibir matriz de correlação com um heatmap
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        title="Matriz de Correlação",
        labels=dict(x="Variável", y="Variável", color="Correlação")
    )
    st.plotly_chart(fig_corr)

    # Discussão sobre correlações
    st.write("""
    **Discussão sobre Correlações**:
    - **Preço e Dano (HDMG_0)**: Espera-se uma correlação positiva, pois armas mais caras tendem a causar mais dano.
    - **Taxa de Disparo e Dano**: Pode haver uma correlação negativa, já que armas com alta taxa de disparo geralmente causam menos dano por tiro.
    - **Capacidade do Carregador e Preço**: Pode haver uma correlação positiva, pois armas com maior capacidade tendem a ser mais caras.
    """)

    # Identificação de correlações fortes
    strong_correlations = corr_matrix.abs() > 0.7  # Definindo um limiar para correlações fortes
    strong_correlations = strong_correlations.stack().reset_index()
    strong_correlations = strong_correlations[strong_correlations[0] & strong_correlations['level_0'] != strong_correlations['level_1']]

    if not strong_correlations.empty:
        st.write("**Correlações Fortes Identificadas**:")
        st.write(strong_correlations[['level_0', 'level_1']].rename(columns={'level_0': 'Variável 1', 'level_1': 'Variável 2'}))
    else:
        st.write("Nenhuma correlação forte foi identificada.")

# Aba 3: Distribuições Probabilísticas
with tab3:
    st.header("3. Aplicação de Distribuições Probabilísticas")

    # Escolha da variável para análise
    st.subheader("Escolha da Variável")
    st.write("""
    Selecione uma variável numérica para aplicar as distribuições probabilísticas:
    """)
    selected_col = st.selectbox(
        "Selecione uma variável:",
        numeric_columns,
        index=numeric_columns.get_loc("HDMG_0")  # Seleciona "HDMG_0" por padrão
    )

    if selected_col:
        data = df[selected_col].dropna()

        # Distribuição Normal
        st.subheader("Distribuição Normal")
        st.write("""
        **Justificativa**: A distribuição Normal é adequada para variáveis contínuas que tendem a se concentrar em torno de uma média. 
        No caso de **HDMG_0** (dano em curta distância), espera-se que os valores se distribuam de forma simétrica em torno de um valor central.
        """)

        # Ajustar uma distribuição normal aos dados
        mu, sigma = norm.fit(data)
        x = np.linspace(min(data), max(data), 100)
        pdf = norm.pdf(x, mu, sigma)

        # Plotar histograma e curva normal
        fig_norm = go.Figure()
        fig_norm.add_trace(go.Histogram(x=data, name="Histograma", nbinsx=20, histnorm="probability density"))
        fig_norm.add_trace(go.Scatter(x=x, y=pdf, mode="lines", name="Distribuição Normal", line=dict(color="red")))
        fig_norm.update_layout(
            title=f"Distribuição Normal Ajustada para {selected_col}",
            xaxis_title=selected_col,
            yaxis_title="Densidade de Probabilidade"
        )
        st.plotly_chart(fig_norm)

        st.write(f"**Média (μ)**: {mu:.2f}")
        st.write(f"**Desvio Padrão (σ)**: {sigma:.2f}")
        st.write("""
        **Interpretação**: A curva vermelha representa a distribuição normal ajustada aos dados. 
        Se os dados seguirem uma distribuição normal, a curva deve se sobrepor bem ao histograma.
        """)

        # Distribuição de Poisson
        st.subheader("Distribuição de Poisson")
        st.write("""
        **Justificativa**: A distribuição de Poisson é adequada para modelar a ocorrência de eventos raros em um intervalo fixo. 
        No caso de **Magazine Capacity** (capacidade do carregador), podemos modelar a frequência de armas com determinada capacidade.
        """)

        # Ajustar uma distribuição de Poisson aos dados
        lambda_est = data.mean()
        x_poisson = np.arange(0, int(data.max()))
        pmf = poisson.pmf(x_poisson, lambda_est)

        # Plotar distribuição de Poisson
        fig_poisson = go.Figure()
        fig_poisson.add_trace(go.Bar(x=x_poisson, y=pmf, name="Distribuição de Poisson"))
        fig_poisson.update_layout(
            title=f"Distribuição de Poisson Ajustada para {selected_col}",
            xaxis_title=selected_col,
            yaxis_title="Probabilidade"
        )
        st.plotly_chart(fig_poisson)

        st.write(f"**Taxa Média (λ)**: {lambda_est:.2f}")
        st.write("""
        **Interpretação**: A distribuição de Poisson mostra a probabilidade de ocorrência de diferentes valores de capacidade do carregador. 
        Valores próximos à taxa média (λ) têm maior probabilidade.
        """)