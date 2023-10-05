import mysql.connector as connection
import random
import time
import sys
myconnect = connection.connect(host = "127.0.0.1", user = "root", password = "Aderinoye234$", database = "election")
cursor = myconnect.cursor()

class voting:

    def __init__ (self):
        self.dept = ["cyber_security", "data_analysis", "data_science","graphic_design",
                     "javascript","ui_ux","web_development"]
        self.pres = ["Emmanuel Adeleke", "Oluwaseun Enoch", "Femi Falana"]
        self.vice = ["Shallom Okeke", "May Zeal","Okon Godwin"]
        self.gen = ["Debby Jay", "Ubani Ezinne", "Abiola Favour"]
        self.start()

    def start(self): #This is the homepage for students to register and login
        print("""WELCOME TO SQI COLLEGE OF ICT\nENTER 1 TO REGISTER\nENTER 2 TO LOG IN\n
              ENTER ANY KEY TO EXIT """)
        self.choice = input(">>>: ")
        if self.choice == "1":
            self.register()
        elif self.choice == "2":
            self.login()
        else:
            sys.exit()

    def register(self): #Students are required to register before logging in
        print(self.dept)
        print("")
        self.dep = input("Enter The Department You Like To Register: ").strip().lower()
        if self.dep in self.dept:
            print("Processing....")
            time.sleep(1)
            self.details = ["Firstname","Lastname","Age","Gender","dep_level"]
            self.info = []
            for i in self.details: #interating required keys to ask for information to enter
                information = input (f"Enter your {i}: ")
                self.info.append(information)
            username = self.info [0][-3:] + str(random.randrange(350,700))#generate students username using random numbers
            self.info.append(username)
            matric_no = random.randrange(2001, 5000)#generate students matricnumber
            self.info.append(matric_no)
            pwd = self.info [1][:3]+ str(random.randrange(800,1000))
            self.info.append(pwd)
            self.enter()#Inserting students details into various department tables in the school database
            print(f"REGISTRATION COMPLETE. YOUR USERNAME IS {username}, YOUR MATRIC_NO IS {matric_no} AND YOUR PASSWORD IS {pwd}")
            self.operate()
            
        else:
            print("DEPARTMENT NOT FOUND")
            self.register()#if condition is not met return back to registeration page

    def enter(self):
        self.dep_querry =f"INSERT INTO {self.dep} (Fname, Lname, Age, Gender, dep_level, username, matric_no, pwd) VALUES({'%s'},{'%s'},{'%s'},{'%s'},{'%s'},{'%s'},{'%s'},{'%s'})"#inputing students value/response into each key/information asked
        self.val = tuple(self.info)
        cursor.execute(self.dep_querry, self.val)
        myconnect.commit()#Inserting students details into database
    
    def login(self):#To login following info are required
        self.dep = input("Enter your department: ")
        if self.dep in self.dept:
            self.user = input("Enter your username: ")
            self.pwd = input("Enter your password: ")
            self.log = f"SELECT * FROM {self.dep} WHERE username = {'%s'} and pwd = {'%s'}"#To access login, select  details
            self.va = (self.user, self.pwd)                                                #from departmental table in Database
            cursor.execute(self.log, self.va)
            self.result = cursor.fetchone()#fetch details if true to log in users successful
            if self.result is not None:
                print("PROCESSING.......")
                time.sleep(2)
                print(f" DEAR {self.result[1]} YOU HAVE SUCCESSFULLY LOGGED IN")
                print("")
                print("")
                self.operate()
                
            else:
                print("INVALID LOG IN DETAILS")#otherwise log in failed, ask users to enter correct details
                self.login()
        else:
            print("INCORRECT DEPARTMENT")#ask users to enter one of the available departments
            self.login()

    def operate (self):#Function for electoral procedurce
        print("""WELCOME TO SQI POLLING UNIT\nWHAT OPERATION WILL YOU LIKE TO PERFORM;\n
              ENTER 1 TO REGISTER TO VOTE\nENTER 2 TO CAST YOUR VOTE\nENTER 3 TO CHECK FOR ELECTION RESULT\nENTER ANY KEY TO EXIT""")
        self.decide = input (">>>>: ")
        if self.decide == "1":
            self.votereg()
        elif self.decide == "2":
            self.cast()
        elif self.decide == "3":
            self.check()
        else:
            sys.exit()

    def votereg(self):#function for electorate to register for election
        self.ma = input("ENTER YOUR MATRIC NUMBER: ")
        self. det = input("ENTER YOUR DEPARTMENT: ")
        if self.det in self.dept:#if users input is present in the available department
            self.query = f"SELECT * FROM {self.det} WHERE matric_no = {'%s'} "#To confirm if details input is
            self.vall = (self.ma,)                                              #in anlignment with details in database
            cursor.execute(self.query, self.vall)
            self.res = cursor.fetchone()
            if self.res is not None:
                self.voter_card = random.randrange(31007, 89009) #Generate voters card for users
                self.full = self.res[1]+ " " + self.res[2] #confirm fullname while fetching fname and lname from database
                self.level = self.res[5]#confirm electorate level from database
                self.qual = "INSERT INTO voters(voter_card, full_name, level, department, matric_no, President, Vice_president, Gen_sec)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"#enter student details into voters portal
                self.vow = (self.voter_card, self.full, self.level, self.det, self.ma, "Not voted","Not voted", "Not voted")#
                cursor.execute(self.qual, self.vow)
                myconnect.commit()
                print (f"DEAR {self.full} you have successfully registered for a voter card. CONGRATULATION your voter card number is {self.voter_card}")
                self.cast()
        else:
            print("NO MATCH!!. TRY AGAIN")
            self.votereg()#reurn back to enter available department
    def cast(self):
        self.ask = int(input("Enter your voter card number: "))
        self.qur = "SELECT * FROM voters WHERE voter_card = %s"#To confirm if electorate input the correect voter_card number
        self.vel = (self.ask,)
        cursor.execute(self.qur, self.vel)
        self.real = cursor.fetchone()#To fetch electorate voter_card number
        if self.real is not None:
            self.confirmcast()
        
    def confirmcast(self):
        cursor.execute(self.qur, self.vel)
        self.real = cursor.fetchone()
        self.vote = input("""TO VOTE FOR YOUR CANDIDATE;\nENTER 1 FOR PRESIDENT\n
                              \nENTER 2 FOR VICE-PRESIDENT\nENTER 3 GEN.SEC\nENTER ANY KEY TO PROCCED TO NEXT VOTING EXERCISE.>>>>: """)
        if self.vote == "1":
            if self.real[5]!= "Not voted":#select column via indexing from database and ensuring that electorate does not cast vote twice
                print("YOU HAVE ALREADY CASTED YOUR VOTE IN THIS CATEGORY")
                self.confirmcast()#users will/will not like to continue voting exercise
            else:
                print(f"THESE ARE THE PRESIDENTIAL CANDIDATES\n{self.pres}")
                self.pres_cast = input("ENTER THE NAME OF YOUR PREFERED CANDIDATE>>>:  ").strip().capitalize()
                while self.pres_cast not in self.pres:#if name entered not part of the presidential candidate
                    print("CANDIDATE NAME NOT PRESENT IN THE BALLOT LIST")
                    self.pres_cast = input("ENTER THE NAME OF YOUR PREFERED CANDIDATE>>>:  ").strip().capitalize()
                else:
                    self.prquar = "UPDATE voters SET President = %s WHERE voter_card = %s"#To input candidate name on voters portal
                    self.vl = (self.pres_cast, self.ask)
                    cursor.execute(self.prquar, self.vl)
                    myconnect.commit() 
                    print("PROCESSING......")
                    time.sleep(2)
                    print("YOU HAVE SUCCESSFUL CASTED YOUR VOTE FOR PRESIDENCY")
                    self.con()#Ask users what operation they want to perform/proceed next voting exercise
            
        elif self.vote == "2":
            if self.real[6]!= "Not voted":# select column via indexing from database and ensuring that electorate does not cast vote twice
                print("YOU HAVE ALREADY CASTED YOUR VOTE IN THIS CATEGORY")
                self.confirmcast #users will/will not like to continue voting exercise
            else:
                print(f"THESE ARE THE CANDIDATES FOR VICE-PRESIDENT\n{self.vice}")
                self.vicepre = input("ENTER THE NAME OF YOUR PREFERED CANDIDATE>>>: ").strip().capitalize()
                while self.vicepre not in self.vice:#if name not present in candidate list ask electorate to input  one of the present name on list
                    print("CANDIDATE NAME NOT PRESENT IN THE BALLOT LIST")
                    self.vicepre = input("ENTER THE NAME OF YOUR PREFERED CANDIDATE>>>: ").strip().capitalize()
                else:
                    self.viquar = "UPDATE voters SET Vice_president = %s WHERE voter_card = %s"#To input candidate name on voters portal
                    self.ver = (self.vicepre, self.ask)
                    cursor.execute(self.viquar, self.ver)#To perform the above operation
                    myconnect.commit()
                    print("PROCESSING....")
                    time.sleep(2)
                    print("YOU HAVE SUCCESSFULLY CASTED YOUR VOTE FOR VICE-PRESIDENT CATEGORY")
                    self.con()
            
        elif self.vote == "3":
            if self.real[7]!= "Not voted":#select column via indexing from database and ensuring that electorate don't cast vote twice
                print("YOU HAVE ALREADY CASTED YOUR VOTE IN THIS CATEGORY")
                self.confirmcast()#users will/will not like to continue voting exercise
            else:
                print(f"THESE ARE THE CANDIDATES FOR GENERAL SECETARY\n{self.gen}")
                self.genpr = input("ENTER THE NAME OF YOUR PREFERED CANDIDATE>>>: ").strip().capitalize()
                while self.genpr not in self.gen:#if name not present in candidate list ask electorate to input  one of the present name on list
                    print("CANDIDATE NAME NOT PRESENT IN THE BALLOT LIST")
                    self.genpr = input("ENTER THE NAME OF YOUR PREFERED CANDIDATE>>>: ").strip().capitalize()
                else:
                    self.genquar = "UPDATE voters SET Gen_sec = %s WHERE voter_card = %s"#To input candidate name on voters portal
                    self.ver = (self.genpr, self.ask)
                    cursor.execute(self.genquar, self.ver)#to perform above operation
                    myconnect.commit()
                    print("PROCESSING......")
                    time.sleep(2)
                    print("YOU HAVE SUCCESSFULLY CASTED YOUR VOTE FOR GENERAL SECETARY CATEGORY")
                    self.con()#Ask electorate to proceed to next voting exercise
        else:
            self.con()
    def check(self):#function for electorate to view total number of vote
        print("ENTER 1 TO VIEW DEPARTMENTAL BASE RESULT\nENTER 2 TO VIEW OVERALL RESULT\nENTER 3 TO GO BACK TO VOTE\nENTER ANY KEY TO EXIT: ")
        self.chk = input(">>>>: ")
        self.every = {}#To interate number of vote per candidate
        if self.chk == "1":#To view departmental winners
            self.dip = input(f"{self.dept}\nENTER WHAT DEPARTMENT YOU LIKE TO VIEW:  ")
            while self.dip not in self.dept:#To ensure electorate enter one of the listed department
                print("DEPARTMENT NOT AVAILABLE")
                self.cat = input("WHAT CATEGORY WILL YOU LIKE TO VIEW\n1. Presidential category\n2. Vice-president category\n3. General secetary category\n4. To GO BACK: ")
            else:
                self.cat = input("WHAT CATEGORY WILL YOU LIKE TO VIEW\n1. Presidential category\n2. Vice-president category\n3. General secetary category\n4. To GO BACK: ")
                if self.cat == "1":
                    for name in self.pres:#interate list of candidate out
                        self.precat_quer ="SELECT count(President) from voters where President=%s and department=%s"#To accumlate total votes per candidate
                        self.preval = (name, self.dip) 
                        cursor.execute(self.precat_quer, self.preval)
                        self.resl = cursor.fetchone()#To fetch name of candidate, electorate voted for
                        print(f"{name} has {self.resl[0]} votes in {self.dip} department")
                        self.every[name]=self.resl#To get the  candidate with the highest number of vote
                    max_pres = max(self.every, key=self.every.get)#To get the name of the candidate with the maximum number
                    score = self.every[max_pres]#To get highest number of vote
                    print(f"The overall winner for presidential category in {self.dip} department is {max_pres} with a total score of {score} ")
                
                elif self.cat == "2":
                    for i in self.vice:#interate list of candidate out
                        self.vice_query = "SELECT count(Vice_president) from voters where Vice_president= %s and department=%s"#To accumlate total votes per candidate
                        self.vicval = (i, self.dip)
                        cursor.execute(self.vice_query,self.vicval)
                        self.rest = cursor.fetchone()#To fetch name of candidate, electorate voted for
                        print(f"{i} has {self.rest[0]} votes in {self.dip} department")
                        self.every[i]=self.rest#To get the  candidate with the highest number of vote
                    max_vice = max(self.every, key=self.every.get)#To get the name of the candidate with the maximum number
                    score = self.every[max_vice]#To get highest number of vote
                    print(f"The overall winner for Vice-president category in {self.dip} department is {max_vice} with a total score of {score} ")

                elif self.cat == "3":
                    for x in self.gen:#interate list of candidate out
                        self.genquerr = "SELECT count(Gen_sec) from voters where Gen_sec=%s and department=%s"#To accumlate total votes per candidate
                        self.genval = (x, self.dip)
                        cursor.execute(self.genquerr,self.genval)
                        self.resl = cursor.fetchone()#To fetch name of candidate, electorate voted for in a particular department
                        print(f"{x} has {self.resl} votes in {self.dip} department")
                        self.every[x]=self.resl#To get the  candidate with the highest number of vote
                    max_gen = max(self.every, key=self.every.get)#To get the name of the candidate with the maximum number
                    score = self.every[max_gen]#To get highest number of vote
                    print(f"The overall winner for general secetary category in {self.dip} department is {max_gen} with a total score of {score}")

        elif self.chk == "2":#To view overall winners
            self.cat = input("WHAT CATEGORY WILL YOU LIKE TO VIEW\n1. Presidential category\n2. Vice-president category\n3. General secetary category\n4. To GO BACK: ")
            self.all = {}
            if self.cat == "1":
                for name in self.pres:#interate list of presidential candidate out
                    self.precat_quer ="SELECT count(President) from voters where President= %s"
                    self.preval = (name,) 
                    cursor.execute(self.precat_quer, self.preval)
                    self.resl = cursor.fetchone()#To fetch name of candidate, electorate voted for
                    print(f"{name} has {self.resl[0]} votes")
                    self.all[name]=self.resl#To get the  candidate with the highest number of vote
                max_pres = max(self.all, key=self.all.get)#To get the name of the candidate with the maximum number
                score = self.all[max_pres]#To get highest number of vote
                print(f"The overall winner for Presidential Category is {max_pres} with the total vote of {score}")
                self.operate()
                    
            elif self.cat == "2":
                for i in self.vice: #interate list of vice-presidential candidate out
                    self.vice_query = "SELECT count(Vice_president) from voters where Vice_president= %s"
                    self.vicval = (i,)
                    cursor.execute(self.vice_query,self.vicval)
                    self.rest = cursor.fetchone()#To fetch name of candidate, electorate voted for
                    print(f"{i} has {self.rest[0]} votes")
                    self.all[i]=self.rest#To get the  candidate with the highest number of vote
                max_vice = max(self.all, key=self.all.get)#To get the name of the candidate with the maximum number
                score = self.all[max_vice]#To get highest number of vote
                print(f"The overall winner for Vice-president category is {max_vice} with the total vote of {score}")
                self.operate()

            elif self.cat == "3":
                for x in self.gen:#interate list of General secetary candidate out
                    self.genquerr = "SELECT count(Gen_sec) from voters where Gen_sec=%s"
                    self.genval = (x,)
                    cursor.execute(self.genquerr,self.genval)
                    self.resl = cursor.fetchone()#To fetch name of candidate, electorate voted for
                    print(f"{x} has {self.resl} votes")
                    self.all[x]=self.resl#To get the  candidate with the highest number of vote
                max_gen = max(self.all, key=self.all.get)#To get the name of the candidate with the maximum number
                score = self.all[max_gen]#To get highest number of vote
                print(f"The overall winner for General secetary category is {max_gen} with the total vote of {score} ")
                self.operate()
            else:
                self.confirmcast()
        elif self.chk == "3":
            self.confirmcast()
        else:
            sys.exit()

    def con(self):#Function for next voting exercise
        print("WHAT OPERATION WILL YOU LIKE TO PERFORM; \nENTER 1 TO CONTINUE VOTE\nENTER 2 TO CHECK RESULT\nENTER KEY TO EXIT: ")
        self.tell = input(">>>: ")
        if self.tell == "1":
            self.confirmcast()
        elif self.tell == "2":
            self.check()
        else:
            sys.exit()#To exit electoral exercise
voting()