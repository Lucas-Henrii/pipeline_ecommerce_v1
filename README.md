# 📊 Pipeline de Análise de Desempenho de E-commerce

Este é um projeto prático de Engenharia de Dados focado no desenvolvimento de uma pipeline de **ETL (Extract, Transform, Load)** robusta. O objetivo principal foi simular um cenário real de e-commerce, integrando **Python**, bancos de dados relacionais com **SQL** e controle de versão via **Git**.

---

## 🗺️ Arquitetura do Projeto

A pipeline foi desenhada seguindo o conceito de medalhão para a organização do Data Lake local:

1. **Extract (Origem SQL):** Os dados transacionais de vendas são armazenados e extraídos de um banco de dados relacional **SQLite** utilizando consultas SQL analíticas direto pelo Python.
2. **Transform (Pandas):** O motor do **Pandas** consome os dados brutos, realiza o cálculo de faturamento por linha ($Quantidade \times Preço$) e agrega as métricas para gerar um indicador de faturamento consolidado por categoria de produto.
3. **Load (Destino Silver):** O relatório final tratado é persistido localmente no formato colunar **Parquet** (via `pyarrow`), garantindo alta performance e compressão para futuras consultas de BI.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Linguagem Principal:** Python 3.12+
* **Manipulação de Dados:** Pandas
* **Armazenamento Colunar:** PyArrow (Parquet)
* **Banco de Dados:** SQLite3 (SQL)
* **Gerenciador de Pacotes:** UV (Fast Python package installer)
* **Controle de Versão:** Git & GitHub

---
