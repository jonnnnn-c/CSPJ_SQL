import os
import shutil
import mysql.connector
from flask import Flask

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')  # import config settings

mydb = mysql.connector.connect(
    host=app.config['HOST'],
    user=app.config['USER'],
    password=app.config['PASSWORD'],
    database=app.config['DATABASE']
)

mycursor = mydb.cursor()

sql = "DROP TABLE IF EXISTS candidates"
mycursor.execute(sql)

sql = "DROP TABLE IF EXISTS users"
mycursor.execute(sql)

sql = "DROP TABLE IF EXISTS companies"
mycursor.execute(sql)

sql = "DROP TABLE IF EXISTS logged_in"
mycursor.execute(sql)

# Would create a new company so delete just in case.
# Company_id might be more than 3 so need delete those manually.
sql = "DROP TABLE IF EXISTS scan_results_company_1"
mycursor.execute(sql)
sql = "DROP TABLE IF EXISTS scan_results_company_2"
mycursor.execute(sql)
sql = "DROP TABLE IF EXISTS scan_results_company_3"
mycursor.execute(sql)

sql = "DROP TABLE IF EXISTS masking"
mycursor.execute(sql)

print("DROPPED TABLE")

# Create Database
mycursor.execute("CREATE TABLE candidates (id INT AUTO_INCREMENT PRIMARY KEY, company_id INT NOT NULL, first_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255), phone_number VARCHAR(255), nric VARCHAR(255), address VARCHAR(255), gender VARCHAR(255), birthdate VARCHAR(255), age VARCHAR(255), field_of_interest VARCHAR(255), comments_box VARCHAR(255), resume VARCHAR(255), notes VARCHAR(255))")

mycursor.execute("CREATE TABLE companies (id INT AUTO_INCREMENT PRIMARY KEY, company_name VARCHAR(255))")
mycursor.execute("ALTER TABLE companies ADD UNIQUE (company_name)")

mycursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, company_id INT NOT NULL, email VARCHAR(255), password VARCHAR(255), registered_on VARCHAR(255), confirmed_on VARCHAR(255), role VARCHAR(255))")
mycursor.execute("ALTER TABLE users ADD CONSTRAINT fk_company_id foreign key(company_id) references companies(id)")

mycursor.execute("CREATE TABLE logged_in (id INT AUTO_INCREMENT PRIMARY KEY, user INT NOT NULL, email VARCHAR(255), company_id INT NOT NULL, role VARCHAR(255), confirmed INT NOT NULL DEFAULT 0, user_id INT)")

sql = "INSERT INTO companies (company_name) VALUES ('Company A')"
mycursor.execute(sql)

# sql = "INSERT INTO companies (company_name) VALUES ('Company B')"
# mycursor.execute(sql)

admin_password = b'P\xfbCg\xfe\xcf\xc3\xff\xec\x02\x9f\xd0BC\x89f\xf3\xb3}\x17]\xa9\xd5\x9fG\xc2\xde\x95p\x8f\x1e;'
cm_password = b'\x18\xde\x87N\xb0\xdf\x87\xd4\x124\xe3\xc4\xa6\xce\x05>\x8f\\\x16m\xdc\xa8\xb8\xf5q\x18p\x1di\xcb$\xe1'
ha_password = b'L\xc9\x96\xad\xd0\xb0>3v4z\xbd\xccR\x92\xad/\xd1\x07\x9d\xb7\x0b\xae\x16\xaa\xb9B\x8a\xcb\x076\x0c'

sql = 'INSERT INTO users (company_id, email, password, registered_on, confirmed_on, role) VALUES (1, "administrator@tool.com", "' + str(admin_password) + '", "2020-06-24 22:45:22.571809", "2020-06-24 22:45:22.571809", "Administrator")'
mycursor.execute(sql)

sql = 'INSERT INTO users (company_id, email, password, registered_on, confirmed_on, role) VALUES (1, "manager@tool.com", "' + str(cm_password) + '", "2020-12-24 09:04:25.121153", "2020-12-24 09:04:25.121153", "Candidate Manager")'
mycursor.execute(sql)

sql = 'INSERT INTO users (company_id, email, password, registered_on, confirmed_on, role) VALUES (1, "agent@tool.com", "' + str(ha_password) + '", "2021-01-19 05:28:38.261383", "2021-01-19 05:28:38.261383", "Hire Agent")'
mycursor.execute(sql)

sql = "INSERT INTO candidates (company_id, first_name, last_name, email, phone_number, nric, address, gender, birthdate, age, field_of_interest, comments_box, resume, notes) VALUES (1, 'Darla', 'Demarco', 'dd@gmail.com', '+6591234567', 'T0123456A', 'Block 131 Bishan Street 11 #03-10 S122131', 'F', '2001-02-06', '19', 'Sales', 'Old Phone number +6592836156', '', '')"
mycursor.execute(sql)

sql = "INSERT INTO candidates (company_id, first_name, last_name, email, phone_number, nric, address, gender, birthdate, age, field_of_interest, comments_box, resume, notes) VALUES (1, 'Mirra', 'Karlsson', 'mk@gmail.com', '+6589876543', 'T0235678B', 'Block 85 Tampines Street 1 #03-79 S109885', 'F', '2002-07-18', '18', 'Education', 'Alternative IC T0376182C', '', '')"
mycursor.execute(sql)

