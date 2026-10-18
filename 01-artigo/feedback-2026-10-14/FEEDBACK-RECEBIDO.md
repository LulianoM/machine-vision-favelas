# Feedback recebido em 14/10/2026 sobre o artigo de 30/09

Material entregue pelo autor em 17/10/2026 na pasta `FEEDBACKS ARTIGOS`: `feedback.txt` (cópia literal em `feedback-original.txt`), quatro áudios de WhatsApp de 14/10 (transcritos localmente com whisper large-v3-turbo; os `.txt` ao lado trazem a transcrição bruta com tempos), o PDF revisado (`machine-vision-favelas-elsevier-2026-09-30-1.pdf`, o mesmo de 30/09) e o livro de Zobel, *Writing for Computer Science*, 3ª ed., indicado como referência de forma (resumo de regras em `zobel-checklist.md`).

Revisor: identificado nas mensagens de WhatsApp como Felipe I. Toledo (escreve em português com traços de espanhol). O plano de correção está em `PLANO-CORRECAO.md`.

## 1. O que o `feedback.txt` contém

1. **"Final structure"**: uma estrutura-alvo de sete seções (Introduction; Related Work; Study Context; Materials and Methods; Results; Discussion; Conclusion), com subseções e, entre colchetes, a seção do artigo de 30/09 de onde cada parte vem. Define três perguntas de pesquisa (RQ1 transferência do sintético e seus determinantes; RQ2 valor do sintético quando há pouco dado real; RQ3 GSD em que armado e desarmado se separam e com que taxa de falso alarme) e quatro experimentos (A zero-shot; B ajuste fino e treino conjunto; C armado e desarmado por altitude; D regimes de luz).
2. **Parecer metodológico** em três blocos: (1) metodologia e validade das conclusões, 5 pontos; (2) rigor estatístico e desenho experimental, 8 pontos; (3) contexto, ética e transparência, 4 pontos. Fecha recomendando priorizar o que afeta a validade, separar o demonstrado do hipotético e do que ainda exige validação, e reorganizar o artigo numa progressão problema, objetivos, método, resultados, conclusões.
3. **Esqueleto de seis seções em português** (Introdução; Trabalhos Relacionados; Metodologia; Resultados Experimentais e Discussão; Limitações e Considerações Éticas; Conclusões e Trabalhos Futuros).
4. **Mensagens de WhatsApp de 14/10, 23h50**: "ajeita tudo baixo isso"; "sinto que você explica os métodos nos resultados e tira conclusões"; "vamos por parte, vai corrigindo isso que mandei em relação à forma, leitura e estrutura da sua ideia e depois manda de novo para revisar melhor".

## 2. Os quatro áudios (transcrição limpa)

**10h09 (28 s).** Está na metade do artigo; manda até sexta-feira porque quis revisar direito. Há coisas de metodologia que se pode melhorar; o resto está certo; há coisas pequenas de bibliografia.

**10h10 (38 s).** O problema do texto gerado com ajuda de IA é a redundância: explica a mesma coisa muitas vezes, repete no mesmo texto o que já foi dito (a sigla, por exemplo, é reexplicada), e os conectores precisam variar.

**10h15 (41 s).** Antes de aplicar a tarefa de classificação (reconhecimento), seria bom propor um método de redução de ordem, "tipo uma matriz de co-similaridade ou algum artifício matemático", que permita refinar o critério de classificação; senão o resultado fica muito sensível.

**10h34 (62 s).** A classificação é uma tarefa difícil; um pré-algoritmo de similaridade evitaria os erros. Na comparação entre modelos (as tabelas do fim), os erros são quase todos iguais: para ele tem de haver uma melhora substancial entre modelos, no mínimo 30 a 40%; senão o artigo prova a mesma hipótese, de que o método "meio que serve, mas está cheio de erros" fora do escopo da base de dados. Vai mandar um retorno escrito depois de revisar bem.

## 3. Leitura consolidada (o que o revisor pede, em ordem de prioridade)

1. **Forma e estrutura primeiro** (pedido explícito por WhatsApp): reorganizar nas seções-alvo; método só na seção de método; resultado só na de resultados; interpretação e conclusão só na discussão e na conclusão; limitações num lugar só; menos repetição, siglas definidas uma vez, conectores variados.
2. **Alinhar perguntas, objetivo e variáveis medidas**, dizendo com todas as letras que a distinção armado e desarmado foi estudada só em imagem sintética, e separar o que foi demonstrado do que é hipótese e do que falta validar.
3. **Rigor de relato**: validação (seleção de modelo) separada de teste independente; GSD além de altitude e justificativa da câmera (zoom); limitações do realismo do sensor; intervalos de confiança e repetições; confirmatório contra exploratório; comparabilidade das referências (imagens e instâncias, seleção de checkpoint); pistas visuais alheias à arma; dependência da configuração do ajuste fino; curvas precisão-recall ou limiares justificados; diversidade das figuras humanas e curva de aprendizado; conclusões sobre luz restritas ao que foi medido.
4. **Contexto, ética e transparência**: explicar a "contextualização informada por campo" e seu estatuto; declarações explícitas de ética, uso dual e conflito de interesse; justificar ou retirar "design science"; reprodutibilidade (publicar o que puder ser publicado, documentar o que não pode ser regenerado).
5. **Sugestões do áudio**: um pré-processamento por similaridade (redução de ordem) antes da classificação; e não tratar diferenças pequenas entre modelos como resultado.
