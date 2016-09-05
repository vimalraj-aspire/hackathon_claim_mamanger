# Claims Manager

### Software Requirement
 * Python3 
 * pip
 * virtual environment
 * MySQL

### Sourcecode Setup
 * [Create Directory for project] - mkdir claims_manager
 * [Navigate into project directory] - cd claims_manager
 * [Clone Cource code form repo] - git clone <this repo URL>

### Virtual environment configuration
 * [Create virtual environment] - virtualenv venv
 * [Set virtual environment to use python 3] - virtualenv -p /usr/bin/python3 venv
 * [Activate virtual environment] - source venv/bin/activate

### Setup python & project dependencies
 * [Install python dependencies]  - pip install -r requirements.txt

### Database

 * [Create a MySQL database (adjust user/pass parameters to your setup)] - mysqladmin -u root create claims_manager 

 * Adjust database username/password in claims_manager/settings.py(main app)

 * [Run migration to create table] - python manage.py migrate

 * [Creat Super admin user] - python manage.py createsuperuser