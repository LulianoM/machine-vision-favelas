#!/usr/bin/env python3
"""
sitios.py: a coleção de sítios que o gerador pode construir, e os eixos em que eles diferem.

Por que isto existe. Até 2026-09-21 o gerador construía sempre o MESMO morro: mesma extensão de
núcleo, mesma altura de encosta, mesmo anel de mata, sem via principal. As 180 imagens do lote 4K
variam câmera, clima e pessoas, mas o lugar é um só. Kiefer, Ott e Zell (2022) geram as 40.000
imagens deles por travessias aleatórias do mapa inteiro, trocando de destino a cada 60 segundos, e
medem retorno decrescente para o tamanho do conjunto: mais imagem do mesmo lugar rende cada vez
menos. Ver `04-bibliografia/kiefer-2022-numeros-conferidos.md`.

O que este módulo NÃO afirma. Que variedade de sítio melhore a transferência é hipótese, não
resultado. O teste de dose em `07-blender/PLANO-EXPERIMENTAL.md`, frente B, existe para medir isso
com orçamento igual (4 sítios de 45 imagens contra 1 sítio de 180) antes de gastar o orçamento
grande. Se não mover nada no recorte pequeno, não move em escala.

Eixos de variação, e a razão de cada um:

  relevo      A favela do caso é de meia encosta, mas Jacarezinho em si é praticamente plano, e
              Rocinha é encosta inteira. A silhueta do alvo visto de cima muda com a inclinação
              do chão em que a pessoa está, então isto não é enfeite.
  via         Avenida cortando o núcleo. Traz asfalto, carro e um corredor largo sem laje. É o
              elemento de cena que mais aproxima o nosso domínio do VisDrone, que é tráfego.
  densidade   Fração de lote ocupado e tamanho do núcleo.
  altura      Média de pavimentos. Muda a oclusão em beco, que é o que derruba a visibilidade.
  mata        Anel em volta, manchas internas, ou ausente.

Uso:
  from sitios import sitio, N_SITIOS
  S = sitio(3)          # dicionário de parâmetros
  sitio(-1)             # o sítio histórico, idêntico ao que gerou ds_morro_4k
"""
import math
import random

# O sítio -1 reproduz exatamente o gerador de antes desta mudança. Serve de controle: qualquer
# lote gerado com --sitio -1 tem de sair igual ao ds_morro_4k para a mesma semente.
HISTORICO = dict(
    nome="historico",
    nuc_a=92.0, nuc_b=58.0, morro_h=62.0,
    relevo="morro", n_bairro=9, arvores=2600,
    pav_base=1.0, pav_amp=4.0, pav_max=6,
    vazio=0.008, mata="anel",
    avenida=None,
)

RELEVOS = ["morro", "plano", "dois_morros", "encosta"]
MATAS = ["anel", "manchas", "ausente"]
N_SITIOS = 40


def sitio(idx):
    """parâmetros do sítio de índice idx. Determinístico: o mesmo idx dá sempre o mesmo sítio."""
    if idx < 0:
        return dict(HISTORICO)

    r = random.Random(90000 + idx * 7919)

    relevo = RELEVOS[idx % len(RELEVOS)]          # varre em ordem, não sorteia: com 4 sítios no
    mata = MATAS[(idx // 4) % len(MATAS)]         # teste de dose, sorteio pode dar 4 iguais

    # O núcleo precisa continuar enchendo o quadro nadir a 150 m, que cobre 187 x 105 m. Deixar o
    # núcleo pequeno demais faz o quadro virar mata, e aí o lote não tem alvo nenhum.
    nuc_a = r.uniform(78.0, 108.0)
    nuc_b = r.uniform(50.0, 70.0)

    if relevo == "plano":
        morro_h = r.uniform(6.0, 16.0)
    elif relevo == "encosta":
        morro_h = r.uniform(55.0, 80.0)
    elif relevo == "dois_morros":
        morro_h = r.uniform(45.0, 68.0)
    else:
        morro_h = r.uniform(48.0, 72.0)

    # Avenida em pouco mais de um terço dos sítios. Nem toda favela tem via de porte; forçar em
    # todas criaria uma correlação falsa entre asfalto e favela que o detector aprenderia.
    avenida = None
    if r.random() < 0.38:
        avenida = dict(
            ang=r.uniform(0, math.pi),                 # orientação no plano
            larg=r.uniform(9.0, 16.0),                 # largura da caixa da via, em metros
            desloc=r.uniform(-0.35, 0.35),             # deslocamento do eixo em relação ao centro
            carros=r.randint(6, 22),
            calcada=r.uniform(1.6, 2.8),
        )

    if mata == "ausente":
        arvores = r.randint(120, 400)
    elif mata == "manchas":
        arvores = r.randint(900, 1800)
    else:
        arvores = r.randint(1900, 3000)

    return dict(
        nome=f"s{idx:02d}_{relevo}" + ("_av" if avenida else "") + f"_{mata}",
        nuc_a=round(nuc_a, 1), nuc_b=round(nuc_b, 1), morro_h=round(morro_h, 1),
        relevo=relevo, n_bairro=r.randint(6, 13), arvores=arvores,
        pav_base=round(r.uniform(0.6, 1.7), 2),
        pav_amp=round(r.uniform(2.6, 5.2), 2),
        pav_max=r.randint(4, 7),
        vazio=round(r.uniform(0.004, 0.035), 4),
        mata=mata,
        avenida=avenida,
    )


if __name__ == "__main__":
    print(f"{'idx':>4} {'nome':<26}{'nuc':>13}{'morro':>7}{'bairros':>9}"
          f"{'arv':>6}{'pav':>12}{'avenida':>9}")
    print("-" * 92)
    for i in list(range(-1, N_SITIOS)):
        s = sitio(i)
        av = f"{s['avenida']['larg']:.0f} m" if s["avenida"] else "nao"
        print(f"{i:>4} {s['nome']:<26}{s['nuc_a']:>6.0f}x{s['nuc_b']:<6.0f}{s['morro_h']:>7.0f}"
              f"{s['n_bairro']:>9}{s['arvores']:>6}"
              f"{s['pav_base']:>7.2f}+{s['pav_amp']:<4.1f}{av:>9}")
