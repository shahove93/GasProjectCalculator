; Inno Setup script for the GasProjectCalculator desktop application.
;
; Per-user installation (no administrator rights / no UAC where possible),
; installing the PyInstaller onedir output from dist\GasProjectCalculator.
; User data (logs, settings) is written by the application to
; %LOCALAPPDATA%\GasProjectCalculator, which is outside {app}; uninstalling
; therefore never removes user-created files.
;
; Build with: powershell -ExecutionPolicy Bypass -File installer\build-installer.ps1

#define AppName "GasProjectCalculator"
#define AppVersion "1.0.0"
#define AppPublisher "GasProjectCalculator"
#define AppExeName "GasProjectCalculator.exe"

[Setup]
AppId={{A3E4B6C1-7F2D-4B8E-9C1A-5D6E7F8091A2}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
VersionInfoVersion=1.0.0.0
DefaultDirName={localappdata}\Programs\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
; Per-user install: no admin rights, no UAC prompt.
PrivilegesRequired=lowest
; The application is a Windows x64 build; refuse a 32-bit target.
ArchitecturesAllowed=x64compatible
OutputDir=Output
OutputBaseFilename=GasProjectCalculator-Setup-{#AppVersion}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
UninstallDisplayName={#AppName}
UninstallDisplayIcon={app}\{#AppExeName}
CloseApplications=no
SetupLogging=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
; Optional desktop shortcut, unchecked by default. The Start Menu shortcut is
; always installed through the [Icons] section below.
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
; Copy the complete PyInstaller onedir tree (exe + _internal dependencies).
Source: "..\dist\GasProjectCalculator\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start Menu shortcut: always created for the current user.
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"; WorkingDir: "{app}"
; Desktop shortcut: only when the optional task is selected.
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent

; No [UninstallDelete] entries: Setup removes only the program files it
; installed. User-created files and the %LOCALAPPDATA%\GasProjectCalculator
; data directory are left untouched.
