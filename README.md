# Portal de Agendamentos de Entrega — Streamlit

Portal demonstrativo em Streamlit para gestão de agendamentos de entrega, com KPIs, kanban, pendências, reagendamentos, ranking de transportadoras, carteira de clientes e exportação de relatórios. A base de dados é a planilha `data/agendamentos.xlsx`.

## Estrutura

```
portal_agendamentos_streamlit/
├── .streamlit/
│   └── config.toml              # Tema do Streamlit
├── assets/
│   └── style.css                # CSS customizado
├── components/
│   └── ui.py                    # Sidebar, header, cards, painéis
├── data/
│   └── agendamentos.xlsx        # Base Excel (aba "agendamentos")
├── pages/
│   ├── 1_Agendamentos.py
│   ├── 2_Pendencias.py
│   ├── 3_Reagendamentos.py
│   ├── 4_Transportadoras.py
│   ├── 5_Clientes.py
│   ├── 6_Relatorios.py
│   └── 7_Configuracoes.py
├── services/
│   └── data_loader.py           # Leitura, normalização e filtros
├── utils/
│   ├── charts.py                # Gráficos Plotly
│   └── kpis.py                  # KPIs e contagens
├── app.py                       # Dashboard (home)
├── requirements.txt
├── .gitignore
└── README.md
```

## Como rodar localmente

```bash
# 1. Crie um ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Suba a aplicação
streamlit run app.py
```

A aplicação abre em `http://localhost:8501`.

## Publicação no GitHub + Streamlit Community Cloud

1. **GitHub**
   - Crie um repositório novo (público ou privado).
   - Faça `git init`, `git add .`, `git commit -m "primeiro commit"` e `git push`.
   - Mantenha a estrutura de pastas exatamente como acima — o Streamlit Cloud lê os arquivos a partir da raiz do repositório.

2. **Streamlit Community Cloud** (https://share.streamlit.io)
   - Faça login com a sua conta GitHub.
   - Clique em **New app** → selecione o repositório, branch e informe `app.py` como **Main file path**.
   - O `requirements.txt` na raiz é detectado automaticamente.
   - Clique em **Deploy**. O primeiro build leva alguns minutos.

## Como trocar a base de dados

Substitua `data/agendamentos.xlsx` por uma nova planilha, mantendo:

- **Nome da aba:** `agendamentos`
- **Colunas mínimas esperadas:**
  `Cliente, CNPJ Cliente, NF, Destino, UF, Transportadora, RC, Coordenador,
  Data Envio de agendamento, Data Sugerida de agendamento, Data Agendada,
  Reagendamento?, Data Entrerga, Analista, Status, Prioridade,
  TipoPendencia, MotivoPendencia, MotivoReagendamento, QtdReagendamentos,
  DiasEmAberto, HorasSemRetorno, Atrasado, SLAStatus, ResponsavelAcao,
  Mes (opcional — recalculado automaticamente)`

Colunas faltantes não quebram o app: as telas que dependem delas mostram um aviso "Sem dados".

## Mudanças relevantes em relação à versão anterior

- Tratamento defensivo de colunas que podem não existir na planilha.
- Stages do kanban alinhados aos `Status` realmente presentes na base
  (`Aguardando Cliente`, `Agendada`, `Confirmada`, `Em Transporte`,
  `Atrasada`, `Entregue`).
- Cache invalidado automaticamente quando o arquivo Excel é alterado (mtime).
- Gráficos não estouram com DataFrame vazio — mostram "Sem dados".
- KPIs com proteção contra divisão por zero, `NaT` e `NaN`.
- Sidebar com Home funcional (sem `st.page_link("app.py")`, que dispara erro).
- Busca da tela de Agendamentos otimizada para colunas específicas, evitando varredura linha-a-linha de todas as células.
- Caminhos de arquivo absolutos (`Path(__file__).resolve().parent.parent`),
  funcionando independente do diretório de onde o `streamlit run` foi
  disparado.
- `requirements.txt` com faixas de versão (em vez de versões cravadas),
  facilitando deploy no Streamlit Cloud.
