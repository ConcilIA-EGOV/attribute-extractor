# Variáveis para execução da aplicação

# Repetições de cada sentença
sentence_repetitions = 1

# Tempo de espera, em segundos, entre cada requisição
time_between_requests = 4

# Método de salvar os resultados feito pelo Thiago
# Com opções txt, json e csv (com informações)
alternative_save = False
output_types = ["csv", "txt"]

# Torna a aplicação mais verborrágica
verbose = False

# Faz com que a aplicação acesse a API da OpenAI. Caso esteja desabilitado,
# utiliza uma mock response (para fins de desenvolvimento)
api_access = True

# Se for verdadeiro, executa os prompts por conjunto de variáveis
groups_variables = False

# O Modelo que será utilizado
MODEL = "gpt-4-1106-preview"
# MODEL = "gpt-3.5-turbo-1106"

# temperatura (grau de criatividade) do modelo
TEMPERATURE = 0.7

# Cabeçalho do arquivo de resultados
CABECALHO = "Sentença,direito de arrependimento,descumprimento de oferta,extravio definitivo,extravio temporário,intervalo de extravio,violação,cancelamento (sem realocação)/alteração de destino,atraso de voo,intervalo de atraso,culpa exclusiva do consumidor,inoperabilidade do aeroporto,no show,overbooking,assistência da companhia aérea,hipervulnerabilidade\n"
