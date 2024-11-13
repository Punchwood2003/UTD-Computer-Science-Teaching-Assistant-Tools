#####################################################################################
# The following script will install all needed dependencies to develop C++ programs #
# locally on a windows machine.                                                     #
#                                                                                   #
# Script Written By: Matthew Sheldon                                                #
#####################################################################################

#Requires -RunAsAdministrator

#####################################################################################
#                 Function to print colored text for conditions                     #
#####################################################################################
function Write-Color {
    param(
        [string]$Text,
        [ConsoleColor]$Color
    )
    $OldColor = $Host.UI.RawUI.ForegroundColor
    $Host.UI.RawUI.ForegroundColor = $Color
    Write-Host $Text
    $Host.UI.RawUI.ForegroundColor = $OldColor
}

#####################################################################################
#                     Function to check if a command exists                         #
#####################################################################################
function CommandExists {
    param([string]$command)
    return (Get-Command $command -ErrorAction SilentlyContinue) -ne $null
}

#####################################################################################
#  Function to check if MinGW is installed by looking for g++ in common locations   #
#####################################################################################
function Check-MingwInstalled {
    if (CommandExists "g++") {
        return $true
    }
    $mingwPaths = @(
        "C:\MinGW\bin\g++.exe", # Standard MinGW path
        "C:\TDM-GCC-64\bin\g++.exe"  # TDM-GCC path
        "C:\ProgramData\mingw64\mingw64\bin\g++.exe" # Installation path when this script is done
    )
    foreach ($path in $mingwPaths) {
        if (Test-Path $path) {
            return $true
        }
    }
    return $false
}

#####################################################################################
#     Function to format JSON in a nicer format than the built-in ConvertTo-Json    #
#####################################################################################
function Format-Json([Parameter(Mandatory, ValueFromPipeline)][String] $json) {
    $indent = 0;
    ($json -Split "`n" | % {
        if ($_ -match '[\}\]]\s*,?\s*$') {
            # This line ends with ] or }, decrement the indentation level
            $indent--
        }
        $line = ('    ' * $indent) + $($_.TrimStart() -replace '":  (["{[])', '": $1' -replace ':  ', ': ')
        if ($_ -match '[\{\[]\s*$') {
            # This line ends with [ or {, increment the indentation level
            $indent++
        }
        $line
    }) -Join "`n"
}

#####################################################################################
#               Function to remove duplicate environment variables                  #
#####################################################################################
function Remove-Duplicate-Environment-Variables {
    # Get the current system (machine) and user environment variables for Path
    $CurrentMPath = [System.Environment]::GetEnvironmentVariable('Path', 'Machine')
    $CurrentUPath = [System.Environment]::GetEnvironmentVariable('Path', 'User')

    # Split both the machine and user Path variables into arrays
    $SortedMPath = $CurrentMPath -split ';' | Sort-Object -Unique
    $SortedUPath = $CurrentUPath -split ';' | Sort-Object -Unique

    # Create a new list for the system Path, excluding duplicates found in the user Path
    $NewMPath = New-Object System.Collections.Generic.List[System.Object]
    ForEach ($x in $SortedMPath) {
        If (-not ($SortedUPath -contains $x)) {
            $NewMPath.Add($x)
        }
    }

    # Join the lists back into strings
    $NewMPath = $NewMPath -Join ';'
    $NewUPath = $SortedUPath -Join ';'

    # Update the path variables
    [System.Environment]::SetEnvironmentVariable('Path', $NewMPath, 'Machine')
    [System.Environment]::SetEnvironmentVariable('Path', $NewUPath, 'User')
}

#####################################################################################
#          Check the installation status of the different dependencies              #
#####################################################################################

# Check installation status
$chocoInstalled = CommandExists "choco.exe"
$mingwInstalled = Check-MingwInstalled
$vscodeInstalled = CommandExists "code"

# Attempt to check if the C++ extensions are installed, handling error silently
$cppExtensionsInstalled = $false
if ($vscodeInstalled) {
    $cppExtensionsInstalled = (code --list-extensions 2>$null | Select-String -Pattern 'ms-vscode.cpptools-extension-pack')
}

