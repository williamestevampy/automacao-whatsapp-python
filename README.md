# 🚀 Sistema Integrado de Automação Comercial & BI - Newpen

Este sistema foi idealizado e desenvolvido integralmente por **William Estevam** para automatizar e otimizar o fluxo de prospecção e vendas na representação comercial da **Newpen**. Ele integra automação de mensagens via WhatsApp, persistência em banco de dados relacional e inteligência de negócios (BI).

## 📋 Sobre o Projeto
O projeto resolve o desafio de gerenciar grandes volumes de contatos de forma profissional. A transição de planilhas Excel para um banco de dados **SQLite** permitiu a criação de um "histórico de ondas" (campanhas), garantindo a continuidade dos envios e evitando a duplicidade de mensagens (SPAM).

## ✨ Funcionalidades Principais
* **ETL (Extração e Carga):** Migração automática de bases em Excel para banco de dados SQL (SQLite).
* **Automação de WhatsApp (Wave System):** Disparos personalizados com tratamento de nomes e controle de campanhas (Onda 1 - Apresentação / Onda 2 - Lançamentos).
* **Persistência de Status em Tempo Real:** Registro automático de envios concluídos, números inválidos e interessados diretamente no banco de dados.
* **Dashboard de BI (Business Intelligence):** Interface interativa em Streamlit para monitoramento de métricas como Taxa de Conversão e Volume de Envios.

## 🛠️ Tech Stack
* **Linguagem:** Python 3.12+
* **Banco de Dados:** SQLite (SQL Relacional)
* **Automação:** Selenium & Webdriver Manager
* **Visualização de Dados:** Streamlit & Matplotlib
* **Processamento de Dados:** Pandas & Openpyxl

## 🏗️ Arquitetura do Sistema
1.  **`migrar_para_sql.py`**: Script responsável por estruturar os dados brutos no banco `.db`.
2.  **`whatsapp_onda2.py`**: Robô de automação que processa a fila de disparos e atualiza o banco de dados em tempo real.
3.  **`app.py`**: Dashboard que extrai inteligência do banco de dados para auxiliar na tomada de decisão comercial.

## 🚀 Como Executar
1. Instale as dependências:
   ```bash
   pip install selenium pandas streamlit matplotlib webdriver-manager openpyxl