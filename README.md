# Survey Dot Com

## Installation (Linux)
*Tested on Ubuntu 16.04 LTS*

### Basics
Just some basic packages needed for Python
```bash
sudo apt update
sudo apt install python-pip python-dev
```

### PostgreSQL
1. Install PostgreSQL create a database named 'survey_dot_com_db'.
2. Create a user w/ all privileges on the database.
3. Add user/pw to envs.json

```bash
sudo apt install postgresql postgresql-contrib libpq-dev
sudo su - postgres
```
```postgres
psql
CREATE DATABASE survey_dot_com_db
CREATE USER someuser WITH PASSWORD 'somepassword';
ALTER ROLE someuser SET client_encoding TO 'utf8';
ALTER ROLE someuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE someuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE survey_dot_com_db TO someuser;
\q
exit
```

### TMI
Unlike SQLite3, a standard database system runs as a separate process in your server (or maybe even a separate physical database server). The way your web server, or Django server, communicates with the DB process (also called the DB server) is through socket communication. It's basically like running a webserver from localhost and opening it with your web browser. Note that the PostgreSQL settings in settings.py include host and port information.

In the above installation, you install PostgreSQL, which automatically starts the DB server, and then run the postgres shell. Running the shell is like ssh'ing into your web server (except this DB server is running on the same computer). From there, you create a database with a postgres user who has permission to access that DB.

Much thanks to Digital Ocean for this awesome [tutorial](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04).

### Pip Stuff
```bash
pip3 install -r requirements.txt
```
