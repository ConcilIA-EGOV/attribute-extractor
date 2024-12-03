# Tempo de espera, em segundos, entre cada requisição
TIME_BETWEEN_REQUESTS = 5

# Faz com que a aplicação acesse a API da OpenAI. Caso esteja desabilitado,
# utiliza uma mock response (para fins de desenvolvimento)
API_ACCESS = False

# Se for verdadeiro, executa os prompts por conjunto de variáveis
GROUPS_VARIABLES = False

# repetiç]oes dos experimentos
SENTENCES_REPETITIONS = 1

# O Modelo que será utilizado
MODEL = "gpt-4o-2024-08-06"
# MODEL = "gpt-4-1106-preview"
# MODEL = "gpt-3.5-turbo-1106"

# temperatura (grau de criatividade) do modelo
TEMPERATURE = 0.7

# Cabeçalho do arquivo de resultados
CABECALHOS = [
    [
        "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,cancelamento/alteracao_destino,atraso,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel",
        "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,violacao_furto_avaria,cancelamento/alteracao_destino,atraso,noshow,overbooking,assistencia_cia_aerea,hipervulneravel,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,intervalo_extravio_temporario,intervalo_atraso"
     ], # conjuntos artigo
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,cancelamento/alteracao_destino,atraso,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel", # original, artigo
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,cancelamento/alteracao_destino,atraso,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel", # original, extravio1
    ]
# Cabeçalho do arquivo de resultados
# CABECALHO = "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,cancelamento/alteracao_destino,atraso,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n"

INTERVALO_EXTRAVIO = "intervalo_extravio_temporario"
INTERVALO_ATRASO = "intervalo_atraso"

# Método de salvar os resultados feito pelo Thiago
# Com opções txt, json e csv (com informações)
OUTPUT_TYPES = ["csv", "txt"]


PATH_RAW_DOCUMENTS_FOLDERS = "data/sentencas"
PATH_PROMPTS = "data/prompts"
PATH_PROMPTS_GRUPOS = "data/prompts/grupos"
PATH_BASE_OUTPUT = "resultados_requisicao"
