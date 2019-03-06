# Offline Installation

The document describes how to install **ATSD Python Client** on a server which is not connected to the Internet. Access to the Internet is required to download Python modules such as `dateutil`, `requests`, and `pandas` upon which the ATSD client depends on.

The process involves copying the modules to an intermediate server which is connected to the Internet and subsequently copying the downloaded files to the disconnected (target) server to install the ATSD client and dependencies.

## Check Versions

Check Python version on both the intermediate and the target servers.

```sh
python3 -V
```

```txt
Python 3.5.2
```

The reported Python version must be `3.5` or later and it must **the same** on both servers. The servers must also have the same processor architecture (both 64-bit).

Check [`pip`](https://pypi.org/project/pip/) version. `pip3` is the package installer for Python `3`.

```sh
pip3 -V
```

```txt
pip 8.1.1 from /usr/lib/python3/dist-packages (python 3.5)
```

If the `pip3` command is not found, install `pip3` for Python `3.5` or later.

If necessary, upgrade the `pip3` program.

```bash
pip3 install --upgrade pip
```

## Download Modules

Log in to the intermediate server with internet access.

Create a temporary `modules` directory in the user's home.

```bash
mkdir /tmp/modules
```

Download `atsd_client` and dependencies to the `/tmp/modules` directory.

```sh
pip3 download 'requests>=2.12.1' python-dateutil tzlocal pandas atsd_client -d /tmp/modules
```

If the `pip3` command is not found, install the `pip3`.

```txt
Collecting requests>=2.12.1
  Downloading https://files.pythonhosted.org/packages/7d/e3/20f3d364d6c8e5d2353c72a67778eb189176f08e873c9900e10c0287b84b/requests-2.21.0-py2.py3-none-any.whl (57kB)
    100% |████████████████████████████████| 61kB 396kB/s
...
Successfully downloaded requests python-dateutil tzlocal pandas atsd-client idna certifi urllib3 chardet six pytz numpy
```

> Upgrade `pip3` if the above command fails with error `unknown command "download"`.

Check that the `/tmp/modules` directory contains `*.whl` and `*.tar.gz` files.

```sh
ls /tmp/modules
```

```txt
atsd_client-3.0.2-py3-none-any.whl
certifi-2018.11.29-py2.py3-none-any.whl
chardet-3.0.4-py2.py3-none-any.whl
idna-2.8-py2.py3-none-any.whl
numpy-1.16.2-cp35-cp35m-manylinux1_x86_64.whl
pandas-0.24.1-cp35-cp35m-manylinux1_x86_64.whl
python_dateutil-2.8.0-py2.py3-none-any.whl
pytz-2018.9-py2.py3-none-any.whl
requests-2.21.0-py2.py3-none-any.whl
six-1.12.0-py2.py3-none-any.whl
tzlocal-1.5.1.tar.gz
urllib3-1.24.1-py2.py3-none-any.whl
```

Unpack the downloaded `.whl` archives.

```sh
unzip '/tmp/modules/*.whl' -d /tmp/modules/ && rm /tmp/modules/*.whl
```

Check the contents of the `/tmp/modules` directory.

```sh
ls /tmp/modules
```

```txt
atsd_client                   pandas-0.24.1.dist-info
atsd_client-3.0.2.dist-info   python_dateutil-2.8.0.dist-info
certifi                       pytz
certifi-2018.11.29.dist-info  pytz-2018.9.dist-info
chardet                       requests
chardet-3.0.4.dist-info       requests-2.21.0.dist-info
dateutil                      six-1.12.0.dist-info
idna                          six.py
idna-2.8.dist-info            tzlocal-1.5.1.tar.gz
numpy                         urllib3
numpy-1.16.2.dist-info        urllib3-1.24.1.dist-info
pandas
```

Copy the `/tmp/modules` directory to the target server.

## Install Modules on the Target Server

Log in to the target server.

You must execute the below steps under the same user as executing ATSD Python scripts.

```sh
su axibase
```

Check that the `/tmp/modules` copied from the intermediate server contains the same files.

```sh
ls /tmp/modules
```

These files must be now copied to the user's Python module directory. The directory location can be determined as follows.

```sh
python3 -m site --user-site
```

```txt
/home/axibase/.local/lib/python3.5/site-packages
```

Check the contents of the directory.

```sh
ls $(python3 -m site --user-site)
```

The directory can be nonexistent. Create it if needed.

```txt
ls: cannot access '/home/axibase/.local/lib/python3.5/site-packages: No such file or directory
```

```sh
mkdir -p $(python3 -m site --user-site)
```

Copy the modules files from `/tmp/modules` directory to the `user-site` directory.

```sh
cp -r /tmp/modules/* -t $(python3 -m site --user-site)
```

Check that the `user-site` directory contains the same files as `/tmp/modules`.

```sh
ls $(python3 -m site --user-site)
```

```txt
atsd_client                   idna-2.8.dist-info               requests
atsd_client-3.0.2.dist-info   numpy                            requests-2.21.0.dist-info
certifi                       numpy-1.16.2.dist-info           six-1.12.0.dist-info
certifi-2018.11.29.dist-info  pandas                           six.py
chardet                       pandas-0.24.1.dist-info          tzlocal-1.5.1.tar.gz
chardet-3.0.4.dist-info       python_dateutil-2.8.0.dist-info  urllib3
dateutil                      pytz                             urllib3-1.24.1.dist-info
idna                          pytz-2018.9.dist-info
```

Install `tzlocal-1.5.1.tar.gz` module from sources.

```sh
pip3 install --no-deps /tmp/modules/tzlocal-1.5.1.tar.gz
```

> If this command fails with message `sudo: pip: command not found`, execute `python3 -m pip install --no-deps /tmp/modules/tzlocal-1.5.1.tar.gz`

Check that the modules are successfully installed.

```sh
python3 -c "import tzlocal, pandas, requests, dateutil, atsd_client"
```

An **empty** output indicates a successful installation. Otherwise, the output displays an error which describes missing modules.

```python
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ImportError: No module named atsd_client
```

## View Module Versions

```sh
pip3 list
```

```txt
atsd-client (3.0.2)
certifi (2018.11.29)
chardet (3.0.4)
idna (2.8)
numpy (1.16.2)
pandas (0.24.1)
pip (8.1.1)
python-dateutil (2.8.0)
pytz (2018.9)
requests (2.21.0)
setuptools (20.7.0)
six (1.12.0)
tzlocal (1.5.1)
urllib3 (1.24.1)
wheel (0.29.0)
```