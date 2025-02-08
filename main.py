#Amazon web scraper I made for quickly tracking changes to amazon products.

#Web page request code modified from this tutorial: https://www.geeksforgeeks.org/scraping-amazon-product-information-using-beautiful-soup/

from bs4 import BeautifulSoup
import requests

HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

#Gets data from url and prints out all the data as well as returning important data to track (availability and sales)
def get_data(URL, print_data=True):

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")

    try:
        title_string = soup.find("span", attrs={"id": 'productTitle'}).string.strip().replace(',', '')
    except AttributeError:
        title_string = "NA"

    try:
        price = "$" + soup.find("span", class_='a-price-whole').get_text() + soup.find("span", class_='a-price-fraction').get_text()
    except AttributeError:
        price = "NA"

    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip().replace(',', '')
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '')
        except:
            rating = "NA"

    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip().replace(',', '')
    except AttributeError:
        review_count = "NA"

    try:
        available = soup.find("div", attrs={'id': 'availability'}).find("span").string.strip().replace(',', '').replace(" ","-")
    except AttributeError:
        available = "NA"

    try:
        sale = soup.find("span", class_='a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage').get_text()
    except AttributeError:
        sale = "None"

    #Prints out all the data if applicable and returns trackable data like availablity and sales info.
    if (print_data):
        print("Full Data:")
        print("Product Title: ", title_string)
        print("Products Price (After Sales): ", price)
        print("Overall Rating: ", rating)
        print("Total Reviews: ", review_count)
        print("Availability: ", available)
        print("Sale: ", sale)
    
    return [available, sale]

def menu(startup_data=False):
    if not startup_data:
        print("*** AMAPY TRACKER ***")
        print("1) Add new url to tracker")
        print("2) Remove url from tracker")
        print("3) Check tracked urls")
        print("4) Settings")
        x = input(">")
    else:
        x = ""
    if x == "1":
        print("Enter C to Cancel")
        url = input("ENTER URL: ")
        if url.lower() != "c":
            try:
                url_status_code = requests.head(url, headers=HEADERS).status_code
                if url_status_code != 200 and url_status_code != 405:
                    print("ERROR: URL returned status code: " + str(url_status_code))
                elif not("amazon" in url):
                    print("ERROR: not a valid amazon URL")
                else:
                    print("Adding url please wait...")
                    #appends url to url file and adds trackable data to previous url data file
                    with open("data/url.txt", "a") as file:
                        file.write(url + "\n")
                    important_data = get_data(url, False)
                    with open("data/pre_url_data.txt", "a") as file:
                        file.write(important_data[0] + " " + important_data[1] + "\n")
                    print("URL added to tracker")
            except:
                print("ERROR: Invalid URL")
            input("PRESS ENTER")
    elif x == "2":
        num = 1
        f = open("data/url.txt", "r")
        lines = f.readlines()
        if len(lines) != 0:
            print("Select URL to remove:")
            for line in lines:
                print(str(num) + ") " + line)
                num += 1
            print(str(num) + ") Cancel")
            x = int(input(">"))
            if x > 0 and x < num:
                #If the users selection is valid the url data and previous url data files have the line with the url removed (more like adds every url back except the one removed)
                with open("data/url.txt", "w") as file:
                    for num, line in enumerate(lines):
                        if num != x-1:
                            file.write(line)
                with open("data/pre_url_data.txt", "w") as file:
                    for num, line in enumerate(lines):
                        if num != x-1:
                            file.write(line)
                print("URL Removed from tracker")
        else:
            print("No URLs in tracker...")
        input("PRESS ENTER")
    elif x == "3" or startup_data: #Executes if user prompts or if startup data setting is on
        startup_data = False
        with open("data/pre_url_data.txt", "r") as file:
            pre_url_data = [a.split() for a in file.readlines()]

        with open("data/url.txt", "r") as file:
            for num, line in enumerate(file.readlines()):
                print("Getting Data...\n")
                important_data = get_data(line)

                print("\nImportant Changes:")
                #Checks for any discrepancys between data just fetched from website and data within the previous url data file.
                if important_data[1] != pre_url_data[num][1]:
                    print("The sale value has changed from " + pre_url_data[num][1] + " to " + important_data[1])

                if important_data[0] != pre_url_data[num][0]:
                    print("The availability has changed from " + pre_url_data[num][0] + " to " + important_data[0])

                if important_data == pre_url_data[num]:
                    print("No Changes found")
                else:
                    #If their was discrepencys previous url data file is written with data just seen by user
                    with open("data/pre_url_data.txt", "r") as f:
                        lines = f.readlines()
                    with open("data/pre_url_data.txt", "w") as f:
                        for num2, line2 in enumerate(lines):
                            if num == num2:
                                f.write(important_data[0] + " " + important_data[1] + "\n")
                            else:
                                f.write(line2)
            input("PRESS ENTER")
    elif x == "4":
        with open("data/settings.txt", "r") as file:
            data_startup_status = file.readlines()[0]
        print("1) Toggle Show URL Data on Start - " + data_startup_status)
        print("2) Cancel")
        x = input(">")
        if x == "1":
            with open("data/settings.txt", "w") as file:
                #Controls if url data is printed out on program start
                if (data_startup_status=="ON"):
                    file.write("OFF")
                    print("Show URL Data on Start set to off")
                else:
                    file.write("ON")
                    print("Show URL Data on Start set to on")
                input("PRESS ENTER")
    menu()

if __name__ == '__main__':
    with open("data/settings.txt", "r") as file:
        if file.readlines()[0] == "ON":
            menu(True)
        else:
            menu()