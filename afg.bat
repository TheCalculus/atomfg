@echo off
setlocal enabledelayedexpansion

REM ANIMATION FRAME GENERATOR (afg)
REM gotta give fancy names even to lazy tools

for /L %%x in (1, 1, 10) do (
    set /a y=%%x - 1
    python main.py 1.054718e-34 9.10938356e-31 25 1 True 21.5 45 %%x !y! 0 0
)

endlocal
