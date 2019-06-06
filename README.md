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
        
2. Install pip: 
    
        All OS: https://www.makeuseof.com/tag/install-pip-for-python/

3. Install Docker:
    
        Ubuntu: https://phoenixnap.com/kb/how-to-install-docker-on-ubuntu-18-04
        MacOS: https://docs.docker.com/v17.12/docker-for-mac/install/
        Windows: ¯\_(ツ)_/¯

4. Install and start Postgres on docker, change **Your_Password** to the actual password you will be using:
        
        All OS: 
            sudo docker run --rm --name pg-docker -e POSTGRES_PASSWORD=ygh8a9bm -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data postgres
            
5. Install psql, Postgres client:
    
        Ubuntu: sudo apt install postgresql-client-common && sudo apt install postgresql-client

6. Open or create the file `CreeTutor/CreeTutorBackEnd/CreeTutorBackEnd/settings_secret.py`

7. Make the contents of settings_secret.py look like this:

       """  
       These settings must never be uploaded onto github.

       Keep it secret
       """

       DB_ROOT = "Your_DB_User"

       DB_PASS = "Your_Password"

       PATH_TO_ALPHABET = "...\CreeTutor\CreeTutorBackEnd\lettergame\static\lettergame\sound\Alphabet"
       PATH_TO_WORD = "...\CreeTutor\CreeTutorBackEnd\lettergame\static\lettergame\sound\Words"
       PATH_TO_LETTERPAIR = "...\CreeTutor\CreeTutorBackEnd\lettergame\static\lettergame\sound\LetterPairs"

8. Install required python packages

    Navigate to the directory `CreeTutor` and run:
        
        pip3 install -r requirements.txt

9. Create database "CreeTutordb" and necessary tables.

   **How to**

   Navigate to the directory `CreeTutor/CreeTutorBackEnd` and run:

        $ psql -h localhost -U postgres -d postgres

   This opens up the postgres shell. Next run the follow queries in the shell after changing "Your_DB_User" and "Your_Password" to the values above:

        postgres=# CREATE DATABASE cree_tutor_db;
        postgres=# CREATE USER Your_DB_User WITH PASSWORD 'Your_Password';
        postgres=# ALTER ROLE Your_DB_User SET client_encoding TO 'utf8';
        postgres=# \q
   
   Once the database is working, you make check that is is working by running the following:

        $ python manage.py dbshell

   To create the tables, in the current directory, run the following commands:

        $ python manage.py makemigrations
        $ python manage.py migrate

10. Now populate the data using the following scripts:
    
    In `CreeTutor/DatabaseInsertions`, run:
        
        python insertintodb.py
        python savedistractors.py
        
    In `CreeTutor/CreeTutorBackEnd/shadowing`, run:
        
        python insert_questions_into_db.py
        python insert_srt_files_and_stats.py
        python insert_configs.py
 ---

##### References
  1. https://en.wikipedia.org/wiki/Plains_Cree
  2. https://en.wikipedia.org/wiki/Polysynthetic_language
