# Portal de Agendamentos de Entrega - Streamlit

Projeto demonstrativo em Streamlit, com visual inspirado nos mockups enviados, usando a planilha `data/agendamentos.xlsx` como base.

## Como rodar localmente

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Estrutura

- `app.py`: Dashboard principal.
- `pages/`: telas do portal.
- `services/data_loader.py`: leitura, limpeza e filtros da planilha.
- `utils/kpis.py`: cálculos dos indicadores.
- `utils/charts.py`: gráficos Plotly.
- `components/ui.py`: menu, header e cards reutilizáveis.
- `assets/style.css`: aparência geral.
- `.streamlit/config.toml`: tema do Streamlit.
- `data/agendamentos.xlsx`: base Excel.

## GitHub + Streamlit Community Cloud

1. Suba estes arquivos para o repositório GitHub mantendo a mesma estrutura.
2. No Streamlit Cloud, selecione o repositório e informe `app.py` como arquivo principal.
3. Garanta que `requirements.txt` esteja na raiz.
4. Para trocar a base, substitua `data/agendamentos.xlsx` por uma nova planilha com a mesma aba `agendamentos` e colunas equivalentes.
