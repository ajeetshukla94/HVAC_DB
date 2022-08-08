import pandas as pd
from flask import Flask, render_template, flash, url_for, request, make_response, jsonify, session,send_from_directory
from werkzeug.utils import secure_filename
import os, time
import io
import base64
import json
import datetime
import os, sys, glob
from flask import send_file
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from fnmatch import fnmatch
import time
import random
from Report_Genration import Report_Genration
from crypt_services import encrypt_sha256
from db_dervices import DBO

user="Admin"
working_directory ="AIR_VELOCITY_REPORT\\{}"
final_working_directory ="AIR_VELOCITY_REPORT\\{}\\{}.xlsx"

app = Flask(__name__)
app.secret_key = 'file_upload_key'
MYDIR = os.path.dirname(__file__)
app.config['UPLOAD_FOLDER'] = "static/inputData/"


ISO_guidlines_master          = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'],"ISO_guidlines.xlsx"))
EUGMP_guidlines_master        = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'],"EUGMP_guidlines.xlsx"))
guidlance_list                = ISO_guidlines_master.Guidelines.unique().tolist()+EUGMP_guidlines_master.Guidelines.unique().tolist()



dbo = DBO()

sent_mail                     = False
condition_list                = ['At Rest','In Operation']
grade_list                    = ['A','B','C','D']
server                        = 'smtp.gmail.com'
port                          =  587
username                      =  "aajeetshk@gmail.com"
password                      =  "ilbumnmnsnqletdk"
send_from                     = "aajeetshk@gmail.com"
send_to                       = "ashish@pinpointengineers.co.in"

