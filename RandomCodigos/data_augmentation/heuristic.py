from heapq import nsmallest as nmin

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

def too_many_characters(input_str, sorted_confidences, sorted_boxes):
    print(sorted_confidences)
    # Check if there are any overlapping boxes (meaning two or more detected characters in the same position)
    xs = []
    for box in sorted_boxes:
        x1, _, _, _ = map(int, box[:4])
        x = x1
        xs.append(x)
    # Must add a condition for a minimum value to be considered overlapping
    # Make a list with the difference between consecutive items on xs
    xs_diff = [xs[i+1] - xs[i] for i in range(len(xs)-1)]
    print(xs, "--", xs_diff)
    # Check which one is the smallest difference, get its id and remove it from the list
    min_diff = nmin(len(input_str)-6,xs_diff)
    print(min_diff)
    for min in min_diff:
        min_diff_id = xs_diff.index(min)
        xs_diff.remove(min)
        print(f"positions {min_diff_id} and {min_diff_id+1} are overlapping, checking confidences...")
        # Check which one has the lowest confidence
        if sorted_confidences[min_diff_id] > sorted_confidences[min_diff_id+1]:
            print(f"removing position {min_diff_id+1}")
            sorted_confidences.pop(min_diff_id+1)
            sorted_boxes.pop(min_diff_id+1)
            input_str = input_str[:min_diff_id+1] + input_str[min_diff_id+2:]
        else:
            print(f"removing position {min_diff_id}")
            sorted_confidences.pop(min_diff_id)
            sorted_boxes.pop(min_diff_id)
            input_str = input_str[:min_diff_id] + input_str[min_diff_id+1:]
    return input_str


def corrected_pairs(i_s, input_str, letter_count, number_count, letter_i, number_i):
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

def LP_validation_and_correction(input_str, sorted_confidences, sorted_boxes):
    # Check if the string has exactly 6 characters
    if len(input_str) < 6:
        reason = "Too few characters, impossible to correct"
        return False, reason, "NA"
    elif len(input_str) > 6:
        reason = "Too many characters"
        return False, reason, too_many_characters(input_str, sorted_confidences, sorted_boxes)
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
            #reason = "Letters and numbers in the same pair"
            i_s.append(i)
    if 0 > len(i_s) > 3:
        return False, None, corrected_pairs(i_s, input_str, letter_count, number_count, letter_i, number_i)
    elif len(i_s) == 3:
        return False, None, "NA"

    # Check the conditions for letter pairs
    if (letter_count == 1 and number_count == 2):
        return True, input_str, None
    elif (letter_count == 2 and number_count == 1):
        if input_str[0] in ["A", "B", "C"] and input_str[5].isalpha():
            return True, input_str, None
        else:
            reason = "Portuguese license plates do not yet start with a D in the 4 letter configuration"
            return False, reason, "NA"
    else:
        reason = "Letters and numbers mixed"
        return False, reason, corrected_pairs(i_s, input_str, letter_count, number_count, letter_i, number_i)


"ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"
"I1"
"O0"
"S5"
"A4"
"B8"
"Z2"
