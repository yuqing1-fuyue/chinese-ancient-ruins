@echo off
chcp 65001 > nul
title 中华古址智鉴 - 启动服务
echo.
echo ╔══════════════════════════════════════════╗
echo ║       中华古址智鉴  启动脚本              ║
echo ╚══════════════════════════════════════════╝
echo.

:: ── 步骤1：检查 Python ──────────────────────────────
echo [1/3] 检查 Python...
python --version 2>nul
if errorlevel 1 (
    echo  未检测到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

:: ── 步骤2：检查依赖是否已安装（只验证核心包）──────────
echo.
echo [2/3] 检查依赖...
python -c "import fastapi, uvicorn" 2>nul
if errorlevel 1 (
    echo  首次运行 / 依赖缺失，正在安装...
    pip install -r requirements.txt -q
    if errorlevel 1 (
        echo  依赖安装失败，请检查网络或手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo  依赖安装完成！
) else (
    echo  依赖已就绪，跳过安装
)

:: ── 步骤3：启动服务 ────────────────────────────────
echo.
echo [3/3] 启动后端服务（端口 8000）...
echo  浏览器访问: http://127.0.0.1:8080
echo  按 Ctrl+C 可停止服务
echo.
python main.py
pause
