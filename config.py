# Variáveis para execução da aplicação

# Repetições de cada sentenca
SENTENCE_REPETITIONS = 1

# Se vai repetir usando o parâmetro n ou não
REPEAT_N = False

# Tempo de espera, em segundos, entre cada requisição
TIME_BETWEEN_REQUESTS = 0

# Torna a aplicação mais verborrágica
VERBOSE = False

# Faz com que a aplicação acesse a API da OpenAI. Caso esteja desabilitado,
# utiliza uma mock response (para fins de desenvolvimento)
API_ACCESS = False

# Se for verdadeiro, executa os prompts por conjunto de variáveis
GROUPS_VARIABLES = False

# O Modelo que será utilizado
MODEL = "gpt-4-1106-preview"
# MODEL = "gpt-3.5-turbo-1106"

# temperatura (grau de criatividade) do modelo
TEMPERATURE = 0.7

# Cabeçalho do arquivo de resultados
CABECALHOS = [
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,cancelamento/alteracao_destino,atraso,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n", # original, refinada para atraso
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,atraso,intervalo_atraso_ou_cancelamento,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n", # sem cancelamento/alteracao_destino
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,atraso,intervalo_atraso_ou_cancelamento,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n", # sem cancelamento/alteracao_destino, usa -1 para intervalo_atraso
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,atraso,intervalo_atraso_ou_cancelamento,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n", # sem cancelamento/alteracao_destino, usa 0 para intervalo_atraso
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,intervalo_atraso_ou_cancelamento,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n", # sem atraso nem cancelamento/alteracao_destino
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,cancelamento/alteracao_destino,atraso,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n", # original, refinada para extravio
    "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,intervalo_extravio,violacao_furto_avaria,cancelamento/alteracao_destino,atraso,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n", # sem extravio_temporario
    ]
# Cabeçalho do arquivo de resultados
# CABECALHO = "sentenca,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporario,intervalo_extravio_temporario,violacao_furto_avaria,cancelamento/alteracao_destino,atraso,intervalo_atraso,culpa_exclusiva_consumidor,condicoes_climaticas/fechamento_aeroporto,noshow,overbooking,assistencia_cia_aerea,hipervulneravel\n"

INTERVALO_EXTRAVIO = "intervalo_extravio_temporario"
INTERVALO_ATRASO = "intervalo_atraso"

# Método de salvar os resultados feito pelo Thiago
# Com opções txt, json e csv (com informações)
ALTERNATIVE_SAVE = False
OUTPUT_TYPES = ["csv", "txt"]
