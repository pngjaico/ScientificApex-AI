param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Argumentos)
if (-not $Argumentos) { $Argumentos = @("--help") }
Set-Location -LiteralPath $PSScriptRoot
& "$PSScriptRoot\.venv\Scripts\python.exe" -m article_machine @Argumentos
exit $LASTEXITCODE
