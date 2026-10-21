# Rodada 5, grupo D: comparacoes D-i e D-ii do PLANO-RODADA5.md 3.6 (recall a conf 0,25, bootstrap de 2.000 quadros, semente 0). Rodar de dentro de 06-resultados.
import json,numpy as np
e=json.load(open('por_regime_s_soldur_4k.json',encoding='utf-8'))['por_regime']
g=json.load(open('por_regime_s_nadir_4k_r5.json',encoding='utf-8'))['por_regime']
arr=lambda pq: np.array([[q['acertos'],q['caixas']] for q in pq],float)
A=arr(e['sol_duro']['por_quadro']); B=arr(g['nublado']['por_quadro']); C=arr(g['sol_duro']['por_quadro'])
r=lambda x:x[:,0].sum()/x[:,1].sum()
rng=np.random.default_rng(0); dii=[]; di=[]
for _ in range(2000):
    ia=rng.integers(0,len(A),len(A)); ib=rng.integers(0,len(B),len(B))
    dii.append(r(A[ia])-r(B[ib])); di.append(r(A[ia])-r(C[ia]))
print('D-ii: especialista sob sol duro %.4f menos generalista sob nublado %.4f = %+.4f, IC95 %s'%(r(A),r(B),r(A)-r(B),np.percentile(dii,[2.5,97.5]).round(4)))
print('D-i : especialista menos generalista, mesmos quadros de sol duro: %.4f - %.4f = %+.4f, IC95 %s'%(r(A),r(C),r(A)-r(C),np.percentile(di,[2.5,97.5]).round(4)))
