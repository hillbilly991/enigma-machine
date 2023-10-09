from enigma import *
from enigma_helpers import *
import itertools as it
import string
from cracking_secrets_helpers import *


class EnigmaCodeCracker:
    """
    EnigmaCodeCracker helps to crack enigma codes by creating all possible
    valid enigma machines given a number of known and unknown settings

    It uses cribs (clues as to what string will be in the code) and a code
    which is a string that needs to be decrypted, creates valid enigma
    machines from them and then retrieves potential solutions

    Currently only supports printing potential solutions but this could be
    extended to support returning potential solutions, too
    """

    def __init__(
        self,
        cribs,
        code,
        rotor_names,
        position_settings,
        ring_settings,
        reflectors,
        lead_settings,
    ):
        if len(cribs) == 0:
            raise EnigmaCodeCrackerError("You must provide at least one crib")

        invalid_string_input = lambda crib: not is_valid_enigma_input_string(crib)

        if any(invalid_string_input(crib) for crib in cribs):
            raise EnigmaCodeCrackerError("One or more of your cribs are invalid")

        if not is_valid_enigma_input_string(code):
            raise EnigmaCodeCrackerError(
                "Code must be a string with at least one character"
            )
        valid_enigma_machines = self.__create_valid_enigma_machines_from_settings__(
            rotor_names, ring_settings, position_settings, reflectors, lead_settings
        )
        self.cribs = cribs
        self.code = code
        self.valid_enigma_machines = valid_enigma_machines
        self.potential_solutions = self.__get_potential_solutions__(
            valid_enigma_machines
        )

    def __create_valid_enigma_machines_from_settings__(
        self,
        rotor_names=[],
        ring_settings=[],
        position_settings=[],
        reflectors=[],
        lead_settings=[],
    ):
        """
        Creates valid enigma machines from inputs
        """
        valid_enigma_machines = []
        for reflector in reflectors:
            for ring_setting in ring_settings:
                for rotor_name in rotor_names:
                    for position_setting in position_settings:
                        for lead_setting in lead_settings:
                            try:
                                enigma_machine = (
                                    EnigmaMachineFactory.create_enigma_machine(
                                        rotor_name,
                                        ring_setting,
                                        position_setting,
                                        lead_settings=lead_setting,
                                        reflector_name=reflector.get("name"),
                                        custom_reflector_mapping=reflector.get(
                                            "custom_reflector_mapping"
                                        ),
                                    )
                                )

                                valid_enigma_machines.append(enigma_machine)
                            except Exception as err:
                                # It might be the case that sometimes the enigma machine
                                # cannot be created as there are faulty settings in them.
                                # We want to swallow these but still see the error message
                                # to:
                                # 1. reduce time and space complexity. If we try to create
                                # too many enigma machines that are faulty, then we are
                                # potentially both increasing the time it takes to crack
                                # codes and using up more memory than is necessary
                                # 2. we want to swallow errors because even if our settings
                                # were incompatible with an enigma machine setup, then we
                                # still want to see whether we can crack the code
                                # with another enigma machine created with different settings
                                # because it will a. tell us that we have cracked the code and
                                # b. give us an indication on how good our implementation is
                                print(err)

        return valid_enigma_machines

    def __get_potential_solutions__(self, valid_enigma_machines):
        """
        Gets the enigma machine setting and the decoded string for any
        enigma machine that finds one of the cribs within the decoded
        string
        """
        potential_solutions = []
        for enigma_machine in valid_enigma_machines:
            decoded_string = enigma_machine.encode(self.code)
            for crib in self.cribs:
                if crib in decoded_string:
                    potential_solutions.append(
                        {
                            "enigma_machine": enigma_machine,
                            "decoded_string": decoded_string,
                        }
                    )

        return potential_solutions

    def print_potential_solutions(self):
        print("---------------------------")
        if len(self.potential_solutions) > 0:
            for potential_solution in self.potential_solutions:
                print(potential_solution)
        else:
            print("Looks like you did not find any potential solutions\n")
            print("Try changing the settings on the enigma machine")
        print("---------------------------")


def cracking_code_one():
    enigma_code_cracker = EnigmaCodeCracker(
        cribs=["SECRETS"],
        code="DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ",
        rotor_names=[["Beta", "Gamma", "V"]],
        ring_settings=[["4", "2", "14"]],
        position_settings=[["M", "J", "M"]],
        reflectors=[
            {"name": "A"},
            {"name": "B"},
            {"name": "C"},
        ],
        lead_settings=[["KI", "XN", "FL"]],
    )

    enigma_code_cracker.print_potential_solutions()


def cracking_code_two():
    enigma_code_cracker = EnigmaCodeCracker(
        cribs=["UNIVERSITY"],
        code="CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH",
        rotor_names=[["Beta", "I", "III"]],
        ring_settings=[["24", "2", "10"]],
        position_settings=get_potential_position_settings(string.ascii_uppercase, 3),
        reflectors=[{"name": "B"}],
        lead_settings=[["VH", "PT", "ZG", "BJ", "EY", "FS"]],
    )

    enigma_code_cracker.print_potential_solutions()


def cracking_code_three():
    enigma_code_cracker = EnigmaCodeCracker(
        cribs=["THOUSANDS"],
        code="ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY",
        rotor_names=get_potential_rotor_names(["II", "IV", "Beta", "Gamma"], 3),
        ring_settings=get_potential_ring_settings([2, 4, 6, 8, 20, 22, 24, 26], 3),
        position_settings=[["E", "M", "Y"]],
        reflectors=[{"name": "A"}, {"name": "B"}, {"name": "C"}],
        lead_settings=[["FH", "TS", "BE", "UQ", "KD", "AL"]],
    )

    enigma_code_cracker.print_potential_solutions()


def cracking_code_four():
    enigma_code_cracker = EnigmaCodeCracker(
        cribs=["TUTOR"],
        code="SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW",
        rotor_names=[["V", "III", "IV"]],
        ring_settings=[["24", "12", "10"]],
        position_settings=[["S", "W", "U"]],
        reflectors=[{"name": "A"}],
        lead_settings=get_potential_lead_settings(
            ["WP", "RJ", "VF", "HN", "CG", "BS"], ["A", "I"]
        ),
    )

    enigma_code_cracker.print_potential_solutions()


def cracking_code_five():
    enigma_code_cracker = EnigmaCodeCracker(
        cribs=["FACEBOOK", "INSTAGRAM", "REDDIT", "TWITTER", "MYSPACE", "YOUTUBE"],
        code="HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX",
        rotor_names=[["V", "II", "IV"]],
        ring_settings=[["6", "18", "7"]],
        position_settings=[["A", "J", "L"]],
        reflectors=get_potential_custom_reflector_mappings(["A", "B", "C"]),
        lead_settings=[["UG", "IE", "PO", "NX", "WT"]],
    )

    enigma_code_cracker.print_potential_solutions()


if __name__ == "__main__":
    cracking_code_one()
    cracking_code_two()
    cracking_code_three()
    cracking_code_four()
    cracking_code_five()
