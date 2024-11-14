import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from wordcloud import WordCloud
import numpy as np
from matplotlib.ticker import MaxNLocator

st.set_page_config(layout='wide',page_icon = 'book', page_title = "GT-Scientometrics")

st.title('Proposta de avaliação das ações acadêmicas de pesquisadores')
st.write("### Organização GT de psicobiologia, neurociência e comportamento")

uploaded_file = st.file_uploader(
    "Faça o upload do CitationOverview da Scopus", type="csv")

# Verificar se o arquivo foi carregado
if uploaded_file is not None:
    st.title("Base de dados")
    # Carregar a base de dados a partir da linha 7
    df = pd.read_csv(uploaded_file)

    data = {
        'Publication Year': pd.to_numeric(df.iloc[6:, 0]),
        'Document Title': df.iloc[6:, 1],
        'ISSN': df.iloc[6:, 2],
        'Journal Title': df.iloc[6:, 3],
        'Volume': df.iloc[6:, 4],
        'Issue': df.iloc[6:, 5]}

    # Pegando os títulos das colunas 7 em diante (linha 5, que é o índice 4 no pandas)
    anos = df.iloc[4, 6:-3].values
    anos[0] = anos[1]-1
    titles = df.iloc[4, 6:].values  # Excluindo as 6 primeiras colunas

    # Atribuindo os títulos das colunas 7 em diante ao dicionário de dados
    for i, titulo in enumerate(titles, start=6):
        col_name = f"{titulo}"  # Nome temporário para evitar conflito
        data[col_name] = df.iloc[6:, i]

    df_data = pd.DataFrame(data)

    st.dataframe(df_data)

    for index in np.arange(df_data["Total"].shape[0]):
        if index > pd.to_numeric(df_data["Total"].iloc[index]):
            hindex = index-1
            break

    st.title('Resumo')
    st.markdown("Total de " +
                str(data['Document Title'].shape[0]) + " publicações")
    num_ocorrencias = (df_data['Publication Year'] >
                       datetime.now().year - 5).sum()
    st.markdown(str(num_ocorrencias) +
                " publicações nos últimos 5 anos")
    n_total_citations = df.iloc[5, -3]
    st.markdown(str(n_total_citations) +
                " citações na carreira")
    st.markdown('Índice H = ' + str(hindex))

    col1, col2 = st.columns([1, 1])
    with col1:
        st.title("Proporção da produção por periódicos")
        values = data["Journal Title"].value_counts(normalize=True) * 100
        labels = values.index  # Rótulos originais

        # Agrupar valores menores que 5% na categoria "Outros"
        mask = values >= 2.5
        values_filtered = values[mask]
        values_filtered["Outros"] = values[~mask].sum(
        )  # Soma dos valores < 5%

        # Gerar o gráfico de pizza
        fig, ax = plt.subplots()
        ax.pie(values_filtered, labels=values_filtered.index,
               autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Assegura que o gráfico fique circular

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)
    with col2:
        st.title("Proporção da produção por ano")

        values = data["Publication Year"].value_counts(normalize=True) * 100
        labels = values.index  # Rótulos originais

        # Agrupar valores menores que 5% na categoria "Outros"
        mask = values >= 5
        values_filtered = values[mask]
        values_filtered["Outros"] = values[~mask].sum(
        )  # Soma dos valores < 5%

        # Gerar o gráfico de pizza
        fig, ax = plt.subplots()
        ax.pie(values_filtered, labels=values_filtered.index,
               autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Assegura que o gráfico fique circular

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

    col1, col2, col3 = st.columns([0.3, 1, 0.3])
    producao = data["Publication Year"].value_counts(normalize=False)

    anos_producao = producao.index  # Os valores únicos da coluna "Publication Year"
    contagem_producao = producao.values
    with col2:
        st.title("Distribuição da produção por ano")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(anos_producao, contagem_producao)

        ax.set_xlabel('Ano')
        ax.set_ylabel('Número de publicações')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        # Exibir o gráfico de dispersão
        st.pyplot(fig)

    # Garantir que n_citation seja numérico
    # Converte para numérico
    anos = pd.to_numeric(anos)
    # Lista de índices de linhas

    st.title("Distribuição das citações por ano")
    valores = st.text_input(
        "Insira entre vírgulas o índice da produção que deseja ver o número de citações ou escreva Todos", "1")
    filtro1 = st.selectbox("Indique o tipo de saída que deseja ter", [
                           'Individual', 'Conjunta'])
    if valores == "Todos":
        col1, col2, col3 = st.columns([0.3, 1, 0.3])
        todos = df_data.iloc[6:, 6:-3].sum()
        with col2:
            todos = df_data.iloc[6:, 6:-3].sum()
            n_citation = pd.to_numeric(todos.values, errors='coerce')
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(anos, n_citation, '-o',
                    label='Todos')
            ax.legend()
            ax.set_xlabel('Ano')
            ax.set_ylabel('Número de Citações')
            # Exibir o gráfico de dispersão
            st.pyplot(fig)

    else:
        col1, col2, col3 = st.columns([0.3, 1, 0.3])
        if filtro1 == "Individual":
            valores_lista = valores.split(',')
            valores_numericos = [float(i) for i in valores_lista]
            indices_raw = list(map(int, valores_lista))
            indices = list(map(lambda x: x - 1, indices_raw))

            with col2:
                fig, ax = plt.subplots(figsize=(10, 4))
                for local in indices:
                    linhas_selecionadas = df_data.iloc[local]
                    n_citation = pd.to_numeric(
                        linhas_selecionadas.iloc[6:-3].values, errors='coerce')
                    ax.plot(anos, n_citation, '-o',
                            label=str(df_data.iloc[local].iloc[3]))
                ax.legend()
                ax.set_xlabel('Ano')
                ax.set_ylabel('Número de Citações')

                # Exibir o gráfico de dispersão
                st.pyplot(fig)
        else:
            with col2:
                valores_lista = valores.split(',')
                valores_numericos = [float(i) for i in valores_lista]
                indices_raw = list(map(int, valores_lista))
                indices = list(map(lambda x: x - 1, indices_raw))

                linhas_selecionadas = df_data.iloc[indices]
                soma = linhas_selecionadas.iloc[0:, 6:-3].sum()
                n_citation = pd.to_numeric(
                    soma.values, errors='coerce')
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(anos, n_citation, '-o')
                ax.set_xlabel('Ano')
                ax.set_ylabel('Número de Citações')
                st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        # Concatenar todo o texto em uma string única
        texto = " ".join(
            df_data['Document Title'].dropna().astype(str).tolist())

        # Gerar a nuvem de palavras
        wordcloud = WordCloud(width=800, height=400,
                              background_color='white').generate(texto)

        # Exibir a nuvem de palavras no Streamlit
        st.write("### Nuvem de palavras da carreira")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    with col2:
        # Concatenar todo o texto em uma string única
        texto = " ".join(
            df_data['Document Title'].iloc[0:4].dropna().astype(str).tolist())

        # Gerar a nuvem de palavras
        wordcloud = WordCloud(width=800, height=400,
                              background_color='white').generate(texto)

        # Exibir a nuvem de palavras no Streamlit
        st.write("### Nuvem de palavras das 5 produções mais citadas")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
