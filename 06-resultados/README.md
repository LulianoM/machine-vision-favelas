# 06-resultados

Tudo que o desktop produz e que o artigo pode citar. Só arquivo leve entra aqui; o pesado fica no desktop e é apontado por `ONDE-ESTAO-OS-DADOS.md`.

```
RESULTADOS.md               narrativa: comandos, hiperparâmetros, tabelas de métricas, o que deu errado
ONDE-ESTAO-OS-DADOS.md      caminho absoluto, tamanho e data de datasets, runs e pesos no desktop
<nome-do-run>/
  args.yaml                 hiperparâmetros exatos (saída do Ultralytics)
  results.csv               métricas por época
  *.png                     curvas, matriz de confusão
  previews/                 até 10 imagens com caixas desenhadas
```

Regra: número só entra no artigo se estiver aqui, com o comando que o gerou. Os três números centrais são o mAP no VisDrone em zero-shot, com 5 a 10% de dado real, e com sintético mais real.
