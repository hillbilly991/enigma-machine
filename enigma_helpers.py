from errors import *


def get_standard_reflector_mapping(reflector_name):
    match reflector_name:
        case "A":
            return tuple("EJMZALYXVBWFCRQUONTSPIKHGD")
        case "B":
            return tuple("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        case "C":
            return tuple("FVPJIAOYEDRZXWGCTKUQSBNMHL")
        case _:
            raise ReflectorError(
                "You tried to get the mapping of a reflector that does not exist"
            )


def get_rotor_mappings(reflector_name):
    match reflector_name:
        case "Beta":
            return {
                "mapping": tuple("LEYJVCNIXWPBQMDRTAKZGFUHOS"),
                "notch": -1,
            }
        case "Gamma":
            return {
                "mapping": tuple("FSOKANUERHMBTIYCWLQPZXVGJD"),
                "notch": -1,
            }
        case "I":
            return {
                "mapping": tuple("EKMFLGDQVZNTOWYHXUSPAIBRCJ"),
                "notch": 16,
            }
        case "II":
            return {
                "mapping": tuple("AJDKSIRUXBLHWTMCQGZNPYFVOE"),
                "notch": 4,
            }
        case "III":
            return {
                "mapping": tuple("BDFHJLCPRTXVZNYEIWGAKMUSQO"),
                "notch": 21,
            }
        case "IV":
            return {
                "mapping": tuple("ESOVPZJAYQUIRHXLNFTGKDCMWB"),
                "notch": 9,
            }
        case "V":
            return {
                "mapping": tuple("VZBRGITYUPSDNHLXAWMJQOFECK"),
                "notch": 25,
            }
        case _:
            raise RotorError(
                "You tried to get the mapping of a rotor that does not exist"
            )


def is_valid_enigma_input_string(string):
    """
    Ensures that the input string is valid

    A valid string for the enigma machine in this project is only uppercased letters
    in the alphabet with no spaces between them
    """
    if not isinstance(string, str):
        return False

    return string.isalpha() and string.isupper()
