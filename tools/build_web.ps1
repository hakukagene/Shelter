param(
    [string]$RenpySdk = 'C:\Users\user\Downloads\renpy-8.5.3-sdk'
)
$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$RenpySdk = (Resolve-Path -LiteralPath $RenpySdk).Path
$outputDirectory = [IO.Path]::GetFullPath((Join-Path $projectRoot 'dist\web'))
if (-not $outputDirectory.StartsWith($projectRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Web build destination must stay inside this project.'
}
if (-not (Test-Path -LiteralPath (Join-Path $RenpySdk 'web\renpy.wasm'))) {
    throw 'Install matching Web support in the Ren''Py launcher first.'
}
$renpyPython = Join-Path $RenpySdk 'lib\py3-windows-x86_64\python.exe'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'
New-Item -ItemType Directory -Force -Path (Join-Path $projectRoot 'dist') | Out-Null
& $renpyPython (Join-Path $RenpySdk 'renpy.py') (Join-Path $RenpySdk 'launcher') web_build $projectRoot --destination $outputDirectory --savedir (Join-Path $projectRoot '.web-build\launcher-saves')
if ($LASTEXITCODE -ne 0) { throw 'Ren''Py web build failed.' }
& $renpyPython (Join-Path $PSScriptRoot 'prepare_web.py') --destination $outputDirectory
if ($LASTEXITCODE -ne 0) { throw 'Safari asset preparation failed.' }
