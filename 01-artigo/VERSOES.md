# Versões do artigo

Cada versão entregue ao autor recebe um número. Os PDFs ficam na Área de Trabalho do desktop, em `Artigo Machine Vision Favelas/vN_AAAA-MM-DD_descricao/`, com nomes `MVF_vN_AAAA-MM-DD_<formato>.pdf`. A versão mais recente também fica solta na Área de Trabalho, com "(versao atual)" no nome. Para regerar uma versão: `git checkout <commit>` e rodar `01-artigo/ferramentas/monta_artigo.py`.

| Versão | Data | O que é | Commit do texto | Arquivos |
|---|---|---|---|---|
| v1 | 2026-09-30 | Versão refinada (análise geral, 17 páginas Elsevier) e resumo para leigo | f17f4f7 | elsevier, previa, resumo-leigo-PT |
| v2 | 2026-10-18 | Reestruturação pelo feedback do Revisor 1 (sete seções), sem coautor delegado, financiamento declarado | b45cc45 | elsevier, resumo-leigo-PT |
| v3 | 2026-10-22 | Resultados da rodada 5 (HERIDAL, sementes, cronogramas, curva, sol duro, 150 m, semente de cena) e tradução para o português | 29523f5 (EN), 3ba70fa (PT) | elsevier, elsevier-PT, PT.epub |
| v4 | 2026-10-26 | Revisão de alto impacto em administração: enquadramento em administração pública, corte para 11,3 mil palavras, apêndice online, QP3 corrigida | f3bb2cd | elsevier (19 p.), jmis (50 p.), jmis-folha-de-rosto, apendice-online (28 p.) |

| v5 | 2026-10-27 | A v3 restaurada e só corrigida (erros de fato, contradições, números fora da fonte, afirmações além da evidência, manchete da QP3), com as 13 figuras, 27 tabelas e o enquadramento originais; a v4 foi rejeitada pelo autor. Comparação em `01-artigo/revisao-2026-10-26/COMPARACAO-v3-v4-v5.md` | b02231e | elsevier (40 p.), jmis (119 p.), jmis-folha-de-rosto |

Próxima versão: v6.
