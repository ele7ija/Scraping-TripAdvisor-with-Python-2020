import sys
import csv
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# default path to file to store data (file doesn't need to exist (directory does), if it does, it'll be overwritten)
path_to_file = "/home/bp/tmp/reviews2.csv"

# default number of scraped pages (put 1000 if you want all of the reviews)
num_page = 1000

# default tripadvisor website of hotel or things to do (attraction/monument) 
url = "https://www.tripadvisor.com/Hotel_Review-g295380-d14037312-Reviews-Sheraton_Novi_Sad-Novi_Sad_Vojvodina.html"

# if you pass the inputs in the command line
if len(sys.argv) == 4:
    path_to_file = sys.argv[1]
    num_page = int(sys.argv[2])
    url = sys.argv[3]

# open the file to save the review
csvFile = open(path_to_file, 'w', encoding="utf-8")
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['Date', 'Rating', 'Type', 'Title', 'Review'])

# import the webdriver
driver = webdriver.Chrome()
print("Loading initial page...")
driver.get(url)
print("...initial page loaded")
time.sleep(2)

for i in range(0, num_page):
    print("Visiting page: ", i+1)

    # expand the review 
    time.sleep(1)
    try:
        driver.find_element(By.XPATH, ".//div[contains(@data-test-target, 'expand-review')]").click()
    except selenium.common.exceptions.StaleElementReferenceException:
        pass  # print("Clicked the Read More element...")
    time.sleep(3)

    container = driver.find_elements(By.XPATH, "//div[@data-reviewid]")
    dates = driver.find_elements(By.XPATH, "//span[contains(string(), 'Date of stay:')]")
    dates = dates[::2]

    for j in range(len(container)):
        rating = container[j] \
            .find_element(By.XPATH, ".//span[contains(@class, 'ui_bubble_rating bubble_')]") \
            .get_attribute("class").split("_")[3][:-1]
        title = container[j].find_element(By.XPATH, ".//div[contains(@data-test-target, 'review-title')]").text
        review = container[j].find_element(By.XPATH, ".//q").text.replace("\n", "  ")
        date = " ".join(dates[j].text.split(" ")[-2:])
        trip_type = ""
        try:
            trip_type_elem = container[j].find_element(By.XPATH, ".//span[@class='trip_type_label']/..")
            trip_type = trip_type_elem.text.replace("Trip type: ", "")
            trip_type = "".join(trip_type.split(" ")[-1:]) if trip_type != "" else ""
        except selenium.common.exceptions.NoSuchElementException:
            pass

        csvWriter.writerow([date, rating, trip_type, title, review])

    try:
        driver.find_element(By.XPATH, './/a[@class="ui_button nav next primary "]').click()
    except selenium.common.exceptions.NoSuchElementException:
        break  # print("Going to the next page")

print("Saved to: " + path_to_file)
driver.quit()
csvFile.close()
