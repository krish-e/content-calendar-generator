# content-calendar-generator

## Table of Contents

1. [Description](#description)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)



## Description

`content-calendar-generator` is a Python project where the program will 
extract product URL from the given link(may not work when tried for a 
different website as the class-name where the URL might be may differ)

Sends request to ChatGPT with the product name and gets social media copy
(3 variations) from which the user can select one or get inspired from it
and create a copy themselves.

Then the program will ask the user for month and year for which the 
content-calendar have to be created.

It's done. The generated content calendar will be in the same directory
in the name out.csv


## Requirements

- Python 3.6+
- Libraries listed in `requirements.txt` (install using `pip install -r requirements.txt`)


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/krish-e/content-calendar-generator.git

2. Navigate to the project directory:

    ```bash
    cd content-calendar-generator

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt


## Usage

1. Run the project from the command line:

    ```bash
    python project.py

2. Follow the on-screen prompts to enter the name and year for which the content calendar have to be created.

3. Give it a few minutes for the program to capture response from ChatGPT.

4. Once the program is done, it will generate the calendar(csv file) for the given month and year with date and mentioned channels.   
