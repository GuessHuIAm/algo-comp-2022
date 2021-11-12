import json
from typing import List, Tuple

def is_stable(input_preferences: dict, matching: List[Tuple]) -> bool:
    """ Helper function to determine whether or not matching is stable. """

    men_rank = input_preferences["preffered_ranking_men"]
    women_rank = input_preferences["preffered_ranking_women"]
    for m, w in matching:
        i = men_rank[m].index(w)
        prefer_over_w = men_rank[m][:i]
        for homewrecker in prefer_over_w:
            homewrecker_curr_match = [match[0] for match in matching if match[1] == homewrecker][0]
            if women_rank[homewrecker].index(m) < women_rank[homewrecker].index(homewrecker_curr_match):
                msg = "{}'s marriage to {} is unstable: " + \
                      "{} prefers {} over {} and {} prefers " + \
                      "{} over her current husband {}"
                print(msg.format(m, w, m, homewrecker, w, homewrecker, m, homewrecker_curr_match))
            return False

    return True

def run_matching(input_preferences: dict) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param input_preferences: a dictionary of Men's preferences of Women and Women's preferences of Men
    :return: `matches`, a List of (Man, Woman) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - How will you keep track of the men who get "freed" up from matches?
        - We know that women never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - It may be helpful to transform the raw `input_preferences` data into a form where preference rank is explicitly (i.e. numerically) stated
        - This is by no means an exhaustive list, feel free to reach out to Leonard/Jeremy for more help!
    """
    matches = []
    men_preferences = input_preferences["preffered_ranking_men"]
    women_preferences = input_preferences["preffered_ranking_women"]
    matching_dict = {}
    freed_men = list(men_preferences.keys())

    man = is_free(freed_men, men_preferences)

    while man != "None":
        # If there is a freed man, find the woman that's next on his preferences
        woman = men_preferences[man][0]
        woman_rank = women_preferences[woman]

        if not(woman in matching_dict):
            matching_dict[woman] = man
            freed_men.pop(0)
        elif woman_rank.index(man) > woman_rank.index(matching_dict[woman]):
            freed_men.append(matching_dict[woman])
            matching_dict[woman] = man
            freed_men.pop(0)
        else:
            # Rejected, pop the woman from the guy's preferences
            men_preferences[man].pop(0)

        man = is_free(freed_men, men_preferences)
    
    for woman, man in matching_dict.items():
        matches.append((man, woman))
    
    print(matches)

    return matches

def is_free(freed_men: list, men_preferences: dict) -> str:
    # Helper function to check if all the men in our game are freed
    if len(freed_men) > 0:
        man = freed_men[0]

        if len(men_preferences[man]) > 0:
            return man

    return "None"

if __name__ == "__main__":
    with open('preferences.json', 'r') as file:
        preferences = json.load(file)

    gs_matches = run_matching(preferences)
    if is_stable(preferences, gs_matches):
        print("CONGRATS! YOU JUST CREATED A STABLE MATCHING :)")
    else:
        print("UNSTABLE MATCHING!")
