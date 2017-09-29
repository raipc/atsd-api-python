# Offline Installation

The document describes how ATSD Python client can be installed on a machine without internet access. The process involves downloading the module and its dependencies to an intermediate server from which the files are then copied to the target machine.

## Download Modules

Login into the server with internet access.

Download the `atsd_client` source code.

```
curl -OL https://github.com/axibase/atsd-api-python/archive/master.zip; \
unzip master.zip; rm master.zip; mv atsd-api-python-master atsd-api-python
# git clone https://github.com/axibase/atsd-api-python.git
```

```
cd atsd-api-python
```

Create a `requirements.txt` file containing the list of required modules (dependencies).

```
requests>=2.12.1
python-dateutil
pandas
```

Download the modules specified in the `requirements.txt` file into a temporary folder.

> If your python version and os are different from the target server proceed to [Download modules for different systems](#Download-modules-for-different-systems)

```sh
mkdir modules
pip download -r requirements.txt -d modules
```

If your python version is less than 2.7.9 download in addition:
```
pip download pyOpenSSL idna -d modules  
```

The directory will contain a set of `*.whl`and `*.tar.gz` files.

```sh
asn1crypto-0.23.0-py2.py3-none-any.whl                  enum34-1.1.6-py2-none-any.whl                           pyOpenSSL-17.3.0-py2.py3-none-any.whl                   six-1.11.0-py2.py3-none-any.whl
certifi-2017.7.27.1-py2.py3-none-any.whl                idna-2.6-py2.py3-none-any.whl                           pycparser-2.18.tar.gz                                   urllib3-1.22-py2.py3-none-any.whl
cffi-1.11.0-cp27-cp27m-manylinux1_x86_64.whl            ipaddress-1.0.18-py2-none-any.whl                       python_dateutil-2.6.1-py2.py3-none-any.whl
chardet-3.0.4-py2.py3-none-any.whl                      numpy-1.13.1-cp27-cp27m-manylinux1_x86_64.whl           pytz-2017.2-py2.py3-none-any.whl
cryptography-2.0.3-cp27-cp27m-manylinux1_x86_64.whl     pandas-0.20.3-cp27-cp27m-manylinux1_x86_64.whl          requests-2.18.4-py2.py3-none-any.whl
```

Unpack the downloaded modules.

```
cd modules
for i in `ls *.whl`; do unzip "$i"; rm "$i"; done;
for i in `ls *.tar.gz`; do tar -xvf "$i"; rm "$i"; done;
```

Copy the `atsd-api-python` directory from the connected server to the target machine.

## Install Modules to the Target Machine

Login into the target server where the ATSD client will be installed.

Change to the `atsd-api-python` directory copied before.

```sh
cd atsd-api-python
```

Copy the previously downloaded modules to a corresponding directory on the target machine.

```sh
mkdir -p `python -m site --user-site` && cp -r modules/* `python -m site --user-site`
```

Install ATSD client.

```sh
python setup.py install
```

Check that the modules have been installed successfully.

```sh
python -c "import atsd_client, pandas, requests, dateutil"
```

The output will be empty if all modules are installed correctly. Otherwise, an error will be displayed showing which modules are missing.

```python
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ImportError: No module named atsd_client
```


### Download modules for different systems 

To fetch dependencies for an interpreter and system other than the ones that pip is running on 

run `pip download` with the `--platform`, `--python-version`, `--implementation` and `--abi` options (more [details](https://pip.pypa.io/en/stable/reference/pip_download/)).

These options set by default to the current system/interpreter. Current list of available option values in [PyPI](https://pypi.python.org/pypi):

|**Option**|**Value**|
|:---|:---|
| platform |win32, win_amd64, manylinux1_i686, manylinux1_x86_64, macosx_10_6_intel, macosx_10_6_intel, macosx_10_9_intel, macosx_10_9_x86_64, macosx_10_10_intel, macosx_10_10_x86_64|
| python-version(abi) |27(27m), 34(34m), 35(35m), 36(36m)|
 
Note that python-version corresponds to concatenated `Python -V` command first two digits.

For example for linux_x86_64 machine with python 2.7.x

```
pip download -r requirements.txt -d modules --only-binary=:all: --platform manylinux1_x86_64 --python-version 27 --implementation cp --abi cp27m
pip download pyOpenSSL idna      -d modules --only-binary=:all: --platform manylinux1_x86_64 --python-version 27 --implementation cp --abi cp27m
pip download pycparser           -d modules
```

If your python version is less than 2.7 or you have not find appropriate modules try to find out them on [PyPI](https://pypi.python.org/pypi)

or use machine with same os and python interpreter.
