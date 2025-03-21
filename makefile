all:
	@echo "make run para rodar o programa"
	@echo "make clean para limpar os arquivos de resultado gerados"
	@echo "make clean_prompts para limpar os arquivos de prompts"
	@echo "make clean_sentencas para limpar os arquivos de sentencas"
	@echo "make env para ativar o ambiente virtual e instalar as dependências"
	@echo "make recycle para reciclar os logs de requisição"

run:
	@rm -rf resultados_requisicao*
	@python3 main.py

clean:
	@rm -rf resultados_requisicao*

clean_prompts:
	@rm -rf data/prompts/*.txt
	@rm -rf data/prompts/grupos/*.txt

clean_sentencas:
	@rm -rf data/sentencas/*/*.txt

env:
	@source bin/activate
	@pip install -r requirements.txt

recycle:
	python3 src/log_recycler.py
