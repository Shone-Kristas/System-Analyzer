System-Analyzer is a command-line tool designed to analyze Linux file structure:
* Classify files on type categories based on file content. 
* Calculates and displays the total size for each file type category and identifies files above a certain size.
* Generates a report of files with unusual permission settings.

To run the System-Analyzer tool:
* Clone the repository
* Install dependencies: 
  ```
  pip install python-magic
  ```
* Navigate to the *System-Analyzer/src* directory
* Run the tool: 
  ```
  python main.py {path} {value}
  ```
  with set options:
  * {path} - full path to the directory you want to scan 
  * {value} - set a certain size in bytes. Files with a size above this value will be put into a report. 

