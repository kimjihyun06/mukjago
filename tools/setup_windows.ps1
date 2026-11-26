<#
  먹자GO 홈페이지 — 윈도 PC 작업 환경 한 번에 갖추기
  (여러 번 돌려도 안전: 이미 있는 것은 건너뜀)

  쓰기 (PowerShell, D:\my-hamepage\my-hamepage 에서):
    powershell -ExecutionPolicy Bypass -File setup_windows.ps1
  하는 일:
    1) winget 으로 Git, Python 3.12, VS Code 설치 (없을 때만)
    2) Claude Code 를 PATH 에 등록 (없을 때만)
    3) kimjihyun06-homepage 를 GitHub(mukjago) 최신본으로 준비
       - 이미 git 저장소면 git pull
       - git 저장소가 아닌 옛 폴더면 kimjihyun06-homepage_예전 으로 이름 바꾸고 새로 clone
    4) 파이썬 부품 설치 (requirements.txt: openpyxl, Pillow, keyring)
    5) git 사용자 이름·메일 설정 (비어 있을 때만, 메일은 GitHub 의 noreply 주소를 권함)
    6) python tools/state.py check 로 점검
  키·비밀번호는 묻지 않는다. Gemini 키가 필요하면 나중에 python tools/set_key.py (암호화 금고)
#>
param(
  [string]$Base = (Get-Location).Path,
  [switch]$NoVSCode
)
$ErrorActionPreference = "Stop"
$Repo = "https://github.com/kimjihyun06/mukjago.git"
$Dir  = Join-Path $Base "kimjihyun06-homepage"
$ok = @(); $warn = @()

function Refresh-Path {
  $env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
}
function Has($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function Ensure($cmd, $id, $label) {
  if (Has $cmd) { $script:ok += "$label 이미 있음"; return }
  Write-Host "[$label] 설치 중 ($id) ..." -ForegroundColor Cyan
  winget install --id $id -e --silent --accept-source-agreements --accept-package-agreements
  Refresh-Path
  if (Has $cmd) { $script:ok += "$label 설치함" } else { $script:warn += "$label 설치 후에도 찾지 못함 — PowerShell 을 새로 열고 다시 실행" }
}

Write-Host "== 먹자GO 작업 환경 준비 ==  ($Base)" -ForegroundColor Green
if (-not (Has "winget")) { throw "winget 이 없습니다. Microsoft Store 에서 '앱 설치 관리자(App Installer)' 를 설치한 뒤 다시 실행하세요." }

# 1) 프로그램
Ensure "git"    "Git.Git"                 "Git"
Ensure "python" "Python.Python.3.12"      "Python"
if (-not $NoVSCode) { Ensure "code" "Microsoft.VisualStudioCode" "VS Code" }
# 윈도의 'python' 가짜 바로가기(스토어 열기)만 있는 경우 대비
try { $pv = & python --version 2>&1; if ($pv -notmatch "Python 3") { throw } ; $ok += "python 동작: $pv" }
catch { $warn += "python 이 실행되지 않음 — PowerShell 을 새로 열고 다시 실행 (설정 > 앱 실행 별칭에서 python 스토어 별칭 끄기)" }

# 2) Claude Code PATH
$cl = Join-Path $env:USERPROFILE ".local\bin"
if ((Test-Path (Join-Path $cl "claude.exe")) -and (([Environment]::GetEnvironmentVariable("Path","User")) -notlike "*$cl*")) {
  [Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path","User") + ";$cl", "User")
  $ok += "Claude Code PATH 등록함"
} else { $ok += "Claude Code PATH 확인" }
Refresh-Path

# 3) 홈페이지 최신본
if (Test-Path (Join-Path $Dir ".git")) {
  Push-Location $Dir; git pull --ff-only; Pop-Location; $ok += "홈페이지 git pull"
} else {
  if (Test-Path $Dir) {
    $old = Join-Path $Base "kimjihyun06-homepage_예전"
    if (Test-Path $old) { $old = "$old-" + (Get-Date -Format "yyyyMMdd-HHmmss") }
    Rename-Item $Dir $old; $ok += "옛 폴더 보관: $(Split-Path $old -Leaf)"
  }
  git clone $Repo $Dir; $ok += "홈페이지 clone"
}

# 4) 파이썬 부품
Push-Location $Dir
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
$ok += "파이썬 부품 설치 (openpyxl, Pillow, keyring)"

# 5) git 사용자 (비어 있을 때만)
if (-not (git config --global user.name)) {
  $n = Read-Host "git 에 기록될 이름 (예: 김지현)"; if ($n) { git config --global user.name $n }
}
if (-not (git config --global user.email)) {
  Write-Host "메일은 공개 기록에 남습니다. GitHub > Settings > Emails 의 '…@users.noreply.github.com' 주소를 권합니다."
  $m = Read-Host "git 에 기록될 메일"; if ($m) { git config --global user.email $m }
}
git config --global core.quotepath false   # 한글 파일 이름이 깨져 보이지 않게
$ok += "git 사용자: $(git config --global user.name) <$(git config --global user.email)>"

# 6) 점검
Write-Host "`n== 점검 ==" -ForegroundColor Green
python tools/state.py check
if ($LASTEXITCODE -eq 0) { $ok += "점검 모두 OK" } else { $warn += "점검에 !! 항목 있음 — 위 목록 확인" }
Pop-Location

# 자료 폴더 확인 (읽기만)
$data = Join-Path $Base "자료\엑셀"
if (Test-Path $data) { $ok += "자료 폴더 있음: $data" } else { $warn += "자료 폴더 없음: $data" }

Write-Host "`n== 결과 ==" -ForegroundColor Green
$ok   | ForEach-Object { Write-Host "  OK  $_" }
$warn | ForEach-Object { Write-Host "  !!  $_" -ForegroundColor Yellow }
Write-Host "`n다음: cd kimjihyun06-homepage  →  python tools/import_all_photos.py --dry  (또는 사진전체갱신.bat)"
