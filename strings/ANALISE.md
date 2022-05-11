# O que assumimos
-  Nenhuma palavra é maior que o número máximo de caracteres que uma linha pode ter
-  quebra de paragrafos, isto é, linha vazia não deve ser tratada
-  mínimo duas palavras por linha
# Algumas soluções possíveis
-   Algoritmo guloso
    -   Simples de implementar e manter
    -   Como em quase todas os problemas de otimização (mochila por exemplo)
     tem a tendência de ser sub-ótimo
-   Programação dinâmica
    -   Implementação um pouco complexa
    -   Resultados melhores que o guloso
    -   Custo de espaço e tempo altos comparado programação dinâmica

## Referências:

1-http://litherum.blogspot.com/2015/07/knuth-plass-line-breaking-algorithm.html
2-https://www.geeksforgeeks.org/word-wrap-problem-dp-19/
3-https://en.wikipedia.org/wiki/Line_wrap_and_word_wrap
4-https://stackoverflow.com/questions/28642880/line-wrapping-algorithm-the-greedy-approach
5-https://stackoverflow.com/questions/17586/best-word-wrap-algorithm