; GLITCHDEX MALL ENGINE - Windows Installer Script
; Build with: makensis installer.nsi
; Requires: NSIS (https://nsis.sourceforge.io)

!include "MUI2.nsh"

; Basic settings
Name "Glitchdex Mall Engine"
OutFile "dist\glitchdex-mall-installer.exe"
InstallDir "$PROGRAMFILES\GlitchdexMall"
InstallDirRegKey HKCU "Software\GlitchdexMall" "InstallDir"

; MUI Settings
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

; Version info
VIProductVersion "1.0.0.0"
VIAddVersionKey "ProductName" "Glitchdex Mall Engine"
VIAddVersionKey "CompanyName" "GLITCHDEX Collective"
VIAddVersionKey "FileDescription" "A first-person dungeon crawler set in a xennial mall"
VIAddVersionKey "FileVersion" "1.0.0.0"
VIAddVersionKey "ProductVersion" "1.0.0.0"

; Installation section
Section "Install"
  SetOutPath "$INSTDIR"

  ; Copy executable and dependencies
  File /r "dist\glitchdex-mall\*"

  ; Create Start Menu shortcuts
  CreateDirectory "$SMPROGRAMS\GlitchdexMall"
  CreateShortcut "$SMPROGRAMS\GlitchdexMall\Glitchdex Mall.lnk" "$INSTDIR\glitchdex-mall.exe"
  CreateShortcut "$SMPROGRAMS\GlitchdexMall\Uninstall.lnk" "$INSTDIR\uninstall.exe"

  ; Create desktop shortcut
  CreateShortcut "$DESKTOP\Glitchdex Mall.lnk" "$INSTDIR\glitchdex-mall.exe"

  ; Write registry key
  WriteRegStr HKCU "Software\GlitchdexMall" "InstallDir" "$INSTDIR"

  ; Create uninstaller
  WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

; Uninstaller section
Section "Uninstall"
  ; Remove shortcuts
  Delete "$SMPROGRAMS\GlitchdexMall\Glitchdex Mall.lnk"
  Delete "$SMPROGRAMS\GlitchdexMall\Uninstall.lnk"
  RMDir "$SMPROGRAMS\GlitchdexMall"
  Delete "$DESKTOP\Glitchdex Mall.lnk"

  ; Remove installation directory
  RMDir /r "$INSTDIR"

  ; Remove registry key
  DeleteRegKey HKCU "Software\GlitchdexMall"
SectionEnd