sql = "INSERT INTO candidates (company_id, first_name, last_name, email, phone_number, nric, address, gender, birthdate, age, field_of_interest, comments_box, resume, notes) VALUES (1, 'Taylor', 'Cook', 'taylorc@gmail.com', '+6582748993', 'T0087364C', 'Block 65 Toa Payoh Lor 3 #12-12 S122565', 'M', '2000-01-14', '20', 'Science and Technology', 'Interested in IT', '', '')"
mycursor.execute(sql)


# ADMINISTRATOR LOGIN
sql = "INSERT INTO logged_in (user, email, company_id, role, confirmed, user_id) VALUES (1, 'administrator@tool.com', 1, 'Administrator', 1, 1)"
mycursor.execute(sql)


'''
# CANDIDATE MANAGER LOGIN
sql = "INSERT INTO logged_in (user, email, company_id, role, confirmed, user_id) VALUES (1, 'manager@tool.com', 1, 'Candidate Manager', 1, 3)"
mycursor.execute(sql)
'''

'''
# HIRE AGENT LOGIN
sql = "INSERT INTO logged_in (user, email, company_id, role, confirmed, user_id) VALUES (1, 'agent@tool.com', 1, 'Hire Agent', 1, 4)"
mycursor.execute(sql)
'''

# For scan results of existing company 1 and 2
mycursor.execute("CREATE TABLE scan_results_company_1 (COMPANY_ID VARCHAR(255), FILENAME VARCHAR(255), SENSITIVITY VARCHAR(255), SG_PHONE VARCHAR(255), SG_ADDRESS VARCHAR(255), EMAIL VARCHAR(255), NRIC VARCHAR(255), URL VARCHAR(255), CREDIT_CARD_NUMBER VARCHAR(255), IP_ADDRESS VARCHAR(255), PERSON VARCHAR(255), GPE VARCHAR(255), DATE VARCHAR(255))")

# For masking configurations
mycursor.execute("CREATE TABLE masking (id INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(255), regex VARCHAR(255), example VARCHAR(255), applyon INT NOT NULL DEFAULT 0)")

sql = "INSERT INTO masking (category, example, applyon) VALUES (%s, %s, %s)"
values = ('SPECIAL DETECTION', 'Dynamic data (eg. websites)', 1)
mycursor.execute(sql, values)

sql = "INSERT INTO masking (category, regex, example, applyon) VALUES (%s, %s, %s, %s)"
values = ('NRIC', '[stfg|STFG]\d{7}[a-z|A-Z]', 'T0123456A', 2)
mycursor.execute(sql, values)

sql = "INSERT INTO masking (category, regex, example, applyon) VALUES (%s, %s, %s, %s)"
values = ('PHONE NUMBER', '(?:\+65|65|\(65\))(?:\s|\-|)[6|8|9]\d{3}(?:\s|\-|)\d{4}|[6|8|9]\d{3}(?:\s|\-|)\d{4}', '+65 9123 4567', 1)
mycursor.execute(sql, values)

sql = "INSERT INTO masking (category, regex, example, applyon) VALUES (%s, %s, %s, %s)"
values = ('EMAIL', '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', 'example@gmail.com', 1)
mycursor.execute(sql, values)

sql = "INSERT INTO masking (category, regex, example, applyon) VALUES (%s, %s, %s, %s)"
values = ('POSTAL CODE', '.*[S|s|Singapore]\s*\d{6}', 'S123456', 1)
mycursor.execute(sql, values)

mydb.commit()
print("CREATED TABLE")

if os.path.exists('../Data_Detection/company_1'):
    shutil.rmtree('../Data_Detection/company_1')
    print('Removed company_1 folder')


'''
MASKING table - applyon
0: none
1: hire agent
2: hire agent, candidate manager
'''

'''
DROP TABLE mydb.candidates;
CREATE TABLE mydb.candidates (id INT AUTO_INCREMENT PRIMARY KEY, company_id INT NOT NULL, first_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255), phone_number VARCHAR(255), nric VARCHAR(255), address VARCHAR(255), gender VARCHAR(255), birthdate VARCHAR(255), age VARCHAR(255), field_of_interest VARCHAR(255), comments_box VARCHAR(255), resume VARCHAR(255), notes VARCHAR(255));
INSERT INTO mydb.candidates (company_id, first_name, last_name, email, phone_number, nric, address, gender, birthdate, age, field_of_interest, comments_box, resume, notes) VALUES (1, 'Darla', 'Demarco', 'dd@gmail.com', '+6591234567', 'T0123456A', 'Block 131 Bishan Street 11 #03-10 S122131', 'F', '2001-02-06', '19', 'Sales', 'Old Phone number +6592836156', '', '');
INSERT INTO mydb.candidates (company_id, first_name, last_name, email, phone_number, nric, address, gender, birthdate, age, field_of_interest, comments_box, resume, notes) VALUES (1, 'Mirra', 'Karlsson', 'mirak@gmail.com', '+6589876543', 'T0235678B', 'Block 85 Tampines Street 1 #03-79 S109885', 'F', '2002-07-18', '18', 'Education', 'Alternative IC T0376182C', '', '');
INSERT INTO mydb.candidates (company_id, first_name, last_name, email, phone_number, nric, address, gender, birthdate, age, field_of_interest, comments_box, resume, notes) VALUES (1, 'Taylor', 'Cook', 'taylorc@gmail.com', '+6582748993', 'T0087364C', 'Block 65 Toa Payoh Lor 3 #12-12 S122565', 'M', '2000-01-14', '20', 'Science and technology', 'Interested in IT', '', '');

'''
