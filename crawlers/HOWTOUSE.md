
## Instalando

Crie um ambiente venv e inicie

```
$ python3 -m venv venv
$ source venv/bin/activate
```
O comando abaixo irá instalar todas as dependências necessárias e criará o banco de dados 
local
```
$ make install
```
Se você quiser contribuir para o projeto instale as dependências dev
```
$ make install-dev
```
Para usar o bot do telegram crie inicialmente um arquivo .env com o seu token de acesso
```
TELEGRAM_TOKEN=TOKEN_AQUI
```
Toda vez que você quiser ligar o bot, execute o comando abaixo
```
$ make bot-start
```
Para acessar o crawler na linha de comando execute o comando abaixo
```
$ python src/reddit/main.py "subreddit1;subreddit2;etc;"
```
### Configurando o crawler
Os parâmetros do crawler pode ser ajustados dentro do arquivo params.yaml.

## Desenvolvimento
Atualizar as dependências
```
$ make sync-env
```
Para obter a lista completa de comandos disponíveis execute o comando abaixo
```
$ make help
```