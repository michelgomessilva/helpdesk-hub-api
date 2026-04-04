function Update-MarkedSection {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Content,

        [Parameter(Mandatory = $true)]
        [string]$StartMarker,

        [Parameter(Mandatory = $true)]
        [string]$EndMarker,

        [Parameter(Mandatory = $true)]
        [string]$Replacement
    )

    $start = $Content.IndexOf($StartMarker)
    $end = $Content.IndexOf($EndMarker)

    if ($start -lt 0 -or $end -lt 0 -or $end -lt $start) {
        throw "Marcadores '$StartMarker' e '$EndMarker' nao encontrados corretamente."
    }

    $prefix = $Content.Substring(0, $start + $StartMarker.Length)
    $suffix = $Content.Substring($end)

    return $prefix + "`r`n" + $Replacement.Trim() + "`r`n" + $suffix
}

function Convert-FeatureIdToOrder {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FeatureId
    )

    $digits = $FeatureId -replace '[^\d]', ''
    if ([string]::IsNullOrWhiteSpace($digits)) {
        return [int]::MaxValue
    }

    return [int]$digits
}

function Normalize-Summary {
    param(
        [string]$Text
    )

    if ([string]::IsNullOrWhiteSpace($Text)) {
        return "Resumo ainda nao preenchido."
    }

    $normalized = ($Text -replace '\r?\n+', ' ' -replace '\s+', ' ').Trim()
    if ($normalized.Length -gt 220) {
        return $normalized.Substring(0, 217) + "..."
    }

    return $normalized
}

function Convert-BodyToLines {
    param(
        [string]$Body
    )

    if ([string]::IsNullOrWhiteSpace($Body)) {
        return @()
    }

    return ($Body -replace "`r`n", "`n" -replace "`r", "`n").Split("`n")
}

function Get-MarkdownSectionContent {
    param(
        [string]$Body,
        [string[]]$HeadingAliases
    )

    $lines = Convert-BodyToLines -Body $Body
    if ($lines.Count -eq 0) {
        return $null
    }

    $normalizedAliases = @($HeadingAliases | ForEach-Object { $_.Trim().ToLowerInvariant() })
    $capturing = $false
    $buffer = New-Object System.Collections.Generic.List[string]

    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        if ($trimmed -match '^(#+)\s*(.+?)\s*$') {
            $headingText = $matches[2].Trim().TrimEnd(':').ToLowerInvariant()
            if ($capturing) {
                break
            }

            if ($normalizedAliases -contains $headingText) {
                $capturing = $true
                continue
            }
        }

        if ($capturing) {
            $buffer.Add($line)
        }
    }

    $result = ($buffer -join "`r`n").Trim()
    if ([string]::IsNullOrWhiteSpace($result)) {
        return $null
    }

    return $result
}

function Get-MarkdownChecklistItems {
    param(
        [string]$Body
    )

    $items = New-Object System.Collections.Generic.List[string]
    foreach ($line in (Convert-BodyToLines -Body $Body)) {
        if ($line.Trim() -match '^(?:[-*]|\d+\.)\s+\[(?: |x|X)\]\s+(.+?)\s*$') {
            $items.Add($matches[1].Trim())
        }
    }

    return @($items)
}

function Get-MarkdownBulletItems {
    param(
        [string]$Body
    )

    $items = New-Object System.Collections.Generic.List[string]
    foreach ($line in (Convert-BodyToLines -Body $Body)) {
        $trimmed = $line.Trim()
        if ($trimmed -match '^(?:[-*]|\d+\.)\s+(?!\[(?: |x|X)\])(.+?)\s*$') {
            $items.Add($matches[1].Trim())
        }
    }

    return @($items)
}

function Get-FirstParagraph {
    param(
        [string]$Body
    )

    if ([string]::IsNullOrWhiteSpace($Body)) {
        return $null
    }

    $paragraphs = ($Body.Trim() -split '(?:\r?\n){2,}') | ForEach-Object { $_.Trim() } | Where-Object { $_ }
    foreach ($paragraph in $paragraphs) {
        if ($paragraph -match '^(#+)\s*.+?\r?\n(.+)$') {
            return $matches[2].Trim()
        }

        if ($paragraph -notmatch '^(#+|\-|[*]|\d+\.)') {
            return $paragraph
        }
    }

    return $paragraphs | Select-Object -First 1
}

