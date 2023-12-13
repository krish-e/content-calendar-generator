import bs4
from bs4 import BeautifulSoup
import requests
import os
import openai
from dotenv import load_dotenv, find_dotenv
from time import sleep
import datetime
import calendar
import random
import pandas as pd
import numpy as np


# Get source code of the manually entered URL
url = "https://www.royaloakindia.com/living/sofas.html"         # Replace URL here
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html')
# print(soup)

# Extract product names from the extracted source code of the URL
h2_temp_soup = soup.find_all('h2', class_="font-semibold text-black capitalize hover:text-primary xs:text-lg xs:font-bold")
h2_soup = bs4.BeautifulSoup(str(h2_temp_soup))
product_names = h2_soup.text.split(",")

product_names[0] = product_names[0].strip("[")
product_names[-1] = product_names[-1].strip("]")

for i in range(len(product_names)):
    product_names[i] = product_names[i][9:].strip()


# Captures all product links in the given html link
links_end = [a['href'] for a in soup.find_all('a', class_="plp-product-image", href=True)]
product_links = ["https://www.royaloakindia.com"+links_end[i] for i in range(len(links_end))]


# Chat-gpt core function
_ = load_dotenv(find_dotenv()) # read local .env file for API key

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]


# Getting copy from chatGPT with randomising
delay = 25      # Min 20 seconds break needed for chatgpt between prompts
final_dict = []
random_set = set()

# Number of product-post set for a month here is 12
while len(random_set) < 12:
    random_set.add(random.randint(1, len(product_names)))

for i in random_set:
    context = [{'role': 'system', 'content': f""" \
    You are an experienced copywriter in digital marketing. Imagine you are crafting short \
    and catchy Instagram copy (each within 7 words) for various products. Create 3 compelling captions separated by commas for the \
    furniture - {product_names[i]}. Be sure to capture the essence of each \
    product in your copy and don't use emojis and the product name. \
    """}]

    response = get_completion_from_messages(context)
    copy_list = [copy[3:].strip('","') for copy in response.split('\n')]
    final_dict.append({"Product Name": product_names[i], "Product Link": product_links[i], "Copy": copy_list})

    sleep(delay)


# Asking for which month to create content calendar
today = datetime.date.today()
month_in_word = calendar.month_name[today.month]
type(month_in_word)

today = datetime.date.today()

user_month = int(input("Calendar for which month(in numbers): "))
user_year = int(input("Calendar for which year(in numbers): "))


# Calculating dates and day - date format(dd-mmm-yy), day format(ddd), and channels(Facebook/Instagram)
month_in_word = calendar.month_name[user_month]
no_of_days = calendar. monthrange(user_year, user_month)[1]

date_dict = {
    'Date': [f"{str(i)} {month_in_word[:3]} {str(user_year)[2:]}" for i in range(1, no_of_days+1)],
    'Day': [],
    'Channels': ['Facebook / Instagram' for i in range(1, no_of_days+1)]
}

# Calculating days in words and adding to date_dict
for i in range(1, no_of_days+1):
    date = datetime.datetime(today.year, today.month, i)
    day_name = date.strftime("%A")[:3]
    date_dict['Day'].append(day_name)


# Converting date_dict to a dataframe-date_out_df
date_out_df = pd.DataFrame(date_dict)


# Filling the final sheet with requirements
out_df = pd.DataFrame(columns=['Product Link', 'Content', 'Caption'])

# Adding product name, link and copy to the new dataframe-out_df
for i in range(len(final_dict)):
    out_df.loc[len(out_df.index), ['Product Name', 'Product Link', 'Content']] = [final_dict[i]['Product Name'],
                                                                                  final_dict[i]['Product Link'], final_dict[i]['Copy']]

    # Adding random gaps filled with Nan
    for i in range(random.randint(1, 2)):
        out_df.loc[len(out_df.index)] = np.nan


# Concatenating date-dataframe and product-dataframe
out_df = pd.concat([date_out_df, out_df], axis='columns')

# Exporting data frame to CSV file
out_df.to_csv('out.csv', index=False)
