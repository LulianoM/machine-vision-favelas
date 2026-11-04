# O que falta modelar e gerar no servidor para fechar o artigo

Machine Vision from the Global South. Lista feita em 2026-11-04, a partir dos cinco itens `[[NEW]]` da versão curta para a AIM 2027 e dos dois pareceres frios de 3/11. Custos tirados dos tempos medidos na rodada 5 (`06-resultados/revisao-2026-10-17/custo-rodada5.md`): render de 2 a 3 minutos por quadro 4K, treino de classe única de 2,5 a 4 h, treino de três classes de 2,6 a 5,4 h, treino de R de 5,9 h, tudo na RTX 2060 do desktop, que faz render e treino um de cada vez.

## A lista

| # | O quê | Modelar ou gerar | Custo | Entra onde |
|---|---|---|---|---|
| 1 | Largura e altura das 5 malhas de arma | Só leitura: abrir o gerador no Blender e anotar a caixa envolvente de cada malha (comprimento, largura, altura em metros); dividir pelos três GSDs (4,88, 2,44 e 1,14 cm/px) | 1 h, sem GPU | 5.1, pegada da arma em pixels (hoje só o comprimento está derivado: 19, 38 e 81 px para 0,92 m; 4, 8 e 18 px para a pistola) |
| 2 | Fração sub-stride (lado menor abaixo de 8 px) de S-oblique e S-oblique-six | Script sobre os rótulos YOLO já existentes, sem render nem treino | 1 h, sem GPU | Tabela 5, duas linhas oblíquas |
| 3 | Ablação de ruído, borrão e JPEG | Re-treinar S-nadir-150 e S-oblique-six com essas degradações como aumento de dados no treino (sem renderizar de novo) e reavaliar zero-shot no VisDrone e no HERIDAL | 2 treinos, 6 a 8 h; com 3 sementes, 1 dia | 6.5, opcional; a frase atual fica se não rodar |
| 4 | Teto R com seleção fora do teste | 1 treino de R com a mesma receita, selecionando o checkpoint na fatia de seleção de 324 imagens em vez do val; recalcular todas as eficácias (razões a R) | 6 h | Responde à crítica mais repetida dos pareceres; hoje o texto só declara o problema |
| 5 | Forma em U da QP3 confundida pelo orçamento | S-nadir-35 e o gêmeo de 75 m treinados com 120 épocas e paciência 30, como o gêmeo de 150 m; matriz de confusão nos mesmos 80 quadros | 2 treinos, 1 dia; com 3 sementes, 2 a 3 dias | 5.4 e 6.1 |
| 6 | Atalho de comprimento testado de fato | Variante do gerador com os objetos confundíveis cortados nos comprimentos das armas (0,62 a 1,05 m); render de 200 quadros a 75 m e 200 a 150 m; 2 treinos de três classes; matriz de confusão | 1,5 a 2 dias | Torna falseável a regra "a forma se perde a 4,88 cm/px", que hoje é uma leitura, e o comprimento, que hoje é "alternativa não testada" |
| 7 | D-ii sem "nulo por regra" | Especialista de sol duro com 3 sementes e o espelho "tudo menos sol duro" (render de 180 quadros mais treino) | 1 a 1,5 dia | 5.5 e 6.3 |
| 8 | Arma na mão | Cinemática das mãos no rig do MakeHuman; re-render de todos os corpora de três classes (35, 75 e 150 m, gêmeos e quadros reservados, cerca de 1.000 quadros) e re-treino do Experimento C inteiro | Cerca de uma semana | Só para o periódico |
| 9 | Teto com a divisão de treino completa | 1 treino de R sobre as 6.471 imagens do VisDrone train (seis vezes o atual) | 1,5 dia | Opcional; o texto já declara R como teto do protocolo, não do VisDrone |

Não dá para fazer no servidor: os casos documentados de objeto cotidiano tomado por arma em operação no Rio (busca bibliográfica e jornalística, com fonte verificável ou a frase sai) e a validação da QP3 em imagem real (não há dado público, e coletar foi excluído por ética).

## Ordem sugerida

1. Até 19/11: itens 1 e 2 (duas horas, sem GPU). Se a máquina estiver livre, o item 4 (uma noite): é a crítica mais forte pelo menor custo. O item 3 fica para o periódico.
2. Depois da submissão, para a revista: itens 5 e 6 juntos (cerca de 4 dias de máquina), que atacam as duas fragilidades da QP3; depois o 7.
3. Itens 8 e 9 só se um revisor pedir.

## Regras que continuam valendo

- Nenhum número entra no texto sem estar em `06-resultados/RESULTADOS.md` com o comando que o gerou.
- O manuscrito não cita caminho, arquivo, script nem nome interno de corpus.
- Renders que derivam dos dados da PCERJ não saem do desktop; só o braço procedural pode ser ilustrado.
