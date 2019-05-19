# evaluate-ML-models
## Install Project on Local Machine
### Create Database
```
mysql -u root -p
show databases;
create database `DB_NAME`;
```

### Clone from the repository
> I normally use pipenv in `dev`, but in this project I used `pip`
```
git clone https://github.com/lifelonglearner127/evaluate-ML-models.git
cd evaluate-ML-models
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Config Local Setting
Create your `instance` project root directory and write down following configration settings in `instance/config.py`
```
SECRET_KEY = 'p9Bv<3Eid9%$i01'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://DB_USER:USER_PASS@localhost/DB_NAME'
```

After that please continue
```
export FLASK_APP=run.py
export FLASK_CONFIG=development
flask db migrate
flask db upgrade
flask run
```

## Deploying heroku
### Add Procfile file
```
web: gunicorn run:app
release: flask db upgrade
```

### Create heroku app
```
heroku login
heroku create evaluate-ml-models
```

### Create heroku database

### Config heroku vars
```
heroku config:set FLASK_APP=run.py
heroku config:set FLASK_CONFIG='production'
heroku config:set SECRET_KEY='p9Bv<3Eid9%$i01'
heroku config:set SQLALCHEMY_DATABASE_URI='postgres://itvutnkxmmgweh:ccbf42b1d41ca00cdde3c6ce2c44722aa98a4ceb2efbcde82aa9efb577e7ca69@ec2-75-101-131-79.compute-1.amazonaws.com:5432/dfbbkdlds8422h'
git push heroku master
```
