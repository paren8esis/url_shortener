# URL Shortener

## Description
This is a Django app that implements a basic URL shortener.

We assume there is a custom database (sqlite in our case) which contains relations between letters and lists of words beginning from those letters,
e.g. 'a' points to a list of words beginning with 'a', and so on.

The app has an input view which takes as input a long URL of the following format: `<scheme>://<host>/<path>`. Then it parses the first letter of the first word of the `<path>` (aka, the first letter of the path) and creates a shortened URL using the first available record from the database. If all words are occupied, then it goes to the next letter of the path and iterates this process n-times, until it finds a non-occupied record to create a short URL with.

# Examples
- input: https://www.techcrunch.com/some-slug-here-starting-from-s  
output: http://example.com/s

- input2: https://www.techcrunch.com/some-other-slug-here-starting-again-from-s  
output2: http://example.com/sa

- input3: https://www.techcrunch.com/some-third-long-slug  
assumption: all words in the wordlist starting from "s" are occupied. So we look for the first available wordlist record starting with "o".  
output3: http://example.com/oaf


## Requirements

- Python==3.6.5  (It hasn't been tested with Python2.x but it should work fine with Python3.x)
- Django==2.0.7
- django-bootstrap3==10.0.1
- django-widget-tweaks==1.4.2
- pytz==2018.5
- tqdm==4.23.4

## Installation

1. Run the script `populate_database.py` located in the root directory giving as argument a .txt file containing all the words we would like to populate our database with.

2. Run the server with the command `python3 manage.py runserver` from the root directory.

## Tests

Tests can be put into the /url_shortener/tests/ directory and run through `python3 manage.py test url_shortener` from the root directory.

## Screenshots
![index page](/images/index.png)
