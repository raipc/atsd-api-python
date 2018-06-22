# Offline Installation

The document describes how ATSD Python client can be installed on a machine without internet access. The process involves downloading the client module and its dependencies to an intermediate server from which the files can be copied to the target machine.

## Check Version

Compare Python versions on the intermediate and the target server.

```sh
python --version
```

If the versions are the same, execute the steps described in [Install using `pip`](#install-using-pip) section.
If the versions are different, proceed to [Install from Prepared Modules](#install-from-prepared-modules) section.

## Install using `pip`

### Download Modules

Log in to the intermediate server with internet access.

Download the `atsd_client` source code.

```sh
curl -OL https://github.com/axibase/atsd-api-python/archive/master.zip; \
unzip master.zip; rm master.zip; mv atsd-api-python-master atsd-api-python
```

Download required Python modules (dependencies) into a temporary folder.

```sh
mkdir modules
```

```sh
pip download 'requests>=2.12.1' python-dateutil pandas tzlocal -d modules
```

> Upgrade `pip` if the above command fails with error `unknown command "download"`.

Check Python version.

```sh
python -V
```

If the version is less than **2.7.9** download additional modules.

```sh
pip download pyOpenSSL idna -d modules
```

The `modules` directory now contains `*.whl`and `*.tar.gz` files.

```sh
ls modules
```

```txt
asn1crypto-0.23.0-py2.py3-none-any.whl                  enum34-1.1.6-py2-none-any.whl                           pyOpenSSL-17.3.0-py2.py3-none-any.whl                   six-1.11.0-py2.py3-none-any.whl
certifi-2017.7.27.1-py2.py3-none-any.whl                idna-2.6-py2.py3-none-any.whl                           pycparser-2.18.tar.gz                                   tzlocal-1.4.tar.gz
cffi-1.11.1-cp27-cp27mu-manylinux1_x86_64.whl           ipaddress-1.0.18-py2-none-any.whl                       python_dateutil-2.6.1-py2.py3-none-any.whl              urllib3-1.22-py2.py3-none-any.whl
chardet-3.0.4-py2.py3-none-any.whl                      numpy-1.13.3-cp27-cp27mu-manylinux1_x86_64.whl          pytz-2017.2-py2.py3-none-any.whl
cryptography-2.0.3-cp27-cp27mu-manylinux1_x86_64.whl    pandas-0.20.3-cp27-cp27mu-manylinux1_x86_64.whl         requests-2.18.4-py2.py3-none-any.whl
```

Unpack the downloaded `.whl` modules.

```sh
for i in `ls modules/*.whl`; do unzip "$i" -d modules/; rm -rf "$i"; done;
```

Unpack the downloaded `.tar.gz` modules.

```sh
for i in `ls modules/*.tar.gz`; do tar -xvf "$i" -C modules/; rm -rf "$i"; done;
```

Copy the `atsd-api-python` and `modules` directories from the intermediate server to the target server.

## Install Modules on the Target Server

Log in to the target server where the ATSD client is being installed.

Copy module files to a user module directory. The directory is located at `python -m site --user-site`.

```sh
mkdir -p `python -m site --user-site` && cp -r modules/. `python -m site --user-site`
```

Install ATSD client.

```sh
python atsd-api-python/setup.py install
```

Check that the modules have been installed successfully.

```sh
python -c "import atsd_client, pandas, requests, dateutil"
```

The output is **empty** if all modules are installed correctly. Otherwise, an error is displayed showing which modules are missing.

```python
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ImportError: No module named atsd_client
```

## Install From Prepared Modules

Copy the [ATSD client module](https://github.com/axibase/atsd-api-python/archive/master.zip) to the target server.

```sh
unzip master.zip; rm master.zip; mv atsd-api-python-master atsd-api-python
```

Copy the [archive with dependencies](https://axibase.com/public/python/modules.tar.gz) to the target server.

Unpack the modules archive.

```sh
tar -xvf modules.tar.gz
```

Copy module files to a user module directory located at `python -m site --user-site`.

```sh
mkdir -p `python -m site --user-site` && cp -r modules/. `python -m site --user-site`
```

Install ATSD client.

```sh
python atsd-api-python/setup.py install
```

Check that the modules have been installed successfully.

```sh
python -c "import atsd_client, pandas, requests, dateutil"
```

The output is empty if all modules are installed correctly. Otherwise, an error is displayed showing which modules are missing.

```python
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ImportError: No module named atsd_client
```

References:

* [`pip download` parameters](https://pip.pypa.io/en/stable/reference/pip_download/)
* [Pandas Versions](http://pandas.pydata.org/)

## View Module Versions

```sh
pip list
```

```txt
Package             Version
------------------- ------------------
asn1crypto          0.24.0
atsd-client         2.2.2
certifi             2018.4.16
cffi                1.11.5
chardet             3.0.4
colorama            0.2.5
cryptography        2.2.2
duplicity           0.6.23
enum34              1.1.6
html5lib            0.999
idna                2.6
ipaddress           1.0.22
lockfile            0.8
numpy               1.14.3
pandas              0.23.0
pip                 10.0.1
pycrypto            2.6.1
pycurl              7.19.3
pyliblzma           0.5.3
pyOpenSSL           17.5.0
pysqlite            1.0.1
python-apt          0.9.3.5ubuntu2
python-dateutil     2.7.3
python-debian       0.1.21-nmu2ubuntu2
pytz                2018.4
requests            2.18.4
setuptools          33.1.1
sh                  1.12.14
six                 1.11.0
ssh-import-id       3.21
urlgrabber          3.9.1
urllib3             1.22
virtualenv          1.11.4
wheel               0.24.0
yum-metadata-parser 1.1.4
```
