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

    if (print_data):
        print("Full Data:")
        print("Product Title: ", title_string)
        print("Products Price (After Sales): ", price)
        print("Overall Rating: ", rating)
        print("Total Reviews: ", review_count)
        print("Availability: ", available)
        print("Sale: ", sale)
    return [available, sale]

def menu():
    print("*** AMAPY TRACKER ***")
    print("1) Add new url to tracker")
    print("2) Remove url from tracker")
    print("3) Check tracked urls")
    x = input(">")
    if x == "1":
        url = input("ENTER URL: ")
        try:
            url_status_code = requests.head(url, headers=HEADERS).status_code
            if url_status_code != 200 and url_status_code != 405:
                print("ERROR: URL returned status code: " + str(url_status_code))
            elif not("amazon" in url):
                print("ERROR: not a valid amazon URL")
            else:
                print("Adding url please wait...")
                File = open("url.txt", "a")
                File.write(url + "\n")
                File.close()
                important_data = get_data(url, False)
                File2 = open("pre_url_data.txt", "a")
                File2.write(important_data[0] + " " + important_data[1] + "\n")
                File2.close()
                print("URL added to tracker")
                input("PRESS ENTER")
        except:
            print("ERROR: Invalid URL")
    elif x == "2":
        num = 1
        f = open("url.txt", "r")
        lines = f.readlines()
        if len(lines) != 0:
            print("Select URL to remove:")
            for line in lines:
                print(str(num) + ") " + line)
                num += 1
            print(str(num) + ") Cancel")
            x = int(input(">"))
            if x > 0 and x < num:
                with open("url.txt", "w") as f:
                    for num, line in enumerate(lines):
                        if num != x-1:
                            f.write(line)
                with open("pre_url_data.txt", "w") as f:
                    for num, line in enumerate(lines):
                        if num != x-1:
                            f.write(line)
                print("URL Removed from tracker")
        else:
            print("No URLs in tracker...")
            input("PRESS ENTER")
    elif x == "3":
        File2 = open("pre_url_data.txt", "r")
        pre_url_data = [a.split() for a in File2.readlines()]
        print(pre_url_data)
        File2.close()
        File = open("url.txt", "r")
        for num, line in enumerate(File.readlines()):
            print("Getting Data...\n")
            important_data = get_data(line)
            print("\nImportant Changes:")
            if important_data[1] != pre_url_data[num][1]:
                print("The sale value has changed from " + pre_url_data[num][1] + " to " + important_data[1])
                f = open("pre_url_data.txt", "r")
                lines2 = f.readlines()
                f.close()
                with open("pre_url_data.txt", "w") as f:
                    for num2, line2 in enumerate(lines2):
                        if num == num2:
                            f.write(important_data[0] + " " + important_data[1] + "\n")
                        else:
                            f.write(line2)
                            
            if important_data[0] != pre_url_data[num][0]:
                print("The availability has changed from " + pre_url_data[num][0] + " to " + important_data[0])
                f = open("pre_url_data.txt", "r")
                lines2 = f.readlines()
                f.close()
                with open("pre_url_data.txt", "w") as f:
                    for num2, line2 in enumerate(lines2):
                        if num == num2:
                            f.write(important_data[0] + " " + important_data[1] + "\n")
                        else:
                            f.write(line2)

            if important_data[0] == pre_url_data[num][0] and important_data[1] == pre_url_data[num][1]:
                print("No Changes found")
            input("PRESS ENTER")
        File.close()
    menu()

if __name__ == '__main__':
    menu()
