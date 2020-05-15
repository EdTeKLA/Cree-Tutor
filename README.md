# CreeTutor

Cree language learning website project.

Information on Plains Cree:
  * Also known as the Y-dialect, it is one of the five main dialects of the Algonquian language<sup>1</sup>.
  * Is the most widely spoken dialect of Cree<sup>1</sup>.
  * Is primarily spoken in Alberta and Saskatchewan but is also spoken in Manitoba and Montana<sup>1</sup>.
  * It is a polysynthetic language<sup>2</sup>.

Current version uses Django 2.0.5, MySql 14.14, Python 3.6.4, and HTML 5

## Build Instructions:
1. Install python 3.6.x: 

        All OS: https://www.python.org/downloads/
	
2. Install a python IDE
	
	Go to JetBrains and download Pycharm
	
		Pycharm (community version is free): https://www.jetbrains.com/pycharm/
		
	To learn how to set up Python on PyCharm on different os follow the following tutorials
	
		All OS: https://www.youtube.com/watch?v=5rSBPGGLkW0
		
        
2. Install pip: 
    
        All OS: https://www.makeuseof.com/tag/install-pip-for-python/

3. Install Docker:
    
    **If you are on a Windows devices check if you have the Education version, if you do install Docker using the link provided. If you are using your own windows device you are likely using Windows Home, with such you will have to follow the steps in the Window Home installation section.**
       
        Ubuntu: https://phoenixnap.com/kb/how-to-install-docker-on-ubuntu-18-04
        MacOS: https://docs.docker.com/v17.12/docker-for-mac/install/
        Windows(Enterprise and Education vers only): https://docs.docker.com/v17.12/docker-for-windows/install/
       
4. Install and start Postgres on docker, change **Your_Password** to the actual password you will be using:

	**This command must be run every time you restart your computer, postgres does not automatically start in docker when you computer starts.** 
        
        MAC, Linux, Ubuntu: 
            sudo docker run --rm --name pg-docker -e POSTGRES_PASSWORD=**Your_Password** -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data postgres
	
   	For Windows os, go into `C:` and create the path `docker\volumes\postgres` then run the following command:
  
	     docker run --rm --name pg-docker -e POSTGRES_PASSWORD=**[Your_Password]** -d -p 5432:5432 -v c:/docker/volumes/postgres:/var/lib/postgresql/data postgres
            
5. Install pgAdmin:
    
   Go to: 
   
   		ALL OS: https://www.pgadmin.org/
		
   Select the version appropriate for your os and install the latest version of pgAdmin.

6. Clone or download the CreeTutor repository

	*NOTE: Easiest option is to download the file as a ZIP file and unzip it into a folder on your desktop named `CreeTutor`*
	

6. Create the file `CreeTutor/CreeTutorBackEnd/CreeTutorBackEnd/settings_secret.py`

7. (Make sure the slashes for the pathes match the system you are working on) Make the contents of settings_secret.py look like this:

       """  
       These settings must never be uploaded onto github.

       Keep it secret
       """

       DB_ROOT = "postgres"

       DB_PASS = "[Your_Password]"

       PATH_TO_ALPHABET = "...\CreeTutor\CreeTutorBackEnd\lettergame\static\lettergame\sound\Alphabet"
       PATH_TO_WORD = "...\CreeTutor\CreeTutorBackEnd\lettergame\static\lettergame\sound\Words"
       PATH_TO_LETTERPAIR = "...\CreeTutor\CreeTutorBackEnd\lettergame\static\lettergame\sound\LetterPairs"

8. Install required python packages

    Navigate to the directory `CreeTutor` and run:
        
        pip3 install -r requirements.txt
	
9. From the google drive folder https://drive.google.com/drive/u/3/folders/1X34CGcXmOzAP5MIJhRtImxXsohHejEP8 download and unzip the Alphabet, Words, and LetterPairs folders, and save them in the pathes given by settings_secret.py

10. Create database "cree_tutor_db" and necessary tables.

   **How to: using psql commands**

   Navigate to the directory `CreeTutor/CreeTutorBackEnd` and run:

        $ psql -h localhost -U postgres -d postgres

   This opens up the postgres shell. Next run the follow queries in the shell after changing [Your_DB_Username] (if you followed the previous steps exactly your username should be `postgres`) and [Your_Password] to the values above:

        postgres=# CREATE DATABASE cree_tutor_db;
        postgres=# CREATE USER [Your_DB_Username] WITH PASSWORD '[Your_Password]';
        postgres=# ALTER ROLE [Your_DB_Username] SET client_encoding TO 'utf8';
        postgres=# \q
   
   **How to: using pgAdmin**
   
    Open up pgAdmin and enter in your password. In the Browzer column, right click on Servers > Create > Server. In the General tab, enter a name for the server. In the Connection tab, enter in the host address (localhost) and password that you used in the previous step. Click Save and in the Browzer column you should see
   
        Servers
           PostgreSQL 11
               Databases
                   ** other databases that you created**
               Login/Group Roles
               Tablespaces
   
    Right click on `Databases` and select `Create > Database...`. A pop-up box will show up and you can enter in the name of the database as `cree_tutor_db` and the owner to your username. (The owner can be changed later however it should match what is written in the `settings.py` and `settings_private.py` files)
   
