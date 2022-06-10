import numpy as np
from urllib import request
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
import time
import json
import variable

"""
Google form spam
1.  Insert Google form viewform link to generate the submit link
2. Insert json format into item list
3. 
"""



url =  variable.url
random_string = "abcdefghijklmnopqrstuvwxyz"


def obtain_entry_list(url):
    """
    Use webdriver to obtain and return entry list from console  
    Obtain the google link  page source
    """
    command = variable.command
    #command to input into broswer console

    webdriver_directory = variable.webdriver_directory

    #setup drive
    s = Service(webdriver_directory)
    dc = DesiredCapabilities.CHROME
    dc['goog:loggingPrefs'] = {'browser': 'ALL'}
    driver = webdriver.Chrome(service=s, desired_capabilities=dc)

    print("driver is starting and obtaining the entry list")
    #open url with webdriver
    driver.get(url)
    time.sleep(4)

    #send command to get log message
    driver.execute_script(command)
    time.sleep(2)

    list_of_message = []
    entry_list = []
    for message in driver.get_log('browser'):
        list_of_message.append(message["message"])
    for message in list_of_message:
        if "entry" in message:
            if "sentinel" not in message:
                entry1 = message[message.find("entry"):-1]
            if "sentinel" in message:
                entry1 = message[message.find("entry"):message.find("_")]
            if entry1 not in entry_list:
                entry_list.append(entry1)

    #obtain page source
    page_source = driver.page_source

    #write obtained page source into save_page.html
    with open("save_page.html", "w") as source_file:
        source_file.write(page_source)

    return entry_list

def obtain_new_item_list():
    """
    Return list of item with entry number added
    """
    ##obtain list of items from dictionary data from app script
    with open("json format data.json", "r") as file1:
        json_data = json.loads(file1.read())
        item_list = json_data["items"]

    #obtain list of item id form list of item
    item_id_list = [item["id"] for item in item_list]
    print("item id list is: ", item_id_list)

    # obtain entry list from console log
    full_entry_list = obtain_entry_list(url)


    #obtain list  of entry with only digits
    entry_number_list = [i[i.find(".")+1:] for i in full_entry_list]


    #  erase element before FB_PUBLIC_LOAD_DATA, create
    #  dictionary   entry number and item id with corresponding position 
    item_id_and_position_dictionary = {}
    entry_id_and_position_dictionary = {}
    with open("save_page.html", "r") as source_file:
        read_file = source_file.read()
        read_file = read_file[read_file.find("FB_PUBLIC_LOAD_DATA_"):]
    with open("save_page.html", "w") as source_file:
        source_file.write(read_file)
    with open("save_page.html", "r") as source_file:
        read_file = source_file.read()
        for item_id in item_id_list:
            position = read_file.find(str(item_id))
            item_id_and_position_dictionary[str(item_id)] = position 

        for entry_number in entry_number_list:
            position = read_file.find(entry_number)
            entry_id_and_position_dictionary[str(entry_number)] = position


    #obtain list of all position of  entry and id
    all_position = []
    for item_id in item_id_and_position_dictionary.values():
        all_position.append(item_id)
    for entry in entry_id_and_position_dictionary.values():
        all_position.append(entry)
    print("allposition: " ,all_position)

    #sort all entry and id posiiton in ascending order
    all_position.sort()

    # create new list of items with entry number added
    new_item_list = []
    for i in range(int(len(all_position)/2)):
        item_id_position = all_position[2*i]  
        for dict_item_id , dict_item_position in  item_id_and_position_dictionary.items():
            if item_id_position == dict_item_position:
                item_id = dict_item_id
                print('the item id is: ', item_id)
        entry_number_position = all_position[2*i+1]
        for dict_entry_number, dict_entry_position in entry_id_and_position_dictionary.items():
            if entry_number_position ==  dict_entry_position:
                entry_number = dict_entry_number
                print('the entry number  is: ', entry_number)

        for item in item_list:
            if str(item["id"]) == item_id:
                #added entry number in new item is string
                item["entry"] = entry_number
                new_item_list.append(item)
        return new_item_list

def add_probability(item_list):
    """
    ask and add desired probability from user for each choices for each question
    """
    item_list2 = []
    for item in item_list:
        item2 = ask_for_probability(item)
        item_list2.append(item2)
    return item_list2

def ask_for_probability(item):
    """
    Ask user for desired probability for each choice of each multiply choice question
    """
    question = item["title"]
    type_of_question = item["type"] 
    
    print("The question is: " + question )
    print("The type of question is" + type_of_question)

    if type_of_question == "TEXT":
        list_of_choice = ["1"]

    elif type_of_question == "MULTIPLE_CHOICE" or  "CHECKBOX" or "LIST":
        list_of_choice = item["choices"]


    elif type_of_question == "SCALE":
        list_of_choice = np.arange( item["lowerBound"],item["upperBound"]+1)

    bias  =  input("Do you want bias distribution?(y/n) ")
    if bias ==  "y":
        probability  = []
        for choice in list_of_choice:
            print("Input the desire probability for: ", choice) 
            probability.append(float(input()))
        item["bias"] = True
        item["probability"] = probability 

        #answer = np.random.choice(list_of_choice, p = probability)
    else:
        item["bias"] = False
       # answer = np.random.choice(list_of_choice)
    return item

def generate_final_url(url, item_list2):
    """Generate the final URL from the list on entry of google form and the google form link"""
    without_viewform_url = url[:-8]
    formResponseURL = without_viewform_url + "formResponse?&pageHistory=0"


    for item2 in item_list2: 
        is_bias = item2["bias"]  
        list_of_choice = item2["choices"]

        if is_bias:
            answer = np.random.choice(list_of_choice, p = item2["probability"])

        else:
            answer = np.random.choice(list_of_choice)

        formResponseURL = formResponseURL+"&entry."+ item2["entry"] +"=" + answer 
        final_url = formResponseURL
    return final_url





#item list: only id number
# new item list = id number and entry number
#item_list_2 = id number, entry number, probability


new_item_list = obtain_new_item_list()

print("the new item list is: ",new_item_list)

item_list_2 = add_probability(new_item_list)

# write many different  new links into file name formlinks.txt
with open("formlinks.txt","w") as link_file:
    for i in range(100):
        link = generate_final_url(url, item_list_2)
        link_file.write(link + "\n")

#read the formlinks.txt replace the space in the link with %20,then  request the url


with open("formlinks.txt","r" ) as link_file:
    links = link_file.readlines()
    n = 1
    for link in links:
        link = link.replace(" ","%20")
        request.urlopen(link)
        print( str(n) + " forms has been sent!")
        n += 1;























