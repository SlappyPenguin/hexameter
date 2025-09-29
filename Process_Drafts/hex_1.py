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

saved_lines = {
"nec se magnanimo maledicere sentit Achilli?" : "SDDD", 
"non sine Marte tamen. bellum cum gente feroci" : "DDSS", 
"ultima caelestum terras Astraea reliquit." : "DSSS", 
"magna gemelliparae venerantur numina divae;" : "DDDS", 
"perque novem noctes venerem tactusque viriles" : "DSDS", 
"sumite serpentis! pro fontibus ille lacuque" : "DSSD", 
"dum licet, et nondum thalamos tenet altera nostros." : "DSDD", 
"spectat, et accensae non fortiter imperat irae," : "DSSD", 
"arcet et in lapidem rictus serpentis apertos" : "DDSS", 
"caerula Liriope, quam quondam flumine curvo" : "DDSS", 
"in cinerem vertunt; silvae cum montibus ardent;" : "DSSS", 
"aut haeret membris frustra temptata revelli," : "SSSS", 
"non dabit absumptis per longum viribus aevum," : "DSSS", 
"paenitet, et vellet non cognita posse reverti." : "DSSD", 
"contigit et glaebam: contactu glaeba potenti" : "DSSS", 
"et pariter frondes, pariter pallescere glandes" : "DSDS", 
"ter centum messes, ter centum musta videre." : "SSSS", 
"adspicit accensum nec tantos sustinet aestus" : "DSSS", 
"pabula canescunt, cum frondibus uritur arbor," : "DSSD", 
"et digitos digitis et frontem fronte premebam." : "DDSS", 
}

for i in range(0, 50):
    try:
        #read line
        line_object = driver.find_element("xpath", "//h2[@class='default-latin-verse']")
        line = line_object.text
        print("Current Line:", line)
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

        time.sleep(1)

    
        if not has_line_saved:
            correct_answer_object = driver.find_element("xpath", "(//div[@class='col-lg-3 col-md-6'])[3]//p")
            correct = correct_answer_object.text
            print("Correct Answer:", correct)
            saved_lines[line] = correct

        next_button = driver.find_element("xpath", "//button[@class='btn btn-primary btn-block']")
        next_button.click()
        time.sleep(1)
    except:
        break


driver.quit()
out_file_python = open("hexameter_python.txt", "w")
for line in saved_lines:
    out_file_python.write('"' + line + '" : "' + saved_lines[line] + '", \n')
out_file_python.close()
