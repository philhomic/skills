param(
    [Parameter(Mandatory = $true)][string]$ToolPath,
    [Parameter(Mandatory = $true)][string]$ConfigDirectory
)
$ErrorActionPreference = 'Stop'
if (-not [System.IO.Path]::IsPathRooted($ToolPath) -or -not [System.IO.Path]::IsPathRooted($ConfigDirectory)) {
    throw 'ToolPath and ConfigDirectory must be absolute paths.'
}
if (-not (Test-Path -LiteralPath $ToolPath -PathType Leaf)) { throw 'Client executable not found.' }
New-Item -ItemType Directory -Path $ConfigDirectory -Force | Out-Null
$previousConfig = $env:BAIDUPCS_GO_CONFIG_DIR
try {
    $env:BAIDUPCS_GO_CONFIG_DIR = $ConfigDirectory
    Write-Host "Session configuration: $ConfigDirectory"
    Write-Host 'Use your own Baidu account. Credentials will be saved in this local directory.'
    $cookieInput = Read-Host 'Paste your Baidu Netdisk Cookie (hidden)' -AsSecureString
    if ($cookieInput.Length -eq 0) { throw 'Cookie must not be empty.' }
    $credential = [System.Management.Automation.PSCredential]::new('cookie', $cookieInput)
    & $ToolPath login "-cookies=$($credential.GetNetworkCredential().Password)"
    if ($LASTEXITCODE -ne 0) { throw 'Login command failed.' }
    & $ToolPath who
    Write-Host 'Verify that the account above is yours before exporting.'
}
finally {
    if ($cookieInput) { $cookieInput.Dispose() }
    Remove-Variable credential, cookieInput -ErrorAction SilentlyContinue
    $env:BAIDUPCS_GO_CONFIG_DIR = $previousConfig
}
