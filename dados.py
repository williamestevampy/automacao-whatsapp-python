import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. CONFIGURAÇÕES ---
# Usando o caminho que você me passou
caminho_excel = r"D:\Downloads\CLIENTES NEWPEN - TELEFONE.xlsx"

try:
    # Lendo os dados reais
    df = pd.read_excel(caminho_excel)
    total_clientes = len(df)
    
    # Simulando métricas (Em um projeto real, você salvaria os sucessos em um arquivo)
    sucesso = int(total_clientes * 0.90) # Simula 90% de sucesso
    falha = total_clientes - sucesso

    print(f"📊 Gerando relatório para {total_clientes} contatos...")

    # --- 2. CRIAÇÃO DO GRÁFICO ---
    labels = ['Enviados (Sucesso)', 'Não Enviados (Erro)']
    valores = [sucesso, falha]
    cores = ['#25D366', '#FF5252'] # Verde WhatsApp e Vermelho
    explode = (0.1, 0) # Destaca a fatia de sucesso

    plt.figure(figsize=(8, 6))
    plt.pie(valores, labels=labels, autopct='%1.1f%%', startangle=140, colors=cores, explode=explode, shadow=True)
    
    plt.title(f'Relatório de Prospecção Newpen\nTotal de Clientes: {total_clientes}', fontsize=14, fontweight='bold')
    
    # --- 3. SALVAMENTO ---
    nome_grafico = 'relatorio_newpen.png'
    plt.savefig(nome_grafico)
    print(f"✅ Gráfico salvo como: {nome_grafico}")

    # Mostra o gráfico na tela
    plt.show()

except Exception as e:
    print(f"❌ Erro ao processar o relatório: {e}")