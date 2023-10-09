import itertools as it
from enigma_helpers import *
import string


def get_potential_rotor_names(rotor_names_allowed, rotor_length):
    return list(it.permutations(rotor_names_allowed, rotor_length))


def get_potential_ring_settings(ring_settings_allowed, rotor_length):
    return list(it.product(ring_settings_allowed, repeat=rotor_length))


def get_potential_position_settings(position_settings_allowed, rotor_length):
    return list(it.product(position_settings_allowed, repeat=rotor_length))


def get_potential_lead_settings(known_leads, leads_with_one_character):
    """
    This method takes known leads, and any leads where we know what one of the characters is
    (but we don't know which one it connects to), and returns a list of possible lead settings
    """
    # first get all the letters that we know have been taken on the plugboard and use these
    # to find any letters that we know must be available
    characters_taken = "".join(known_leads + leads_with_one_character)
    available_characters = [
        char for char in list(string.ascii_uppercase) if char not in characters_taken
    ]

    # then get all the potential leads by looping through all the leads that we know will need
    # to connect to another letter on the plugboard
    potential_leads = []
    for lead_missing_one_character in leads_with_one_character:
        for available_character in available_characters:
            potential_leads.append(lead_missing_one_character + available_character)

    # with these, we then need to find as many pairings that can happen between these missing
    # letters. For example, if we know that one letter 'I' and another letter 'A' need to
    # connect to another letter on the plugboard, and we know that "WPRJVFHNCGBSAI" are already
    # taken - we will produce combinations where "A" + another letter not in "WPRJVFHNCGBSAI" and
    # "I" + another letter not in "WPRJVFHNCGBSAI" are added to a tuple i.e:
    # [("AZ", "IK"), ("AZ", "AK") etc.]
    # note that in the second tuple, "AZ" and "AK" appear together. If this combination was added
    # to the plugboard then this would not be valid so we filter these out below
    potential_missing_combinations = list(
        it.combinations(potential_leads, len(leads_with_one_character))
    )

    potential_lead_settings = []
    for potential_missing_combo in potential_missing_combinations:
        known_leads_copy = known_leads.copy()
        potential_missing_combo_in_string = "".join(potential_missing_combo)
        potential_missing_combo_has_duplicates = len(
            set(potential_missing_combo_in_string)
        ) < len(potential_missing_combo_in_string)

        if not potential_missing_combo_has_duplicates:
            for valid_lead in potential_missing_combo:
                known_leads_copy.append(valid_lead)

            potential_lead_settings.append(known_leads_copy)

    return potential_lead_settings


def get_potential_custom_reflector_mappings(standard_reflector_names):
    """
    If there were four pairs of wires that were swapped from a normal reflector
    then you could use this method to return all the possible reflector mappings
    that it could have been
    """
    potential_custom_reflector_mappings = []

    for standard_reflector_name in standard_reflector_names:
        potential_reflector_mappings_with_swapped_wires = (
            get_potential_reflector_mappings_with_swapped_wires(standard_reflector_name)
        )
        for (
            potential_custom_reflector_mapping
        ) in potential_reflector_mappings_with_swapped_wires:
            potential_custom_reflector_mappings.append(
                potential_custom_reflector_mapping
            )

    return potential_custom_reflector_mappings


