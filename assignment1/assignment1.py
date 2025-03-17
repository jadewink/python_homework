import statistics

#Task 1 Hello
def hello():
    greeting = "Hello!"
    print(greeting)
    return greeting

# hello()

#Task 2 Greet with a Formatted String
def greet(name):
    greeting = (f"Hello, {name}!")
    print (greeting)
    return greeting

# greet("Jordyn")

#Task 3 Calculator
# If statement version
# def calc(number_1, number_2, operator = "multiply"):
#     #add, subtract, multiply, divide, modulo, int_divide (for integer division) and power
#     result = None

#     if operator == "add":
#         result = number_1 + number_2
#     elif operator == "subtract":
#         result = number_1 - number_2
#     elif operator == "multiply":
#         try: number_1 * number_2
#         except:
#             return ("You can't multiply those values!")
#         result = number_1 * number_2
#     elif operator == "divide":
#         try: number_1 / number_2
#         except ZeroDivisionError:
#             return ("You can't divide by 0!")
#         result = number_1 / number_2
#     elif operator == "modulo":
#         result = number_1 % number_2
#     elif operator == "int_divide":
#         result = number_1 // number_2
#     elif operator == "power":
#         result = number_1 ** number_2
#     else:
#         result = "Please enter a value"
#     print(result)
#     return result
    
# calc(1, 4, "subtract")

# Case statement Version
def calc(number_1, number_2, operator = "multiply"):
    #add, subtract, multiply, divide, modulo, int_divide (for integer division) and power
    result = None
    match(operator):
        case "add":
            result = number_1 + number_2
        case "subtract":
            result = number_1 - number_2
        case "multiply":
            try: number_1 * number_2
            except:
                return ("You can't multiply those values!")
            result = number_1 * number_2
        case "divide":
            try: number_1 / number_2
            except ZeroDivisionError:
                return ("You can't divide by 0!")
            result = number_1 / number_2
        case "modulo":
            result = number_1 % number_2
        case "int_divide":
            result = number_1 // number_2
        case "power":
            result = number_1 ** number_2
    print(result)
    return result
    
# calc(1, 4, "subtract")

#Task 4 Data Type Conversion
def data_type_conversion(value, type):
    result = None

    match (type):
        case "float":
            result = float(value)
        case "str":
            result = str(value)
        case "int":
            try: int(value)
            except:
                return (f"You can't convert {value} into a {type}.")
            result = int(value)
    return result

#Task 5 Grading System, Using *args
def grade(*args):
    try: average = sum(args)/len(args)
    except:
        return ( "Invalid data was provided.")
    print (average)
    # A: 90 and above
    if average >= 90:
        return "A"
    # B: 80-89
    elif average > 80 and average < 89:
        return "B"
    # C: 70-79
    elif average > 70 and average < 79:
        return "C"
    # D: 60-69
    elif average > 60 and average < 69:
        return "D"
    # F: Below 60
    elif average > 60:
        return "F"

#grade(1, 2, 4)
    
#Task 6 Use a For Loop with a Range
def repeat(string, count):
    result_string = ""
        
    for i in range(count):
        result_string += (f"{string}")
        print (result_string)
    
    return result_string

# repeat("boston", 4)

#Task 7 Student Scores, Using **kwargs
def student_scores(type, **kwargs):
    match (type):
        case "best":
            for key, value in kwargs.items():
                return max(kwargs, key=kwargs.get)
        case "mean":
            for key, value in kwargs.items():
                return statistics.mean(kwargs.values())
    
#student_scores("mean", Tom=75, Dick=89, Angela=91, Frank=50)

#Task 8 Titleize, with String and List Operations
def titleize(title):
    #Split title words into a list
    words = title.split()
    #Blank list for capitalized words
    capital_words = []

    for i, word in enumerate(words):
        #If the word is the first or last word, always capitalize it
        if word == words[0] or word == words[-1]:
            word = word.capitalize()
        #If the word is a little word and not the first or last word, don't capitalize it
        elif word in ["a", "on", "an", "the", "of", "and", "is", "in"]:
            word = word
        #Capitalize all other words
        else: word = word.capitalize()

        #Put new capitalized word in list
        capital_words.append(word)
        
        #Join words in list into one capitalized string with spaces in between the words
        capital_title = " ".join(capital_words)

    return(capital_title)

# titleize("war and peace")

#Task 9: Hangman, with more String Operations
def hangman(secret, guess):
    secret_list = list(secret)
    guess_list = list(guess)
    answer_list =[]

    #compare each letter of secret to each letter of guess, create answer list with _ or matching letter in correct place
    for i, letter in enumerate(secret_list):
        if letter in guess_list:
            answer_list.append(letter)
        else: answer_list.append("_")
   
    answer = "".join(answer_list)
    return answer

#hangman("difficulty", "ico")

#Task 10 Pig Latin, Another String Manipulation Exercise

 

def pig_latin(phrase):
    words = phrase.split()
    removed_chars = ""
    remaining_text = ""
    pig_list = []
    pig_phrase = ""
    
    for letters in words:
        #(3) "qu" is a special case, as both of them get moved to the end of the word, as if they were one consonant letter 
        #even if they are not the first or second letter
        if letters[0] in ["q", "u"] and letters[1] in ["q", "u"] or letters[1] in ["q", "u"] and letters[2] in ["q", "u"]:
            if letters[1] in ["q", "u"] and letters[2] in ["q", "u"]:
                removed_chars = letters[:3]
                remaining_text = letters[3:]
            else: 
                removed_chars = letters[:2]
                remaining_text = letters[2:]
        #(2) If the string starts with one or several consonants, they are moved to the end and "ay" is tacked on after them.
        elif letters[0] not in ["a", "e", "i", "o", "u"]:
            if letters[1] not in ["a", "e", "i", "o", "u"]:
                removed_chars = letters[:2]
                remaining_text = letters[2:]
            else:
                removed_chars = letters[:1]
                remaining_text = letters[1:]
        #(1) If the string starts with a vowel (aeiou), "ay" is tacked onto the end. 
        elif letters[0] in ["a", "e", "i", "o", "u"]:
            removed_chars = ""
            remaining_text = letters

        new_word = remaining_text + removed_chars + "ay"
        pig_list.append(new_word)
        pig_phrase = " ".join(pig_list)

    return pig_phrase

#pig_latin("square")