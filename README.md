# CreeTutor

Cree language learning website project.

Information on Plains Cree:
  * Also known as the Y-dialect, it is one of the five main dialects of the Algonquian language<sup>1</sup>.
  * Is the most widely spoken dialect of Cree<sup>1</sup>.
  * Is primarily spoken in Alberta and Saskatchewan but is also spoken in Manitoba and Montana<sup>1</sup>.
  * It is a polysynthetic language<sup>2</sup>.

Current version uses Django 2.0.5, MySql 14.14, Python 3.6.4, and HTML 5

## Build Instructions:
1. Install python 3.6.x
2. Install pip
3. Install mysql
4. Install mysqlclient
5. Install Django 2.0.x
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

8. Create database "CreeTutordb" and necessary tables.

   **How to**

   Navigate to the directory `CreeTutor/CreeTutorBackEnd` and run:

        $ mysql -u[user] -p[password]

   Where `[user]` and `[password]` are the user and password determined in the MySQL installation process.


   This opens up the mysql shell. Next run the follow queries in the shell:

        > create database CreeTutordb DEFAULT CHARACTER SET utf8mb4;
        > alter database CreeTutordb CHARACTER SET utf8 COLLATE utf8_bin;
        > exit
   
   Once the database is working, you make check that is is working by running the following:

        $ python manage.py dbshell

   To create the tables, in the current directory, run the following commands:

        $ python manage.py makemigrations
        $ python manage.py migrate

    This will fill the database with the models created in the file `CreeTutor/CreeTutorBackEnd/lettergame/models.py`. For   more information on models, please see the how to blurb at the top of `CreeTutorBackEnd/lettergame/models.py`.
    
    The database is now ready to be populated with available data.
 ---

##### References
  1. https://en.wikipedia.org/wiki/Plains_Cree
  2. https://en.wikipedia.org/wiki/Polysynthetic_language
