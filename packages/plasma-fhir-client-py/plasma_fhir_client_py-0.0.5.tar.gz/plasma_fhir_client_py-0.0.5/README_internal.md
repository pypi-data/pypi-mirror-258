# plasma-fhir-client-py



## Publishing to PIP
For more detailed instructions, follow the guide here: https://packaging.python.org/en/latest/tutorials/packaging-projects/

1. Delete `/dist`
2. Update version in `__init__.py`
3. Build the project: `python3 -m build`
4. Upload archives: `python3 -m twine upload --repository pypi dist/*`