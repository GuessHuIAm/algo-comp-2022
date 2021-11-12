import numpy as np
import random
from typing import List, Tuple

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """
    matches = []
    # Our participants are numbered from 0 to n - 1
    
    # Let's label a random half of the users as the proposers and the other half as the receivers
    participants = len(gender_id)
    proposers = random.sample(range(participants), participants // 2)
    receivers = list(set(range(participants)) - set(proposers))
    freed_proposers = proposers[:]
    proposer_preferences = {}
    receiver_preferences = {}

    # Adjusting the table for incompatible gender-preference combinations
    for person1 in range(participants):
        gender1 = gender_id[person1]
        preference1 = gender_pref[person1]
        for person2 in range(person1, participants):
            gender2 = gender_id[person2]
            preference2 = gender_pref[person2]
            if not compatible(gender1, preference1, gender2, preference2):
                scores[person1][person2] = 0.0
                scores[person2][person1] = 0.0
    
    # Creating the preference lists, removing incompatible matches
    for person in range(participants):
        compatability_list = scores[person]
        if person in proposers:
            proposer_ranking = receivers[:]

            for receiver in receivers:
                if compatability_list[receiver] == 0.0:
                    proposer_ranking.remove(receiver)
            num_receivers = len(proposer_ranking)

            for i in range(num_receivers):
                receiver = proposer_ranking[i]
                proposer_ranking[i] = (receiver, compatability_list[i])

            proposer_ranking.sort(key=lambda x: x[1], reverse=True)

            for i in range(num_receivers):
                receiver = proposer_ranking[i][0]
                proposer_ranking[i] = receiver

            proposer_preferences[person] = proposer_ranking

        else:
            receiver_ranking = proposers[:]
            for proposer in proposers:
                if compatability_list[proposer] == 0.0:
                    receiver_ranking.remove(proposer)
            num_proposers = len(receiver_ranking)

            for i in range(num_proposers):
                proposer = receiver_ranking[i]
                receiver_ranking[i] = (proposer, compatability_list[i])

            receiver_ranking.sort(key=lambda x: x[1], reverse=True)

            for i in range(num_proposers):
                proposer = receiver_ranking[i][0]
                receiver_ranking[i] = proposer

            receiver_preferences[person] = receiver_ranking
    
    matching_dict = {}
    proposer = is_free(freed_proposers, proposer_preferences)

    while proposer != "None":
        # If there is a freed proposer, find the receiver that's next on his preferences
        receiver = proposer_preferences[proposer][0]
        receiver_rank = receiver_preferences[receiver]

        if not(receiver in matching_dict):
            matching_dict[receiver] = proposer
            freed_proposers.pop(0)
        elif receiver_rank.index(proposer) < receiver_rank.index(matching_dict[receiver]):
            freed_proposers.append(proposer)
            matching_dict[receiver] = proposer
            freed_proposers.pop(0)
        else:
            # Rejected, pop this receiver from the person's preferences
            proposer_preferences[proposer].pop(0)

        proposer = is_free(freed_proposers, proposer_preferences)
    
    for receiver, proposer in matching_dict.items():
        matches.append((proposer, receiver))
    
    print(matches)

    return matches

def is_free(freed_proposers: list, proposer_preferences: dict) -> str:
    # Helper function to check if all the proposers in our matching process are freed
    if len(freed_proposers) > 0:
        proposer = freed_proposers[0]

        if len(proposer_preferences[proposer]) > 0:
            return proposer

    return "None"

def compatible(gender1, preference1, gender2, preference2):
    # Helper function that returns False if two people are incompatible
    if preference1 == "Men" and gender2 not in ["Male", "Nonbinary"]:
        return False
    if preference1 == "Women" and gender2 not in ["Female", "Nonbinary"]:
        return False
    if preference2 == "Men" and gender1 not in ["Male", "Nonbinary"]:
        return False
    if preference2 == "Women" and gender1 not in ["Female", "Nonbinary"]:
        return False
    return True

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()

    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
