Instructions for ITIS Database PostgreSql Download 

1. A PostgreSql database is required to use this data file. If you want
   the database installed on your local system, download and install
   the PostgreSql database from http://www.postgresql.org/download/. 

Note: Downloads and installation instructions are provided on 
      the PostgreSql site. The ITIS staff doesn't provide 
      installation or usage support for PostgreSql.

2. Download the latest ITIS PostgreSql zip file (itisPostgreSql.zip)
   from http://www.itis.gov/downloads. This file is normally updated
    monthly on the last day of the month. 

3. Use an archive tool, Finder, or Windows Explorer to unzip
   the ITIS data file. This will create a folder containing
   the data installation files.


Installation Instructions for All Platforms.

Caution: When you install this new ITIS data in PostgreSql,
   any existing database named "ITIS" will be dropped
   (permanently removed) before the new database is 
   created and the new data loaded. If this is not what you
   want, you should investigate backup and/or data 
   preservation options prior to loading the new data.

1. Open a terminal or command prompt and navigate to the folder where you
   unzipped the ITIS download file.

2. Enter the following:

      psql -U root -f ITIS.sql

   If your PostgreSql user is not root, substitute your user
   name for root. Also, if you are updating a remote 
   server, you will need to  add a -h <servername> to 
   the command

3. When prompted for your PostgreSql user's password, enter
   it and the load process will start.

Note: Depending on the speed and resources of the system
   where you are loading the data, the load process 
   could take several minutes.

