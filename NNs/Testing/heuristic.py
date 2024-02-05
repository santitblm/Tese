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

def overlapping(x1, y1, x2, y2, X1, Y1, X2, Y2, conf0, conf1, thresh = 0.9):

    i = max(0, min(x2, X2) - max(x1, X1)) * max(0, min(y2, Y2) - max(y1, Y1))
    a1, a2 = (x2-x1) * (y2 - y1), (X2 - X1) * (Y2 - Y1)

    if i >= thresh * a1 or i >= thresh * a2:
        if conf0 < conf1:
            return True, 0
        else:
            return True, 1
    else:
        return False, None

def too_many_characters(input_str, sorted_confidences, sorted_boxes):
    # Check if there are any overlapping boxes (meaning two or more detected characters in the same position)
    
    x1, y1, x2, y2 = map(int, sorted_boxes[0][:4])
    conf0 = sorted_confidences[0]
    i = 0
    for box, conf1 in zip(sorted_boxes[1:], sorted_confidences[1:]):

        X1, Y1, X2, Y2 = map(int, box[:4])
        overlaps, pos = overlapping(x1, y1, x2, y2, X1, Y1, X2, Y2, conf0, conf1)
        if overlaps:
            sorted_boxes.remove(sorted_boxes[i+pos:1+i+pos][0])
            sorted_confidences.remove(sorted_confidences[i+pos:1+i+pos][0])
        i += 1
        x1, y1, x2, y2 = X1, Y1, X2, Y2
        conf0 = conf1

        
    return input_str, sorted_confidences, sorted_boxes

######################################################################################################################################
    #xs = []
    #for box in sorted_boxes:
    #    x1, _, _, _ = map(int, box[:4])
    #    x = x1
    #    xs.append(x)
    # Must add a condition for a minimum value to be considered overlapping
    # Make a list with the difference between consecutive items on xs
    #xs_diff = [xs[i+1] - xs[i] for i in range(len(xs)-1)]
    #print(xs, "--", xs_diff)
    # Check which one is the smallest difference, get its id and remove it from the list
    #min_diff = nmin(len(input_str)-6,xs_diff)
    #print(min_diff)
    #for min in min_diff:
    #    min_diff_id = xs_diff.index(min)
    #    xs_diff.remove(min)
        #print(f"positions {min_diff_id} and {min_diff_id+1} are overlapping, checking confidences...")
        # Check which one has the lowest confidence
    #    if sorted_confidences[min_diff_id] > sorted_confidences[min_diff_id+1]:
            #print(f"removing position {min_diff_id+1}")
    #        sorted_confidences.pop(min_diff_id+1)
    #        sorted_boxes.pop(min_diff_id+1)
    #        input_str = input_str[:min_diff_id+1] + input_str[min_diff_id+2:]
    #    else:
            #print(f"removing position {min_diff_id}")
    #        sorted_confidences.pop(min_diff_id)
    #        sorted_boxes.pop(min_diff_id)
    #        input_str = input_str[:min_diff_id] + input_str[min_diff_id+1:]
    #return input_str, sorted_confidences, sorted_boxes
######################################################################################################################################
    


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


def Try_config_correction(input_str): # Sometimes the first or last pair is 11 and it is read as II, this is a very specific case
    if input_str[0] == input_str[1] == "I":
        new_str = "11" + input_str[2:]
        return True, new_str
    elif input_str[4] == input_str[5] == "I":
        new_str = input_str[:4] + "11"
        return True, new_str
    else:
        return False, None


def LP_validation_and_correction(input_str, sorted_confidences, sorted_boxes):
    reason = LP_val(input_str)

    # If the LP is invalid, try to correct it according to the reason
    if reason is not None:

        if reason[0] == 0: # Too few characters
            return False, None
        
        elif reason[0] == 1: # Too many characters
            for i in range(3): # Will try to correct it 3 times, if it doesn't work, it will return False
                return False, None
                input_str, sorted_confidences, sorted_boxes = too_many_characters(input_str, sorted_confidences, sorted_boxes)
                reason = LP_val(input_str)
                if reason[0] is None:
                    return True, input_str
                elif reason[0] != 1:
                    LP_validation_and_correction(input_str, sorted_confidences, sorted_boxes)
            return False, None
        
        elif reason[0] == 2: # Letters and numbers in the same pair
            new_str = corrected_pairs(reason[1], input_str, reason[2], reason[3], reason[4])
                                      # (i_s, input_str, letter_count, number_count, letter_i)
            if "?" in new_str: # Couldn't correct
                return False, None
            
            reason = LP_val(new_str)
            if reason[0] is None:
                return True, new_str
            else:
                return False, None
            
        elif reason[0] >= 3: # Reasons 3, 5 or 6 are all impossible to correct
            if reason[0] == 4:
                return Try_config_correction(input_str)
            else:
                return False, None
        




    # If the LP is valid
    else:
        return True, input_str




def LP_val(input_str):

    if len(input_str) < 6: # Not enough Characters
        reason = 0
        return [reason]
    elif len(input_str) > 6: # Too many characters
        reason = 1
        return [reason]
    
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
<<<<<<< Updated upstream
        return None # Valid
    
    elif (letter_count == 2 and number_count == 1):
        if input_str[0] in ["A", "B", "C"] and input_str[5].isalpha():
            return None # Valid
=======
        return True, None, input_str
    elif (letter_count == 2 and number_count == 1):
        if input_str[0] in ["A", "B", "C"] and input_str[5].isalpha():
            return True, None, input_str
>>>>>>> Stashed changes
        else:
            reason = 6 # Starts with D onwards (DA00AA)
            return [reason]
        
    else:
        reason = 4 # Invalid configuration (e.g. AAAA00, 00AAAA)
        return [reason]


# Reasons:
# 0: Too few characters
# 1: Too many characters
# 2: Letters and numbers in the same pair
# 3: All pairs mixed
# 4: Invalid configuration (e.g. AAAA00, 00AAAA)
# 5: Only numbers or only letters
# 6: 2 pairs of letters but starts with D onwards (DA00AA)