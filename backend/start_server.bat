@echo off
echo Starting AI Career Path Recommender Backend...
echo.

rem The following command starts the FastAPI server using uvicorn.
rem It specifies the host, port, and enables auto-reload for development.

uvicorn server:app --host 0.0.0.0 --port 8000 --reload

pause
