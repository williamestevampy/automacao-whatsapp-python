import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import time
import os

# --- CONFIGURAÇÕES ---
caminho_excel = r"D:\Downloads\CLIENTES NEWPEN - TELEFONE.xlsx"
perfil_path = os.path.join(os.getcwd(), "Sessao_Whatsapp")
resultados = []

try:
    df = pd.read_excel(caminho_excel, dtype={'telefone': str})
    # Limpeza de segurança nas colunas (remove espaços e deixa minúsculo)
    df.columns = [str(c).strip().lower() for c in df.columns]
    total_contatos = len(df)
    print(f"✅ Planilha carregada! Colunas detectadas: {list(df.columns)}")
except Exception as e:
    print(f"❌ Erro ao ler Excel: {e}")
    exit()

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={perfil_path}")
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=options)
navegador.get("https://web.whatsapp.com/")

print("🚀 Aguardando WhatsApp...")
WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.ID, "side")))

# --- LOOP DE ENVIO ---
for i, linha in df.iterrows():
    progresso = f"[{i + 1}/{total_contatos}]"
    nome_cliente = linha['nome']
    
    # Tratamento do número
    numero = "".join(filter(str.isdigit, str(linha['telefone']).split('.')[0]))
    if not numero.startswith("55"): numero = "55" + numero

    mensagem = f"Oi, {nome_cliente}! Tudo bem? Sou o William da Newpen... 🎨"
    link = f"https://web.whatsapp.com/send?phone={numero}&text={urllib.parse.quote(mensagem)}"
    
    navegador.get(link)
    try:
        time.sleep(12)
        if len(navegador.find_elements(By.XPATH, '//*[contains(text(), "inválido")]')) > 0:
            print(f"{progresso} ❌ Número Inválido: {nome_cliente}")
            resultados.append({'Cliente': nome_cliente, 'Status': 'Erro'})
            navegador.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            continue

        campo_texto = WebDriverWait(navegador, 15).until(
            EC.presence_of_element_located((By.XPATH, '//footer//div[@contenteditable="true"]'))
        )
        campo_texto.send_keys(Keys.ENTER)
        print(f"{progresso} ✅ Enviado: {nome_cliente}")
        resultados.append({'Cliente': nome_cliente, 'Status': 'Sucesso'})
        time.sleep(10)
    except:
        print(f"{progresso} ⚠️ Erro técnico com {nome_cliente}")
        resultados.append({'Cliente': nome_cliente, 'Status': 'Erro'})

# Salva o log real para o seu portfólio
pd.DataFrame(resultados).to_csv('log_envios.csv', index=False, encoding='utf-8-sig')
print("\n🏁 Processo concluído! Arquivo 'log_envios.csv' gerado.")
navegador.quit()