'''Reasons:
0: Too few characters
1: Too many characters
2: Letters and numbers in the same pair
3: Invalid configuration (e.g. AAAA00, 00AAAA)
4: Only numbers or only letters
5: 2 pairs of letters but starts with D onwards (DA00AA)'''

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


def corrected_pairs(i_s, input_str, letter_count, number_count, letter_i):#, number_i):
    if len(i_s) == 1:
        i = i_s[0]
        if letter_count == 0:
            if input_str[i*2].isalpha():
                new_str = input_str[:i*2+1] + n_to_lt.get(input_str[i*2+1], "?") + input_str[i*2+2:]
            else:
                new_str = input_str[:i*2] + n_to_lt.get(input_str[i*2], "?") + input_str[i*2+1:]
        elif number_count == 0 or (number_count == 1 and (letter_i[0] == 1 or i == 1)):
            if input_str[i*2].isdigit():
                new_str = input_str[:i*2+1] + lt_to_n.get(input_str[i*2+1], "?") + input_str[i*2+2:]
            else:
                new_str = input_str[:i*2] + lt_to_n.get(input_str[i*2+1], "?") + input_str[i*2+1:]
        else:
            new_str = input_str           
    #These conditions would never be met because all pairs are correct  
    elif letter_count == 3:
        new_str = input_str[:2] + lt_to_n.get(input_str[2], "?") + lt_to_n.get(input_str[3], "?") + input_str[4:]
    elif number_count == 3:
        # Check if the numbers' pairs are present in the dictionary
        new_str = input_str
    else:
        new_str = input_str 
    
    return new_str

def LP_val_reason(input_str):
    ### Check if layout is valid: ###

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

    if 0 > len(i_s) > 3:
        reason = 2 # Letters and numbers in the same pair
        return [reason, i_s, letter_count, number_count, letter_i]
    elif len(i_s) == 3:
        reason = 3 # All pairs mixed
        return [reason]
    
    # Check the conditions for letter pairs
    if (letter_count == 1 and number_count == 2):
        return None # Valid
    
    elif (letter_count == 2 and number_count == 1):
        if input_str[0] in ["A", "B", "C"] and input_str[5].isalpha():
            return None # Valid
        else:
            reason = 6 # Starts with D onwards (DA00AA)
            return [reason]
        
    else:
        reason = 4 # Invalid configuration (e.g. AAAA00, 00AAAA)
        return [reason]

def LP_val(LP):
    reason = LP_val_reason(LP)
    if reason is None:
        return True
    elif reason[0] == 2:
        _, i_s, letter_count, number_count, letter_i = reason
        new_LP = corrected_pairs(i_s, LP, letter_count, number_count, letter_i)
        if LP_val_reason(new_LP) is None:
            return True
        else:
            return False
    else:
        return False
    


# Reasons:
# 0: Too few characters
# 1: Too many characters
# 2: Letters and numbers in the same pair
# 3: All pairs mixed
# 4: Invalid configuration (e.g. AAAA00, 00AAAA)
# 5: Only numbers or only letters
# 6: 2 pairs of letters but starts with D onwards (DA00AA)