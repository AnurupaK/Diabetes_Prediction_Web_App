from flask import Flask, request, jsonify,render_template
from numberValidation import validate_inputs
from Digits import checkDigits
from range_check import rangeCheck
import os
import sys
import pickle
import numpy as np
import pandas as pd

model = pickle.load(open('../models/LogR_model.pkl','rb'))

app = Flask(__name__,template_folder='../Frontend/templates',static_folder='../Frontend/static')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AI_Service')))

from doctor_response import get_doc_response, update_model, Doc_instruction

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report.html')
def report():
    return render_template('report.html')

@app.route('/api/Inputs', methods=['POST'])
def get_outcome():
    data = request.get_json()  # Converts JSON payload to Python dictionary
    glucose = data['glucose']
    bp = data['bp']
    insulin = data['insulin']
    bmi = data['bmi']
    age = data['age']
    print(glucose, bp, insulin, bmi, age)
    print(type(glucose), type(bp), type(insulin), type(bmi), type(age))
    
    ##Range check
    global dict_input
    dict_input = {
        'Glucose':glucose,
        'BP':bp,
        'Insulin':insulin,
        'BMI':bmi,
        'Age':age
    }
    
    check = rangeCheck(dict_input)
    if (check==True):
        
            ##Digits checking
            inputList = [glucose,bp,insulin,bmi,age]
            digit_check = checkDigits(inputList)
            print(digit_check)
            
            
            ##Checking if numbers are negative, doesn't come in int or float or field is empty
            valids = validate_inputs(glucose,bp,insulin,bmi,age)['all_valid']
            print(valids)
            
            if(digit_check==True and valids==True):
                message = "Great! I will analyze your data 🤭"
                return jsonify({'message':message,'value_msg':1})
            elif(digit_check==False and valids==False):
                message = "Oops! Maybe you sould put your data correctly 🫢"
                return jsonify({'message':message,'value_msg':0})
            elif(digit_check==True and valids==False):
                message = "Ahh! I see, can you try putting correct data and not keeping input areas blank 🧐"
                return jsonify({'message':message,'value_msg':0})
            else:
                message = "Ahh! Such absurd numbers.😂"
                return jsonify({'message':message,'value_msg':0})
    else:
        message = (
                        "Try putting values in range and not keeping input areas blank 🧐.\n"
                        "Here are the ranges:\n"
                        "🍭 Glucose: 0 to 201\n"
                        "🩸 BP: 0 to 123\n"
                        "💉 Insulin: 0 to 850\n"
                        "⚖️ BMI: 0 to 70\n"
                        "🕰️ Age: 0 to 90"
               )
        return jsonify({'message':message,'value_msg':0})
    
@app.route('/api/checkDiabetes',methods = ['POST'])
def CheckDiabetes():
    data = request.get_json()  # Converts JSON payload to Python dictionary
    Glucose = data['glucose']
    BloodPressure = data['bp']
    Insulin = data['insulin']
    BMI = data['bmi']
    Age = data['age']
    print(Glucose,BloodPressure,Insulin,BMI,Age)
    
    
    
    
    feature_names = ['Glucose','BloodPressure','Insulin','BMI','Age']
    data_array = np.array([[Glucose,BloodPressure,Insulin,BMI,Age]])
    input_df = pd.DataFrame(data_array,columns=feature_names)
    prediction = model.predict(input_df)[0]
    
    ifDiabetic = 1
    global outcome
    
    if prediction==1:
        outcome = "You are diabetic 😢"
        ifDiabetic = 1
    else:
        outcome = "You are not diabetic 😎"
        ifDiabetic = 0
    
    print(outcome)
    return jsonify({'outcome':outcome,'check':1,'ifDB':ifDiabetic})

@app.route('/api/get_doc', methods = ['POST'])
def DoctorResponse():

    data = request.get_json()
    outcome = data['outcome']
    glucose = data['glucose']
    bp = data['bp']
    insulin = data['insulin']
    bmi = data['bmi']
    age = data['age']
    
    instruction_for_doctor = Doc_instruction(outcome,glucose,bp,insulin,bmi,age)
    print(instruction_for_doctor)
    
    if instruction_for_doctor is None:
        return jsonify({'error': 'Invalid Instruction for Doctor'})

    # Update model with instruction
    update_model(instruction_for_doctor)
    doc_response = ""
    
    doc_response = get_doc_response("Review patient data") 
    
    message = 'Sent successfully'
    print(f"message: {message}")
    print(doc_response)
    
    return jsonify({'doc_response': doc_response,'ready_to_chat':1})
    

@app.route('/api/start_chat',methods = ['POST'])
def StartConversation():
    data = request.get_json()
    user = data['user_response']
    bot_response = get_doc_response(user)
    print(bot_response)
    return jsonify({'bot_response':bot_response})

@app.route('/api/getData',methods = ['POST'])
def get_Data():
    glucose = dict_input['Glucose']
    bp = dict_input['BP']
    insulin = dict_input['Insulin']
    bmi = dict_input['BMI']
    age = dict_input['Age']
        
    return jsonify({'glucose':glucose,'bp':bp,'insulin':insulin,'bmi':bmi,'age':age,'outcome':outcome})



if __name__ == '__main__':
    app.run(debug=True)
