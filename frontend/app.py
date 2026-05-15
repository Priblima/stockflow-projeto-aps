import os
from typing import Any

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="StockFlow", page_icon="📦", layout="wide")


def get_headers() -> dict[str, str]:
    token = st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def api_request(method: str, path: str, **kwargs: Any):
    url = f"{API_URL}{path}"
    try:
        response = requests.request(method, url, headers=get_headers(), timeout=10, **kwargs)
        return response
    except requests.exceptions.RequestException as exc:
        st.error(f"Não foi possível conectar à API: {exc}")
        return None


def show_api_error(response):
    try:
        detail = response.json().get("detail", response.text)
    except Exception:
        detail = response.text
    st.error(f"Erro {response.status_code}: {detail}")


def login_view():
    st.title("📦 StockFlow — Controle de Estoque")
    st.caption("Sistema web com FastAPI + Streamlit + SQLite + JWT")

    tab_login, tab_register = st.tabs(["Entrar", "Criar conta"])

    with tab_login:
        with st.form("form_login"):
            email = st.text_input("E-mail", value="admin@stockflow.com")
            senha = st.text_input("Senha", type="password", value="admin123")
            submit = st.form_submit_button("Entrar")

        if submit:
            response = api_request("POST", "/auth/login", json={"email": email, "senha": senha})
            if response and response.status_code == 200:
                st.session_state["token"] = response.json()["access_token"]
                st.success("Login realizado com sucesso!")
                st.rerun()
            elif response:
                show_api_error(response)

    with tab_register:
        with st.form("form_register"):
            nome = st.text_input("Nome completo")
            email_cadastro = st.text_input("E-mail de cadastro")
            senha_cadastro = st.text_input("Senha", type="password")
            submit_register = st.form_submit_button("Cadastrar usuário")

        if submit_register:
            payload = {"nome": nome, "email": email_cadastro, "senha": senha_cadastro}
            response = api_request("POST", "/auth/register", json=payload)
            if response and response.status_code == 201:
                st.success("Usuário cadastrado! Faça login para acessar o sistema.")
            elif response:
                show_api_error(response)

    st.info("Dica: rode `cd backend && python -m scripts.seed` para criar o usuário demo admin@stockflow.com / admin123.")


def sidebar_user():
    response = api_request("GET", "/auth/me")
    if response and response.status_code == 200:
        user = response.json()
        st.sidebar.success(f"Logado como: {user['nome']}")
        st.sidebar.caption(f"Perfil: {user['perfil']}")
    else:
        st.session_state.pop("token", None)
        st.rerun()

    if st.sidebar.button("Sair"):
        st.session_state.pop("token", None)
        st.rerun()


