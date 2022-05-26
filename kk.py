from flask import Flask, render_template, url_for,request,redirect
app = Flask(__name__)
import sqlite3

connection = sqlite3.connect('chven.db',check_same_thread=False)



table = """CREATE TABLE users(
           name VARCHAR(15),
           lastname VARCHAR(15),
           Python VARCHAR(3),
           Calculus VARCHAR(3),
           Startups VARCHAR(3),
           Average VARCHAR(4)
         );"""
cursor = connection.cursor()
# cursor.execute(f'ALTER TABLE users ADD color VARCHAR(10)') 

def insertInformationIndb(name,lastname,python,calculus,startups):
    pythoni = int(python)
    calculusi = int(calculus)
    startupsi = int(startups)
    average = int((calculusi+startupsi+pythoni)/3)
    average = str(average)
    if pythoni>=0 and pythoni<=100 and calculusi>=0 and calculusi<=100 and startupsi>=0 and startupsi<=100 :
        if float(average) > 50:
            code = f'INSERT INTO users VALUES("{name}","{lastname}","{pythoni}","{startupsi}","{calculusi}","{average}","green")'
            cursor.execute(code)
            connection.commit() 
        else:  
            code = f'INSERT INTO users VALUES("{name}","{lastname}","{pythoni}","{startupsi}","{calculusi}","{average}","red")'
            cursor.execute(code)
            connection.commit() 
    else:
        return 'fill the form with the correct points, from 0 to 100.'

def showAll():
    code = 'SELECT * FROM users'
    cursor.execute(code)
    sourse = cursor.fetchall()
    return sourse

def showconcret(source):
    list = []
    word =''
    for i in source:
        if i!=" ":
            word += i
        else :
            list.append(word)
            word = '' 
    list.append(word)        
    try:
        code = f'SELECT * FROM users WHERE name LIKE "%{list[0]}%" AND lastname LIKE "%{list[1]}%"'
        print(code)
        cursor.execute(code)
        sourse = cursor.fetchall()
        print(source)
        return sourse    
        
    except:
        try:
             code = f'SELECT * FROM users WHERE name LIKE "%{list[0]}%"'
             print(code) 
             cursor.execute(code)
             sourse = cursor.fetchall()
             print(sourse)
             print('kk')
             if sourse!=[]:
               return sourse  
             else:
                 code = f'SELECT * FROM users WHERE lastname LIKE "%{list[0]}%"'
                 print(code)
                 cursor.execute(code)
                 sourse = cursor.fetchall()
                 print(source)
                 return sourse    
           
        except:
            try:
             code = f'SELECT * FROM users WHERE lastname="{list[0]}"'
             print(code)
             cursor.execute(code)
             sourse = cursor.fetchall()
             print(source)
             return sourse    
            except:
                print('idk')

@app.route('/',methods=['POST','GET'])
def mainPage():
    if request.method == 'GET':
        student = showAll() 
        return render_template('kk.html',students = student)

    elif request.method == 'POST':
        info = request.form
        hm = insertInformationIndb(info['name'],info['lastname'],info['Python'],info['Calculus'],info['Startups'])

        if hm !='fill the form with the correct points, from 0 to 100.':
            student = showAll()
            return render_template('kk.html',students = student)

        else:
            student = showAll()
            return render_template('kk.html',students = student,sms = hm) 

@app.route('/deleted',methods=['POST'])
def deleted():
    info = request.form
    info = list(info)
    list1 = []
    word =''

    for i in info[0]:
        
        if i!=" ":
            word += i
        else :
            list1.append(word)
            word = '' 

    list1.append(word) 
    code =   f'DELETE FROM users WHERE name="{list1[0]}" AND lastname="{list1[1]}"'
    cursor.execute(code)
    connection.commit() 
    print(list)
    return redirect('/')     

@app.route('/result',methods = ['POST','GET'])
def result():
    if request.method=='POST':
         source = request.form
         result1 = showconcret(source['info'])
         print(result1)
         return render_template('kkk.html',students = result1)

if __name__ == '__main__':
   app.run(debug=True)