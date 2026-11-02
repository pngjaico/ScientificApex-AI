#requires -Version 5.1
<#
.SYNOPSIS
    Inventaria o backup historico em C: e copia para D: apenas o que ainda
    nao existe em D:, com hash SHA-256 e manifesto verificavel.

.DESCRIPTION
    Nao apaga nada. Por padrao apenas gera o manifesto (dry-run). Use
    -Executar para copiar os arquivos ausentes/conflitantes para
    archive\legado_C_2026-11.

    Arquivos de dependencias/caches (.venv, node_modules, __pycache__ etc.)
    ficam fora do inventario. O topo "tools" (navegadores Playwright) e
    classificado como reproduzivel e nao e copiado.

.EXAMPLE
    .\scripts\migrar_legado_c.ps1
    .\scripts\migrar_legado_c.ps1 -Executar
#>
[CmdletBinding()]
param(
    [string]$Origem = 'C:\Users\Usuario-pc\Desktop\Doutorado',
    [string]$DestinoBase = 'D:\Usuario-pc\Projetos\Doutorado',
    [string]$ArquivoRelativo = 'archive\legado_C_2026-11',
    [string[]]$TopLevelReprodutivel = @('tools'),
    [switch]$Executar
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $Origem)) {
    throw "Origem nao encontrada: $Origem"
}
if (-not (Test-Path -LiteralPath $DestinoBase)) {
    throw "Destino nao encontrado: $DestinoBase"
}

$Arquivo = Join-Path $DestinoBase $ArquivoRelativo
$ExcluirRegex = '\\(node_modules|\.venv|\.git|\.playwright-osf|__pycache__|\.pytest_cache|\.ruff_cache|\.mypy_cache|\.expo|\.firebase)\\'

function Get-MapaDeArquivos {
    param([string]$Raiz)
    $mapa = @{}
    Get-ChildItem -LiteralPath $Raiz -Recurse -File -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch $ExcluirRegex } |
        ForEach-Object {
            $rel = $_.FullName.Substring($Raiz.Length).TrimStart('\')
            $mapa[$rel] = $_
        }
    return $mapa
}

function Get-Sha256 {
    param([string]$Caminho)
    return (Get-FileHash -LiteralPath $Caminho -Algorithm SHA256).Hash
}

Write-Host "Inventariando C: ..." -ForegroundColor Cyan
$mapaC = Get-MapaDeArquivos -Raiz $Origem
Write-Host "  $($mapaC.Count) arquivos (sem caches/dependencias)" -ForegroundColor DarkGray

Write-Host "Inventariando D: ..." -ForegroundColor Cyan
$mapaD = Get-MapaDeArquivos -Raiz $DestinoBase
Write-Host "  $($mapaD.Count) arquivos (sem caches/dependencias)" -ForegroundColor DarkGray

$registros = New-Object System.Collections.Generic.List[object]
$contagem = @{
    identico = 0
    somente_c = 0
    conflito = 0
    reproduzivel = 0
}
$bytesSomenteC = 0L
$bytesConflito = 0L

$i = 0
foreach ($rel in ($mapaC.Keys | Sort-Object)) {
    $i++
    if ($i % 1000 -eq 0) {
        Write-Host "  hash $i / $($mapaC.Count) ..." -ForegroundColor DarkGray
    }

    $arquivoC = $mapaC[$rel]
    $topo = ($rel -split '\\')[0]
    $status = $null
    $shaC = $null
    $shaD = $null

    if ($TopLevelReprodutivel -contains $topo) {
        $status = 'reproduzivel'
        $contagem.reproduzivel++
    }
    elseif (-not $mapaD.ContainsKey($rel)) {
        $status = 'somente_c'
        $shaC = Get-Sha256 -Caminho $arquivoC.FullName
        $contagem.somente_c++
        $bytesSomenteC += $arquivoC.Length
    }
    else {
        $arquivoD = $mapaD[$rel]
        if ($arquivoC.Length -ne $arquivoD.Length) {
            $status = 'conflito'
            $shaC = Get-Sha256 -Caminho $arquivoC.FullName
            $shaD = Get-Sha256 -Caminho $arquivoD.FullName
            $contagem.conflito++
            $bytesConflito += $arquivoC.Length
        }
        else {
            $shaC = Get-Sha256 -Caminho $arquivoC.FullName
            $shaD = Get-Sha256 -Caminho $arquivoD.FullName
            if ($shaC -eq $shaD) {
                $status = 'identico'
                $contagem.identico++
            }
            else {
                $status = 'conflito'
                $contagem.conflito++
                $bytesConflito += $arquivoC.Length
            }
        }
    }

    $registros.Add([pscustomobject]@{
        relative_path = $rel
        top_level     = $topo
        size_bytes    = $arquivoC.Length
        sha256_c      = $shaC
        sha256_d      = $shaD
        status        = $status
    })
}

