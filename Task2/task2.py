from bs4 import BeautifulSoup
import requests
import sys
import re


def file_handler():
    """
    Handler for file opening and writing,
    opens file with websites and saves
    converted output to 'counted_websites.csv'
    """
    writer = open(sys.argv[2], 'w')
    reader = open(sys.argv[1], 'r')
    writer.write("address,number_of_buttons\n")
    for row in reader:
        url = row.rstrip('\n')
        writer.write(url + ',' + str(parse_html(url)) + '\n')
    reader.close()
    writer.close()


def parse_html(website):
    """
    Parser for html file implemented using Beaufifulsoup,
    searches for tags given in task instructions and returns
    a set containing proper elements
    """
    """
    We'll be keeping all of our elements
    in a tet to avoid repeating elements
    """
    final_list = set([])
    #Parse website, add port if it's localhost
    if website == "localhost":
        r = requests.get("http://" + website + ":8000")
    else:
        r = requests.get("http://" + website)
    soup = BeautifulSoup(r.content, 'lxml')
    #Find all button tags and add it to our set
    for button_tag in soup.find_all('button'):
        final_list.add(button_tag)
    #Find all input tags of type "submit", "reset" and "button"
    for input_tag in soup.find_all('input'):
        if input_tag.get('type') == "submit":
            final_list.add(input_tag)
        if input_tag.get('type') == "reset":
            final_list.add(input_tag)
        if input_tag.get('type') == "button":
            final_list.add(input_tag)
    """
    Find all elements with class tag, process it to lowercase,
    check if "btn" or "button" is in that tag
    """
    for class_tag in soup.find_all(class_=True):
        parsed = list(map(lambda x: x.lower(), class_tag['class']))
        for class_list in parsed:
            if "button" in class_list or "btn" in class_list:
                final_list.add(class_tag)
    return len(final_list)


if __name__ == '__main__':
    file_handler()
