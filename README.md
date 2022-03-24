# Python Web Scraper built with Beautiful Soup and XLSXWriter

This script parses the HTML from the Terminal 18 website and sends it to an excel sheet in a more useful format.
Currently requires an html file to be within the same folder, this will change once the script starts pulling live data.
Data gets dumped into a local excel sheet, this will change to write to a shared excel sheet in the cloud.

*requires latest version of Python
## Steps to setup:
1. run `pip install pipenv`
2. run `pipenv install`
3. run `pipenv shell`
4. run `python parser.py`

Output will be stored in `sample_output.xlsx`

TODO:
- Pull from live website rather than from static HTML file
- have script continuously run in order to pull updates when they happen and update the sheet accordingly
