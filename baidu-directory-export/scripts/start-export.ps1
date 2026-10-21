param(
    [Parameter(Mandatory = $true)][string]$ToolPath,
    [Parameter(Mandatory = $true)][string]$ConfigDirectory,
    [Parameter(Mandatory = $true)][string]$Target,
    [Parameter(Mandatory = $true)][string]$OutputDirectory,
    [string]$PythonExecutable = 'python'
)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
Write-Host ''
Write-Host '========== 百度网盘目录导出向导 ==========' -ForegroundColor Cyan
Write-Host "目标目录：$Target"
Write-Host "输出位置：$OutputDirectory"
Write-Host '本向导只读取目录名称，不下载、移动或修改网盘原文件。'
Write-Host ''
Write-Host '第一步：请在自己的浏览器中登录 https://pan.baidu.com，确认是自己的账号。'
Write-Host '第二步：按 F12 → Network（网络），刷新页面。'
Write-Host '第三步：选择 pan.baidu.com 的 list?... 请求，或 Doc 中的 main 请求。'
Write-Host '第四步：Headers → Request Headers → Cookie，复制完整值，不含 Cookie:。'
Write-Host '注意：不是 Response Headers 中的 Set-Cookie。不要将 Cookie 发到聊天中。'
Write-Host ''
Write-Host '账号密码登录已长期不维护，可能报 50052；这里使用浏览器登录后的 Cookie。'
Write-Host '粘贴时输入会隐藏。凭据保存在本次独立配置目录，不会写入导出文件。'
Write-Host "本次配置目录：$ConfigDirectory"
Write-Host ''
try {
    & (Join-Path $PSScriptRoot 'login.ps1') -ToolPath $ToolPath -ConfigDirectory $ConfigDirectory
    $confirmation = Read-Host '上方是否显示你自己的正确账号？输入 Y 继续导出，其他输入取消'
    if ($confirmation -ne 'Y') { throw '已取消。未执行目录导出。' }
    & $PythonExecutable -X utf8 (Join-Path $PSScriptRoot 'directory_export.py') export --tool $ToolPath --config-dir $ConfigDirectory --target $Target --output $OutputDirectory
    if ($LASTEXITCODE -ne 0) { throw '导出未通过校验，请查看上方错误和输出目录中的日志。' }
    Write-Host ''
    Write-Host '导出完成：directory.txt 和 directory.html' -ForegroundColor Green
    Write-Host "保存位置：$OutputDirectory"
    Write-Host '可以将成功提示告诉助手，继续核验 HTML 交互。不要发送 Cookie。'
}
catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
}
Read-Host '按回车关闭此窗口' | Out-Null