def get_potential_reflector_mappings_with_swapped_wires(reflector_name):
    """
    This method gets the reflector mappings from standard reflectors A, B and C, and creates as many
    combinations as possible whereby four pairs of wires in each of the reflectors are swapped

    This is used to solve Code 5 in the assignment
    """
    reflector_mapping = get_standard_reflector_mapping(reflector_name)
    standard_reflector_pairings = get_standard_reflector_pairings(reflector_mapping)
    four_pairs = list(it.combinations(standard_reflector_pairings, 4))

    potential_reflector_mappings_with_swapped_wires = []

    for four_pair in four_pairs:
        potential_two_pairs_to_swap = list(it.combinations(four_pair, 2))
        for first_two_pairs in potential_two_pairs_to_swap:
            second_two_pairs = list(set(four_pair) - set(first_two_pairs))

            first_two_pairs_swapped = swap_wire_pairs(
                first_two_pairs[0], first_two_pairs[1]
            )
            second_two_pairs_swapped = swap_wire_pairs(
                second_two_pairs[0], second_two_pairs[1]
            )

            four_potential_reflector_mappings_in_pairs = (
                get_four_potential_reflector_mappings_in_pairs(
                    first_two_pairs_swapped,
                    second_two_pairs_swapped,
                    standard_reflector_pairings,
                    four_pairs,
                )
            )

            for (
                potential_reflector_mapping
            ) in four_potential_reflector_mappings_in_pairs:
                potential_reflector_mappings_with_swapped_wires.append(
                    {
                        "name": "Custom",
                        "custom_reflector_mapping": {
                            "original_reflector_name": reflector_name,
                            "mapping": convert_reflector_pairs_to_reflector_mapping(
                                potential_reflector_mapping
                            ),
                        },
                    }
                )

    return potential_reflector_mappings_with_swapped_wires


def get_standard_reflector_pairings(reflector_definition):
    """
    For each character in a standard reflector, find the corresponding wire that it maps
    to

    For example, if A maps onto D in a reflector, then you will see that D is in the
    position of A in the alphabet, and A is in the position of D i.e:
    Alphabet: ABCD
    Reflector mapping: DCBA

    This method puts these mappings into a set of tuples, and makes sure that each letter
    is unique i.e:
    set((C, B), (D, A))
    """
    standard_reflector_pairings = set()
    letter_already_added = set()

    for index, char in enumerate(reflector_definition):
        if char not in letter_already_added:
            paired_char = string.ascii_uppercase[index]
            standard_reflector_pairings.add((paired_char, char))
            letter_already_added.add(paired_char)
            letter_already_added.add(char)

    return standard_reflector_pairings


def swap_wire_pairs(pair_one, pair_two):
    first_swap = [(pair_one[0], pair_two[0]), (pair_one[1], pair_two[1])]
    second_swap = [(pair_one[0], pair_two[1]), (pair_one[1], pair_two[0])]

    return [first_swap, second_swap]


def get_four_potential_reflector_mappings_in_pairs(
    first_two_pairs_swapped,
    second_two_pairs_swapped,
    standard_reflector_pairings,
    four_pairs,
):
    """
    This method returns any standard reflector pairings plus any new ones
    that have been swapped in four different combinations

    For example if (F, Z) and (G, K) have been swapped to look like this:
    (F, G) and (Z, K) then one of the potential reflector pairings that
    this method will return would look something like this:

    [standard reflector pairings + (F, G), (Z, K)]
    """
    potential_reflector_mappings_in_pairs = []
    standard_reflector_pairings_without_swapped_pairs = set(
        standard_reflector_pairings
    ) - set(four_pairs)

    for i, j in it.product(range(2), repeat=2):
        potential_reflector_mappings_in_pairs.append(
            list(
                it.chain(
                    first_two_pairs_swapped[i] + second_two_pairs_swapped[j],
                    standard_reflector_pairings_without_swapped_pairs,
                )
            )
        )

    return potential_reflector_mappings_in_pairs


def convert_reflector_pairs_to_reflector_mapping(reflector_pairs):
    """
    This method takes the reflector pairs that have been created from the swaps
    and puts them into how a standard reflector is mapped. For example if a
    reflector originally had this mapping:
    ('C', 'D', 'A', 'B')

    they would have been paired up in this way:
    set((A, C))
    set((B, D))

    after two of the wires were swapped, they could be paired up like this:
    set((A, D))
    set((B, C))

    and this method would therefore put them into this mapping:
    ('D', 'C', 'B', 'A')

    whereby A, which is the 1st letter in the alphabet, and D, which is the fourth,
    are mapped onto each others usual position because they are paired with one
    another
    """
    alphabet_list = list(string.ascii_uppercase)
    mapping = {char: char for char in alphabet_list}

    for char1, char2 in reflector_pairs:
        mapping[char1], mapping[char2] = mapping[char2], mapping[char1]

    return tuple([mapping[char] for char in alphabet_list])
