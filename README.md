# News-Feed-Scraper

A small working prototype of centralized newsfeed system.

## Purpose
We want to build a small newsfeed management system which will accept a simple text file as input containing news sites such as:
* http://slate.com
* https://www.reuters.com/places/india
* ...

The system will crawl through all of these sites, extract individual news and store them as JSON files/documents.

## Features
* Download the news feed from different sources in parallel. This feature is natively provided by the library used for scraping in this app.
* Store all news feed as JSON files to the local file system. For example, if the app is run for date 2019-10-08, it will create a folder named `2019-10-08` and place all json files there. The format of the json file is "<news-source>_<publish-date>.json". Example - `reuters_2019-10-08T12.05.32.json`
* Dump all news feed to MongoDB as json documents. This app uses free cloud hosted version of MongoDB ([MongoDB Atlas](https://www.mongodb.com/cloud/atlas)).
* Check for duplicity of feed by combination of (title, publish_date). If present, it skips the insertion to MongoDB.
* Generate summary.
  1. Create a summary file (summary.txt) in the output folder, e.g, `2019-10-08`. The file summarizes the count of all downloaded articles from all sources.
  2. Create a error log file (error_logs.txt) in the output folder, e.g, `2019-10-08`. The log file contains details of all the news feed that errored out during parsing/building. It stores the stack trace which can be used for debugging purposes.

## How to setup and run tests/lint

Make sure python3.7 is installed and added to path. If not installed, the installation setup has been described [below](https://github.com/anidok/News-Feed-Scraper#debugging-problems).
    
    python --version
    
or

    python3.7 --version

Then create a virtual environment for the project.

    virtualenv -p python venv
    . venv/bin/activate
    
or

    virtualenv -p python3.7 venv
    . venv/bin/activate



Then on all platforms install the python dependencies:

    pip install -r requirements-dev.txt

Note there is a separate requirements.txt file that excludes all but the dependencies required for deployment. Any production dependencies should be added to both files.


Optionally install the pre-commit hook by copying the following into .git/hooks/pre-commit

    #!/bin/sh
    git-pylint-commit-hook
    
Save the file and make it executable

    chmod +x .git/hooks/pre-commit
    
Note the above two steps can be ignored as we already have linter/pylint setup in our project as explained below.

Run tests:

    python -m unittest

Run Linting:

    sh scripts/lint.sh
    
The above command will run the shell script to run linting on the complete code base to check for PEP8 errors, bugs, stylic inconsistencies as per the python standards. The project uses a healthy combination of different linting tools (pylint, flake8 and so) to get the better results and generates the report. Our goal is to make the code base (both src and tests) 100% lint approved.

After successful execution of the above shell script, Run

    echo $?
It will check the exit code of the last command. If the output is 0 (zero), the linting has passed successfully. If the output is non-zero integer, it indicates there are some linting issues which can be found in the generated report and can be fixed accordingly.

### What does this give me?
The scraping can be run by running the python program.

    python src/news_scrapper.py --root_dir <output-directory> --source_list <path-to-source-file>
    
For example,

    python src/news_scrapper.py --root_dir F:/Scraper/Articles --source_list F:/Scraper/news_source.txt
    
Make sure the file `news_source.txt` exists in the specfied location. A sample [news_source.txt](https://github.com/anidok/News-Feed-Scraper/blob/master/scraper/news_source.txt) has been provided in the repo. All the output files (json files, summary.txt and error_logs.txt) will be generated in the specified output directory.

To make things easier, the above command is wrapped by a shell script [news_feed.sh](https://github.com/anidok/News-Feed-Scraper/blob/master/scripts/news_feed.sh). 

The script contains the above python command to run the app with a deafult output directory and relative location to the source file present in the repo. We can just run the script or we can edit it and provide our custom path. To do this, open the script in a text editor and replace the values for `root_dir` and `source_list` with custom values where we want to have our input/output.

Now run the script
    
    sh scripts/news_feed.sh
    
The script will run for some time (~mins) depending on the count of sources we provided and total number of articles present on those sources for the particular day the app is run. 

For functionality testing, It is advised to provide a single source containing a small number of articles. `http://slate.com` is one preferred input for which it takes about 3 mins to scrape all articles on any given day. For testing multiple sources, `http://slate.com` and `https://www.reuters.com/places/india` are two example values and it takes about 8 mins to scrape articles from these 2 sources combined.

Once the script execution completes, the output can be found in the local file system and MongoDB cluster.

### Debugging Problems
When running the app, it might give sqlite3 import error.

              from _sqlite3 import *
        ImportError: No module named '_sqlite3'
        
This may be because python3.7 was not compiled properly. The following stackoverflow link explains how to fix it. It explains for python3.6 but the same can be referred and replicated for python3.7 with minor changes.

https://stackoverflow.com/questions/39907475/cannot-import-sqlite3-in-python3

Modified commands from the above post for python 3.7

On Linux     
     
     sudo apt-get install libsqlite3-dev
     sudo apt-get remove python3.7
     cd /tmp && wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
     tar -xvf Python-3.7.4.tgz
     cd Python-3.7.4 && ./configure
     make && sudo make install
     
Python3.7 should now be compiled with proper headers and app should run fine.
     
