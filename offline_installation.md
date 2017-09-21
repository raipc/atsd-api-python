### Check environment

* Login into offline machine

* Find out path that holds locally-installed packages:

```
python -m site --user-site | xargs stat
```

If it doesnt't exist create:
```
python -m site --user-site | xargs mkdir -p
```


### Download atsd_client and required modules

* Login into machine with internet access

* Download atsd_client sources:

```
git clone https://github.com/axibase/atsd-api-python.git
# or curl -OL https://github.com/axibase/atsd-api-python/archive/master.zip; unzip master.zip; rm master.zip; mv atsd-api-python-master atsd-api-python

```

* Prepare requirements list:

```
cat <<EOF >> requirements.txt
requests[security]
python-dateutil
pytz
EOF
```

* Download required modules into temporary folder

```
mkdir modules
pip install --download ./modules -r requirements.txt
```

* Unpack modules to be able to use on offline machine:

```
cd modules
for i in `ls *.whl`; do unzip "$i"; rm "$i"; done;
for i in `ls *.tar.gz`; do tar -xvf "$i"; rm "$i"; done;
```

### Transfer required modules

* Transfer `modules/*` to offline machine folder that holds locally-installed packages
* Transfer `atsd-api-python` to offline machine to install latest client version


### Install modules

* Login into offline machine

* Install `atsd_client`

```
cd atsd-api-python
python setup.py install
```
