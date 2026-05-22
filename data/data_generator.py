"""
============================================================
ADERE Produtos Auto Adesivos
Gerador de Dados Fictícios para Testes
Cria base Excel com ~1000 registros realistas
============================================================
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# ---- Seed para reprodutibilidade ----
random.seed(42)
np.random.seed(42)


# ---- Dados mestres ----
CLIENTES = [
    ("Telhanorte", "60.597.786/0001-15", "São Paulo", "SP"),
    ("Leroy Merlin", "04.722.690/0001-15", "Barueri", "SP"),
    ("C&C Casa e Construção", "61.189.288/0001-90", "São Paulo", "SP"),
    ("Sodimac", "13.404.592/0001-36", "Osasco", "SP"),
    ("Obramax", "45.991.011/0001-44", "São Paulo", "SP"),
    ("Assaí Atacadista", "06.057.223/0001-71", "São Paulo", "SP"),
    ("Carrefour", "45.543.915/0001-81", "Barueri", "SP"),
    ("Makro Atacadista", "33.372.251/0001-91", "São Paulo", "SP"),
    ("Tok&Stok", "57.547.735/0001-99", "Barueri", "SP"),
    ("Casas Pernambucanas", "00.607.123/0001-26", "Guarulhos", "SP"),
    ("Magazine Luiza", "47.960.950/0001-21", "Franca", "SP"),
    ("Lojas Americanas", "33.014.556/0001-96", "Rio de Janeiro", "RJ"),
    ("Kalunga", "44.683.408/0001-80", "São Paulo", "SP"),
    ("Raia Drogasil", "61.585.865/0001-51", "São Paulo", "SP"),
    ("Grupo Pereira", "07.752.236/0001-24", "Florianópolis", "SC"),
    ("Condor Super Center", "75.315.333/0001-09", "Curitiba", "PR"),
    ("GPA - Grupo Pão de Açúcar", "47.508.411/0001-56", "São Paulo", "SP"),
    ("Walmart Brasil", "00.063.960/0001-70", "Curitiba", "PR"),
    ("Cencosud Brasil", "60.764.307/0001-64", "São Paulo", "SP"),
    ("Arno & Co Distribuidora", "12.345.678/0001-99", "Campinas", "SP"),
    ("Ferraço Materiais", "98.765.432/0001-12", "Ribeirão Preto", "SP"),
    ("Constrular", "11.222.333/0001-44", "Belo Horizonte", "MG"),
    ("Total Construções", "22.333.444/0001-55", "Porto Alegre", "RS"),
    ("Construfix Sul", "33.444.555/0001-66", "Curitiba", "PR"),
    ("Maxfort Distribuição", "44.555.666/0001-77", "Fortaleza", "CE"),
    ("Distribuidora Nordeste", "55.666.777/0001-88", "Recife", "PE"),
    ("BH Construções", "66.777.888/0001-99", "Belo Horizonte", "MG"),
    ("Construção & Arte", "77.888.999/0001-10", "Salvador", "BA"),
    ("Novo Mundo", "88.999.000/0001-21", "Goiânia", "GO"),
    ("Insinuante", "99.000.111/0001-32", "Salvador", "BA"),
]

TRANSPORTADORAS = [
    "JSL", "Braspress", "Tegma", "Patrus", "Translovato",
    "Rodonaves", "TNT", "Correios", "J&T Express", "Sequoia",
    "Log-In", "Ryder", "DHL", "Fedex Brasil", "Total Express",
]

COORDENADORES = [
    "Marcos Oliveira", "Ana Paula Silva", "Ricardo Ferreira",
    "Camila Santos", "Thiago Costa", "Juliana Almeida",
]

ANALISTAS = [
    "Pedro Nascimento", "Fernanda Lima", "Bruno Carvalho",
    "Letícia Souza", "Gabriel Martins", "Isabela Rocha",
    "Rafael Pereira", "Natália Gomes", "Diego Rodrigues",
    "Amanda Vieira",
]

RCS = [f"RC{str(i).zfill(4)}" for i in range(1, 51)]

STATUS_LIST = [
    "Faturada",
    "Aguardando contato",
    "Contato realizado",
    "Aguardando cliente",
    "Agendada",
    "Confirmada",
    "Em transporte",
    "Entregue",
    "Reagendada",
    "Atrasada",
    "Crítica",
    "Cliente recusou",
]

# Pesos de distribuição (simula cenário real)
STATUS_WEIGHTS = [5, 10, 8, 12, 15, 10, 12, 18, 6, 8, 4, 2]

OBSERVACOES_TEMPLATES = [
    "Cliente confirmou recebimento do e-mail de agendamento.",
    "Tentativa de contato sem retorno. Aguardando.",
    "Endereço de entrega confirmado pelo cliente.",
    "Cliente solicitou reagendamento por falta de espaço no armazém.",
    "Transportadora confirmou coleta do material.",
    "NF aguardando liberação financeira do cliente.",
    "Contato realizado com gerente de logística - {analista}.",
    "Entrega reagendada a pedido do cliente.",
    "Material parado no CD da transportadora aguardando autorização.",
    "Cliente não atendeu nas 3 tentativas. Escalado para coordenador.",
    "Agendamento confirmado para o turno da manhã.",
    "Entrega sem avaria registrada. Recibo assinado.",
    "Divergência de endereço identificada. Em correção.",
    "Cliente solicitou agendamento para data futura.",
    "Transportadora informou atraso na rota por condições climáticas.",
    "Pendência de documentação: DANFE não recebida pelo cliente.",
    "Primeira tentativa de agendamento recusada. Nova data em negociação.",
    "NF emitida com valor divergente - em análise financeira.",
    "Entregue com sucesso. Comprovante anexado ao sistema.",
    "Cliente confirmou disponibilidade para recebimento.",
]


def gerar_nf() -> str:
    """Gera número de NF fictício realista."""
    return str(random.randint(100000, 999999))


def gerar_data_faturamento(base: datetime) -> datetime:
    """Gera data de faturamento nos últimos 90 dias."""
    dias_atras = random.randint(0, 90)
    return base - timedelta(days=dias_atras)


def calcular_datas(data_fat: datetime, status: str) -> dict:
    """
    Calcula datas derivadas com base no status e data de faturamento.
    Simula o fluxo real: faturamento → envio → sugerida → agendada.
    """
    data_envio    = None
    data_sugerida = None
    data_agendada = None
    sla_dias      = None
    tempo_parado  = None
    hoje = datetime.now()

    # Data de envio (1-3 dias após faturamento)
    if status not in ["Faturada"]:
        data_envio = data_fat + timedelta(days=random.randint(1, 3))

    # Data sugerida (3-7 dias após envio)
    if status in [
        "Aguardando cliente", "Agendada", "Confirmada",
        "Em transporte", "Entregue", "Reagendada",
        "Atrasada", "Crítica",
    ] and data_envio:
        data_sugerida = data_envio + timedelta(days=random.randint(3, 7))

    # Data agendada (pode ser diferente da sugerida)
    if status in ["Agendada", "Confirmada", "Em transporte", "Entregue", "Reagendada"] and data_sugerida:
        delta = random.randint(-2, 5)
        data_agendada = data_sugerida + timedelta(days=delta)

    # Para status crítico/atrasado, a data agendada já passou
    if status in ["Atrasada", "Crítica"] and data_sugerida:
        data_agendada = data_sugerida + timedelta(days=random.randint(-10, -1))

    # SLA (dias úteis desde faturamento até hoje ou entrega)
    if status == "Entregue" and data_agendada:
        sla_dias = (data_agendada - data_fat).days
    else:
        sla_dias = (hoje - data_fat).days

    # Tempo parado (dias sem movimentação)
    ultima_mov = data_envio or data_fat
    tempo_parado = (hoje - ultima_mov).days if status not in ["Entregue"] else 0

    return {
        "data_envio":    data_envio,
        "data_sugerida": data_sugerida,
        "data_agendada": data_agendada,
        "sla_dias":      max(0, sla_dias),
        "tempo_parado":  max(0, tempo_parado),
    }


def gerar_observacao(status: str, analista: str) -> str:
    """Gera observação coerente com o status."""
    obs = random.choice(OBSERVACOES_TEMPLATES)
    return obs.replace("{analista}", analista)


def gerar_base_dados(n: int = 1000) -> pd.DataFrame:
    """
    Gera DataFrame com n registros fictícios realistas.

    Args:
        n: Número de registros a gerar

    Returns:
        DataFrame com todos os campos do portal
    """
    hoje = datetime.now()
    registros = []

    for i in range(n):
        cliente_data  = random.choice(CLIENTES)
        nome_cliente, cnpj, cidade, uf = cliente_data
        transportadora = random.choice(TRANSPORTADORAS)
        coordenador    = random.choice(COORDENADORES)
        analista       = random.choice(ANALISTAS)
        rc             = random.choice(RCS)
        status         = random.choices(STATUS_LIST, weights=STATUS_WEIGHTS, k=1)[0]
        nf             = gerar_nf()
        data_fat       = gerar_data_faturamento(hoje)

        datas = calcular_datas(data_fat, status)

        ultima_atualizacao = hoje - timedelta(hours=random.randint(0, 72))

        registros.append({
            "NF":                 nf,
            "Status":             status,
            "Cliente":            nome_cliente,
            "CNPJ":               cnpj,
            "Cidade":             cidade,
            "UF":                 uf,
            "RC":                 rc,
            "Coordenador":        coordenador,
            "Transportadora":     transportadora,
            "Analista":           analista,
            "Data_Faturamento":   data_fat.strftime("%Y-%m-%d"),
            "Data_Envio":         datas["data_envio"].strftime("%Y-%m-%d") if datas["data_envio"] else None,
            "Data_Sugerida":      datas["data_sugerida"].strftime("%Y-%m-%d") if datas["data_sugerida"] else None,
            "Data_Agendada":      datas["data_agendada"].strftime("%Y-%m-%d") if datas["data_agendada"] else None,
            "SLA_Dias":           datas["sla_dias"],
            "Tempo_Parado_Dias":  datas["tempo_parado"],
            "Observacoes":        gerar_observacao(status, analista),
            "Ultima_Atualizacao": ultima_atualizacao.strftime("%Y-%m-%d %H:%M"),
        })

    df = pd.DataFrame(registros)

    # Ajustes pós-geração
    # Garante que entregues tenham data agendada
    mask_entregue = df["Status"] == "Entregue"
    df.loc[mask_entregue & df["Data_Agendada"].isna(), "Data_Agendada"] = (
        pd.to_datetime(df.loc[mask_entregue & df["Data_Agendada"].isna(), "Data_Faturamento"])
        + pd.to_timedelta(df.loc[mask_entregue & df["Data_Agendada"].isna(), "SLA_Dias"], unit="D")
    ).dt.strftime("%Y-%m-%d")

    return df


def salvar_excel(df: pd.DataFrame, caminho: str) -> None:
    """
    Salva o DataFrame como Excel com formatação básica.

    Args:
        df:      DataFrame a salvar
        caminho: Caminho de destino do arquivo .xlsx
    """
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    with pd.ExcelWriter(caminho, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Agendamentos")
        wb = writer.book
        ws = writer.sheets["Agendamentos"]

        # Largura automática das colunas
        for col in ws.columns:
            max_len = max(len(str(cell.value)) if cell.value else 0 for cell in col) + 4
            ws.column_dimensions[col[0].column_letter].width = min(max_len, 30)

    print(f"✅ Base de dados gerada: {caminho} ({len(df)} registros)")


if __name__ == "__main__":
    df = gerar_base_dados(1000)
    salvar_excel(df, "data/agendamentos.xlsx")
    print(df.head())
    print(f"\nDistribuição de status:\n{df['Status'].value_counts()}")
