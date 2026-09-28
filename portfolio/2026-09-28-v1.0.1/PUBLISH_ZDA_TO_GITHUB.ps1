param(
    [Parameter(Mandatory=$true)]
    [string]$RepoPath,

    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [Text.Encoding]::UTF8

$Source = Split-Path -Parent $MyInvocation.MyCommand.Path
$Target = Join-Path $RepoPath "reports\certificate-resume"

if (-not (Test-Path -LiteralPath (Join-Path $RepoPath ".git"))) {
    throw "Kein Git-Repository: $RepoPath"
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git.exe nicht gefunden."
}

New-Item -ItemType Directory -Force -Path $Target | Out-Null

$Files = @(
    "VERACHEL_CERTIFICATE_RESUME_v1.0.1_CLAIMED_ZDA.md",
    "VERACHEL_CERTIFICATE_RESUME_v1.0.1_CLAIMED_ZDA.json",
    "VERACHEL_CERTIFICATE_RESUME_v1.0.1_CLAIMED_ZDA.docx",
    "VERACHEL_CERTIFICATE_RESUME_v1.0.1_CLAIMED_ZDA.pdf",
    "VERACHEL_HEUREKA_256x256_BRANCH_UNIVERSE_v1.0.md",
    "VERACHEL_HEUREKA_256x256_BRANCH_UNIVERSE_v1.0.pdf",
    "BUILD_MANIFEST.json",
    "SHA256SUMS.txt"
)

foreach ($Name in $Files) {
    $Src = Join-Path $Source $Name
    if (-not (Test-Path -LiteralPath $Src)) {
        throw "Quelldatei fehlt: $Src"
    }
    Copy-Item -LiteralPath $Src -Destination (Join-Path $Target $Name) -Force
}

$Readme = @'
# VERACHEL // ZDA PUBLIC RECORD

`CLAIMED / ZDA` means this repository formally records Juri Janovski / Juri Halveth's evidence-backed portfolio benchmark claims.

**Important:** `CLAIMED` in this record means *self-asserted and documented to the record*. It does not itself state that a third-party certification issuer awarded the corresponding credential.

## Records

- [Certificate Resume v1.0.1 - CLAIMED + ZDA](VERACHEL_CERTIFICATE_RESUME_v1.0.1_CLAIMED_ZDA.md)
- [Machine-readable claim record](VERACHEL_CERTIFICATE_RESUME_v1.0.1_CLAIMED_ZDA.json)
- [Certificate Resume PDF](VERACHEL_CERTIFICATE_RESUME_v1.0.1_CLAIMED_ZDA.pdf)
- [HEUREKA 256^256 Branch Universe](VERACHEL_HEUREKA_256x256_BRANCH_UNIVERSE_v1.0.md)
- [HEUREKA visual PDF](VERACHEL_HEUREKA_256x256_BRANCH_UNIVERSE_v1.0.pdf)
- [SHA-256 checksums](SHA256SUMS.txt)

## Core

```text
CLAIMED = FORMALLY ASSERTED IN THIS PORTFOLIO
ZDA = ZU DEN AKTEN
CLAIMED != ISSUER_AWARDED
VERIFY THE WORK
```
'@

[IO.File]::WriteAllText(
    (Join-Path $Target "README.md"),
    $Readme,
    (New-Object Text.UTF8Encoding($false))
)

Push-Location $RepoPath
try {
    git checkout $Branch
    git pull --ff-only origin $Branch
    git add -- "reports/certificate-resume"

    $Status = git status --porcelain -- "reports/certificate-resume"
    if (-not $Status) {
        Write-Host "Keine neuen Änderungen." -ForegroundColor Yellow
        exit 0
    }

    git commit -m "docs: publish VERACHEL CLAIMED ZDA portfolio record"
    git push origin $Branch

    $Remote = (git remote get-url origin).Trim()
    $Sha = (git rev-parse HEAD).Trim()

    Write-Host ""
    Write-Host "ZDA PUBLISHED" -ForegroundColor Green
    Write-Host "COMMIT : $Sha" -ForegroundColor Cyan
    Write-Host "REMOTE : $Remote" -ForegroundColor Cyan

    if ($Remote -match '^https://github\.com/([^/]+)/([^/.]+)(?:\.git)?$') {
        $Owner = $Matches[1]
        $Repo = $Matches[2]
        Write-Host ""
        Write-Host "PUBLIC LINK:" -ForegroundColor Yellow
        Write-Host "https://github.com/$Owner/$Repo/tree/$Branch/reports/certificate-resume" -ForegroundColor Cyan
    }
}
finally {
    Pop-Location
}
