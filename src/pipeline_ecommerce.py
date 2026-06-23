import sqlite3
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Caminho do projeto
DB_PATH = Path(__file__).parent.parent / "data" / "ecommerce.db"
OUTPUT_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "processed"
    / "relatorio_faturamento.parquet"
)


def inicializar_banco_de_dados():
    """Gera um banco de dados SQL local com dados simulados de vendas"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    # Correção: NOT EXISTS (e não EXIXTS)
    cursor.execute(""" CREATE TABLE IF NOT EXISTS vendas (
                   id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                   produto TEXT NOT NULL,
                   categoria TEXT NOT NULL,
                   quantidade INTEGER NOT NULL,
                   preco_unitario REAL NOT NULL,
                   data_venda TEXT NOT NULL)
                    """)

    cursor.execute("SELECT COUNT(*) FROM vendas")
    if cursor.fetchone()[0] == 0:
        dados = [
            ("Notebook Dell", "Eletrônicos", 2, 4500.00, "2026-06-01"),
            ("iPhone 15", "Eletrônicos", 1, 7000.00, "2026-06-01"),
            ("Cadeira Ergonômica", "Móveis", 5, 1200.00, "2026-06-02"),
            ("Teclado Mecânico", "Eletrônicos", 10, 350.00, "2026-06-02"),
            ("Mesa de Escritório", "Móveis", 2, 1500.00, "2026-06-03"),
            ("Monitor 29 Ultrawide", "Eletrônicos", 3, 1600.00, "2026-06-03"),
            ("Livro de Python e Dados", "Livros", 20, 90.00, "2026-06-04"),
            ("Livro de SQL Avançado", "Livros", 15, 110.00, "2026-06-04"),
        ]
        cursor.executemany(
            """ INSERT INTO vendas (produto, categoria, quantidade, preco_unitario, data_venda)
                           VALUES (?, ?, ?, ?, ?)
                            """,
            dados,
        )
        conexao.commit()
        # Correção: logging.info (e não INFO)
        logging.info("Banco de dados inicializado com sucesso!")

    # O fechamento da conexão deve ficar fora do 'if' para sempre fechar o banco
    conexao.close()


def extrair_dados_sql() -> pd.DataFrame:
    logging.info("Extraindo dados do banco SQLite via SQL...")

    try:
        conexao = sqlite3.connect(DB_PATH)

        query = "SELECT * FROM vendas"
        df = pd.read_sql_query(query, conexao)

        conexao.close()

        logging.info(f"Sucesso! {len(df)} registros extraídos via SQL.")
        return df

    except Exception as e:
        logging.error(f"Erro na extração SQL: {e}")
        return None


def transformar_dados_vendas(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Iniciando a transformação e agrupamento dos dados financeiros...")

    try:
        df_copia = df.copy()

        df_copia["faturamento"] = df_copia["quantidade"] * df_copia["preco_unitario"]

        df_copia["data_venda"] = pd.to_datetime(df_copia["data_venda"])

        logging.info("Transformação realizada com sucesso!")
        return df_copia

    except Exception as e:
        logging.error(f"Erro na transformação dos dados: {e}")
        return None


def carregar_dados_vendas(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Iniciando a carga do relátorio do Data Lake local...")

    try:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        df.to_parquet(OUTPUT_PATH, index=False)

        logging.info(f"Sucesso absoluto! Relatório Parquet gravado em: {OUTPUT_PATH}")

    except Exception as e:
        logging.error(f"Erro ao carregar os dados no Data Lake: {e}")


if __name__ == "__main__":
    inicializar_banco_de_dados()

    df_vendas = extrair_dados_sql()

    if df_vendas is not None:
        df_tratado = transformar_dados_vendas(df_vendas)

    if df_tratado is not None:
        carregar_dados_vendas(df_tratado)

    if df_tratado is not None:
        print("\n--- DADOS BRUTOS DO BANCO SQL ---")
        print(df_vendas)
        print("-----------------------------------\n")