def send_mail(subject,text,files,file_name,isTls=True):
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = subject
        msg.attach(MIMEText(text))
        if file_name!="":
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(files, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename={}.xlsx'.format(file_name))
            msg.attach(part)
        
        #context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
        #SSL connection only working on Python 3+
        smtp = smtplib.SMTP(server, port)
        if isTls:
            smtp.starttls()
        smtp.login(username,password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.quit()
        
#################################### Start Login logout add user ######################################       
@app.route("/")
def render_default():
    if 'user' in session:
        session_var = session['user']
        ret_page = "HVAC_UI/Air_velocity.html"
        if session_var["role"] == "admin":
            ret_page = "ADMIN/UpdateCompanyDetails.html"
        return make_response(render_template(ret_page,msg = False, err = False, warn = False, role = session_var["role"]),200)     
    return make_response(render_template('LOGIN_PAGE/login.html'),200)
    
@app.route("/render_login", methods=["GET", "POST"])
def render_login():
    customer_details  = dbo.get_company_details()
    company_name_list = customer_details.COMPANY_NAME.unique().tolist()
    if request.method == 'POST':
      form_data = request.form
      l_id = form_data['login'].lower()
      pwd  = form_data['password']
      print(password)
      enc_pass = encrypt_sha256(l_id+pwd)  
      print(enc_pass)   
      account = dbo.get_cred(l_id)
      
      if(enc_pass == account["password"]):
          session_var = {"user": l_id, "role": account["role"],"username": account["username"]}
          session['user'] = session_var
          print('Login Successful')
          print(dbo.selected_instrument_dropdown("AIR_VELOCITY",session_var['user']))
          company_name_list             = dbo.selected_instrument_dropdown("AIR_VELOCITY",session_var['user']).COMPANY_NAME.unique().tolist()
          equipment_list                = dbo.selected_instrument_dropdown("AIR_VELOCITY",session_var['user']).SR_NO_ID.unique().tolist()
        
          if account["role"] == "admin":
              ret_page = "ADMIN/add_user.html"
          if account["role"] == "analyst":
              ret_page = "HVAC_UI/Air_velocity.html"
          if account["role"] == "operation":
              ret_page = "ELOGBOOK/approve_instrument_request.html"
          return make_response(render_template(ret_page,company_list=company_name_list,
                                grade_list = grade_list,
                                equipment_list = equipment_list,user_type='admin',
                                msg = True, err = False, warn = False, role = account["role"]),200)
      else:
          flash('Invalid Credentials')
          return make_response(render_template("LOGIN_PAGE/login.html", msg = False, err = True, warn = False),403)
    else:
        print('get request')
        
        
@app.route("/add_user_page")
def add_user_page():
    if 'user' in session:
        session_var = session['user']
        role = session_var["role"]
        return make_response(render_template('ADMIN/add_user.html',role = role),200) 
    return make_response(render_template('LOGIN_PAGE/login.html'),200)
    
@app.route("/thermal_report")
def thermal_report():
    if 'user' in session:
        session_var = session['user']
        role = session_var["role"]
        return make_response(render_template('HVAC_UI/Thermal.html',role = role),200) 
    return make_response(render_template('LOGIN_PAGE/login.html'),200)

        
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('selected_file', None)
    global Selected_files
    Selected_file = None
    flash('Logout Successful')
    return make_response(render_template("LOGIN_PAGE/login.html",msg = True, err = False, warn = False, message='Logout Successful'),200)


@app.route("/submit_add_user" )    
def submit_add_user():
    if 'user' in session:
        data            = request.args.get('params_data')
        data            = json.loads(data)    
        observation     = data['observation']
        temp_df         = pd.DataFrame.from_dict(observation,orient ='index')
        temp_df         = temp_df[['Role','fname','lname','Password']]
        print(temp_df)  
        for row in temp_df.itertuples():            
            fname    = row[2]
            lname    = row[3]
            role     = row[1]
            password = row[4]
            print(password)
            fname    = fname.lower()
            lname    = lname.lower()
            username = fname+lname[:2]+str(random.randint(10,99))
            print(username)
            dbo.create_user(username,fname,lname, role, encrypt_sha256(username+password))   

            subject   = "NEW USER REGISTERED TYPE -{} ID: {} ".format(role,username)
            text      = """Hi PinPoint Team \n\n
                           {} {} has been reigistered into HVAC system with  {} role \n\n
                           Kindly note done Login ID for Reference - {}
                           Regards \n
                           Ajeet Shukla :) :) :)""".format(fname,lname,role,username)
            #send_mail(subject,text,"","") 
        d = {"error":"none","userID":username}   
        return json.dumps(d)
#################################### End Login logout add user ######################################          
@app.route("/render_Air_velocity")
def render_Air_velocity():
    if 'user' in session:
        session_var = session['user']
        role = session_var["role"]
        #customer_details              = dbo.get_company_details()        
        company_name_list             = dbo.selected_instrument_dropdown("AIR_VELOCITY",session_var['user']).COMPANY_NAME.unique().tolist()
        equipment_list                = dbo.selected_instrument_dropdown("AIR_VELOCITY",session_var['user']).SR_NO_ID.unique().tolist()
        return make_response(render_template('HVAC_UI/Air_velocity.html',grade_list=grade_list,        
                            company_list=company_name_list,equipment_list =equipment_list,
                            role = role),200)
    return make_response(render_template('LOGIN_PAGE/login.html'),200)
    
    
@app.route("/render_paotest")
def render_paotest():
    if 'user' in session:
        session_var = session['user']
        role = session_var["role"]
        company_name_list             = dbo.selected_instrument_dropdown("PAO_TEST",session_var['user']).COMPANY_NAME.unique().tolist()
        equipment_list = dbo.selected_instrument_dropdown("PAO_TEST",session_var['user']).SR_NO_ID.unique().tolist()
        return make_response(render_template('HVAC_UI/PAO.html',company_list=company_name_list,
                                equipment_list =equipment_list, role = role),200)
    return make_response(render_template('LOGIN_PAGE/login.html'),200)
    
@app.route("/render_particle_count")
def render_particle_count():
    if 'user' in session:
        session_var = session['user']
        role = session_var["role"]
        #customer_details              = dbo.get_company_details()
        company_name_list             = dbo.selected_instrument_dropdown("PARTICLE_COUNT",session_var['user']).COMPANY_NAME.unique().tolist() 
        equipment_list                = dbo.selected_instrument_dropdown("PARTICLE_COUNT",session_var['user']).SR_NO_ID.unique().tolist()
        return make_response(render_template('HVAC_UI/particle_count.html',company_list=company_name_list,
    					     guidlance_list = guidlance_list  ,
    					     equipment_list = equipment_list,
                             condition_list = condition_list, role = role),200)
    return make_response(render_template('LOGIN_PAGE/login.html'),200)

 
@app.route("/get_available_directory", methods=['POST', 'GET'])
def get_available_directory():
    if 'user' in session:
        data          = request.args.get('params_data')
        report_type   = json.loads(data)
        report_type   = report_type.replace(" ","_")
        directory     = 'static\\Report\\{}'.format(report_type)
        sub_list      =os.listdir(directory)
        sub_list.insert(0,"ALL")
        dict_list=[]
        for x in sub_list:
            thisdict ={"id":x,"name":x}
            dict_list.append(thisdict)
        d = {"dict_list":dict_list,
             "start_date":str(datetime.datetime.today().strftime('%d/%m/%Y')),
             "end_date":str(datetime.datetime.today().strftime('%d/%m/%Y')),        
            }   
        return json.dumps(d)
    return make_response(render_template('LOGIN_PAGE/login.html'),200)
    
 
@app.route("/update_company_details", methods=['POST', 'GET'])
def update_company_details():
    if 'user' in session:
        data              = request.args.get('params_data')
        company_name_val  = json.loads(data)
        company_address   = ""
        report_id         = ""    
        location          = ""
        test_taken        = datetime.datetime.today().strftime('%d/%m/%Y')
        if company_name_val is not None :
            temp_df = dbo.get_company_details_by_company_name(company_name_val)
            report_id =str(temp_df.REPORT_NUMBER.values[0])
            company_address =str(temp_df.ADDRESS.values[0])       
           
        d = {
            "error":"none",
            "company_address":company_address,
            "report_id":str("PPE0{}AV01A".format(report_id)),
            "test_taken":test_taken,
            "location":location,
        }
        return json.dumps(d)
    return make_response(render_template('LOGIN_PAGE/login.html'),200)
    
    
@app.route("/update_instument_details", methods=['POST', 'GET'])
def update_instument_details():
    if 'user' in session:
        data          = request.args.get('params_data')
        SR_NO_val     = json.loads(data)
        print(SR_NO_val)
        INSTRUMENT_NAME = ""
        MAKE            = ""
        MODEL_NUMBER    = "" 
        done_date       = ""
        due_date        = ""
        VALIDITY        = ""
    
        if SR_NO_val is not None :
            temp_df         = dbo.get_equipment_by_id(SR_NO_val)       
            INSTRUMENT_NAME = str(temp_df.EQUIPMENT_NAME.values[0])
            MAKE            = str(temp_df.MAKE.values[0])
            MODEL_NUMBER    = str(temp_df.MODEL_NUMBER.values[0])
            done_date       = str(temp_df.DONE_DATE.values[0]).split()[0]
            due_date        = str(temp_df.DUE_DATE.values[0]).split()[0]
            VALIDITY        = str(temp_df.DUE_DATE.values[0]).replace("-","/").split()[0]
            
           
        d = {
            "error":"none",
            "INSTRUMENT_NAME" : INSTRUMENT_NAME,
            "MAKE"           :  MAKE,
            "MODEL_NUMBER"   :  MODEL_NUMBER,
            "done_date"      :  done_date,
            "due_date"       :  due_date,
            "VALIDITY"        : VALIDITY,  
        }
        return json.dumps(d)
    return make_response(render_template('LOGIN_PAGE/login.html'),200)



@app.route("/update_grade", methods=['POST', 'GET'])
def update_grade(): 
    if 'user' in session:
        data          = request.args.get('params_data')
        gl_value      = json.loads(data)  
        print(gl_value)
        if "ISO" in gl_value :    
            grade_list    = ISO_guidlines_master.loc[(ISO_guidlines_master.Guidelines==gl_value)]['Grade'].tolist()      
        if "EU" in gl_value  :
            grade_list    = EUGMP_guidlines_master.loc[(EUGMP_guidlines_master.Guidelines==gl_value)]['Grade'].unique().tolist()      
          
        dict_list=[]
        for x in grade_list:
            thisdict ={"id":x,"name":x}
            dict_list.append(thisdict)
        d = {"dict_list":dict_list,"error":"none"}
        return json.dumps(d)
    return make_response(render_template('LOGIN_PAGE/login.html'),200)


@app.route("/get_limits", methods=['POST', 'GET'])
def get_limits():
    if 'user' in session:    
        data          = request.args.get('params_data')
        full_data     = json.loads(data)   
        gl_value      = full_data['gl_value']
        grade         = full_data['grade']
        condition     = full_data['condition']
        print(gl_value)
        if "EU" not in gl_value :
            value1        = ISO_guidlines_master.loc[(ISO_guidlines_master.Guidelines==gl_value)
                                                        &
                                                (ISO_guidlines_master.Grade==grade)
                                                 ]['point_five_percent'].values[0]
            value2        = ISO_guidlines_master.loc[(ISO_guidlines_master.Guidelines==gl_value)
                                                        &
                                                (ISO_guidlines_master.Grade==grade)
                                                 ]['five_percent'].values[0]   
        if "EU" in gl_value  : 
        
            value1        = EUGMP_guidlines_master.loc[(EUGMP_guidlines_master.Guidelines==gl_value)
                                                        &
                                                (EUGMP_guidlines_master.Grade==grade)
                                                        &
                                                (EUGMP_guidlines_master.Condition==condition)
                                                 ]['point_five_percent'].values[0]
                                                 
                                                 
            value2        = EUGMP_guidlines_master.loc[(EUGMP_guidlines_master.Guidelines==gl_value)
                                                        &
                                                (EUGMP_guidlines_master.Grade==grade)
                                                        &
                                                (EUGMP_guidlines_master.Condition==condition)
                                                 ]['point_five_percent'].values[0]
        
            
            
        
        d = {"value1":str(value1),
             "value2":str(value2),
             "error":"none"}
        print(d)
        return json.dumps(d)
    return make_response(render_template('LOGIN_PAGE/login.html'),200)     


@app.route("/submit_air_velocity")
def submit_air_velocity():
    if 'user' in session:
        data          = request.args.get('params_data')
        full_data     = json.loads(data)
        basic_details = full_data['basic_details']
        observation   = full_data['observation']    
        company_name  = basic_details['company_name']
        temp_df       = pd.DataFrame.from_dict(observation,orient ='index')
        session_var   = session['user']		
        file_name,file_path = Report_Genration.generate_report_air_velocity(temp_df ,basic_details,session_var['user'])    
        subject       = "HVAC-Air Velocity Automated Genrated Report - {}".format(company_name)
        text          = "Hi PinPoint Team \n\nPlease find attached automated Generated File {} for {} \n\nRegards \nAjeet Shukla :) :) :)".format(file_name,company_name)
       
        if sent_mail:
            send_mail(subject,text,file_path,file_name) 
        d = {"error":"none","file_name":file_name,"file_path":file_path}
       
        return json.dumps(d)    
        
@app.route("/submit_thermal_report")
def submit_thermal_report():
    if 'user' in session:
        data          = request.args.get('params_data')
        basic_details = json.loads(data)        
        session_var   = session['user']		
        file_name,file_path = Report_Genration.generate_thermal_report(basic_details)           
        d = {"error":"none","file_name":file_name,"file_path":file_path}
       
        return json.dumps(d) 
    
@app.route("/submit_data_pao")
def submit_data_pao():
    if 'user' in session:
        data          = request.args.get('params_data')
        full_data     = json.loads(data)
        basic_details = full_data['basic_details']
        observation   = full_data['observation']
        company_name  = basic_details['company_name']
        temp_df = pd.DataFrame.from_dict(observation,orient ='index')
        session_var = session['user']
        file_name,file_path=Report_Genration.generate_report_pao(temp_df,basic_details,session_var['user'])
        subject   = "HVAC-PAO Automated Genrated Report - {}".format(company_name)
        text      = "Hi PinPoint Team \n\nPlease find attached automated Generated File {} for {} \n\nRegards \nAjeet Shukla :) :) :)".format(file_name,company_name)
    
        if sent_mail :
            send_mail(subject,text,file_path,file_name) 
        d = {"error":"none","file_name":file_name,"file_path":file_path}        
        return json.dumps(d)
 
@app.route("/submit_particle_report")
def submit_particle_report():
    if 'user' in session:
        data          = request.args.get('params_data')
        full_data     = json.loads(data)
        basic_details = full_data['basic_details']
        observation   = full_data['observation']	
        company_name  = basic_details['company_name']
        temp_df       = pd.DataFrame.from_dict(observation,orient ='index')
        session_var = session['user']
        file_name,file_path=Report_Genration.generate_report_particle_count(temp_df,basic_details,session_var['user'],
                                                                             EUGMP_guidlines,ISO_guidlines_master)
        subject   = "Particle Count Automated Genrated Report - {}".format(company_name)
        text      = "Hi PinPoint Team \n\nPlease find attached automated Generated File {} for {} \n\nRegards \nAjeet Shukla :) :) :)".format(file_name,company_name)
        if sent_mail:
            send_mail(subject,text,file_path,file_name) 
        d = {"error":"none","file_name":file_name,"file_path":file_path}        
        return json.dumps(d)
    
    

 ################################# Start get approve and update instrument######################################
@app.route("/submit_updateinstrumentDetails" )    
def submit_updateinstrumentDetails():
    if 'user' in session:
        data            = request.args.get('params_data')
        data            = json.loads(data)   
        observation     = data['observation']
        temp_df         = pd.DataFrame.from_dict(observation,orient ='index')
        temp_df         = temp_df[['Type','EQUIPMENT_NAME','MAKE','MODEL_NUMBER','SR_NO_ID','DONE_DATE','DUE_DATE','STATUS','ISSUED_TO','COMPANY_NAME' ,'REMARK']]
        dbo.update_equipment(temp_df)
        d = {"error":"none",}   
        return json.dumps(d)
      
@app.route("/update_approve_deny_request" )    
def update_approve_deny_request():
    if 'user' in session:
        session_var = session['user']
        data            = request.args.get('params_data')
        data            = json.loads(data)   
        observation     = data['observation']
        temp_df         = pd.DataFrame.from_dict(observation,orient ='index')
        temp_df         = temp_df[['SR_NO_ID','APPROVE/DENY','REMARK','COMPANY_NAME']]
        print(temp_df)
        dbo.update_request_for_equipment(temp_df,session_var['user'])
        d = {"error":"none",}   
        return json.dumps(d)     
        
@app.route("/UpdateinstrumentDetails")
def UpdateinstrumentDetails():
    if 'user' in session:
        session_var = session['user']
        role        = session_var["role"]
        equipment_details   = dbo.get_equipment()
        equipment_list      = equipment_details.to_dict('records')
        return make_response(render_template('ADMIN/UpdateinstrumentDetails.html',equipment_list  = equipment_list, role = role),200) 
    return make_response(render_template('LOGIN_PAGE/login.html'),200)
 
@app.route("/approve_instrument_request")
def approve_instrument_request():
    if 'user' in session:
        session_var = session['user']
        role        = session_var["role"]
        equipment_details   = dbo.get_penidng_for_approval_equipment()
        equipment_list      = equipment_details.to_dict('records')
        return make_response(render_template('ELOGBOOK/approve_instrument_request.html',equipment_list  = equipment_list, role = role),200) 
    return make_response(render_template('LOGIN_PAGE/login.html'),200)
    
    
@app.route("/elogbook")
def elogbook():
    if 'user' in session:
        session_var = session['user']
        role        = session_var["role"]
        logbook     = dbo.get_logBook()
        logbook     = logbook.to_dict('records')
        return make_response(render_template('ELOGBOOK/elogbook.html',logbook  = logbook, role = role),200) 
    return make_response(render_template('LOGIN_PAGE/login.html'),200)
    

@app.route("/request_instrument")
def request_instrument():
    if 'user' in session:
        customer_details  = dbo.get_company_details()
        company_name_list = customer_details.COMPANY_NAME.unique().tolist()
        session_var = session['user']
        role        = session_var["role"]
        equipment_details   = dbo.get_available_equipment()
        equipment_list      = equipment_details.to_dict('records')
        return make_response(render_template('ELOGBOOK/request_instrument.html',
                             equipment_list=equipment_list,company_list=company_name_list, role = role),200) 
    return make_response(render_template('LOGIN_PAGE/login.html'),200)
    
@app.route("/push_instrument_request")
def push_instrument_request():
    if 'user' in session:
        session_var = session['user']
        role        = session_var["role"]         
        data            = request.args.get('params_data')
        observation     = json.loads(data)       
        dbo.request_for_equipment(observation['selected_eq'],observation['company_name'],
                                 observation['REMARK'],session_var['username'])
        d = {"error":"none"}
        return json.dumps(d) 
    return make_response(render_template('LOGIN_PAGE/login.html'),200)        
         
################################# End get approve and update instrument######################################     
   

        
 #################### Start  Update and get Company Details ################################################       
@app.route("/UpdateCompanyDetails")
def UpdateCompanyDetails():
    if 'user' in session:
        session_var = session['user']
        role        = session_var["role"]
        customer_details  = dbo.get_company_details()
        customer_list     = customer_details.to_dict('records')
        return make_response(render_template('ADMIN/UpdateCompanyDetails.html',customer_list  = customer_list, role = role),200) 
    return make_response(render_template('LOGIN_PAGE/login.html'),200)    
    
@app.route("/submit_updateCompanyDetails" )    
def submit_updateCompanyDetails():
    if 'user' in session:
        data            = request.args.get('params_data')
        data            = json.loads(data)   
        observation     = data['observation']
        temp_df         = pd.DataFrame.from_dict(observation,orient ='index')
        temp_df         = temp_df[['COMPANY_NAME','ADDRESS','REPORT_NUMBER']]
        dbo.update_company_details(temp_df)
        d = {"error":"none",}   
        return json.dumps(d)
 #################### End  Update and get Company Details ################################################       

if __name__ == '__main__':
    app.debug = True
    app.run()

