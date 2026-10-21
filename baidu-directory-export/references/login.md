# 登录和配置隔离

## Windows 本机交互登录

优先使用 `scripts/start-export.ps1`：启动可见 PowerShell 窗口，向导给出中文分步说明，隐藏输入 Cookie，显示账号供本人确认，然后自动调用导出脚本。参数为 `-ToolPath`、`-ConfigDirectory`、`-Target`、`-OutputDirectory`；路径均使用绝对路径。可通过 `Start-Process powershell.exe -ArgumentList ...` 启动，正确引用包含空格的参数；不要传 Cookie 到启动命令。应在用户明确要求可见交互窗口后使用；否则按当前工具政策取得授权。不要自动使用 `-ExecutionPolicy Bypass`；若策略阻止脚本，报告具体错误。

先确定 BaiduPCS-Go 可执行文件绝对路径，并为此人此次任务生成独立配置目录。脚本仅修改自身进程环境，退出后恢复，不改系统环境变量，不读取其他人的默认配置。

使用者自行运行（路径均由代理替换后再提供）：

```powershell
& '<技能目录>\scripts\login.ps1' -ToolPath '<BaiduPCS-Go.exe绝对路径>' -ConfigDirectory '<本次配置目录绝对路径>'
```

普通用户名/密码登录长期不维护，可能返回 `50052`；优先网页登录后使用 Cookie。操作步骤：

1. 使用者在自己的浏览器登录 `https://pan.baidu.com`，确认是自己的账号。
2. F12 → Network（网络），刷新，选择发往 `https://pan.baidu.com/` 的 `list?...` 请求，或 Doc 中的 `main` 页面请求。
3. Headers → Request Headers → Cookie，复制完整值（不包含 `Cookie:`）。不要复制响应中的 Set-Cookie。
4. 在上述脚本的隐藏提示中粘贴。无需发到聊天，也不要截图包含凭据。

脚本通过客户端 `login -cookies=...` 登录：Cookie 不写入脚本或终端历史，但传给客户端时会短暂出现在本机进程参数中；客户端会把登录凭据保存到指定配置目录。不要在不可信的共享系统上操作。共享同一个操作系统账户下的配置目录不能视为安全隔离；不同人员应使用各自系统账户或可信独立环境。

登录后由使用者确认 `who` 显示自己的账号。导出脚本总是显式设置相同配置目录。登录成功而代理仍看到 uid 0 时，先检查运行环境/配置位置，不打印配置或凭据；让使用者直接在已登录终端运行导出脚本即可。

退出此任务账号（只清除本地客户端会话，不改网盘原文件）：

```powershell
$env:BAIDUPCS_GO_CONFIG_DIR = '<本次配置目录绝对路径>'
& '<BaiduPCS-Go.exe绝对路径>' logout
```

非 Windows 环境可由使用者在自己的交互终端完成客户端登录，并显式设置同名环境变量；不要将 Windows 脚本当作通用登录器。
