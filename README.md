# GroupMe Scraper

## Overview:
This program is a script that allows users to download their group message data on GroupMe. The program downloads group messages, performs some some analytics, and generates visualizations of the data.

<img src = "https://user-images.githubusercontent.com/26987971/76921936-a24bf180-68a5-11ea-8e69-410904b8189d.png" width = 500 />

<img src = "https://user-images.githubusercontent.com/26987971/76922076-19818580-68a6-11ea-9437-e29cc976fce2.png" width = 500 />

<img src = "https://user-images.githubusercontent.com/26987971/76922212-6c5b3d00-68a6-11ea-8cc0-c273f1cc8f18.png" width = 500 />

## Setup:
To be able to use this project, you will need to go to the [GroupMe Developer Portal](https://dev.groupme.com) and obtain an access token:

 - Do so by creating a new application. Call it whatever you would like. Note that in the form for creating the application, a callback url is required by the form but not used by this Python script, so whatever is entered doesn't really matter.
 - Under the application details, copy the string where it says
   "[Name]'s Access Token".
 - Create a new file in the directory on the same level as `app.py`
   called `config.json`.
 - Copy and paste the below JSON snippet, which tells the program what your GroupMe access code is and defines a path for saving the data.


The contents of `config.json` should be as follows:

    {
	"path" : "data",
	"token" : "[YOUR ACCESS TOKEN HERE]"
	}

To install the necessary packages, go to the command line, navigate to the project directory, and type `pip install -r requirements.txt`. Note that you may want to set up a virtual environment beforehand.

## Run

The first time you run the program, type in the command line `python app.py -s`. This will create a file named `groups.json` under the config path `/data` which is set in `config.json`. This json file contains the names and ID number of all group messages in GroupMe.

Functionality of the program includes:

 - `python app.py` downloads data for all group messages. Adding one or more of the following flags is highly recommended unless you want to scrape all groupchats that you are in
 - `python app.py -i [id]` where `[id]` is one or more GroupMe ID numbers that the program will look at
 - `python app.py -f [input.txt]` where `[input.txt]` is one or more files containing one or more ID numbers of groupchats to include
 - `python app.py -e [exclude.txt]` where `[exclude.txt]` is one or more files containing  one or more ID numbers of groupchats to exclude. Takes precedent over other options.
 - `python app.py -s` which only updates the `groups.json` file

The program will store all collected data under the `data` directory, with a separate folder for each groupchat. When the program finishes, it will exit on its own.

## Files

 - `app.py`: the main script that is run. Parses inputs and calls other imported functions.
 - `groups.py`: defines a function called `get_all_groups` which scrapes the GroupMe API for summary data for groupchats (not the messages themselves).
 - `messagegroup.py`: defines a `messagegroup` class which serves as a container for a pandas DataFrame containing messages and information about them. Numerous functions for commonly used operations are defined here. Additionally, this class defines the function `from_groupme_id()` for scraping GroupMe for individual messages given a GroupMe ID.
 - `routines.py`: defines more complicated routines for analyzing `messagegroup` objects, including generating statistics, filtering, and generating visualizations. Allows for batch processing of groupme messages.
 - `requirements.txt`: Lists package requirements
