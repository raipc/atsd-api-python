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

The directory will contain a set of `*.whl` files.

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
cp -r modules/* `python -m site --user-site`
```

Install ATSD client.

```sh
python setup.py install
```

