for /r %%f in (*.dsk) do (
	@echo Exporting %%f
	@echo Exporting path %%~pf
	.\dsktool.exe extract * to "%%~pfEXPORTED_FILES" "%%f"
)
