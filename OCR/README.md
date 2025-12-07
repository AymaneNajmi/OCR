# OCR Project

This repository contains a local OCR project workspace. It was scaffolded by an assistant and contains a Python virtual environment at `.venv` (if present) and any project files you add.

Getting started (recommended):

1. Open PowerShell and temporarily allow script execution for this session (safe):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Or use the batch activation in Command Prompt:

```cmd
cd "C:\Users\Administrateur\Documents\OCR"
.venv\Scripts\activate.bat
```

2. Install dependencies (if `requirements.txt` exists):

```powershell
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Notes:
- The folder currently contains a virtual environment at `.venv`. Files under `.venv` are ignored by `.gitignore` by default. If you have data files inside the `.venv` folder (for example a CSV), consider moving them to a `data/` directory so they are tracked by git and not removed when recreating the venv.
- To push this repo to GitHub, provide the remote repository URL (HTTPS or SSH) and I can run the push for you, or follow the commands below:

```powershell
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

If you want me to create the remote GitHub repo for you, tell me whether you have the GitHub CLI (`gh`) installed and authenticated, or share the repo URL.
