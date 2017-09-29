# Offline Installation

The document describes how ATSD Python client can be installed on a machine without internet access. The process involves downloading the module and its dependencies to an intermediate server from which the files are then copied to the target machine. The intermediate server should have the same Python version and operating system type as the target server.

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

Download required modules (dependencies) into a temporary folder.

> If your python version and os are different from the target server proceed to [Download Platform-Dependent Module](#download-platform-dependent-module)

```sh
mkdir modules
pip download 'requests>=2.12.1' python-dateutil pandas -d modules
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

## Install Modules on the Target Server

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


### Download Platform-Dependent Module

If the Python version and operating system type are different on the intermediate server, download `pandas` module by specifying the target platform explicitly. 

* Python 2.7 Linux x86_64 Example

```
pip download pandas -d modules --only-binary=:all: --platform manylinux1_x86_64 --python-version 27 --implementation cp --abi cp27m
```

For python version less than 2.7 pandas has to be built from sources.

References:

* [`pip download` parameters](https://pip.pypa.io/en/stable/reference/pip_download/)
* [Pandas Versions](http://pandas.pydata.org/)
