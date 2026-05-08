import pandas as pd
import sqlite3
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
perfil_path = os.path.join(os.getcwd(), "Sessao_Whatsapp")
banco_nome = 'banco_newpen.db'

def atualizar_status_no_sql(nome, status):
    conn = sqlite3.connect(banco_nome)
    cursor = conn.cursor()
    # Criamos a coluna status_envio se ela não existir (Segurança)
    try:
        cursor.execute("ALTER TABLE clientes ADD COLUMN status_envio TEXT")
    except:
        pass 
    
    cursor.execute("UPDATE clientes SET status_envio = ? WHERE nome = ?", (status, nome))
    conn.commit()
    conn.close()

# 1. Carregar dados do SQL (Não mais do Excel!)
conn = sqlite3.connect(banco_nome)
df = pd.read_sql("SELECT * FROM clientes", conn)
conn.close()

# Iniciar Navegador
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={perfil_path}")
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
navegador.get("https://web.whatsapp.com/")

print("🚀 Aguardando login...")
WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.ID, "side")))

for i, linha in df.iterrows():
    nome = linha['nome']
    # Pula se já foi enviado com sucesso
    if linha.get('status_envio') == 'Sucesso':
        continue

    numero = "".join(filter(str.isdigit, str(linha['telefone'])))
    if not numero.startswith("55"): numero = "55" + numero
    
    msg = f"Oi {nome}, tudo bem? Sou o William da Newpen! 🎨"
    link = f"https://web.whatsapp.com/send?phone={numero}&text={urllib.parse.quote(msg)}"
    
    navegador.get(link)
    try:
        time.sleep(10)
        # Verifica número inválido
        if len(navegador.find_elements(By.XPATH, '//*[contains(text(), "inválido")]')) > 0:
            atualizar_status_no_sql(nome, 'Invalido')
            print(f"❌ {nome}: Número inválido")
            continue

        campo = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//footer//div[@contenteditable="true"]')))
        campo.send_keys(Keys.ENTER)
        
        atualizar_status_no_sql(nome, 'Sucesso')
        print(f"✅ {nome}: Enviado!")
        time.sleep(5)
    except:
        atualizar_status_no_sql(nome, 'Erro')
        print(f"⚠️ {nome}: Erro no envio")

navegador.quit()
print("🏁 Banco de Dados atualizado em tempo real!")