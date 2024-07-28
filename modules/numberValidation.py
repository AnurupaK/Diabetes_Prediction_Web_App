def validate_inputs(glucose, bp, insulin, bmi, age):
    def is_valid_number(value):
        if(value is not None and isinstance(value,(int,float)) and value>=0):
            return True
        else:
            return False

    is_glucose_valid = is_valid_number(glucose)
    is_bp_valid = is_valid_number(bp)
    is_insulin_valid = is_valid_number(insulin)
    is_bmi_valid = is_valid_number(bmi)
    is_age_valid = is_valid_number(age)

    return {
        'is_glucose_valid': is_glucose_valid,
        'is_bp_valid': is_bp_valid,
        'is_insulin_valid': is_insulin_valid,
        'is_bmi_valid': is_bmi_valid,
        'is_age_valid': is_age_valid,
        'all_valid': is_glucose_valid and is_bp_valid and is_insulin_valid and is_bmi_valid and is_age_valid
    }