function Convert-ToBulletBlock {
    param(
        [string[]]$Items,
        [string]$Fallback = "- A detalhar"
    )

    $validItems = @($Items | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
    if ($validItems.Count -eq 0) {
        return $Fallback
    }

    return (($validItems | ForEach-Object { "- $($_.Trim())" }) -join "`r`n")
}

function Convert-ToAcceptanceCriteriaBlock {
    param(
        [string[]]$Items,
        [string]$Fallback = "- [ ] Criterio a detalhar"
    )

    $validItems = @($Items | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
    if ($validItems.Count -eq 0) {
        return $Fallback
    }

    return (($validItems | ForEach-Object { "- [ ] $($_.Trim())" }) -join "`r`n")
}

function Set-MarkdownSectionContent {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Content,

        [Parameter(Mandatory = $true)]
        [string]$Heading,

        [Parameter(Mandatory = $true)]
        [string]$SectionBody
    )

    $pattern = "(?ms)(## " + [regex]::Escape($Heading) + "\r?\n\r?\n)(.*?)(?=\r?\n## |\z)"
    return [regex]::Replace($Content, $pattern, ('$1' + $SectionBody.Trim() + "`r`n"), 1)
}

function Build-ImportedFeatureContent {
    param(
        [Parameter(Mandatory = $true)]
        [string]$TemplateContent,

        [Parameter(Mandatory = $true)]
        [string]$FeatureId,

        [Parameter(Mandatory = $true)]
        [string]$Title,

        [Parameter(Mandatory = $true)]
        [string]$Today,

        [Parameter(Mandatory = $true)]
        [int]$IssueNumber,

        [Parameter(Mandatory = $true)]
        [string]$IssueUrl,

        [string]$Body,

        [string[]]$Labels = @()
    )

    $quotedToday = '`' + $Today + '`'
    $firstParagraph = Get-FirstParagraph -Body $Body

    $summarySource = Get-MarkdownSectionContent -Body $Body -HeadingAliases @("resumo", "summary", "visao geral")
    if (-not $summarySource) { $summarySource = $firstParagraph }
    if (-not $summarySource) { $summarySource = "Feature importada da issue #$IssueNumber no GitHub." }

    $problemSource = Get-MarkdownSectionContent -Body $Body -HeadingAliases @("problema", "contexto", "dor", "motivacao")
    if (-not $problemSource) { $problemSource = $firstParagraph }
    if (-not $problemSource) { $problemSource = "Necessidade identificada a partir da issue #$IssueNumber." }

    $objectiveSource = Get-MarkdownSectionContent -Body $Body -HeadingAliases @("objetivo", "goal", "outcome")
    if (-not $objectiveSource) { $objectiveSource = "Implementar a feature '$Title' conforme descrito na issue #$IssueNumber." }

    $scopeSection = Get-MarkdownSectionContent -Body $Body -HeadingAliases @("escopo", "scope", "entrega", "implementacao")
    $scopeItems = @()
    if ($scopeSection) {
        $scopeItems = Get-MarkdownBulletItems -Body $scopeSection
    }
    if ($scopeItems.Count -eq 0) {
        $scopeItems = Get-MarkdownChecklistItems -Body $Body
    }
    if ($scopeItems.Count -eq 0) {
        $scopeItems = Get-MarkdownBulletItems -Body $Body
    }

    $nonScopeSection = Get-MarkdownSectionContent -Body $Body -HeadingAliases @("fora de escopo", "nao escopo", "non-scope", "out of scope")
    $nonScopeItems = @()
    if ($nonScopeSection) {
        $nonScopeItems = Get-MarkdownBulletItems -Body $nonScopeSection
    }

    $acceptanceSection = Get-MarkdownSectionContent -Body $Body -HeadingAliases @("criterios de aceitacao", "critérios de aceitação", "acceptance criteria", "definition of done")
    $acceptanceItems = @()
    if ($acceptanceSection) {
        $acceptanceItems = Get-MarkdownChecklistItems -Body $acceptanceSection
        if ($acceptanceItems.Count -eq 0) {
            $acceptanceItems = Get-MarkdownBulletItems -Body $acceptanceSection
        }
    }
    if ($acceptanceItems.Count -eq 0) {
        $acceptanceItems = Get-MarkdownChecklistItems -Body $Body
    }
    if ($acceptanceItems.Count -eq 0 -and $scopeItems.Count -gt 0) {
        $acceptanceItems = $scopeItems | Select-Object -First 3
    }

    $labelsBlock = if ($Labels.Count -gt 0) {
        ($Labels | ForEach-Object { "- Label importada: $_" }) -join "`r`n"
    } else {
        "- Labels ainda nao definidas na issue."
    }

    $functionalItems = @()
    if ($scopeItems.Count -gt 0) {
        $functionalItems = $scopeItems | Select-Object -First 3
    } elseif ($acceptanceItems.Count -gt 0) {
        $functionalItems = $acceptanceItems | Select-Object -First 3
    }

    $functionalBlock = if ($functionalItems.Count -gt 0) {
        @(
            ("- RF01: " + $functionalItems[0])
            $(if ($functionalItems.Count -ge 2) { "- RF02: $($functionalItems[1])" } else { "- RF02: A detalhar" })
            $(if ($functionalItems.Count -ge 3) { "- RF03: $($functionalItems[2])" } else { "- RF03: A detalhar" })
        ) -join "`r`n"
    } else {
        "- RF01: A detalhar`r`n- RF02: A detalhar`r`n- RF03: A detalhar"
    }

    $content = $TemplateContent
    $content = $content.Replace("FXXX", $FeatureId.ToUpperInvariant())
    $content = $content.Replace("Nome da feature", $Title)
    $content = $content.Replace("- Criado em:", "- Criado em: $quotedToday")
    $content = $content.Replace("- Atualizado em:", "- Atualizado em: $quotedToday")
    $content = $content.Replace("- Origem no GitHub:", "- Origem no GitHub: #$IssueNumber - $IssueUrl")

    $content = Set-MarkdownSectionContent -Content $content -Heading "Resumo" -SectionBody (Normalize-Summary -Text $summarySource)
    $content = Set-MarkdownSectionContent -Content $content -Heading "Problema" -SectionBody $problemSource
    $content = Set-MarkdownSectionContent -Content $content -Heading "Objetivo" -SectionBody $objectiveSource
    $content = Set-MarkdownSectionContent -Content $content -Heading "Escopo" -SectionBody (Convert-ToBulletBlock -Items $scopeItems -Fallback "- Escopo inicial importado da issue e ainda precisa de refinamento.")
    $content = Set-MarkdownSectionContent -Content $content -Heading "Fora de Escopo" -SectionBody (Convert-ToBulletBlock -Items $nonScopeItems -Fallback "- Fora de escopo ainda nao explicitado na issue.")
    $content = Set-MarkdownSectionContent -Content $content -Heading "Contexto de Negocio" -SectionBody $labelsBlock
    $content = Set-MarkdownSectionContent -Content $content -Heading "Requisitos Funcionais" -SectionBody $functionalBlock
    $content = Set-MarkdownSectionContent -Content $content -Heading "Criterios de Aceitacao" -SectionBody (Convert-ToAcceptanceCriteriaBlock -Items $acceptanceItems)
    $content = Set-MarkdownSectionContent -Content $content -Heading "Referencias" -SectionBody ("- Issue / Task: #$IssueNumber - $IssueUrl`r`n- PR:`r`n- Documentacao: docs/spec-driven-development.md")
    $content = Set-MarkdownSectionContent -Content $content -Heading "Historico de Decisoes" -SectionBody "- $Today - Spec criada automaticamente a partir da issue #$IssueNumber."

    $importedSection = @"
## Conteudo Importado do GitHub

### Titulo Original

$Title

### Labels

$(if ($Labels.Count -gt 0) { ($Labels | ForEach-Object { "- $_" }) -join [Environment]::NewLine } else { "- Nenhuma label" })

### Descricao Original

$(if ([string]::IsNullOrWhiteSpace($Body)) { "Sem descricao na issue." } else { $Body })
"@

    return $content.TrimEnd() + "`r`n`r`n" + $importedSection.Trim() + "`r`n"
}

function Update-SpecDrivenDocument {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SpecDocPath,

        [Parameter(Mandatory = $true)]
        [string]$FeatureId,

        [Parameter(Mandatory = $true)]
        [string]$Title,

        [Parameter(Mandatory = $true)]
        [string]$Status,

        [Parameter(Mandatory = $true)]
        [string]$Origin,

        [Parameter(Mandatory = $true)]
        [string]$DocumentPath,

        [string]$Summary,

        [string[]]$Labels = @()
    )

    if (-not (Test-Path -LiteralPath $SpecDocPath)) {
        throw "Documento central nao encontrado em '$SpecDocPath'."
    }

    $content = Get-Content -LiteralPath $SpecDocPath -Raw

    $indexPattern = '(?ms)<!-- FEATURES_INDEX_START -->(.*?)<!-- FEATURES_INDEX_END -->'
    $indexMatch = [regex]::Match($content, $indexPattern)
    if (-not $indexMatch.Success) {
        throw "Nao foi possivel localizar o bloco de indice de features."
    }

    $indexLines = @()
    foreach ($line in ($indexMatch.Groups[1].Value -split "\r?\n")) {
        $trimmed = $line.Trim()
        if ($trimmed.StartsWith('|') -and -not $trimmed.StartsWith('| ---')) {
            $indexLines += $trimmed
        }
    }

    $newRow = "| $FeatureId | $Title | $Status | $Origin | ``$DocumentPath`` |"
    $filteredRows = @()
    foreach ($row in $indexLines) {
        if ($row -notmatch "^\|\s*$([regex]::Escape($FeatureId))\s*\|") {
            $filteredRows += $row
        }
    }
    $filteredRows += $newRow

    $sortedRows = $filteredRows | Sort-Object `
        @{ Expression = { Convert-FeatureIdToOrder (($_ -split '\|')[1].Trim()) } }, `
        @{ Expression = { (($_ -split '\|')[1].Trim()) } }

    $indexReplacement = ($sortedRows -join "`r`n")
    $content = Update-MarkedSection `
        -Content $content `
        -StartMarker "<!-- FEATURES_INDEX_START -->" `
        -EndMarker "<!-- FEATURES_INDEX_END -->" `
        -Replacement $indexReplacement

    $contextPattern = '(?ms)<!-- FEATURES_CONTEXT_START -->(.*?)<!-- FEATURES_CONTEXT_END -->'
    $contextMatch = [regex]::Match($content, $contextPattern)
    if (-not $contextMatch.Success) {
        throw "Nao foi possivel localizar o bloco de contexto das features."
    }

    $labelsText = if ($Labels.Count -gt 0) { ($Labels | ForEach-Object { '`' + $_ + '`' }) -join ', ' } else { "nenhuma" }
    $summaryText = Normalize-Summary -Text $Summary
    $contextLines = @(
        "### $FeatureId - $Title",
        "",
        ("- Status: " + '`' + $Status + '`'),
        ("- Origem: " + '`' + $Origin + '`'),
        ("- Documento: " + '`' + $DocumentPath + '`'),
        ("- Labels: " + $labelsText),
        ("- Resumo: " + $summaryText)
    )
    $contextBlock = $contextLines -join "`r`n"

    $existingBlocks = @()
    foreach ($block in (($contextMatch.Groups[1].Value.Trim()) -split "(?=^### )", 0, "Multiline")) {
        $trimmedBlock = $block.Trim()
        if (-not [string]::IsNullOrWhiteSpace($trimmedBlock) -and $trimmedBlock -notmatch "^###\s+$([regex]::Escape($FeatureId))\b") {
            $existingBlocks += $trimmedBlock
        }
    }
    $existingBlocks += $contextBlock.Trim()

    $sortedBlocks = $existingBlocks | Sort-Object `
        @{ Expression = {
            $firstLine = (($_ -split "\r?\n")[0] -replace '^###\s+', '')
            $id = ($firstLine -split '\s+-\s+', 2)[0]
            Convert-FeatureIdToOrder $id
        } }, `
        @{ Expression = {
            $firstLine = (($_ -split "\r?\n")[0] -replace '^###\s+', '')
            ($firstLine -split '\s+-\s+', 2)[0]
        } }

    $contextReplacement = ($sortedBlocks -join "`r`n`r`n")
    $content = Update-MarkedSection `
        -Content $content `
        -StartMarker "<!-- FEATURES_CONTEXT_START -->" `
        -EndMarker "<!-- FEATURES_CONTEXT_END -->" `
        -Replacement $contextReplacement

    Set-Content -LiteralPath $SpecDocPath -Value $content -Encoding UTF8
}