# If choco is alrady installed, then check for MinGW and VS Code using Choco as well
if ($chocoInstalled) {
    $mingwInstalled = $mingwInstalled -or (choco list | Select-String -Pattern 'mingw')
    $vscodeInstalled = $vscodeInstalled -or (choco list | Select-String -Pattern 'vscode')
}

# Define the output format
$tabLength = 30

# Output installation statuses
Write-Host "Checking installation statuses..."
$dashes = "-" * ($tabLength + 19) # + 19 for "[Condition Not Met]".length()
Write-Host $dashes

# Chocolatey check
Write-Host "Chocolatey:" -NoNewline
if ($chocoInstalled) {
    $output = " " * ($tabLength - "Chocolatey:".Length) + "[Condition Met]"
    Write-Color $output "Green"
}
else {
    $output = " " * ($tabLength - "Chocolatey:".Length) + "[Condition Not Met]"
    Write-Color $output "Red"
}

# MinGW check
Write-Host "MinGW (GCC Compiler):" -NoNewline
if ($mingwInstalled) {
    $output = " " * ($tabLength - "MinGW (GCC Compiler):".Length) + "[Condition Met]"
    Write-Color $output "Green"
}
else {
    $output = " " * ($tabLength - "MinGW (GCC Compiler):".Length) + "[Condition Not Met]"
    Write-Color $output "Red"
}

# Visual Studio Code check
Write-Host "Visual Studio Code:" -NoNewline
if ($vscodeInstalled) {
    $output = " " * ($tabLength - "Visual Studio Code:".Length) + "[Condition Met]"
    Write-Color $output "Green"
}
else {
    $output = " " * ($tabLength - "Visual Studio Code:".Length) + "[Condition Not Met]"
    Write-Color $output "Red"
}

# VSCode C++ Extensions check
Write-Host "VSCode C++ Extensions:" -NoNewline
if ($cppExtensionsInstalled) {
    $output = " " * ($tabLength - "VSCode C++ Extensions:".Length) + "[Condition Met]"
    Write-Color $output "Green"
}
else {
    $output = " " * ($tabLength - "VSCode C++ Extensions:".Length) + "[Condition Not Met]"
    Write-Color $output "Red"
}

Write-Host $dashes
Write-Host ""

#####################################################################################
#         Give the user some time to read the output of the initial search          #
#####################################################################################

# Pause for 3 seconds
Start-Sleep -Seconds 3

# Enable execution of PowerShell scripts
Set-ExecutionPolicy Bypass -Scope Process -Force

#####################################################################################
#                             Install the missing dependencies                      #
#####################################################################################

# Install Chocolatey if not already installed
if (-not $chocoInstalled) {
    Write-Host "Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    $env:PATH += ";C:\ProgramData\chocolatey\bin"
}
else {
    Write-Host "Chocolatey already installed."
}


# Install MinGW for GCC C++ Compiler if not already installed
if (-not $mingwInstalled) {
    Write-Host "Installing MinGW..."
    choco install mingw -y
    $mingwPath = "C:\ProgramData\chocolatey\lib\mingw\tools\install\mingw64\bin"
    $env:PATH += ";C:\ProgramData\mingw64\mingw64\bin"
}
else {
    Write-Host "MinGW already installed."
}


# Install Visual Studio Code if not already installed
if (-not $vscodeInstalled) {
    Write-Host "Installing Visual Studio Code..."
    choco install vscode -y
    # Add VS Code path to the environment variable
    $vscodePath = "C:\Program Files\Microsoft VS Code\bin"
    $env:PATH += ";$vscodePath"
}
else {
    Write-Host "Visual Studio Code already installed."
}


# Install Visual Studio Code C++ extensions if not already installed
if (-not $cppExtensionsInstalled) {
    Write-Host "Installing Visual Studio Code C++ extensions..."
    code --install-extension ms-vscode.cpptools-extension-pack
}
else {
    Write-Host "C++ extensions already installed."
}

# Updating path reference
[Environment]::SetEnvironmentVariable("Path", $env:PATH, [EnvironmentVariableTarget]::Machine)
# Remove duplicate environment variables
Remove-Duplicate-Environment-Variables

