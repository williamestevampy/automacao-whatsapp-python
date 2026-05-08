import pandas as pd
import sqlite3

# 1. Carregar os dados do Excel
caminho_excel = r"D:\Downloads\CLIENTES NEWPEN - TELEFONE.xlsx"
df = pd.read_excel(caminho_excel)

# Limpeza básica de colunas
df.columns = [str(c).strip().lower() for c in df.columns]

# 2. Conectar ao Banco de Dados SQL (ele cria o arquivo se não existir)
conexao = sqlite3.connect('banco_newpen.db')

# 3. Salvar os dados na tabela 'clientes'
# Se a tabela já existir, ele substitui (replace)
df.to_sql('clientes', conexao, if_exists='replace', index=False)

print("✅ Dados migrados com sucesso para o banco_newpen.db!")
conexao.close()