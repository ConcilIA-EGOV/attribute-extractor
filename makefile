all:
	@echo "make run para rodar o programa"
	@echo "make clean para limpar os arquivos de resultado gerados"
	@echo "make clean_prompts para limpar os arquivos de prompts"
	@echo "make clean_sentencas para limpar os arquivos de sentencas"

run:
	@python3 main.py

clean:
	@rm -rf resultados_requisicao

clean_prompts:
	@rm -rf data/prompts/*.txt
	@rm -rf data/prompts/grupos/*.txt

clean_sentencas:
	@rm -rf data/sentencas/*/*.txt
