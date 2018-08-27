# Offline Installation

Install the ATSD Python Client on a machine without internet access. Download the client module and dependencies to an intermediate server and copy the files to the target machine.

## Check Version

Ensure Python versions are the same on the intermediate and the target server:

```sh
python -V
```

## Download Modules

Log in to the intermediate server with internet access.

Download `atsd_client` and dependencies into a temporary folder:

```sh
pip download 'requests>=2.12.1' python-dateutil tzlocal atsd_client -d modules
```

Download `pandas` to use `SQLService` and support transformations from ATSD API client data structures to `pandas` DataFrame.

```sh
pip download pandas -d modules
```

> Upgrade `pip` if the above command fails with error `unknown command "download"`.

The `modules` directory now contains `*.whl`and `*.tar.gz` files:

```sh
ls modules
```

```txt
asn1crypto-0.24.0-py2.py3-none-any.whl          chardet-3.0.4-py2.py3-none-any.whl                      pandas-0.22.0.tar.gz                        requests-2.19.1-py2.py3-none-any.whl
atsd_client-2.2.5-py2.py3-none-any.whl          cryptography-2.2.2-cp34-abi3-manylinux1_x86_64.whl      pycparser-2.18.tar.gz                       six-1.11.0-py2.py3-none-any.whl
certifi-2018.4.16-py2.py3-none-any.whl          idna-2.7-py2.py3-none-any.whl                           pyOpenSSL-18.0.0-py2.py3-none-any.whl       tzlocal-1.5.1.tar.gz
cffi-1.11.5-cp34-cp34m-manylinux1_x86_64.whl    numpy-1.14.5-cp34-cp34m-manylinux1_x86_64.whl           python_dateutil-2.7.3-py2.py3-none-any.whl  urllib3-1.23-py2.py3-none-any.whl
pytz-2018.5-py2.py3-none-any.whl
```

Unpack the downloaded `.whl` modules:

```sh
for i in $(ls modules/*.whl); do unzip "$i" -d modules/; rm -rf "$i"; done;
```

Copy the `modules` directory from the intermediate server to the target server.

## Install Modules on the Target Server

Log in to the target server.

Copy module files to a user module directory. The directory is located at `python -m site --user-site`:

```sh
mkdir -p $(python -m site --user-site) && cd modules && mv $(ls --hide=*.tar.gz) -t $(python -m site --user-site)
```

Install other modules from sources:

```sh
pip install $(ls)
```

Check that the modules are successfully installed:

```sh
python -c "import tzlocal, pandas, requests, dateutil, atsd_client"
```

If `pandas` integration is required, check that `pandas` module is installed:

```sh
python -c "import pandas"
```

An **empty** output corresponds to a successful installation. Otherwise, the output displays an error which describes missing modules.

```python
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ImportError: No module named atsd_client
```

## View Module Versions

```sh
pip list
```

```txt
Package         Version
--------------- ---------
asn1crypto      0.24.0
atsd-client     2.2.5
certifi         2018.4.16
cffi            1.11.5
chardet         3.0.4
cryptography    2.2.2
enum34          1.1.6
idna            2.7
ipaddress       1.0.22
numpy           1.14.5
pandas          0.23.1
pip             10.0.1
pycparser       2.18
pyOpenSSL       18.0.0
python-dateutil 2.7.3
pytz            2018.5
requests        2.19.1
setuptools      39.2.0
six             1.11.0
tzlocal         1.5.1
urllib3         1.23
wheel           0.31.1
```