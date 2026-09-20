# Rubrica de avaliação do texto técnico

Criada em 2026-09-20 [DESKTOP] para dirigir o loop de refinamento das seções técnicas
(`03b`, `06b`, `07b`, `08b`). Mesma lógica de `07-blender/RUBRICA-FIDELIDADE.md`: critério
declarado e testável, para separar "melhorou" de "parece ter melhorado".

Escopo: SÓ as seções técnicas. As seções do orientador (01, 02, 03, 04, 05, 06, 07, 08) e as de
segurança pública não são avaliadas aqui e não devem ser editadas.

## Os critérios

### 1. Rastreabilidade de número (peso 3, eliminatório)
Todo número no texto existe num arquivo sob `06-resultados/` ou é `[X]`. Nenhum número
estimado, arredondado de memória, herdado de outro braço sem dizer, ou inferido de expectativa.
**Teste:** extrair cada número do texto e localizar a fonte. Um número sem fonte reprova a seção.

### 2. Convenção dos premiados (peso 2)
As três convenções medidas na missão M39 sobre 8 papers premiados de 2026:
evidência sem modelo antes de qualquer estimação; robustez como seção numerada no corpo com
subseções, não apêndice; heterogeneidade com seção própria.
**Teste:** as três presentes e na ordem certa.

### 3. Condição de derrubada declarada (peso 2)
Cada subseção de robustez diz, antes da medição, o que precisaria aparecer para a afirmação
que ela protege cair. **Teste:** nenhuma subseção de 8 sem condição explícita.

### 4. Ausência de afirmação não sustentada (peso 3, eliminatório)
Nenhuma frase afirma desempenho, generalização ou capacidade que os dados não sustentam. Em
particular: nada sobre Jacarezinho que venha do benchmark, nada sobre acurácia de classe, nada
que prometa ferramenta operacional. **Teste:** listar toda afirmação de capacidade e checar a
evidência que a sustenta.

### 5. Autocrítica presente e específica (peso 2)
O texto reporta o que deu errado, não só o que deu certo: o piloto que falhou, a retratação do
gap de escala, o limite de 1080p da câmera real. **Teste:** as três presentes, com número.

### 6. Densidade metodológica (peso 2)
A trilha é presidida por um Senior Member da AAAI e não há discussants. Um leitor técnico
consegue reimplementar o pipeline a partir do texto? **Teste:** listar o que faltaria para
reimplementar.

### 7. Prosa (peso 1)
Inglês acadêmico, voz ativa onde couber, sem travessão (regra do projeto), sem adjetivo de
venda, sem "novel", "robust", "state-of-the-art" aplicados ao próprio trabalho.
**Teste:** buscar as palavras proibidas e frases de autoelogio.

### 8. Integração com o texto do orientador (peso 2)
As seções técnicas referenciam as seções dele pelos números certos, não contradizem o
enquadramento ético dele, e não reescrevem o que é dele. **Teste:** conferir cada referência
cruzada contra o arquivo citado.

## Pontuação

Média ponderada. Os critérios 1 e 4 são eliminatórios: falha em qualquer um dos dois zera a
rodada, independentemente do resto, porque os dois são sobre honestidade e não sobre qualidade.

Abaixo de 8,0 o texto não está pronto para o orientador ler.

## Histórico

Ver `HISTORICO-TEXTO.md`.
