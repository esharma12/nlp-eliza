# Esha Sharma 02/05/2024 CMSC 416 PA-1 1) The problem to be solved is to create a therapist chatbot called Eliza that
# is able to converse as humanly as possible with any user. Eliza should be able to respond to concerns,
# personal problems, questions, statements and respond with appropriate psychobabble that makes the user feel heard
# and supported, using regular expressions. Eliza should use spot specific words and use them in Eliza's response.
# Eliza should also take the user's statements and transform them into related questions/responses. 2) Usage: python
# eliza.py. To quit program, enter 'quit'. Example Input/Output: [eliza] Hi, I'm a psychotherapist. What is your
# name? My name is Esha. [eliza] Hi Esha. How can I help you today? I want to rule the world. [eliza] Why do you want
# to rule the world? I don't know, I think I crave power. [eliza] Why don't you tell me more about your cravings? ...
# 3) The algorithm I have used to solve is a pattern-matching algorithm using a dictionary of regex of potential
# responses. The dictionary contains regexes of potential things a patient might tell or ask of a therapist. The
# responses are appropriate psychobabble in response, and are chosen randomly while also reflecting pronouns and
# irregular verbs. Once a match if found, then a eliza response is selected randomly. Before, returning the randomly
# chosen response, the captured part of the user's response is split into keywords, and all the pronouns and verbs
# that must be reflected are, ex. from me to you, am to are
# the reflected sub-response is it attached to the random eliza response and returned to main to be printed


import re
import random
import shutil


# Main method initiates conversation between eliza and user. Calls get_name function to call user by name and then
# enters loop to continue conversation, choosing eliza's correct response randomly through the regex rule library
# when a matching keyword is found for each of the user's statements. loop breaks when user chooses to. eliza says
# goodbye
def main():
    width, _ = shutil.get_terminal_size()
    print(' ELIZA THE PSYCHOTHERAPIST'.center(width, '='))
    print("[eliza] Hi, I'm a psychotherapist. What is your name?")
    nameString = input()
    name = get_name(nameString)
    print("[eliza] Hi {}. How can I help you today?".format(name))
    while True:
        user_input = input()
        if user_input.lower() == "quit":
            print("[eliza] Goodbye!")
            break
        else:
            statement = re.sub(r'[^\w\s]', '', user_input)
            print("[eliza] " + choose_response(statement))


# This method gets the user's name from their response. First, it strips the response string of all punctuation.
# This accounts for trailing punctuation at the end of their response, but also for the case where they
# respond I'm instead of I am or name's instead of name is
# Outputs only the name, even if it is given in a sentence string or as a one-word response
def get_name(nameString):
    nameString = re.sub(r'[^\w\s]', '', nameString)
    name = nameString
    if re.search(r'\b[Ii][Ss]\b', nameString):
        name = re.search(r'\b[Ii][Ss]\b\s(.*?)$', nameString)
        return name.group(1)
    elif re.search(r'\b[Aa][Mm]\b', nameString):
        name = re.search(r'\b[Aa][Mm]\b\s(.*?)$', nameString)
        return name.group(1)
    elif re.search(r'\b[Ii][Mm]\b', nameString):
        name = re.search(r'\b[Ii][Mm]\b\s(.*?)$', nameString)
        return name.group(1)
    elif re.search(r'\b[Nn]ames\b', nameString):
        name = re.search(r'\b[Nn]ames\b\s(.*?)$', nameString)
        return name.group(1)
    return name


# This method finds a pattern match in the user's response and then chooses Eliza's response randomly
# the potential pronouns and verbs that need to be reflected are, for example, me and I, are changed to you and your.
def choose_response(statement):
    for pattern, responses in potential_responses:
        match = re.search(pattern, statement)
        if match:
            response = random.choice(responses)
            for subgroup in match.groups():
                keywords = subgroup.lower().split()
                # go through each keyword in the subgroup of the part of the response to reflect
                # the pronouns and verbs for
                for i, keyword in enumerate(keywords):
                    if keyword in reconstructions:
                        keywords[i] = reconstructions[keyword]
            sub_response = ' '.join(keywords)
            return response.replace("%1", sub_response)
    # if no match, then return default statement to handle things eliza can't understand like gibberish and complex
    # statements
    return random.choice(default)


