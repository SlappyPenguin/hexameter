from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("https://www.hexameter.co/login")

saved_lines = {}
all_lines = []

compression_factor = 20

def init_dictionary():
    dictionary_file = open("hexameter.txt", "r")

    for line in dictionary_file:
        line = line.strip()
        line = line.split(" 0 ")
        line[0] = line[0][:20]
        saved_lines[line[0]] = line[1]

    dictionary_file.close()

def perform_login(email, password):
    name_input = driver.find_element("name", "email")
    name_input.send_keys(email)

    password_input = driver.find_element("name", "password")
    password_input.send_keys(password)

    login_button = driver.find_element("xpath", "//button[@class='btn btn-primary']")
    login_button.click()

def enter_scan_page():
    scan_button = driver.find_element("xpath", "//a[@class='nav-link' and @data-toggle='modal' and @data-target='#modal-select-author']")
    scan_button.click()
    time.sleep(1)

    all_authors = driver.find_element("xpath", "//button[@name='author' and @value='0' and @type='submit' and @class='btn btn-default btn-block']")
    all_authors.click()
    time.sleep(1)

def save_dictionary():
    out_file = open("hexameter.txt", "w")
    for line in saved_lines:
        out_file.write(line + " 0 " + saved_lines[line] + "\n")
    out_file.close()
    full_file = open("hexameter_full.txt", "a")
    for line in all_lines:
        full_file.write(line + " 0 " + saved_lines[line[:compression_factor]] + "\n")
    full_file.close()

init_dictionary()

perform_login("jordanramsay21@gmail.com", "plmoknijb")
enter_scan_page()

while True:
    try:
        #read line
        line_object = driver.find_element("xpath", "//h2[@class='default-latin-verse']")
        line_full = line_object.text
        response = ""
        line = line_full[:compression_factor]

        has_line_saved = line in saved_lines
        if has_line_saved:
            response = saved_lines[line]
        else:
            all_lines.append(line_full)
            response = "DSDS"
        #write response
        response_input = driver.find_element("xpath", "//input[@data-toggle='popover' and @placeholder='Scansion']")
        response_input.send_keys(response)

        submit_button = driver.find_element("xpath", "//button[@class='btn btn-primary btn-block']")
        submit_button.click()

        time.sleep(1)

        if not has_line_saved:
            correct_answer_object = driver.find_element("xpath", "(//div[@class='col-lg-3 col-md-6'])[3]//p")
            correct = correct_answer_object.text
            saved_lines[line] = correct

        next_button = driver.find_element("xpath", "//button[@class='btn btn-primary btn-block']")
        next_button.click()
        
        time.sleep(1)
    except:
        break

save_dictionary()
driver.quit()