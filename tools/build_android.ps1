param(
    [string]$RenpySdk = 'C:\Users\user\Downloads\renpy-8.5.3-sdk',
    [switch]$Setup
)

$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$RenpySdk = (Resolve-Path -LiteralPath $RenpySdk).Path
$raptDirectory = Join-Path $RenpySdk 'rapt'
$buildCache = Join-Path $projectRoot '.android-build'
$outputDirectory = Join-Path $projectRoot 'dist\android'
$javaDirectory = Join-Path $buildCache 'java'
$sdkDirectory = Join-Path $raptDirectory 'Sdk'
$sdkManager = Join-Path $sdkDirectory 'cmdline-tools\latest\bin\sdkmanager.bat'
$renpyPython = Join-Path $RenpySdk 'lib\py3-windows-x86_64\python.exe'
$renpyScript = Join-Path $RenpySdk 'renpy.py'

if (-not (Test-Path -LiteralPath (Join-Path $raptDirectory 'android.py'))) {
    throw 'Install the matching Ren''Py Android support (RAPT) in the Ren''Py SDK first.'
}
New-Item -ItemType Directory -Force -Path $buildCache, $outputDirectory | Out-Null

if ($Setup -and -not (Test-Path -LiteralPath $javaDirectory)) {
    Write-Host 'Downloading a portable Eclipse Temurin JDK 21.'
    $releases = Invoke-RestMethod -Uri 'https://api.adoptium.net/v3/assets/latest/21/hotspot?architecture=x64&image_type=jdk&os=windows&vendor=eclipse'
    $jdkPackage = $releases[0].binary.package
    $jdkArchive = Join-Path $buildCache 'temurin-21.zip'
    Invoke-WebRequest -Uri $jdkPackage.link -OutFile $jdkArchive
    if ((Get-FileHash -LiteralPath $jdkArchive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $jdkPackage.checksum) {
        throw 'JDK checksum mismatch.'
    }
    Expand-Archive -LiteralPath $jdkArchive -DestinationPath $javaDirectory
}

$jdkFolders = @(Get-ChildItem -LiteralPath $javaDirectory -Directory -ErrorAction SilentlyContinue |
    Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'bin\javac.exe') })
if ($jdkFolders.Count -ne 1) {
    throw 'A portable JDK is missing. Run this script with -Setup.'
}

# These settings apply only to this build process, not Windows' global settings.
$env:JAVA_HOME = $jdkFolders[0].FullName
$env:ANDROID_HOME = $sdkDirectory
$env:ANDROID_SDK_ROOT = $sdkDirectory
$env:ANDROID_USER_HOME = Join-Path $buildCache 'android-user'
$env:GRADLE_USER_HOME = Join-Path $buildCache 'gradle'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'
$env:Path = (Join-Path $env:JAVA_HOME 'bin') + ';' + $env:Path
New-Item -ItemType Directory -Force -Path $env:ANDROID_USER_HOME | Out-Null

if ($Setup) {
    if (-not (Test-Path -LiteralPath $sdkManager)) {
        Write-Host 'Downloading the Android command-line tools used by Ren''Py 8.5.3.'
        $sdkArchive = Join-Path $buildCache 'android-commandline-tools.zip'
        $sdkUnpack = Join-Path $buildCache 'sdk-unpack'
        Invoke-WebRequest -Uri 'https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip' -OutFile $sdkArchive
        Expand-Archive -LiteralPath $sdkArchive -DestinationPath $sdkUnpack -Force
        New-Item -ItemType Directory -Force -Path (Join-Path $sdkDirectory 'cmdline-tools') | Out-Null
        Copy-Item -LiteralPath (Join-Path $sdkUnpack 'cmdline-tools') -Destination (Join-Path $sdkDirectory 'cmdline-tools\latest') -Recurse
    }
    Write-Host 'Accepting Android SDK licenses and installing build dependencies.'
    1..100 | ForEach-Object { 'y' } | & $sdkManager "--sdk_root=$sdkDirectory" --licenses
    if ($LASTEXITCODE -ne 0) { throw 'Android SDK license setup failed.' }
    1..100 | ForEach-Object { 'y' } | & $sdkManager "--sdk_root=$sdkDirectory" 'platform-tools' 'platforms;android-36' 'build-tools;36.0.0'
    if ($LASTEXITCODE -ne 0) { throw 'Android SDK package installation failed.' }
}

if (-not (Test-Path -LiteralPath $sdkManager)) {
    throw 'Android SDK is missing. Run this script with -Setup.'
}

# Use RAPT's signing convention. Preserve these keys for future app updates.
$androidKey = Join-Path $projectRoot 'android.keystore'
$bundleKey = Join-Path $projectRoot 'bundle.keystore'
if (-not (Test-Path -LiteralPath $androidKey)) {
    & (Join-Path $env:JAVA_HOME 'bin\keytool.exe') -genkeypair -keystore $androidKey -alias android -keyalg RSA -keysize 2048 -keypass android -storepass android -dname 'CN=Shelter' -validity 20000
    if ($LASTEXITCODE -ne 0) { throw 'Android signing key generation failed.' }
}
if (-not (Test-Path -LiteralPath $bundleKey)) {
    Copy-Item -LiteralPath $androidKey -Destination $bundleKey
}

& $renpyPython $renpyScript (Join-Path $RenpySdk 'launcher') android_build $projectRoot --destination $outputDirectory --savedir (Join-Path $buildCache 'launcher-saves')
if ($LASTEXITCODE -ne 0) { throw 'Ren''Py Android build failed.' }

$packages = @(Get-ChildItem -LiteralPath $outputDirectory -Filter '*.apk' -File)
if ($packages.Count -eq 0) { throw 'No APK was produced.' }
$packages | Select-Object FullName, Length
