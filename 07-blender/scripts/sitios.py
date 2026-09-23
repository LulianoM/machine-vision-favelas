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
    nome="historico", paleta="referencia",
    nuc_a=92.0, nuc_b=58.0, morro_h=62.0,
    relevo="morro", n_bairro=9, arvores=2600,
    pav_base=1.0, pav_amp=4.0, pav_max=6,
    vazio=0.008, mata="anel",
    avenida=None,
)

RELEVOS = ["morro", "plano", "dois_morros", "encosta"]
MATAS = ["anel", "manchas", "ausente"]
# Paleta de cobertura e fachada. "referencia" é a do ds_morro_4k (pesos medidos na ortofoto);
# as outras deslocam os pesos entre laje crua, cerâmica e laje pintada, e giram o matiz das
# fachadas. Variedade de lugar sem isto era só traçado; a aparência era a mesma em todo sítio.
PALETAS = ["ceramica", "laje", "pintada", "referencia", "escura"]
# Corredor dos seis primeiros sítios, fixado para o teste de dose: avenida, rua estreita, rio,
# nenhum, avenida, rua. O sítio -1 (histórico) não tem corredor.
VIAS_FIXAS = ["avenida", "rua", "rio", None, "avenida", "rua"]
N_SITIOS = 40


def sitio(idx):
    """parâmetros do sítio de índice idx. Determinístico: o mesmo idx dá sempre o mesmo sítio."""
    if idx < 0:
        return dict(HISTORICO)

    r = random.Random(90000 + idx * 7919)

    relevo = RELEVOS[idx % len(RELEVOS)]          # varre em ordem, não sorteia: com 4 sítios no
    mata = MATAS[idx % len(MATAS)]                # teste de dose, sorteio pode dar 4 iguais.
    # Mata varre a cada sítio (era a cada 4): na prévia de 22/09, 5 dos 6 sítios saíram com anel
    # e 40 a 50% do quadro era árvore, a mesma árvore. 4 e 3 são primos entre si, então relevo
    # e mata só se repetem juntos a cada 12 sítios.
    paleta = PALETAS[idx % len(PALETAS)]

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

    # Corredor cortando o núcleo: avenida larga com faixa e carros, rua estreita sem faixa, ou
    # rio (água, margem de barro, sem carro). Nem toda favela tem via de porte; forçar em todas
    # criaria uma correlação falsa entre asfalto e favela que o detector aprenderia. Nos seis
    # primeiros sítios o tipo é fixado à mão para o teste de dose ter um de cada; daí em diante
    # sorteia. O sorteio consome o mesmo número de chamadas em todos os ramos, para os sítios já
    # vistos não mudarem de núcleo ou de bairro quando o tipo muda.
    u_tipo = r.random()
    if idx < len(VIAS_FIXAS):
        tipo = VIAS_FIXAS[idx]
    else:
        tipo = ("avenida" if u_tipo < 0.22 else "rua" if u_tipo < 0.42
                else "rio" if u_tipo < 0.52 else None)
    avenida = None
    if tipo is not None:
        ang = r.uniform(0, math.pi)                    # orientação no plano
        u_larg = r.uniform(0, 1)
        desloc = r.uniform(-0.35, 0.35)                # deslocamento do eixo em relação ao centro
        u_car = r.randint(6, 22)
        u_cal = r.uniform(0, 1)
        if tipo == "avenida":
            avenida = dict(tipo=tipo, ang=ang, larg=9.0 + 7.0 * u_larg, desloc=desloc,
                           carros=u_car, calcada=1.6 + 1.2 * u_cal)
        elif tipo == "rua":
            avenida = dict(tipo=tipo, ang=ang, larg=4.5 + 2.5 * u_larg, desloc=desloc,
                           carros=max(1, u_car // 4), calcada=0.8 + 0.6 * u_cal)
        else:                                          # rio: a "calçada" é a margem de barro
            avenida = dict(tipo=tipo, ang=ang, larg=6.0 + 10.0 * u_larg, desloc=desloc,
                           carros=0, calcada=2.5 + 3.0 * u_cal)

    if mata == "ausente":
        arvores = r.randint(120, 400)
    elif mata == "manchas":
        arvores = r.randint(900, 1800)
    else:
        arvores = r.randint(1900, 3000)

    return dict(
        nome=f"s{idx:02d}_{relevo}" + (f"_{avenida['tipo']}" if avenida else "") + f"_{mata}_{paleta}",
        paleta=paleta,
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