11. Once the database is working, you make check that is is working by running the following:

        $ python manage.py dbshell
   
  	 *If not working, repeat the steps and try again.*

   To create the tables, in the current directory, run the following commands:

        $ python manage.py makemigrations
        $ python manage.py migrate
	
12. Troubleshooting
	
	a) If you have changed your database username in your settings_secret.py file to something other than postgres you will have problem making migrations. The error:
	
	
	To solve this issue, go on pgAdmin and select `Tools > Query Tool` and paste the following text editor, after changing the `[Your_DB_Username]` to your username
	
		GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO [Your_DB_Username];
		GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO [Your_DB_Username];
		GRANT ALL PRIVILEGES ON DATABASE cree_tutor_db TO [Your_DB_Username];
		ALTER USER [Your_DB_Username] CREATEDB;

	Click on the lightning bolt button and try running these commands again
	
		python manage.py makemigrations
		python manage.py migrate
	
	b)   Another possible issue that may is arise will produce an error like below.
	```
	CT-user@creetutor-server:~/CreeTutor/CreeTutorBackEnd$ python3 manage.py migrate
	Operations to perform:
	  Apply all migrations: admin, auth, contenttypes, core, lettergame, sessions
	Running migrations:
	  Applying admin.0001_initial...Traceback (most recent call last):
	  File "/home/CT-user/.local/lib/python3.6/site-packages/django/db/backends/utils.py", line 84, in _execute
	    return self.cursor.execute(sql, params)
	psycopg2.errors.UndefinedTable: relation "modified_user" does not exist
	``` 
	These errors can occur sometimes with Django if migrations of different apps are applied in different order on default. To rectify this, you may attempt to makemigrations and migrate for login and then try to migrate the rest as follows:
	`python3 manage.py makemigrations login`,
	`python3 manage.py migrate login `,
	`python3 manage.py makemigrations`, then finally
	`python3 manage.py migrate`.

13. Now populate the data using the following scripts:
    
    In `CreeTutor/DatabaseInsertions`, run:
        
        python insertintodb.py
        python savedistractors.py
    
    If you get a FileNotFoundError: [Errno 2], then right click the Alphabet, Words, and LetterPairs folders to then copy path and use these full paths in secrets_setting.py (this gets rid of the '...' at the beginning).
    
    In `CreeTutor/CreeTutorBackEnd/login`, run:
        
        python insert_options_into_db.py
        
    From the google drive folder https://drive.google.com/drive/u/3/folders/1oO5P64U-IsA2OpNrIqOc6GNWDnZjg1Oi download the srts folder and save that in `CreeTutor/CreeTutorBackEnd/shadowing/static`.
    
    In `CreeTutor/CreeTutorBackEnd/shadowing`, run:
        
        python insert_questions_into_db.py
        python insert_srt_files_and_stats.py
        python insert_configs.py
 
 An error may occur:
 '''
 python3 insert_questions_into_db.py
Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
psycopg2.errors.UndefinedTable: relation "shadowing_feedback_questions" does not exist
LINE 1: ..., "shadowing_feedback_questions"."no_answer" FROM "shadowing...
'''

If this happens try running
`python3 manage.py makemigrations shadowing`,
`python3 manage.py migrate shadowing `

 then try running the insert files again.
 
## Windows Home installation process

Docker does not work on Windows 10 Home, which is what many people have. Therefore, additional steps is needed for Django to run with PostgreSQL. 

1. Download ProtgreSQL
 
    Go to https://www.postgresql.org/download/windows/ to download the latest postgresql version.
    
    Set up your password and remember it, as it will be used for all future prostgresql access. The package that you download should include a management tool "pgAdmin" which will greatly help you set up databases. 
 
2. Set up virtual environment (optional)
 
    Run the following commands in terminal:
    
        $ pip install virtualenvwrapper-win
    
    Then create a virtual environment for this project 
    
        $ mkvirtualenv cree_tutor
    
    Now you should see (cree_tutor) next to the command prompt, this shows that you are in the virtual environment.
    
    Everytime you start command prompt you will have to activate the environment by using:
    
        $ workon cree_tutor

