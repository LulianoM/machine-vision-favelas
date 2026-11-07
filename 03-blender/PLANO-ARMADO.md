# Plano: tornar a distinção armado e desarmado mensurável

Aberto em 2026-09-20 [DESKTOP], por direção do autor, em resposta ao item 3 de
`docs/DIVERGENCIAS.md`. A decisão foi melhorar a distinção em vez de retirá-la do artigo.

## O diagnóstico, com número

O que o fuzil de 0,90 m ocupa, pela ótica do gerador (lente Z30 equivalente a 28,8 mm):

| Altura | Render | GSD | Fuzil | Pessoa em planta |
|---|---|---|---|---|
| 150 m | 4K | 4,88 cm/px | 18,4 x 1,0 px | 9,8 px |
| 150 m | 1080p | 9,76 cm/px | 9,2 x 0,5 px | 4,9 px |
| 100 m | 4K | 3,25 cm/px | 27,7 x 1,5 px | 14,8 px |
| 75 m | 4K | 2,44 cm/px | 36,9 x 2,0 px | 19,7 px |

**A arma é resolvível em comprimento e sub-pixel em largura.** O que chega ao sensor é uma
estrutura linear fina que quebra a silhueta da pessoa, não a forma do objeto. Portanto a tarefa
não é reconhecer uma arma: é decidir se uma linha escura de 18 px saindo de um blob de 10 px é
uma arma ou outra coisa.

Isso reformula o problema. O erro que importa não é deixar de detectar; é **chamar de arma o que
não é**, e hoje não temos nenhuma medida disso, porque no corpus não existe nada além de armas
que produza uma linha escura.

## O que falta na pipeline, em ordem de valor

### 1. Negativos difíceis (o mais importante, técnico e ético)

Pessoas desarmadas carregando objeto alongado, que é o que se vê numa favela: vassoura, rodo,
cano de PVC, vergalhão, tábua, guarda-chuva fechado, enxada, pedaço de mangueira, tapete
enrolado, remo, muleta.

Sem isso a rede aprende "linha escura igual a armada", e a taxa de falso positivo no mundo real
fica não medida. É exatamente o dano de uso dual que o artigo discute, e é a contribuição mais
forte que essa frente pode dar: **medir com que frequência um detector treinado em sintético
chama de arma uma vassoura.**

Implementação: classe própria `pessoa_objeto`, ou negativo explícito dentro de `pessoa_desarmada`.
Recomendo classe própria no gerador e fusão na avaliação, para poder medir os dois jeitos.

### 2. Variedade de arma

Hoje é sempre o mesmo modelo, na mesma pose, com o mesmo contraste, e é por isso que a distinção
é aprendível no sintético e não significa nada. Acrescentar de 5 a 6 modelos cobrindo a faixa
real: pistola (0,20 m), submetralhadora (0,50 m), fuzil de coronha retrátil (0,65 m), fuzil
(0,90 m), espingarda (1,05 m). Variar material e cor: polímero preto, coronha de madeira, metal
gasto, cano com fita.

### 3. Variedade de porte

A tiracolo nas costas, no ombro com cano para cima, no ombro com cano para baixo, baixo pronto
com as duas mãos, numa mão ao lado do corpo, encostada na parede ao lado da pessoa, pousada na
laje. Cada uma projeta uma assinatura diferente em nadir, e algumas não projetam nenhuma.

### 4. Varredura de GSD

Gerar o mesmo conjunto a 150, 100 e 75 m em 4K, e medir a separabilidade em cada um contra os
negativos difíceis. Produz uma curva de limiar de resolução: **a partir de que GSD a distinção
existe acima da linha de base dos negativos?**

Esse é o resultado publicável, e é o enquadramento eticamente correto: diz quando a capacidade é
real e quando é ilusão. Um artigo sobre uso dual que entrega o limiar a partir do qual a
capacidade deixa de existir é mais forte que um que entrega acurácia.

### 5. A métrica certa

Não reportar acurácia de classe. Reportar, em função da GSD:

- taxa de falso positivo sobre `pessoa_objeto` (vassoura chamada de arma)
- taxa de falso positivo sobre `pessoa_desarmada` sem objeto
- recall de `pessoa_armada`
- e a diferença entre a primeira e a segunda, que isola o quanto o objeto alongado engana

## O que isso muda no artigo

A Seção 11.5 hoje recusa reportar a distinção porque ela é artefato do gerador. Com negativos
difíceis e variedade, a recusa deixa de ser necessária e vira outra coisa: a Seção passa a
reportar **a curva de falso positivo sobre objeto confundível**, que é uma medida do risco, não
da capacidade. A recusa de reportar acurácia permanece; o que entra é o custo do erro.

## Ordem de execução

1. Modelos de arma e objetos confundíveis em `people_mpfb.py` (ou módulo novo `objetos.py`).
2. Poses de porte.
3. Geração do conjunto a 150 m, com as três classes balanceadas.
4. Treino e medição da matriz de confusão contra os negativos difíceis.
5. Repetir a 100 e 75 m, montar a curva de limiar.
