## Prerequisites
Install the following packages using pip.
```bash
pip install twine
pip install build
pip install poetry
```

## Build and Publish
To build the package, run the following command in the root directory of the project.
```bash
.\publish
```

It will prompt you to enter your username and password for PyPl. After entering the credentials, the files will be uploaded to PyPl.

If you want to set it up to not ask for your credentials every time, create a file called `.pypirc` in your home directory and add the following content to it.
```pypirc
[pypi]
username = __token__
password = pypi-<your-token>
```
