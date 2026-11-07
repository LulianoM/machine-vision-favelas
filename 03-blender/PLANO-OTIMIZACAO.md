# Plano de otimização do gerador, para depois do render atual

Aberto em 2026-09-20 [DESKTOP]. **Não executar enquanto `ds_morro_4k` estiver rodando**: reiniciar
descarta as imagens já feitas e as duas coisas disputam a mesma GPU.

## O custo atual, medido

180 imagens a 3840x2160 com 96 amostras: **175 s por imagem**, cerca de 8,7 h no total. Medido no
log de `ds_morro_4k`, campo `render_s`, com dispersão de 163 a 189 s e um caso isolado de 361 s.

Máquina: RTX 2060 de 6 GB. Cena: cerca de 200 mil faces mais 2.600 instâncias de árvore.

## Suspeitas ordenadas, ainda NÃO medidas separadamente

Registro como suspeitas porque não rodei o A contra B. Medir antes de mexer é o ponto do
`teste_fidelidade.py`, e vale aqui também.

1. **Névoa volumétrica.** A caixa de ar vai de `GZ.min() - 12` até `GZ.max() + 190`, e todo raio
   de câmera atravessa esse meio com `volume_bounces = 1`. Volumétrico é o multiplicador clássico
   de custo no Cycles. Entrou depois da quinta validação, e o salto de tempo por imagem coincide.
2. **2.600 árvores com folha em alpha.** Cada folha é um cartão transparente, e cada raio que
   cruza copa paga vários saltos de transparência. A cena tem mata em toda a borda do quadro.
3. **4K.** Quatro vezes os pixels de 1080p. É inevitável: é ele que dá o alvo de 24,6 px em vez
   de 10,1 px, que foi o erro que invalidou o primeiro treino.
4. **VRAM.** Com 200 mil faces, 2.600 instâncias e as texturas do Poly Haven, 6 GB pode estar
   raspando. Se derramar para a CPU, o custo explode sem aviso no log.

## Correções a aplicar, em ordem de ganho por risco

### 1. `use_persistent_data` (ganho provavelmente alto, risco nulo)

```python
scene.render.use_persistent_data = True
```

A cena é construída UMA vez e só as pessoas mudam entre quadros. Sem isso o Cycles ressincroniza
os 200 mil faces e as 2.600 instâncias a cada imagem. Custa memória e é exatamente o caso de uso
para o qual a opção existe.

### 2. Encolher a caixa de ar (ganho médio, risco baixo)

Hoje `_vz1 = GZ.max() + 190`. A câmera está a 150 m acima do terreno do centro, então 190 m acima
do ponto MAIS ALTO do morro é folga grande. Baixar para `+ 40` acima da câmera reduz o caminho
óptico sem mudar o airlight que a câmera de fato atravessa. **Remedir o contraste depois**, porque
foi a densidade dessa névoa que trouxe o B/R da sombra para 0,98.

### 3. Podar árvore fora do quadro (ganho médio, risco baixo)

São 2.600 árvores num sítio de 250 x 205 m, mas o quadro nadir cobre 187 x 105 m. Árvore fora do
tronco de visão da câmera só custa. Duas saídas: manter a densidade só num raio útil, ou marcar
as distantes com `hide_render` por quadro em função do centro de câmera sorteado.

### 4. Amostras de 96 para 64 (ganho direto, risco de ruído)

Com denoise ligado, 64 costuma bastar em cena difusa. **Medir antes**: rodar `teste_fidelidade.py`
nas duas e comparar, porque ruído a mais numa caixa de 24 px pode virar falso negativo.

### 5. Paralelismo

Uma GPU só, então paralelizar render não ajuda. O que ajuda de verdade:

- **Separar render de treino.** Hoje os dois disputam a mesma placa. O treino pode rodar enquanto
  o próximo lote renderiza se o lote for menor que a VRAM livre, mas o mais seguro é enfileirar.
- **Fatiar o dataset em faixas de semente** e rodar em sequência com `--start`, de modo que uma
  interrupção não perca tudo. Hoje uma queda em 113 de 180 perde as 113.
- **Escrever manifesto e rótulo antes do render**, não depois. Se o processo cair, o que já foi
  anotado sobrevive.

### 6. Retomada

O gerador não tem `--start`. Acrescentar, junto com a checagem de arquivo já existente, para que
uma execução interrompida continue de onde parou em vez de recomeçar. É o item que mais dói hoje.

## Como validar que a otimização não estragou nada

Rodar `03-blender/scripts/teste_fidelidade.py` antes e depois sobre a mesma semente, e exigir que
nenhuma das dez métricas saia da faixa. A névoa e a contagem de amostras mexem diretamente em
contraste, meio-tom e B/R da sombra, que são três dessas métricas.
