# application vote en ligne

## Création d'un environnement virtuel sous windows

```
C:\PythonXX\Python -m venv myenv
myenv\Scripts\activate

```

## Création d'un environnement virtuel sous Mac

```
python3 -m venv -myenv --without-pip
source myenv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

## Création d'un environnement virtuel sous linux 

```
sudo apt-get install python-virtualenv
virtualenv --python=python3.4 myenv
source myenv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

## Installation de Django

```
pip install django
django-admin startproject <project_name>
cd <project_name>
python manage.py startapp <app_name>
```

## Installation des dépendances

```
pip install -r requirements.txt
```

## Lancement des migrations

```
./manage.py migrate
```

## Lancement du serveur

```
python manage.py runserver
```
