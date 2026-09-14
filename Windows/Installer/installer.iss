; Inno Setup Script for AI RAT Detection Dashboard
[Setup]
AppId={{C5369A18-8687-4B3B-864B-87146522EA76}}
AppName=AI RAT Detection Dashboard
AppVersion=1.0.0
AppPublisher=AI RAT Detection Dashboard Project
DefaultDirName={autopf}\AI RAT Detection Dashboard
DefaultGroupName=AI RAT Detection Dashboard
OutputDir=.
OutputBaseFilename=AI-RAT-Detection-Dashboard-Setup
SetupIconFile=..\..\Core\assets\icon.ico
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\Portable\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "*.zip"

[Icons]
Name: "{group}\AI RAT Detection Dashboard"; Filename: "{app}\AI-RAT-Detection-Dashboard.exe"; IconFilename: "{app}\assets\icon.ico"
Name: "{autodesktop}\AI RAT Detection Dashboard"; Filename: "{app}\AI-RAT-Detection-Dashboard.exe"; IconFilename: "{app}\assets\icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\AI-RAT-Detection-Dashboard.exe"; Description: "{cm:LaunchProgram,AI RAT Detection Dashboard}"; Flags: nowait postinstall skipifsilent