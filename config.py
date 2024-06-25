# Variáveis para execução da aplicação

# Repetições de cada sentença
SENTENCE_REPETITIONS = 1

# Se vai repetir usando o parâmetro n ou não
REPEAT_N = False

# Tempo de espera, em segundos, entre cada requisição
TIME_BETWEEN_REQUESTS = 0

# Torna a aplicação mais verborrágica
VERBOSE = False

# Faz com que a aplicação acesse a API da OpenAI. Caso esteja desabilitado,
# utiliza uma mock response (para fins de desenvolvimento)
API_ACCESS = True

# Se for verdadeiro, executa os prompts por conjunto de variáveis
GROUPS_VARIABLES = False

# O Modelo que será utilizado
MODEL = "gpt-4-1106-preview"
# MODEL = "gpt-3.5-turbo-1106"

# temperatura (grau de criatividade) do modelo
TEMPERATURE = 0.7

# Cabeçalho do arquivo de resultados
CABECALHO = "sentença,direito_de_arrependimento,descumprimento_de_oferta,extravio_definitivo,extravio_temporário,intervalo_extravio_temporário,violação_furto_avaria,cancelamento/alteração_destino,atraso,intervalo_atraso,culpa_exclusiva_consumidor,condições_climáticas/fechamento_aeroporto,noshow,overbooking,assistência_cia_aérea,hipervulnerável\n"

INTERVALO_EXTRAVIO = "intervalo_extravio_temporário"
INTERVALO_ATRASO = "intervalo_atraso"

# Método de salvar os resultados feito pelo Thiago
# Com opções txt, json e csv (com informações)
ALTERNATIVE_SAVE = False
OUTPUT_TYPES = ["csv", "txt"]
