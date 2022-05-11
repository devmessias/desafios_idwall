
## Executando

```
$ python src/main.py  -c 40 -i "input.txt" -o "output.txt" --justify
```

para ajuda 
```
$ python src/main.py -h
```

## Instalando (dev)

No momento não temos nenhuma dependência externa para executar o projeto, então não precisamos instalar nenhuma biblioteca com exceção se formos para desenvolvermos o projeto

Crie um ambiente venv e inicie

```
$ python3 -m venv venv
$ source venv/bin/activate
```

Se você quiser contribuir para o projeto instale as dependências dev
```
$ make install-dev
```

Atualizar as dependências
```
$ make sync-env
```
Para obter a lista completa de comandos disponíveis execute o comando abaixo
```
$ make help
```