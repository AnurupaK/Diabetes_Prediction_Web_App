def checkDigits(number_list):
    digit_check = True
    if number_list == []:
        return False
    else:
        for number in number_list:
            if(number is not None and number>=0):
                if (number >= 0 and number <= 9):
                    digit_check = True
                elif (number >= 10 and number <= 99):
                    digit_check = True
                elif (number >= 100 and number <= 999):
                    digit_check = True
                else :
                    digit_check = False
                    break
    
    if digit_check==True:
        return True
    else:
        return False
    