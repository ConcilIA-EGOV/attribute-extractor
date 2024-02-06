# Variáveis para execução da aplicação

# Repetições de cada sentença
SENTENCE_REPETITIONS = 1

# Tempo de espera, em segundos, entre cada requisição
TIME_BETWEEN_REQUESTS = 0

# Método de salvar os resultados feito pelo Thiago
# Com opções txt, json e csv (com informações)
ALTERNATIVE_SAVE = False
OUTPUT_TYPES = ["csv", "txt"]

# Torna a aplicação mais verborrágica
VERBOSE = False

# Faz com que a aplicação acesse a API da OpenAI. Caso esteja desabilitado,
# utiliza uma mock response (para fins de desenvolvimento)
API_ACCESS = True

# Se for verdadeiro, executa os prompts por conjunto de variáveis
GROUPS_VARIABLES = False

# O Modelo que será utilizado
# MODEL = "gpt-4-1106-preview"
MODEL = "gpt-3.5-turbo-1106"

# temperatura (grau de criatividade) do modelo
TEMPERATURE = 0.7

# Cabeçalho do arquivo de resultados
CABECALHO = "Sentença,direito de arrependimento,descumprimento de oferta,extravio definitivo,extravio temporário,intervalo de extravio,violação,cancelamento (sem realocação)/alteração de destino,atraso de voo,intervalo de atraso,culpa exclusiva do consumidor,inoperabilidade do aeroporto,no show,overbooking,assistência da companhia aérea,hipervulnerabilidade\n"
