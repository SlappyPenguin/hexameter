# Maximise window and zoom out

from selenium import webdriver
import time

compression_size = 100
email = "jordanramsay21@gmail.com"
saved_lines = {}

def compress_line(line):
    return line[:compression_size]

def init_hashmap():
    input_file = open("hexameter_input.txt", "r")
    for line in input_file:
        line = line.strip()
        line = line.split(" 0 ")
        line[0] = compress_line(line[0])
        saved_lines[line[0]] = line[1]
    input_file.close()

def login(email, password):
    name_input = driver.find_element("name", "email")
    name_input.send_keys(email)
    password_input = driver.find_element("name", "password")
    password_input.send_keys(password)
    login_button = driver.find_element("xpath", "//button[@class='btn btn-primary']")
    login_button.click()
    time.sleep(1)

def start_scanning():
    scan_button = driver.find_element("xpath", "//a[@class='nav-link' and @data-toggle='modal' and @data-target='#modal-select-author']")
    scan_button.click()
    time.sleep(1)
    all_authors_button = driver.find_element("xpath", "//button[@name='author' and @value='0' and @type='submit' and @class='btn btn-default btn-block']")
    all_authors_button.click()
    time.sleep(1)

def scan_line():
    line_object = driver.find_element("xpath", "//h2[@class='default-latin-verse']")
    line = line_object.text

    response = ""
    has_line_saved = compress_line(line) in saved_lines
    if has_line_saved:
        response = saved_lines[compress_line(line)]
    else:
        response = "DSDS"
    
    time.sleep(1)
    response_input = driver.find_element("xpath", "//input[@data-toggle='popover' and @placeholder='Scansion']")
    response_input.send_keys(response)
    submit_button = driver.find_element("xpath", "//button[@class='btn btn-primary btn-block']")
    submit_button.click()
    time.sleep(2)

    try:
        popup_button = driver.find_element("xpath", "//button[@type='button' and @class='close' and @data-dismiss='modal' and @aria-label='Close']")
        popup_button.click()
        time.sleep(3)
    except:
        pass

    return (line, has_line_saved)

def store_and_continue(line, has_line_saved):
    if not has_line_saved:
        answer_object = driver.find_element("xpath", "(//div[@class='col-lg-3 col-md-6'])[3]//p")
        answer = answer_object.text
        saved_lines[compress_line(line)] = answer
        output_file.write(line + " 0 " + answer + "\n")

    time.sleep(1)
    next_button = driver.find_element("xpath", "//button[@class='btn btn-primary btn-block']")
    next_button.click()
    time.sleep(1.5)

init_hashmap()
driver = webdriver.Chrome()
driver.get("https://www.hexameter.co/login")
time.sleep(1)
login(email, "plmoknijb")
start_scanning()

output_file = open("hexameter_output.txt", "w")
while True:
    try:
        line, has_line_saved = scan_line()
        store_and_continue(line, has_line_saved)
    except:
        time.sleep(20)
        break
output_file.close()
driver.quit()



