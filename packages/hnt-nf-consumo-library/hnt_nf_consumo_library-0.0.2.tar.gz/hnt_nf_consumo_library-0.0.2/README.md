

virtualenv venv
. ./venv/bin/activate
pip install --upgrade pip
pip install pytest
pip install requests
pip install python-dotenv





# How to cleanup generated files to publish
```sh
rm -r build dist hnt_nf_consumo_library.egg-info
```

```powershell
Remove-Item .\build\ -Force -Recurse
Remove-Item .\dist\ -Force -Recurse
Remove-Item .\hnt_sap_nota_pedido_library.egg-info\ -Force -Recurse
```

# How to publish the package to test.pypi.org
```sh
python setup.py sdist bdist_wheel
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

# How to publish the package to pypi.org (username/password see lastpass Pypi)
```sh
python setup.py sdist bdist_wheel
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```