$resumo = [pscustomobject]@{
    generated_at_utc     = (Get-Date).ToUniversalTime().ToString('o')
    origem               = $Origem
    destino              = $DestinoBase
    arquivo              = $Arquivo
    executar             = [bool]$Executar
    total_arquivos_c     = $mapaC.Count
    total_arquivos_d     = $mapaD.Count
    identicos            = $contagem.identico
    somente_em_c         = $contagem.somente_c
    conflitos            = $contagem.conflito
    reproduziveis        = $contagem.reproduzivel
    bytes_somente_c      = $bytesSomenteC
    bytes_conflitos      = $bytesConflito
}

Write-Host ""
Write-Host "Resumo:" -ForegroundColor Yellow
$resumo | Format-List

if (-not $Executar) {
    Write-Host "DRY-RUN: manifesto nao foi gravado e nada foi copiado." -ForegroundColor Yellow
    Write-Host "Rode com -Executar para criar $Arquivo e copiar os arquivos." -ForegroundColor Yellow
    return
}

New-Item -ItemType Directory -Path $Arquivo -Force | Out-Null
$planilha = Join-Path $Arquivo 'inventario_completo.csv'
$registros | Export-Csv -LiteralPath $planilha -NoTypeInformation -Encoding UTF8

$manifesto = Join-Path $Arquivo 'MANIFESTO_DE_MIGRACAO.json'
$resumo | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifesto -Encoding UTF8

$copiados = 0
$falhas = New-Object System.Collections.Generic.List[object]

foreach ($r in $registros) {
    if ($r.status -notin @('somente_c', 'conflito')) { continue }

    $origemArquivo = Join-Path $Origem $r.relative_path
    if ($r.relative_path -match '^\.env') {
        $destinoArquivo = Join-Path $Arquivo (Join-Path 'segredos' $r.relative_path)
    }
    elseif ($r.status -eq 'conflito') {
        $destinoArquivo = Join-Path $Arquivo (Join-Path 'conflitos' $r.relative_path)
    }
    else {
        $destinoArquivo = Join-Path $Arquivo $r.relative_path
    }

    $pastaDestino = Split-Path -Parent $destinoArquivo
    New-Item -ItemType Directory -Path $pastaDestino -Force | Out-Null
    Copy-Item -LiteralPath $origemArquivo -Destination $destinoArquivo -Force

    $shaCopia = Get-Sha256 -Caminho $destinoArquivo
    if ($shaCopia -ne $r.sha256_c) {
        $falhas.Add([pscustomobject]@{
            relative_path = $r.relative_path
            esperado      = $r.sha256_c
            obtido        = $shaCopia
            destino       = $destinoArquivo
        })
    }
    else {
        $copiados++
    }
}

$relatorio = [pscustomobject]@{
    generated_at_utc = (Get-Date).ToUniversalTime().ToString('o')
    copiados         = $copiados
    falhas           = $falhas.Count
    detalhes_falhas  = $falhas
}

$relatorio | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $Arquivo 'RELATORIO_DE_COPIA.json') -Encoding UTF8

Write-Host ""
Write-Host "Copiados e verificados: $copiados" -ForegroundColor Green
Write-Host "Falhas de hash:        $($falhas.Count)" -ForegroundColor $(if ($falhas.Count -eq 0) { 'Green' } else { 'Red' })
Write-Host "Manifesto: $manifesto"
Write-Host "Inventario: $planilha"
