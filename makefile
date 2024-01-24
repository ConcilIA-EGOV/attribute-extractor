all:
	@echo "make run para rodar o programa"
	@echo "make clean para limpar os arquivos gerados"

run:
	@python3 main.py

clean:
	rm -rf resultados
	rm -rf data/log/*
