# Ambiente do desktop

Levantado em 2026-09-17 [DESKTOP] com `nvidia-smi`, `Get-CimInstance` e `python -c "import torch, ultralytics"`.

## Máquina

| Item | Valor |
|---|---|
| Sistema | Microsoft Windows 10 Pro, versão 10.0.19045 |
| Processador | AMD Ryzen 5 5600X (6 núcleos, 12 threads) |
| Memória | 32 GB (31,9 GB utilizáveis). É o recurso escasso: Blender, ODM e DataLoader juntos estouram |
| GPU | NVIDIA GeForce RTX 2060, 6 GB, modo WDDM |
| Driver NVIDIA | 610.62 (CUDA do driver: 13.3) |
| Disco C: | 609 GB usados, 321 GB livres (em 2026-09-17) |
| Usuário Windows | `marti` |

## Python e treino

| Item | Valor |
|---|---|
| Ambiente virtual de treino | `C:\arma3-favela\venv` (4,7 GB), criado com `python -m venv` |
| Python base | 3.11.15, instalado pelo `uv` em `C:\Users\marti\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none` |
| PyTorch | 2.14.0+cu126 (CUDA 12.6), `torch.cuda.is_available()` = True |
| torchvision | 0.29.0+cu126 |
| Ultralytics | 8.4.148 |
| Outros usados pelos scripts | rasterio, numpy, opencv (cv2), gdown |
| Ambiente do servidor MCP do Blender | `C:\arma3-favela\mcp-venv` (blender-mcp 1.9.1, mcp 1.30.0) |

Atenção: o `pyvenv.cfg` aponta para o Python do `uv`. Se o `uv` atualizar ou remover esse Python, o venv quebra. Recriar é barato: `requirements` em `02-projeto-ufrj-2022/arma3-2022/scripts/requirements.txt` mais `rasterio`.

## Programas

| Programa | Versão | Caminho |
|---|---|---|
| Blender | 5.2.1 LTS (Steam) | `C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe` |
| Extensão MPFB (MakeHuman) | 2.0.17 | `%APPDATA%\Blender Foundation\Blender\5.2\extensions\user_default\mpfb` |
| Addon blender-mcp | arquivo de 2026-09-11 | `%APPDATA%\Blender Foundation\Blender\5.2\scripts\addons\blender_mcp.py` |
| OpenDroneMap | 3.6.2 nativo Windows | `C:\ODM\run.bat` (atalho: `03-blender/scripts/run_odm.cmd`) |
| ARMA 3 | Steam | `C:\Program Files (x86)\Steam\steamapps\common\Arma 3\` |
| Missão do ARMA 3 | | `C:\Users\marti\Documents\Arma 3\missions\dsFavela.Tanoa\` |
| Git | 2.54.0.windows.1 | `C:\Users\marti\AppData\Local\hermes\git\cmd\git.exe` |
| GitHub CLI | 2.101.0 (instalado em 2026-09-17 pelo winget) | `C:\Program Files\GitHub CLI\gh.exe`, autenticado como LulianoM |

## Pastas

| Pasta | Papel |
|---|---|
| `C:\projetos\machine-vision-favelas` | Clone do repositório, base de trabalho a partir de 2026-09-18 |
| `C:\arma3-favela` | Pasta antiga, 44 GB, arquivo morto intacto. Continua sendo onde moram datasets, pesos, ODM, assets e venv |
| `C:\Users\marti\Documents\SecondBrain - Glados` | Cofre do Obsidian. Nota do projeto em `Projetos\Arma3-Favela-Dataset\README.md` |
| `%USERPROFILE%\.claude\projects\` | Memória local do Claude Code. Não é canal entre máquinas |

## Armadilhas desta máquina (custaram horas, já resolvidas)

- MPFB entrega cada peça com modificador de subdivisão. Com 200 pessoas um render foi de 20 s para 23 min. Removido em `people_mpfb.build_pool`.
- Textura de fotogrametria já tem sol e sombra no pixel. Iluminar com ambiente neutro; céu físico só por raio de câmera (nó Light Path).
- `sky.sun_rotation` do Blender é azimute de bússola (0 = +Y norte, 90 = +X leste), verificado empiricamente. Lâmpada: `rotation_euler = (radians(90-elev), 0, radians(180-azimute))`.
- Blender 5: `matrix_world` fica desatualizada depois de mover objeto; chamar `view_layer.update()` antes de ler `bound_box`. Vídeo só depois de `image_settings.media_type = 'VIDEO'`. `action.fcurves` virou layers, strips e channelbags.
- O `train_yolo.py` original trava no Windows (treino no nível do módulo, DataLoader reimporta). Usar a versão com `if __name__ == "__main__"`.
- ODM: rodar por `run_odm.cmd`. `--rerun-from odm_meshing --mesh-size 1500000 --mesh-octree-depth 11` remalha em cerca de 25 min, mas só com a máquina livre; disputando RAM ele para de consumir CPU e nunca termina.
- ARMA 3 não expõe controles para automação: só cliques em primeiro plano (SendInput) chegam ao jogo, e ler a tela exigiu OCR do Windows (`02-projeto-ufrj-2022/arma3-2022/scripts/windows/ocr.ps1`).
