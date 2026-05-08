import pandas as pd
import matplotlib.pyplot as plt

# Caminhos dos arquivos
caminho_excel = r"D:\Downloads\CLIENTES NEWPEN - TELEFONE.xlsx"
caminho_log = "log_envios.csv"

try:
    # 1. Lendo os dados técnicos do Robô (Log)
    df_log = pd.read_csv(caminho_log)
    total_invalido = len(df_log[df_log['Status'] == 'Erro'])
    total_sucesso = len(df_log[df_log['Status'] == 'Sucesso'])

    # 2. Lendo os seus dados comerciais (Excel)
    df_excel = pd.read_excel(caminho_excel)
    # Limpeza de segurança na coluna retorno
    df_excel.columns = [str(c).strip().lower() for c in df_excel.columns]
    
    if 'retorno' in df_excel.columns:
        total_retorno = len(df_excel[df_excel['retorno'].astype(str).str.strip().str.lower() == 'sim'])
    else:
        total_retorno = 0
        print("⚠️ Coluna 'retorno' não encontrada no Excel. Usando 0.")

    # 3. CÁLCULO DE MÉTRICAS
    # Calculamos a taxa de conversão sobre os envios que REALMENTE deram certo
    taxa_conversao = (total_retorno / total_sucesso) * 100 if total_sucesso > 0 else 0

    print(f"📊 --- RELATÓRIO TÉCNICO E COMERCIAL ---")
    print(f"❌ Números Inválidos (Erro): {total_invalido}")
    print(f"✅ Mensagens Entregues: {total_sucesso}")
    print(f"💬 Clientes que Responderam: {total_retorno}")
    print(f"📈 Conversão Real: {taxa_conversao:.1f}%")

    # 4. GRÁFICO DE BARRAS COMPARATIVO
    categorias = ['Números Inválidos', 'Mensagens Enviadas', 'Retorno (Vendas)']
    valores = [total_invalido, total_sucesso, total_retorno]
    cores = ['#e74c3c', '#3498db', '#2ecc71'] # Vermelho, Azul e Verde

    plt.figure(figsize=(10, 6))
    barras = plt.bar(categorias, valores, color=cores)

    # Adiciona os números no topo de cada barra
    for barra in barras:
        yval = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom', fontweight='bold')

    plt.title(f'Performance de Prospecção Newpen\nTaxa de Resposta: {taxa_conversao:.1f}%', fontsize=14, fontweight='bold')
    plt.ylabel('Quantidade')
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    plt.savefig('relatorio_geral_newpen.png')
    print("\n✅ Relatório visual salvo como: relatorio_geral_newpen.png")
    plt.show()

except FileNotFoundError:
    print("❌ Erro: O arquivo 'log_envios.csv' não foi encontrado. Rode o robô primeiro!")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")