def produtos_view():
    st.header("Produtos")

    with st.expander("Cadastrar novo produto", expanded=True):
        with st.form("form_produto"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome do produto")
                categoria = st.text_input("Categoria")
                quantidade = st.number_input("Quantidade inicial", min_value=0, step=1)
            with col2:
                peso = st.number_input("Peso", min_value=0.0, step=0.01, format="%.2f")
                preco = st.number_input("Preço", min_value=0.0, step=0.01, format="%.2f")
            submit = st.form_submit_button("Cadastrar produto")

        if submit:
            payload = {
                "nome": nome,
                "categoria": categoria,
                "quantidade": int(quantidade),
                "peso": float(peso),
                "preco": float(preco),
            }
            response = api_request("POST", "/produtos", json=payload)
            if response and response.status_code == 201:
                st.success("Produto cadastrado com sucesso!")
                st.rerun()
            elif response:
                show_api_error(response)

    st.subheader("Consulta de produtos")
    colf1, colf2, colf3 = st.columns(3)
    with colf1:
        filtro_nome = st.text_input("Filtrar por nome")
    with colf2:
        filtro_categoria = st.text_input("Filtrar por categoria")
    with colf3:
        apenas_baixo = st.checkbox("Somente estoque baixo")

    params = {}
    if filtro_nome:
        params["nome"] = filtro_nome
    if filtro_categoria:
        params["categoria"] = filtro_categoria
    if apenas_baixo:
        params["estoque_baixo"] = True

    response = api_request("GET", "/produtos", params=params)
    produtos = []
    if response and response.status_code == 200:
        produtos = response.json()
        st.dataframe(produtos, use_container_width=True)
    elif response:
        show_api_error(response)

    if produtos:
        st.subheader("Atualizar ou excluir produto")
        produto_options = {f"#{p['id']} — {p['nome']}": p for p in produtos}
        selected_label = st.selectbox("Selecione um produto", list(produto_options.keys()))
        selected = produto_options[selected_label]

        with st.form("form_update"):
            col1, col2 = st.columns(2)
            with col1:
                nome_edit = st.text_input("Nome", value=selected["nome"])
                categoria_edit = st.text_input("Categoria", value=selected["categoria"])
                quantidade_edit = st.number_input("Quantidade", min_value=0, value=int(selected["quantidade"]), step=1)
            with col2:
                peso_edit = st.number_input("Peso", min_value=0.0, value=float(selected["peso"]), step=0.01, format="%.2f")
                preco_edit = st.number_input("Preço", min_value=0.0, value=float(selected["preco"]), step=0.01, format="%.2f")
            update = st.form_submit_button("Salvar alterações")

        col_del1, col_del2 = st.columns([1, 4])
        with col_del1:
            delete = st.button("Excluir produto", type="secondary")
        with col_del2:
            st.caption("A exclusão remove também o histórico de movimentações desse produto.")

        if update:
            payload = {
                "nome": nome_edit,
                "categoria": categoria_edit,
                "quantidade": int(quantidade_edit),
                "peso": float(peso_edit),
                "preco": float(preco_edit),
            }
            response = api_request("PUT", f"/produtos/{selected['id']}", json=payload)
            if response and response.status_code == 200:
                st.success("Produto atualizado!")
                st.rerun()
            elif response:
                show_api_error(response)

        if delete:
            response = api_request("DELETE", f"/produtos/{selected['id']}")
            if response and response.status_code == 204:
                st.success("Produto excluído!")
                st.rerun()
            elif response:
                show_api_error(response)


def estoque_view():
    st.header("Entrada e Saída de Estoque")

    response = api_request("GET", "/produtos")
    if not response or response.status_code != 200:
        if response:
            show_api_error(response)
        return

    produtos = response.json()
    if not produtos:
        st.warning("Cadastre pelo menos um produto antes de movimentar o estoque.")
        return

    produto_options = {f"#{p['id']} — {p['nome']} (Qtd: {p['quantidade']})": p for p in produtos}
    selected_label = st.selectbox("Produto", list(produto_options.keys()))
    selected = produto_options[selected_label]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Entrada")
        with st.form("form_entrada"):
            quantidade = st.number_input("Quantidade de entrada", min_value=1, step=1, key="qtd_entrada")
            observacao = st.text_input("Observação", key="obs_entrada")
            submit = st.form_submit_button("Registrar entrada")
        if submit:
            payload = {"produto_id": selected["id"], "quantidade": int(quantidade), "observacao": observacao}
            response = api_request("POST", "/estoque/entrada", json=payload)
            if response and response.status_code == 201:
                st.success("Entrada registrada!")
                st.rerun()
            elif response:
                show_api_error(response)

    with col2:
        st.subheader("Saída")
        with st.form("form_saida"):
            quantidade = st.number_input("Quantidade de saída", min_value=1, step=1, key="qtd_saida")
            observacao = st.text_input("Observação", key="obs_saida")
            submit = st.form_submit_button("Registrar saída")
        if submit:
            payload = {"produto_id": selected["id"], "quantidade": int(quantidade), "observacao": observacao}
            response = api_request("POST", "/estoque/saida", json=payload)
            if response and response.status_code == 201:
                st.success("Saída registrada!")
                st.rerun()
            elif response:
                show_api_error(response)

    st.subheader("Histórico de movimentações")
    response = api_request("GET", "/estoque/movimentacoes")
    if response and response.status_code == 200:
        st.dataframe(response.json(), use_container_width=True)
    elif response:
        show_api_error(response)


def relatorios_view():
    st.header("Relatórios")

    response = api_request("GET", "/relatorios/resumo")
    if response and response.status_code == 200:
        resumo = response.json()
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Produtos", resumo["total_produtos"])
        col2.metric("Itens em estoque", resumo["quantidade_total_itens"])
        col3.metric("Valor total", f"R$ {resumo['valor_total_estoque']:.2f}")
        col4.metric("Estoque baixo", resumo["produtos_estoque_baixo"])
        col5.metric("Movimentações", resumo["total_movimentacoes"])
    elif response:
        show_api_error(response)

    st.subheader("Produtos com estoque baixo")
    limite = st.number_input("Limite", min_value=0, value=5, step=1)
    response = api_request("GET", "/relatorios/baixo-estoque", params={"limite": int(limite)})
    if response and response.status_code == 200:
        st.dataframe(response.json(), use_container_width=True)
    elif response:
        show_api_error(response)


def main():
    if "token" not in st.session_state:
        login_view()
        return

    st.sidebar.title("StockFlow")
    sidebar_user()

    menu = st.sidebar.radio("Menu", ["Produtos", "Estoque", "Relatórios"])

    if menu == "Produtos":
        produtos_view()
    elif menu == "Estoque":
        estoque_view()
    else:
        relatorios_view()


if __name__ == "__main__":
    main()
