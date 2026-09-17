# Setup do desktop (Windows) como máquina central

Tempo estimado: 30 a 40 minutos, uma vez só. Tudo abaixo roda no DESKTOP, exceto onde diz [MAC].

## 0. Pré-requisitos

```powershell
winget install Git.Git
winget install GitHub.cli
winget install tailscale.tailscale
```

Claude Code já está instalado no desktop. Se não estiver: `irm https://claude.ai/install.ps1 | iex`.

## 1. Rede privada entre as duas máquinas (Tailscale)

1. Abrir o Tailscale no desktop e entrar com a conta Google pessoal.
2. [MAC] `brew install --cask tailscale` (ou App Store), abrir e entrar com a MESMA conta.
3. No painel https://login.tailscale.com/admin/machines: renomear a máquina Windows para `desktop` e, no menu dela, marcar "Disable key expiry" (senão o desktop sai da rede depois de 180 dias).
4. [MAC] Testar: `ping desktop`.

Por que Tailscale: funciona atrás de CGNAT (o normal em internet residencial no Brasil, onde abrir porta no roteador não resolve), não expõe nada à internet pública, não precisa de domínio e é gratuito para uso pessoal.

## 2. Clonar o repositório

```powershell
gh auth login
mkdir C:\projetos
gh repo clone LulianoM/machine-vision-favelas C:\projetos\machine-vision-favelas
```

## 3. SSH no desktop, acessível só pelo Tailscale

PowerShell como administrador:

```powershell
cd C:\projetos\machine-vision-favelas\docs
Set-ExecutionPolicy -Scope Process Bypass -Force
.\setup-desktop.ps1
```

O script instala o OpenSSH Server, restringe a porta 22 à faixa do Tailscale, autoriza a chave pública do MacBook (`docs/chaves/macbook.pub`) e desliga suspensão e hibernação. No fim imprime o usuário Windows, o nome da máquina e o IP Tailscale. Ele foi escrito no Mac e ainda não foi testado neste Windows: ler a saída.

[MAC] Acrescentar em `~/.ssh/config`, trocando o usuário:

```
Host desktop
  HostName desktop
  User USUARIO_WINDOWS
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
```

[MAC] Testar: `ssh desktop nvidia-smi`. Se responder com a tabela da GPU, o Claude do Mac passa a conseguir consultar o desktop sozinho (estado do treino, logs, métricas) e copiar arquivos grandes com `scp` ou `rsync`, sem passar pelo GitHub.

## 4. Migrar o trabalho que já existe no desktop para dentro do repositório

Abrir o Claude Code na pasta ANTIGA de trabalho (a do pacote de 11/09) e colar o conteúdo de `docs/PROMPT-MIGRACAO-DESKTOP.md`. Depois disso, trabalhar sempre a partir de `C:\projetos\machine-vision-favelas`.

## 5. Tela do desktop a partir do Mac (o ARMA 3 precisa de interface gráfica)

SSH não mostra janela. Para operar o editor Eden, o jogo, Blender ou Unreal a partir do MacBook:

- Opção simples: Parsec (https://parsec.app), gratuito para uso pessoal. Instalar no desktop como host e no Mac como cliente, mesma conta. Feito para jogo, latência baixa, atravessa NAT sozinho.
- Opção aberta: Sunshine no desktop (https://app.lizardbyte.dev) e Moonlight no Mac, conectando pelo nome `desktop` do Tailscale. Usa o encoder da GPU NVIDIA.
- Evitar a Área de Trabalho Remota da Microsoft para isso: o servidor só existe no Windows Pro e o desempenho com jogo é ruim.

Em qualquer das opções, o Windows precisa estar com sessão iniciada e com um monitor ligado ou um plugue HDMI fantasma.

## 6. Opcional: dirigir o Claude do desktop pelo navegador ou pelo celular

Na pasta do repositório: duplo clique em `docs\iniciar-claude-remoto.cmd`. A sessão aparece em https://claude.ai/code e no app do Claude (aba Code). Roda no desktop com acesso à GPU e aos arquivos locais; o navegador é só a janela. A janela do terminal precisa ficar aberta. Para subir sozinho ao ligar: `Win+R`, `shell:startup`, colar ali um atalho para o `.cmd`.

É opcional. Com o item 3 funcionando, `ssh desktop` e rodar `claude` dentro da sessão cumpre o mesmo papel, com a ressalva de que o primeiro login do Claude deve ser feito localmente no desktop (o login abre navegador).

## 7. Para o desktop ficar de fato sempre disponível

- BIOS: "Restore on AC Power Loss" em "Power On", para religar sozinho depois de queda de luz.
- Windows Update: definir horário ativo amplo e aceitar que reinícios vão acontecer. Tailscale e sshd são serviços e voltam sozinhos antes do login. Parsec, Sunshine e o Claude remoto só voltam depois do login; quem quiser resiliência total configura login automático (Sysinternals Autologon), sabendo que isso reduz a segurança física da máquina.

## Conferência final, do Mac

```bash
ping -c 2 desktop
ssh desktop "nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv"
ssh desktop "cd C:\projetos\machine-vision-favelas; git log --oneline -3"
```
