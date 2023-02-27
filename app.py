import pandas as pd
import plotly.express as px
import streamlit as st

# Lendo as bases de dados
df_vendas = pd.read_excel("Vendas.xlsx")
df_produtos = pd.read_excel("Produtos.xlsx")

# Merge
df = pd.merge(df_vendas,df_produtos, how="left", on="ID Produto")

# Novas Colunas
df["Custo"]     = df["Custo Unitário"] * df["Quantidade"]
df["Lucro"]     = df["Valor Venda"] - df["Custo"]
df["mes_ano"]   = df["Data Venda"].dt.to_period("M").astype(str)

# Agrupamentos
produtos_vendidos_marca = df.groupby("Marca")["Quantidade"].sum().sort_values(ascending=True).reset_index()
lucro_categoria = df.groupby("Categoria")["Lucro"].sum().reset_index()
lucro_mes_categoria = df.groupby(["mes_ano", "Categoria"])["Lucro"].sum().reset_index()

# Criando o App

def main():

    st.title("Análise de Vendas")
    st.image("vendas.png")

    total_custo = (df["Custo"].sum()).astype(str)
    total_custo = total_custo.replace(".",",")
    total_custo = "R$" + total_custo[:2] + "." + total_custo[2:5] + "." + total_custo[5:]

    lucro = (round(df["Lucro"].sum(),2)).astype(str)
    lucro = lucro.replace(".",",")
    lucro = "R$" + lucro[:2] + "." + lucro[2:5] + "." + lucro[5:]

    st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Custo", total_custo)
    with col2:
        st.metric("Lucro", lucro)
    with col3:
        st.metric("Total Clientes", )

    col1, col2 = st.columns(2)

    fig = px.bar(produtos_vendidos_marca, x="Quantidade",y="Marca", orientation="h", text="Quantidade", width=380, height=400, title="Total Produtos Vendidos por Marca")
    col1.plotly_chart(fig)

    fig1 = px.pie(lucro_categoria, values='Lucro', names='Categoria',
    title="Lucro por Categoria",width=450, height=400 )
    col2.plotly_chart(fig1)

    fig2 = px.line(lucro_mes_categoria, x="mes_ano", y="Lucro", 
    title='Lucro X Mês X Categoria', width=900, height=400,
    markers=True, color="Categoria", 
              labels={"mes_ano":"Mês", "Lucro":"Lucro no Mês"})
    st.plotly_chart(fig2)

if __name__ == '__main__':
    main()
    #v2