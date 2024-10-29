for %%f in (*.src) do (
	@echo Processing %%f
	.\detoken "%%f" -einz80 > "%%f".TXT"
)
for %%f in (*.bak) do (
	@echo Processing %%f
	.\detoken "%%f" -einz80 > "%%f".TXT
)