#####################################################################################
#                 Add the formatting guide for C/C++ code to VS Code                #
#####################################################################################

# Path to VS Code's settings.json file
$vsCodeSettingsPath = "$env:APPDATA\Code\User\settings.json"

# Directory of the .clang-format file
$clangFormatFileDirectory = "$env:USERPROFILE\Documents\VS Code\"

# Path to store the .clang-format file
$clangFormatFilePath = "$clangFormatFileDirectory.clang-format"

# Check if settings.json exists
$vsCodeSettings = $null
if (Test-Path $vsCodeSettingsPath) {
    try {
        # Attempt to read and parse the settings.json file
        $vsCodeSettings = Get-Content -Raw $vsCodeSettingsPath | ConvertFrom-Json
    }
    catch {
        # If the file is not valid JSON, initialize an empty hashtable
        Write-Warning "Invalid JSON in settings.json. Initializing a new settings object."
        $vsCodeSettings = @{}
    }
}
else {
    # If the file doesn't exist, initialize an empty hashtable
    Write-Warning "settings.json not found. Initializing a new settings object."
    $vsCodeSettings = @{}
}

# Define the new C++ formatting rules
$cppFormattingRules = @"
---
BasedOnStyle: Google                             # Start with Google style as a base
ColumnLimit: 80                                  # Limit lines to 80 characters
IndentWidth: 4                                   # Use 4 spaces for indentation
UseTab: Never                                    # Always use spaces, not tabs
AlignTrailingComments: true                      # Align trailing comments
BreakBeforeBraces: Allman                        # Align braces vertically
IndentCaseLabels: true                           # Indent case labels in switch statements
AllowShortIfStatementsOnASingleLine: false       # One statement per line
AllowShortLoopsOnASingleLine: false              # One statement per line
AlignOperands: true                              # Align operators for better readability
IndentWrappedFunctionNames: true                 # Indent wrapped long statements
BreakConstructorInitializersBeforeComma: true    # Format constructor initializers
---
"@

# Create the directory if it is not already present
if (-not (Test-Path $clangFormatFileDirectory)) {
    New-Item -Path $clangFormatFileDirectory -ItemType Directory | Out-Null
}

# Write the .clang-format file with the defined rules
if (!(Test-Path $clangFormatFilePath)) {
    $clangFormatFilePath | Out-File -FilePath $clangFormatFilePath -Force | Out-Null
}
$cppFormattingRules | Set-Content -Path $clangFormatFilePath | Out-Null

# Update the reference
if ($vsCodeSettings.psobject.properties.match('C_Cpp.clang_format_style').Count) {
    $vsCodeSettings."C_Cpp.clang_format_style" = "file:$clangFormatFilePath".Replace('\', '/') | Out-Null
}
else {
    Add-Member -InputObject $vsCodeSettings -NotePropertyName "C_Cpp.clang_format_style" -NotePropertyValue "file:$clangFormatFilePath".Replace('\', '/') | Out-Null
}

# Add format on save
if ($vsCodeSettings.psobject.properties.match('editor.formatOnSave').Count) {
    $vsCodeSettings."editor.formatOnSave" = $true
}
else {
    Add-Member -InputObject $vsCodeSettings -NotePropertyName "editor.formatOnSave" -NotePropertyValue $true | Out-Null
}

# Convert the updated settings back to JSON format
$updatedSettings = $vsCodeSettings | ConvertTo-Json -Depth 10 | Format-Json

# Ensure the directory exists before writing the file
$settingsDir = Split-Path $vsCodeSettingsPath
if (!(Test-Path $settingsDir)) {
    New-Item -ItemType Directory -Path $settingsDir
}

# Write the updated settings back to the settings.json file
$updatedSettings | Set-Content -Path $vsCodeSettingsPath

Write-Host "VS Code settings updated with C++ formatting rules."

#####################################################################################
#                                End of program prompt                              #
#####################################################################################

# Confirm installation
Write-Host
Write-Color "C++ development environment setup is complete!" "Green"
