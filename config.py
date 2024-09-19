# Variáveis para execução da aplicação

# Repetições de cada sentenca
SENTENCE_REPETITIONS = 1

# Se vai repetir usando o parâmetro n ou não
REPEAT_N = False

# Tempo de espera, em segundos, entre cada requisição
TIME_BETWEEN_REQUESTS = 5

# Torna a aplicação mais verborrágica
VERBOSE = False

# Faz com que a aplicação acesse a API da OpenAI. Caso esteja desabilitado,
# utiliza uma mock response (para fins de desenvolvimento)
API_ACCESS = True

# Se for verdadeiro, executa os prompts por conjunto de variáveis
GROUPS_VARIABLES = False

# O Modelo que será utilizado
MODEL = "gpt-4o-2024-08-06"
# MODEL = "gpt-4-1106-preview"
# MODEL = "gpt-3.5-turbo-1106"

# temperatura (grau de criatividade) do modelo
TEMPERATURE = 0.7

# Cabeçalho do arquivo de resultados
CABECALHOS = [
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,cancelamento/alteracao_destino,atraso,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n", # original, artigo'
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,atraso,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n", # Atraso3 - sem cancelamento/alteracao_destino, usa -1 para intervalo_atraso
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,cancelamento/alteracao_destino,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n", # Atraso4 - sem atraso, usa 0 para intervalo_atraso
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n", # Atraso5 - sem atraso nem cancelamento/alteracao_destino
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,intervalo_extravio_temporario,violacao_furto_avaria,cancelamento/alteracao_destino,atraso,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n", # Extravio2 - sem extravio_temporario
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,cancelamento/alteracao_destino,atraso,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n", # original, main
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
PATH_BASE_OUTPUT = "data/resultados_requisicao"
PATH_LOG = "resultados_requisicao"
PATH_RESULTS = "resultados_requisicao"
