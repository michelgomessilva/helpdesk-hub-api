param(
    [Parameter(Mandatory = $true)]
    [string]$FeatureId,

    [Parameter(Mandatory = $true)]
    [string]$Slug,

    [Parameter(Mandatory = $true)]
    [string]$Title
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
. (Join-Path $PSScriptRoot "_shared.ps1")
$specDocPath = Join-Path $repoRoot "docs\spec-driven-development.md"
$templatePath = Join-Path $repoRoot "docs\features\_template.md"
$targetFileName = ("{0}-{1}.md" -f $FeatureId.ToLowerInvariant(), $Slug.ToLowerInvariant())
$targetPath = Join-Path $repoRoot ("docs\features\{0}" -f $targetFileName)
$documentPath = "docs/features/$targetFileName"
$today = Get-Date -Format "yyyy-MM-dd"
$quotedToday = "- Criado em: " + '`' + $today + '`'
$quotedUpdatedToday = "- Atualizado em: " + '`' + $today + '`'

if (-not (Test-Path -LiteralPath $templatePath)) {
    throw "Template nao encontrado em '$templatePath'."
}

if (Test-Path -LiteralPath $targetPath) {
    throw "A feature '$targetFileName' ja existe."
}

$content = Get-Content -LiteralPath $templatePath -Raw
$content = $content.Replace("FXXX", $FeatureId.ToUpperInvariant())
$content = $content.Replace("Nome da feature", $Title)
$content = $content.Replace("- Criado em:", $quotedToday)
$content = $content.Replace("- Atualizado em:", $quotedUpdatedToday)
$content = Set-MarkdownSectionContent `
    -Content $content `
    -Heading "Diretrizes Arquiteturais" `
    -SectionBody (Get-ArchitectureGuidelinesBlock)

Set-Content -LiteralPath $targetPath -Value $content -Encoding UTF8

Update-SpecDrivenDocument `
    -SpecDocPath $specDocPath `
    -FeatureId $FeatureId.ToUpperInvariant() `
    -Title $Title `
    -Status "Draft" `
    -Origin "Manual" `
    -DocumentPath $documentPath `
    -Summary "Feature criada a partir do template padrao e pronta para refinamento tecnico."

Write-Host "Feature criada em: $targetPath"
Write-Host "Documento central atualizado em: $specDocPath"
