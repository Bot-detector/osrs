# development
## setup
```
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
## for admin purposes saving & upgrading

```
venv\Scripts\activate
call pip freeze > requirements.txt
powershell "(Get-Content requirements.txt) | ForEach-Object { $_ -replace '==', '>=' } | Set-Content requirements.txt"
call pip install -r requirements.txt --upgrade
call pip freeze > requirements.txt
powershell "(Get-Content requirements.txt) | ForEach-Object { $_ -replace '>=', '==' } | Set-Content requirements.txt"
```
## build & publish
building package and deploying to pypi
https://packaging.python.org/en/latest/tutorials/packaging-projects/
```
python -m pip install --upgrade build
python -m build
python -m pip install --upgrade twine
twine upload dist/*
```