# This is a dictionary of default responses for the chance the user inputs gibberish or something eliza doesn't
# understand
default = [
    "I am not sure I understand.",
    "I'm not following. Could you rephrase?",
    "Can you say that another way?",
    "I'm sorry, I don't understand.",
    "I don't quite understand, can you rephrase that?",
    "I don't quite understand, can you say that another way?",
    "Let us shift gears... Tell me about your family.",
    "Fascinating, tell me more!"
]
# This is a dictionary of potential responses for when the user inputs a pattern of response that is matched
# to the regexes in the dictionary
potential_responses = [
    [r'[Ii] want (.*)',
     ["Why do you want %1?",
      "How would it help to get %1?",
      "Are you sure you want %1?"]
     ],
    [r'[Ii] will (.*)',
     ["In what way will you %1?",
      "Are you sure you will %1?"]
     ],
    [r'[Ii] need (.*)',
     ["Why do you want %1?",
      "How would it help to get %1?",
      "Are you sure you want %1?"]
     ],
    [r'I think (.*)',
     ["Do you really think %1?",
      "But you are not entirely not sure %1?"]
     ],
    [r'[Qq]uit',
     ["Thank you for talking with me!",
      "Goodbye!",
      "Bye-bye! Have a good day!"]
     ],
    [r'I can\'?t (.*)',
     ["How do you know you can't %1?",
      "Perhaps you could %1 if you tried something new.",
      "What steps would you need to take to %1?"]
     ],
    [r'[Ii] am (.*)',
     ["Did you come to me because you are %1?",
      "How long have you been %1?",
      "Are you content with being %1?"]
     ],
    [r'\b[Cc]rave\b (.*)',
     ["Why don't you tell me more about your cravings.",
      "What else do you crave?",
      "What about %1 do you crave?"]
     ],
    [r'(.*)?[Mm]y [Mm]other(.*)?',
     ["Tell me more about your mother.",
      "Who else in your family %1?",
      "Does she influence you strongly?",
      "What else comes to mind when you think of your mother?"]
     ],
    [r'[Mm]other(.*)?',
     ["How did you react when she %1?"]
     ],
    [r'[Ee]verything(.*)?',
     ["Is it possible that this is black-and-white thinking?",
      "I'm sorry everything %1, what would need to change for this to not be true?"]
     ],
    [r'My (.*)',
     ["I see, your %1.",
      "Why do you say that your %1?",
      "When your %1, how do you feel?"]
     ],
    [r'(.*)?[Mm]y [Ff]other(.*)?',
     ["Tell me more about your father.",
      "Who else in your family %1?",
      "Does he influence you strongly?",
      "What else comes to find when you think of your father?"]
     ],
    [r'(.*) [Ss]orry (.*)',
     ["There are many times when apologies are not needed.",
      "Why are you sorry %1?"]
     ],
    [r'What (.*)',
     ["How would an answer to that help you?",
      "What do you think?"]
     ],
    [r'How (.*)',
     ["Perhaps you can answer your own question.",
      "What is it you're really asking?"]
     ],
    [r'[Ff]ather(.*)?',
     ["How did you react when he %1?"]
     ],
    [r'[Bb]ecause (.*)',
     ["Is that the real reason?",
      "What would it mean if everything did not %1"
      "If %1, what else must be true?"]],
    [r'(.*) friend (.*)?',
     ["Tell me more about your friends.",
      "How did you react when your friend %1?",
      "Why don't you tell me about a different friend?"]
     ],
    [r'[Ii] was (.*)',
     ["Tell me more about how you were %1.",
      "Why do you think you were %1?",
      "Tell me more about why you were %1."]
     ],
    [r'[Yy]es(.*)?',
     ["You seem absolutely certain.",
      "Okay, can you elaborate a bit?"]
     ],
    [r'[Nn]o(.*)?',
     ["You seem absolutely certain.",
      "Okay, can you elaborate a bit as to why %1?"]
     ],
    [r'[Cc]an you (.*)?',
     ["If I could %1, then how would you feel?",
      "Why do you ask if I can %1?"
      ]],
    [r'(.*)?dream(.*)?',
     ["What does this dream suggest to you?",
      "How often do you remember your dreams?",
      "Do you believe your dreams influence your waking world?"]
     ],
    [r'(.*)?glad(.*)?',
     ["I'm happy to hear that, what else in your life has made you feel glad?"]
     ],
    [r'(.*)?sad(.*)?',
     ["I'm sorry to hear that, what else in your life has made you feel sad?"]
     ]
]

# This is a dictionary of reflected pronouns and verbs, mirrored to allow for a correct response from eliza
reconstructions = {
    "i": "you",
    "was": "were",
    "were": "was",
    "am": "are",
    "i'm": "you are",
    "i'd": "you would",
    "I will": "you will",
    "i've": "you have",
    "my": "your",
    "are": "am",
    "me": "you",
    "you": "me",
    "myself": "yourself",
    "you're": "i am",
    "i'll": "you will",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine"
}
main()
