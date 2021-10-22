#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses


# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    score = 0

    # Return zero if the gender of one user is not compatible with the preferences of another
    if not(user1.gender in user2.preferences) or not(user2.gender in user1.preferences):
        return 0
    
    # Deduct compatibility based on the difference in grad_year (this will be 40% of the score)
    score = 4 - abs(user1.grad_year - user2.grad_year)

    common_answers = 0
    for user1_answer, user2_answer in zip(user1.responses, user2.responses):
        if user1_answer == user2_answer:
            common_answers += 1
    
    score += (float(common_answers) / len(user1.responses)) * 6

    return score / 10


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
