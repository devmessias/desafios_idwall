
# Analise de Requisitos

## Primeiro requisito
>Sua missão é encontrar e listar as *threads* que estão bombando no Reddit naquele momento!
Consideramos como bombando *threads* com 5000 pontos ou mais.

-   Só será considerado threads com 5000 pontos ou mais.

### Pontos de ambiguidade
- O que seria **naquele momento**?
   - Como isso não foi bem especificado seria interessante manter isso como um parâmetro ajustável 
talvez dentro de um YAML

## Segundo requisito
>- Lista com nomes de subreddits separados por ponto-e-vírgula (`;`). Ex: "askreddit;worldnews;cats"

- Inputs serão serparados por ponto-e-vírgula
  - Todo input será correto ou devemos tratar erros?
  - Não existe um limite de subreddits a ser analisado, se o usuário mandar milhares?
    - Bem problemático.
    - Olhar no robots.txt do old.reddit.com para ver se existe alguma regra para isso.
    - Como tratar a paginação?
    - Quebrar em multiprocessos
      - Obviamente a captura de cada subreddit não depende das outras.
      - Se um processo falhar isso não deveria afetar os outros ou invalidar os trabalhos já executados
      - Se uma captura de um subreddit já foi feita X segundos atrás, não deveria ser necessário fazer novamente.
    - usar um sistema de filas e multiprocessos?
      - Suponha que temos 1k de subreddits, quebramos em batches de 10 (a depender do número de cores e políticas do reddit) e processamos cada batch e agurdamos Y segundos para executar o próximo batch.
## Terceiro requisito
>Essa parte pode ser um CLI simples, desde que a formatação da impressão fique legível.

-  Seria uma boa usar o rich para isso

## Quarto requisito
>Construir um robô que nos envie essa lista via Telegram sempre que receber o comando `/NadaPraFazer [+ Lista de subrredits]` (ex.: `/NadaPraFazer programming;dogs;brazil`)

- O robô deveria ser capaz de invocar o crawler que só deveria realizar a captura se dados os requisitos de cache não estiverem ok.
- O robô não deveria ser acoplado ao crawler, por exemplo, eles poderiam estar inclusive máquinas diferentes, mas compartilhando o mesmo banco de dados seja esse banco qual for.
- Alguma maneira de monitorar se o robô está "vivo" (CRON?), ligar se o robô estiver offline, etc.