#How to use

###Assumptions:
  For any of these to work, sound files *must* be in the following directory:
    `CreeTutor/CreeTutorBackEnd/lettergame/static/lettergame/sound`
  The script expects to split the path on `/static/` and will fail if it is elsewhere.
  Also, the html script expects to find it in the sound directory, and will return `not found`
  otherwise


###insertintodb.py
  NOTE: Database name and password are hardcoded. Audio file types accepted (wav or m4a) is also hardcoded.
  NOTE: Script deletes everything currently in tables before insertion to avoid primary key errors. PLEASE ensure
  to save necessary data before running this script.
  Database insertions will only be successful if database and necessary tables have already been created.
  To execute, run
    `python insertintodb.py`
  Program will ask for the path of where the recordings are for words, single letters, and letter pairs.

  ####How to check if successful:
    In the folder `/CreeTutor/CreeTutorBackEnd/` run the following command
      `python manage.py dbshell`
    To access the mysql shell. Then run any of the following queries to see the inserted data
      `select * from alphabet;`
      `select * from words;`
      `select * from letter_pairs;`
    Run
      `exit`
    To quit the shell.
