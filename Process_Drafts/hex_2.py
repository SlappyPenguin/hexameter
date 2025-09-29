from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("https://www.hexameter.co/login")

name_input = driver.find_element("name", "email")
user_email = "jordanramsay21@gmail.com"
name_input.send_keys(user_email)

password_input = driver.find_element("name", "password")
user_password = "plmoknijb"
password_input.send_keys(user_password)

login_button = driver.find_element("xpath", "//button[@class='btn btn-primary']")
login_button.click()

#check that the login was successful
assert driver.current_url == "https://www.hexameter.co/home"

#click scan button
scan_button = driver.find_element("xpath", "//a[@class='nav-link' and @data-toggle='modal' and @data-target='#modal-select-author']")
scan_button.click()

time.sleep(1)

all_authors = driver.find_element("xpath", "//button[@name='author' and @value='0' and @type='submit' and @class='btn btn-default btn-block']")
all_authors.click()

time.sleep(1)

dictionary_file = open("hexameter.txt", "r")

saved_lines = {}

for line in dictionary_file:
    line = line.strip()
    line = line.split(" 0 ")
    saved_lines[line[0]] = line[1]

dictionary_file.close()

while True:
    try:
        #read line
        line_object = driver.find_element("xpath", "//h2[@class='default-latin-verse']")
        line = line_object.text
        response = ""
        
        has_line_saved = line in saved_lines
        if has_line_saved:
            response = saved_lines[line]
        else:
            response = "DSDS"
        #write response
        response_input = driver.find_element("xpath", "//input[@data-toggle='popover' and @placeholder='Scansion']")
        response_input.send_keys(response)

        submit_button = driver.find_element("xpath", "//button[@class='btn btn-primary btn-block']")
        submit_button.click()

        time.sleep(2)

        try:
            popup_button = driver.find_element("xpath", "//button[@type='button' and @class='close' and @data-dismiss='modal' and @aria-label='Close']")
            popup_button.click()
            time.sleep(2)
        except:
            pass

        if not has_line_saved:
            correct_answer_object = driver.find_element("xpath", "(//div[@class='col-lg-3 col-md-6'])[3]//p")
            correct = correct_answer_object.text
            saved_lines[line] = correct

        next_button = driver.find_element("xpath", "//button[@class='btn btn-primary btn-block']")
        next_button.click()
        time.sleep(1)
    except:
        break

driver.quit()
out_file = open("hexameter.txt", "w")
for line in saved_lines:
    out_file.write(line + " 0 " + saved_lines[line] + "\n")
out_file.close()
