#requires -Version 5.1
<#
.SYNOPSIS
    Diagnostica worktrees Git e, opcionalmente, remove um worktree temporario.

.DESCRIPTION
    Por padrao e somente leitura: lista worktrees, status e commits exclusivos.
    Nada e removido sem -Executar. A remocao forcada exige -Forcar.

.EXAMPLE
    .\scripts\limpar_worktrees.ps1

.EXAMPLE
    .\scripts\limpar_worktrees.ps1 -Executar
#>
[CmdletBinding()]
param(
    [string]$Raiz,
    [switch]$Executar,
    [switch]$Forcar
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($Raiz)) {
    $scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
    $Raiz = (Resolve-Path (Join-Path $scriptDir '..')).Path
}

function Invoke-Git {
    param([string[]]$Argumentos)
    $saida = & git -C $Raiz @Argumentos 2>&1
    return @{ Codigo = $LASTEXITCODE; Saida = $saida }
}

$lista = Invoke-Git @('worktree', 'list', '--porcelain')
if ($lista.Codigo -ne 0) {
    throw "git worktree list falhou: $($lista.Saida -join ' ')"
}

$worktrees = @()
$atual = @{}
foreach ($linha in $lista.Saida) {
    if ([string]::IsNullOrWhiteSpace($linha)) {
        if ($atual.Count -gt 0) { $worktrees += [pscustomobject]$atual; $atual = @{} }
        continue
    }
    $partes = $linha -split ' ', 2
    $atual[$partes[0]] = if ($partes.Count -gt 1) { $partes[1] } else { $true }
}
if ($atual.Count -gt 0) { $worktrees += [pscustomobject]$atual }

Write-Host "Worktrees registrados: $($worktrees.Count)" -ForegroundColor Cyan
foreach ($item in $worktrees) {
    $caminho = [string]$item.worktree
    $existe = Test-Path -LiteralPath $caminho
    $status = @()
    if ($existe) {
        $status = & git -C $caminho status --short 2>&1
    }
    $entradas = @($status).Count
    $branch = if ($item.branch) { $item.branch } else { '(detached)' }
    Write-Host ""
    Write-Host "  $caminho" -ForegroundColor Yellow
    Write-Host "    branch: $branch | existe: $existe | status: $entradas entrada(s)"
    if ($entradas -gt 0) {
        Write-Host "    amostra: $((@($status) | Select-Object -First 3) -join ' | ')" -ForegroundColor DarkYellow
    }
}

$secundarios = @($worktrees | Where-Object {
    $caminho = [System.IO.Path]::GetFullPath([string]$_.worktree)
    $caminho -ne [System.IO.Path]::GetFullPath($Raiz)
})

if ($secundarios.Count -eq 0) {
    Write-Host ""
    Write-Host "Nenhum worktree secundario registrado." -ForegroundColor Green
    return
}

Write-Host ""
Write-Host "Worktrees secundarios: $($secundarios.Count)" -ForegroundColor Yellow
foreach ($item in $secundarios) {
    Write-Host "  $([string]$item.worktree)"
}
if (-not $Executar) {
    Write-Host "DRY-RUN: nada foi removido. Use -Executar para remover os worktrees listados." -ForegroundColor Yellow
    return
}

foreach ($item in $secundarios) {
    $caminho = [string]$item.worktree
    if (-not (Test-Path -LiteralPath $caminho)) {
        Write-Host "  ignorando caminho ausente: $caminho"
        continue
    }
    $resposta = Read-Host "Remover worktree '$caminho'? Digite SIM para confirmar"
    if ($resposta -ne 'SIM') {
        Write-Host "  mantido: $caminho" -ForegroundColor DarkGray
        continue
    }
    $gitArgs = @('worktree', 'remove', $caminho)
    if ($Forcar) { $gitArgs += '--force' }
    & git -C $Raiz @gitArgs
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  removido: $caminho" -ForegroundColor Green
    } else {
        Write-Host "  falhou: $caminho (use -Forcar somente se nao houver trabalho exclusivo)" -ForegroundColor Red
    }
}
