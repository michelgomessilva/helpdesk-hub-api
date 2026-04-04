param(
    [Parameter(Mandatory = $true)]
    [string]$Repository,

    [Parameter(Mandatory = $true)]
    [int]$IssueNumber,

    [Parameter(Mandatory = $true)]
    [string]$FeatureId,

    [Parameter(Mandatory = $true)]
    [string]$Slug
)

$ErrorActionPreference = "Stop"

if (-not $env:GITHUB_TOKEN) {
    throw "Defina a variavel de ambiente GITHUB_TOKEN para importar a issue do GitHub."
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
. (Join-Path $PSScriptRoot "_shared.ps1")
$specDocPath = Join-Path $repoRoot "docs\spec-driven-development.md"
$templatePath = Join-Path $repoRoot "docs\features\_template.md"
$targetFileName = ("{0}-{1}.md" -f $FeatureId.ToLowerInvariant(), $Slug.ToLowerInvariant())
$targetPath = Join-Path $repoRoot ("docs\features\{0}" -f $targetFileName)
$documentPath = "docs/features/$targetFileName"
$today = Get-Date -Format "yyyy-MM-dd"

if (-not (Test-Path -LiteralPath $templatePath)) {
    throw "Template nao encontrado em '$templatePath'."
}

if (Test-Path -LiteralPath $targetPath) {
    throw "A feature '$targetFileName' ja existe."
}

$headers = @{
    Authorization = "Bearer $($env:GITHUB_TOKEN)"
    Accept        = "application/vnd.github+json"
    "User-Agent"  = "helpdesk-hub-api-spec-importer"
}

$issueUrl = "https://api.github.com/repos/$Repository/issues/$IssueNumber"
$issue = Invoke-RestMethod -Method Get -Uri $issueUrl -Headers $headers

$title = [string]$issue.title
$body = [string]$issue.body
$labels = @()

if ($issue.labels) {
    $labels = @($issue.labels | ForEach-Object { $_.name })
}

$content = Get-Content -LiteralPath $templatePath -Raw
$content = Build-ImportedFeatureContent `
    -TemplateContent $content `
    -FeatureId $FeatureId.ToUpperInvariant() `
    -Title $title `
    -Today $today `
    -IssueNumber $IssueNumber `
    -IssueUrl $issue.html_url `
    -Body $body `
    -Labels $labels

Set-Content -LiteralPath $targetPath -Value $content -Encoding UTF8

Update-SpecDrivenDocument `
    -SpecDocPath $specDocPath `
    -FeatureId $FeatureId.ToUpperInvariant() `
    -Title $title `
    -Status "Draft" `
    -Origin "GitHub #$IssueNumber" `
    -DocumentPath $documentPath `
    -Summary $body `
    -Labels $labels

Write-Host "Spec criada a partir da issue #$IssueNumber em: $targetPath"
Write-Host "Documento central atualizado em: $specDocPath"
