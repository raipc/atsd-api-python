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
requests[security]
python-dateutil
pytz
```

Download the modules specified in the `requirements.txt` file into a temporary folder.

```sh
mkdir modules
pip install --download ./modules -r requirements.txt
```

The directory will contain a set of `*.whl`and `*.tar.gz` files.

```sh
asn1crypto-0.22.0-py2.py3-none-any.whl                  cryptography-2.0.3-cp27-cp27m-macosx_10_6_intel.whl     pyOpenSSL-17.3.0-py2.py3-none-any.whl                   requests-2.18.4-py2.py3-none-any.whl
certifi-2017.7.27.1-py2.py3-none-any.whl                enum34-1.1.6-py2-none-any.whl                           pycparser-2.18.tar.gz                                   six-1.11.0-py2.py3-none-any.whl
cffi-1.11.0-cp27-cp27m-macosx_10_6_intel.whl            idna-2.6-py2.py3-none-any.whl                           python_dateutil-2.6.1-py2.py3-none-any.whl              urllib3-1.22-py2.py3-none-any.whl
chardet-3.0.4-py2.py3-none-any.whl                      ipaddress-1.0.18-py2-none-any.whl                       pytz-2017.2-py2.py3-none-any.whl
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

Copy the previously downloaded modules to a corresponding directory on the local machine.

```sh
mkdir -p `python -m site --user-site` && cp -r modules/* `python -m site --user-site`
```

Install ATSD client.

```sh
python setup.py install
```

