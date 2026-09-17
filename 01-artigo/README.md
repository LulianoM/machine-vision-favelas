# 01-artigo

## Como esta pasta funciona

- `rascunhos-professor/` guarda os .docx do orientador, congelados. Nome: `AAAA-MM-DD_vN_Autor.docx`. Nunca editar.
- `manuscrito/` é a cópia de trabalho, um arquivo por seção. É aqui que se edita. O primeiro commit é o texto verbatim da v2, então `git log -p manuscrito/` mostra tudo que mudou em relação ao que o orientador escreveu.
- `PENDENCIAS.md` lista os problemas verificados do rascunho.
- Quando chegar uma v3 do orientador: salvar em `rascunhos-professor/`, rodar o script numa pasta temporária e comparar com `manuscrito/` antes de sobrescrever qualquer coisa.

```
python3 ferramentas/docx_para_secoes.py rascunhos-professor/AAAA-MM-DD_v3_Irigaray.docx /tmp/v3
diff -ru manuscrito /tmp/v3
```

## Seções da v2 (2026-09-10)

| Arquivo | Seção | Palavras |
|---|---|---|
| `01-introduction.md` | Título e introdução (sem título de seção no original) | 1.287 |
| `02-literature-review.md` | Literature Review | 1.005 |
| `03-methodology.md` | Methodology: Research Protocol, Data Collection, and Positionality | 416 |
| `04-situating-the-study.md` | Situating the Study: Violence, Policing, and Territorial Control in Rio de Janeiro | 1.145 |
| `05-case-jacarezinho.md` | Rio de Janeiro's Favelas and the Case of Jacarezinho | 387 |
| `06-results-proposed-model.md` | Results: A Proposed Machine Vision Model and Synthetic-Training Strategy | 289 |
| `07-conclusion.md` | Conclusion (Limitations, Delimitations, Future Research) | 1.115 |
| `08-references.md` | References | 660 |
| | Total | 6.304 |

Sem as referências: 5.644 palavras. A v1 de 2026-09-09 tinha cerca de 3.200.

## Versões recebidas

| Data | Arquivo | Observação |
|---|---|---|
| 2026-09-09 | `2026-09-09_v1_Irigaray.docx` | 42.767 bytes |
| 2026-09-10 | `2026-09-10_v2_Irigaray.docx` | 61.519 bytes. Vigente |
| 2026-09-17 | (não arquivado) | Download `Machine Vision from the Global South(2).docx`: MD5 idêntico ao da v2. Não é versão nova |
