# Versões do artigo

Cada versão entregue ao autor recebe um número. Os PDFs ficam na Área de Trabalho do desktop, em `Artigo Machine Vision Favelas/vN_AAAA-MM-DD_descricao/`, com nomes `MVF_vN_AAAA-MM-DD_<formato>.pdf`. A versão mais recente também fica solta na Área de Trabalho, com "(versao atual)" no nome. Para regerar uma versão: `git checkout <commit>` e rodar `01-artigo/ferramentas/monta_artigo.py`.

| Versão | Data | O que é | Commit do texto | Arquivos |
|---|---|---|---|---|
| v1 | 2026-09-30 | Versão refinada (análise geral, 17 páginas Elsevier) e resumo para leigo | f17f4f7 | elsevier, previa, resumo-leigo-PT |
| v2 | 2026-10-18 | Reestruturação pelo feedback do Revisor 1 (sete seções), sem coautor delegado, financiamento declarado | b45cc45 | elsevier, resumo-leigo-PT |
| v3 | 2026-10-22 | Resultados da rodada 5 (HERIDAL, sementes, cronogramas, curva, sol duro, 150 m, semente de cena) e tradução para o português | 29523f5 (EN), 3ba70fa (PT) | elsevier, elsevier-PT, PT.epub |
| v4 | 2026-10-26 | Revisão de alto impacto em administração: enquadramento em administração pública, corte para 11,3 mil palavras, apêndice online, QP3 corrigida | f3bb2cd | elsevier (19 p.), jmis (50 p.), jmis-folha-de-rosto, apendice-online (28 p.) |

| v5 | 2026-10-27 | A v3 restaurada e só corrigida (erros de fato, contradições, números fora da fonte, afirmações além da evidência, manchete da QP3), com as 13 figuras, 27 tabelas e o enquadramento originais; a v4 foi rejeitada pelo autor. Comparação em `01-artigo/revisao-2026-10-26/COMPARACAO-v3-v4-v5.md` | b02231e | elsevier (40 p.), jmis (119 p.), jmis-folha-de-rosto |

| v6 | 2026-10-27 | A v5 com as decisões do autor sobre as declarações: ética (sem comitê, por não haver participantes nem dados pessoais), conflito de interesse explícito (sem vínculo com polícia ou fornecedores), coautor delegado fora, declaração de IA e disponibilidade de dados como estavam; removidas a origem no projeto UFRJ de 2022, os agradecimentos e as menções às imagens do levantamento | 06b6387 | elsevier (40 p.), elsevier-PT, jmis (119 p.), jmis-folha-de-rosto |

| v7 | 2026-10-27 | A v6 com o resumo ampliado: parágrafo inicial com a visão da administração pública e da segurança pública sobre a dificuldade de treinar detectores aéreos para zonas urbanas complexas; palavras-chave public security e public administration | 40b2e1c | elsevier (40 p.), elsevier-PT (42 p.), jmis (119 p.), jmis-folha-de-rosto |

| v8 | 2026-10-27 | A v7 com duas subseções novas na seção 3 (3.3 a virada tecnológica na segurança pública; 3.4 a base ética do treino sintético; a antiga 3.3 vira 3.5), nove fontes da Public Administration Review conferidas no Crossref, citações em toda a seção 1 (de 10 para 40) e o resumo centrado na segurança pública | 9129ce3 | elsevier (41 p.), elsevier-PT (44 p.), jmis (124 p.), jmis-folha-de-rosto |

| v9 | 2026-11-02 | A v8 corrigida pela revisão simulada da AIM (`01-artigo/revisao-2026-11-02/PARECER-AIM.md`), sem perda de conteúdo: par do resumo alinhado (mesma condição nos dois benchmarks), objetivo restrito ao medido, lacuna de segurança pública fechada na 1.4, 2.4, 3.3, 6.4 e conclusão, declaração de uso dual, resultados fora dos Métodos, d′ unificado, seção 2 com os dois benchmarks, contradições da seção 3 corrigidas, seis referências de software e método e traduções dos títulos em português. Leitura final de ponta a ponta; no montador, legenda presa à tabela e tabelas largas quebrando entre páginas (sem páginas vazias). O PDF de submissão é o Elsevier em inglês, sem aviso de prévia | 2ab58b9 (texto), d4530f3 (leitura final), 683548f (vereditos finais) | elsevier-submissao (41 p.), elsevier-PT (44 p.) |

Próxima versão: v10.
