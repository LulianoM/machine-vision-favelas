#Requires -RunAsAdministrator
<#
  Prepara o desktop Windows para ser acessado pelo MacBook via SSH, somente pela rede Tailscale.
  Rodar em PowerShell "como administrador", de dentro da pasta docs do repositório:

      Set-ExecutionPolicy -Scope Process Bypass -Force
      .\setup-desktop.ps1

  Pode ser rodado mais de uma vez. ATENCAO: escrito no Mac, ainda nao testado neste Windows.
  Leia a saida de cada etapa.
#>
param(
    [string]$ChavePublica = "$PSScriptRoot\chaves\macbook.pub"
)
$ErrorActionPreference = "Stop"

Write-Host "`n[1/5] OpenSSH Server" -ForegroundColor Cyan
$cap = Get-WindowsCapability -Online -Name "OpenSSH.Server*"
if ($cap.State -ne "Installed") {
    Add-WindowsCapability -Online -Name $cap.Name | Out-Null
    Write-Host "      instalado"
} else {
    Write-Host "      ja estava instalado"
}
Set-Service -Name sshd -StartupType Automatic
Start-Service sshd

Write-Host "[2/5] Shell padrao das sessoes SSH = PowerShell" -ForegroundColor Cyan
if (-not (Test-Path "HKLM:\SOFTWARE\OpenSSH")) { New-Item -Path "HKLM:\SOFTWARE\OpenSSH" | Out-Null }
New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell `
    -Value "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" `
    -PropertyType String -Force | Out-Null

Write-Host "[3/5] Firewall: porta 22 aceita somente a rede Tailscale (100.64.0.0/10)" -ForegroundColor Cyan
if (-not (Get-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -DisplayName "OpenSSH Server (sshd)" `
        -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 | Out-Null
}
Set-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -RemoteAddress "100.64.0.0/10"

Write-Host "[4/5] Chave publica do MacBook" -ForegroundColor Cyan
if (-not (Test-Path $ChavePublica)) { throw "Nao achei a chave publica em $ChavePublica" }
$chave = (Get-Content $ChavePublica -Raw).Trim()

function Add-Chave([string]$arquivo) {
    $pasta = Split-Path $arquivo
    if (-not (Test-Path $pasta)) { New-Item -ItemType Directory -Path $pasta | Out-Null }
    $jaTem = (Test-Path $arquivo) -and (Select-String -Path $arquivo -SimpleMatch $chave -Quiet)
    if (-not $jaTem) { Add-Content -Path $arquivo -Value $chave -Encoding ascii }
}
# Usuario do grupo Administradores: o sshd le este arquivo, com ACL restrita a Administradores e SYSTEM.
# SIDs em vez de nomes porque o Windows em portugues traduz o nome dos grupos.
$arqAdmin = "$env:ProgramData\ssh\administrators_authorized_keys"
Add-Chave $arqAdmin
icacls.exe $arqAdmin /inheritance:r /grant "*S-1-5-32-544:F" /grant "*S-1-5-18:F" | Out-Null
# Usuario comum: o sshd le este.
Add-Chave "$env:USERPROFILE\.ssh\authorized_keys"
Restart-Service sshd

Write-Host "[5/5] Energia: nunca suspender nem hibernar na tomada" -ForegroundColor Cyan
powercfg /change standby-timeout-ac 0
powercfg /change hibernate-timeout-ac 0

Write-Host "`nPronto. Anote para configurar o Mac:" -ForegroundColor Green
Write-Host ("  usuario Windows : " + $env:USERNAME)
Write-Host ("  nome da maquina : " + $env:COMPUTERNAME)
$ts = "$env:ProgramFiles\Tailscale\tailscale.exe"
if (Test-Path $ts) {
    Write-Host ("  IP Tailscale    : " + (& $ts ip -4))
} else {
    Write-Host "  Tailscale ainda nao instalado: winget install tailscale.tailscale" -ForegroundColor Yellow
}
