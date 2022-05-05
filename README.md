# Sample QC Backend
Sample QC backend runs on Python. You will have to follow this set up if it's your first time running this project locally.

## Basic Setup Instructions <br>

**Install python3 and pip3** <br>
```
$ brew install python
```
```
$ brew install pip3
```

**Get mySQL running on your machine** <br>
```
$ brew install mysql
```
You'll then need to start your mySQL server (this will keep it running in the background on your machine) <br>
```
$ brew services start mysql
```
First time downloads, you'll want to securely set up the mySQL server by running <br>
```
$ mysql_secure_installation
```
Follow the prompts and set up your root password <br>
At this point, you can connect to your mySQL server with the following command <br>
```
$ mysql -u root -p
```
NOTE: you can also use mySQL Workbench for a UI to manipulate your db <br>

**Set up your Virtual Environment** <br>
```
$ pip3 install virtualenv
```
Make sure you `cd` into `igo-sample-qc-backend` in your terminal, then run the following cmd to setup the VE locally <br>
```
$ virtualenv venv
```
Activate the venv <br>
```
$ source venv/bin/activate
```
You should now see `(venv)` appear at the beginning of your terminal prompt indicating that you are working inside the virtualenv <br>
Check out [this setup walk through](https://sourabhbajaj.com/mac-setup/Python/virtualenv.html) for additional steps/options <br>

**Set up config file** <br>
Create a new file at root level of this project called `secret_config.py` <br>
To get fields needed for this config, consult a fellow dev :) but the most important field needed in this config is a `SQLALCHEMY_DATABASE_URI` field that matches a user in your local mySQL instance.<br>
Example field: <br>
```
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://sample_qc_dev_user1:napkinWatermelon1Dev!@localhost:3306/dev_sample_qc"
```

How to create mySQL users and grant privileges (do this within `mysql>` server):
```
# CREATE USER 'sample_qc_dev_user1'@'localhost' IDENTIFIED BY 'napkinWatermelon1Dev!';
# GRANT ALL PRIVILEGES ON dev_sample_qc.* TO 'sample_qc_dev_user1'@'localhost';
```

[Look here for more info on how you can add/remove users from your MySQL server](https://sebhastian.com/mysql-error-1396/)

**Install project packages**<br>
(this is usually only for the first run) <br>
```
$ pip3 install -r requirements.txt
```

**Start the python server** <br>
```
$ python3 run.py
```
NOTE: You might run into an error that `uwsgi` is not defined. To run locally, you might have to comment out all references to `uwsgi`  in the `qc_report.py` file