3. Download Django

   In command prompt, execute the command
   
         $ pip install django
   
   To verify that you have properly install django run
   
         $ python -m django --version
   
4. Go into `CreeTutor` folder and run the command
  
         $ django-admin startproject cree_tutor_db
   
5. Go into the `cree_tutor_db\cree_tutor_db\settings.py` file and change the `DATABASE` 
         
         DATABASES = {
             'default': {
                 'ENGINE': 'django.db.backends.postgresql',
                 'NAME': 'CreeTutor',
                 'USER': '[your username]',
                 'PASSWORD': '[enter your postgresql password here]',
                 'HOST': '127.0.0.1',
                 'PORT': '5432'
             }
         }
   
6. Open or create the file `CreeTutor/CreeTutorBackEnd/CreeTutorBackEnd/settings_secret.py`

7. Make the contents of `settings_secret.py` look like this:

       """  
       These settings must never be uploaded onto github.

       Keep it secret
       """

       DB_ROOT = "[Your_DB_Username]"

       DB_PASS = "[enter your postgresql password here]"

       PATH_TO_ALPHABET = "...\CreeTutor\CreeTutorBackEnd\lettergame\static\lettergame\sound\Alphabet"
       PATH_TO_WORD = "...\CreeTutor\CreeTutorBackEnd\lettergame\static\lettergame\sound\Words"
       PATH_TO_LETTERPAIR = "...\CreeTutor\CreeTutorBackEnd\lettergame\static\lettergame\sound\LetterPairs"

8. Downloading other necessary requirements 

   Navigate to the directory `CreeTutor` and run:
        
        $ pip install -r requirements-windows.txt
 
9. (recommended) Create database "cree_tutor_db" and necessary tables using pgAdmin
   
    If you'd like to use command line prompts to set up your database, look at the optional step 10. Otherwise, continue on.
   
    Open up pgAdmin and enter in your password. You should see
   
        Servers
           PostgreSQL 11
               Databases
                   ** other databases that you created**
               Login/Group Roles
               Tablespaces
   
    Right click on `Databases` and select `Create > Database...`. A pop-up box will show up and you can enter in the name of the database as `cree_tutor_db` and the owner to your username. (The owner can be changed later however it should match what is written in the `settings.py` and `settings_private.py` files)
 
10. (optional psql) Create database "CreeTutordb" and necessary tables using psql
    
    If you'd like to use command line prompts to set up the database please read on, if not skip to step 9. 
    
    **How to**
    
    Try to run 
        
         $ psql --version
    
    if it shows an error you will have to add postgres onto your path. To do this, note down where you saved postgreSQL on your device and add it to the windows path. 
    
    For example, if your files are at `C:\Program Files\PostgreSQL\9.5\` then you can add the lib and bin folder using the following command
    
	       $ set PATH [C:\Program Files\PostgreSQL\9.5\lib]
	       $ set PATH [C:\Program Files\PostgreSQL\9.5\bin]

    See if you have added it to your path by restarting command prompt and running
        
        $ psql --version
    
    If it is not, manuallly add it in by going into `This PC > Properties > Advanced System Settings > Environmental Variables > System Variables`
    
    Click on `Edit` and in the path section add `C:\Program Files\PostgreSQL\9.5\lib` and `C:\Program Files\PostgreSQL\9.5\bin`
    
    Check if it has been added to your path by restarting command prompt and running
            
        $ psql --version
        
    Navigate to the directory `CreeTutor/CreeTutorBackEnd` and run:

        $ psql -h localhost -U postgres -d postgres

    This opens up the postgres shell. Next run the follow queries in the shell after changing your username and password:

        postgres=# CREATE DATABASE cree_tutor_db;
        postgres=# CREATE USER [Your_DB_Username] WITH PASSWORD '[enter your password here]';
        postgres=# ALTER ROLE [Your_DB_Username] SET client_encoding TO 'utf8';
        postgres=# \q
 
11. Testing if the database is working

     Once the database is working, you make check that is is working by running the following:

        $ python manage.py dbshell

     To create the tables, navigate into `CreeTutor\cree_tutor_db` and run the following commands:

        $ python manage.py makemigrations
        $ python manage.py migrate
 
 
 ---

##### References
  1. https://en.wikipedia.org/wiki/Plains_Cree
  2. https://en.wikipedia.org/wiki/Polysynthetic_language
  3. https://docs.djangoproject.com/en/2.2/intro/install/
