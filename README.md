# 🚀 Sistema Integrado de Automação Comercial & BI

Este sistema foi idealizado e desenvolvido para transformar o fluxo de prospecção manual em um processo tecnológico automatizado, unindo **Python** e **Business Intelligence**.

## 👤 Autor
Este projeto foi integralmente desenvolvido por **William Antonio Estevam**.
- 🎓 **Estudante de Análise e Desenvolvimento de Sistemas (ADS)** – Centro Universitário Estácio.
- 💼 **Objetivo:** Aplicar engenharia de software e análise de dados para resolver problemas reais de produtividade no setor comercial.

## 🛠️ Tecnologias e Habilidades Aplicadas
- **Linguagem:** Python 3.12+
- **Automação Web:** Selenium & Webdriver-manager.
- **Engenharia de Dados:** Pandas (Manipulação de DataFrames e exportação de logs em CSV).
- **Data Visualization:** Matplotlib (Criação de gráficos de performance).
- **Versionamento:** Git & GitHub.

## 📈 Como o Sistema Funciona
O projeto opera em um ecossistema de duas etapas:
1. **Módulo de Execução (`whatsapp_pro.py`)**: Realiza o disparo de mensagens personalizadas e gera um arquivo de log em tempo real com o status de cada operação.
2. **Módulo de Inteligência (`gerar_relatorio.py`)**: Consome os dados gerados, processa as métricas e exporta um gráfico de aproveitamento para suporte à tomada de decisão.

## ⚙️ Instalação
```bash
# Clone o repositório
git clone [https://github.com/williamestevampy/automacao-whatsapp-python.git](https://github.com/williamestevampy/automacao-whatsapp-python.git)

# Instale as dependências
pip install pandas selenium webdriver-manager matplotlib openpyxl