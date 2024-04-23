
# Actual code to run this is in the bottom

lt_to_n = {
    "I": "1",
    "O": "0",
    "S": "5",
    "A": "4",
    "B": "8",
    "Z": "2",
    "T": "7",
    "G": "6"
}

n_to_lt = {v: k for k, v in lt_to_n.items()}

def corrected_pairs(i_s, input_str, letter_count, number_count, letter_i, number_i):
    if len(i_s) == 1:
        i = i_s[0]

        if letter_count == 0:
            if input_str[i*2].isalpha():
                new_str = input_str[:i*2+1] + n_to_lt.get(input_str[i*2+1], "?") + input_str[i*2+2:]
            else:
                new_str = input_str[:i*2] + n_to_lt.get(input_str[i*2], "?") + input_str[i*2+1:]

        elif (number_count == 0 and i == 1) or (number_count == 1 and number_i[0] != 1):
            if input_str[i*2].isdigit():
                new_str = input_str[:i*2+1] + lt_to_n.get(input_str[i*2+1], "?") + input_str[i*2+2:]
            else:
                new_str = input_str[:i*2] + lt_to_n.get(input_str[i*2], "?") + input_str[i*2+1:]

        else:
            new_str = input_str

    else:
        new_str = input_str 
    
    return new_str

def LP_val(input_str):

    #if len(input_str) < 6: # Not enough Characters
    #    reason = 0
    #    return [reason]
    #elif len(input_str) > 6: # Too many characters
    #    reason = 1
    #    return [reason]
    
    # Initialize counters for letters and numbers
    letter_count = 0
    number_count = 0
    i_s = []
    letter_i = []
    number_i = []

    # Check pairs of characters
    for i in range(3):
        char1 = input_str[2*i]
        char2 = input_str[2*i + 1]

        # Check if both characters in the pair are letters or both are numbers
        if (char1.isalpha() and char2.isalpha()) or (char1.isdigit() and char2.isdigit()):
            if char1.isalpha():
                letter_count += 1
                letter_i.append(i)
            else:
                number_count += 1
                number_i.append(i)
        else:
            i_s.append(i)

    if 0 < len(i_s) < 3:
        reason = 2 # Letters and numbers in the same pair
        return [reason, i_s, letter_count, number_count, letter_i, number_i]
    elif len(i_s) == 3:
        reason = 3 # All pairs mixed
        return [reason]
    
    # Check the conditions for letter pairs
    if (letter_count == 1 and number_count == 2):
        if "K" in input_str:
            check_K = input_str.split("K")
            if len(check_K[0]) == 4 and len(check_K)[1] == 1:
                return None #K found in the right position, all other conditions are met
            else:
                reason = 7 #K found in a wrong spot
                return [reason]
        else:
            return None # Valid
    
    elif (letter_count == 2 and number_count == 1):

        if "K" in input_str:
            reason = 7
            return [reason]
        
        elif input_str[0] in ["A", "B"] and input_str[5].isalpha():
            return None # Valid
        else:
            reason = 6 # Starts with C onwards (CA00AA), not present as of today, Q2 2024
            return [reason]
        
    else:
        reason = 4 # Invalid configuration (e.g. AAAA00, 00AAAA)
        return [reason]

def check_for_wrongLPs(predictions_file):
    with open(predictions_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        LP = line.split(" ")[0]
        reason_fault = LP_val(LP)
        if reason_fault is not None:
            print(LP, reason_fault[0],"\n")
            if reason_fault[0] == 2:
                #print(reason_fault)
                _, i_s, letter_count, number_count, letter_i, number_i = reason_fault
                new_str = corrected_pairs(i_s, LP, letter_count, number_count, letter_i, number_i)
                print(new_str, "\n")


# Code to run the script below this line



video = "20240415_155436900.MOV"
predictions_file = f"/home/santilm/Desktop/Results_LPDet+OCR/{video}/predictions.txt"


check_for_wrongLPs(predictions_file)