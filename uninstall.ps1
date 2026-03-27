# Claude Keitaro Uninstaller for Windows PowerShell

Write-Host "Uninstalling Claude Keitaro..."

Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\keitaro" -ErrorAction SilentlyContinue

@("keitaro-setup","keitaro-campaigns","keitaro-flows","keitaro-reports","keitaro-optimize","keitaro-landing","keitaro-audit") | ForEach-Object {
    Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\$_" -ErrorAction SilentlyContinue
}

@("campaign-analyzer","flow-optimizer","landing-generator") | ForEach-Object {
    Remove-Item -Force "$env:USERPROFILE\.claude\agents\$_.md" -ErrorAction SilentlyContinue
}

Write-Host "Claude Keitaro uninstalled."
