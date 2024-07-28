#Glucose: 0 to 201
#BP: 0 to 123
#Insulin: 0 to 850
#BMI: 0 to 70
#Age: 0 to 90

def rangeCheck(inputDict):
    # Default to False for all parameters
    isGlucose, isBP, isInsulin, isBMI, isAge = False, False, False, False, False
    
    # Check if the dictionary is empty
    if not inputDict:
        return False
    
    # Iterate through the dictionary and validate values
    for key, value in inputDict.items():
        if value is None:  # Handle the case where the value might be None
            continue
        
        if key.lower() == 'glucose' and 0 <= value <= 201:
            isGlucose = True
        elif key.lower() == 'bp' and 0 <= value <= 123:
            isBP = True
        elif key.lower() == 'insulin' and 0 <= value <= 850:
            isInsulin = True
        elif key.lower() == 'bmi' and 0 <= value <= 70:
            isBMI = True
        elif key.lower() == 'age' and 0 <= value <= 90:
            isAge = True
    
    # Return True if all parameters are valid, otherwise False
    return isGlucose and isBP and isInsulin and isBMI and isAge

   