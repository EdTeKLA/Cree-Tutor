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
3. Install mysql from https://dev.mysql.com/downloads/mysql/
You will need to select "use legacy authentication method"
Write down the password you created.
4. Install mysqlclient
If there is an error, download the wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python and navigate to the downloads folder then run pip install mysqlclient-1.3.13-cp??whatever?the?filename?downloaded.whl
5. Install Django 2.0.x
6. Clone this directory
7. Open or create the file `CreeTutor/CreeTutorBackEnd/CreeTutorBackEnd/settings_secret.py`
8. Make the contents of settings_secret.py look like this:

"""
These settings must never be uploaded onto github.

Keep it secret
"""

db_root = "root"
db_pass = "PutPasswordHere"

9. Make a MySQL schema named "CreeTutordb"

   **How to**

   Navigate to the directory `CreeTutor/CreeTutorBackEnd` and run:

        $ python manage.py dbshell

        @Delaney This doesn't work. It gave me "returned non-zero exit status 1." I managed to get into the mysql shell anotehr way but we need to sort this out. Made an issue.#1

   To open up the mysql shell. Next run the follow queries in the shell:

        > create database CreeTutordb;
        > exit

11. Navigate to CreeTutor/CreeTutorBackEnd and run:

        $ python manage.py migrate

    to populate the database with django models and the models created in models.py. For more information
    on models, please see the how to blurb at the top of `CreeTutorBackEnd/lettergame/models.py`.
 ---

##### References
  1. https://en.wikipedia.org/wiki/Plains_Cree
  2. https://en.wikipedia.org/wiki/Polysynthetic_language
