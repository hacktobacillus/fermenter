Development Setup
=================
install the following on your system:
```
apt-get install python3-dev python3-pip
```

clone with ssh (to be able to edit) and setup venv:
```
git clone git@github.com:hacktobacillus/fermenter.git
```

install virtualenv
```
sudo pip install virtualenv
```

setup the virtualenv
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r --upgrade ./requirements.txt
```


