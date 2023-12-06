from enigma import *
from cracking_secrets import *
import unittest
import string


class TestPlugLeads(unittest.TestCase):
    def test_less_than_two_letters_added(self):
        with self.assertRaises(PlugLeadError):
            PlugLead("A")

    def test_more_than_two_letters_added(self):
        with self.assertRaises(PlugLeadError):
            PlugLead("ABC")

    def test_chars_are_in_alphabet(self):
        with self.assertRaises(PlugLeadError):
            PlugLead("!")

        with self.assertRaises(PlugLeadError):
            PlugLead("8")

        with self.assertRaises(PlugLeadError):
            PlugLead(",")

    def test_chars_are_unique(self):
        with self.assertRaises(PlugLeadError):
            PlugLead("AA")

    def test_opposite_mapping(self):
        lead = PlugLead("AG")
        self.assertEqual(lead.encode("A"), "G")
        self.assertEqual(lead.encode("G"), "A")

    def test_different_letter_encoded(self):
        lead = PlugLead("AG")
        self.assertEqual(lead.encode("B"), "B")


class TestPlugboard(unittest.TestCase):
    def test_plug_lead_chars_are_not_unique(self):
        plugboard = Plugboard()
        lead = PlugLead("AG")
        lead_two = PlugLead("AF")
        plugboard.add(lead)

        with self.assertRaises(PlugboardError):
            plugboard.add(lead_two)

    def test_plug_lead_chars_are_unique(self):
        plugboard = Plugboard()
        lead = PlugLead("AG")
        lead_two = PlugLead("BF")
        plugboard.add(lead)
        plugboard.add(lead_two)


class TestRotorCradle(unittest.TestCase):
    def test_more_than_four_rotors_added(self):
        rotor_cradle = RotorCradle()
        rotor_one = Rotor("I")
        rotor_two = Rotor("II")
        rotor_three = Rotor("III")
        rotor_four = Rotor("IV")
        rotor_five = Rotor("V")

        rotor_cradle.add_rotor(rotor_one)
        rotor_cradle.add_rotor(rotor_two)
        rotor_cradle.add_rotor(rotor_three)
        rotor_cradle.add_rotor(rotor_four)

        with self.assertRaises(RotorCradleError):
            rotor_cradle.add_rotor(rotor_five)

    def test_only_one_reflector_allowed(self):
        rotor_cradle = RotorCradle()
        reflector_one = Reflector("A")
        reflector_two = Reflector("B")

        rotor_cradle.add_reflector(reflector_one)
        with self.assertRaises(RotorCradleError):
            rotor_cradle.add_reflector(reflector_two)


class TestRotor(unittest.TestCase):
    def test_incorrect_mapping(self):
        with self.assertRaises(RotorError):
            Rotor("XASASDASD")

    def test_standard_rotor_mapping(self):
        rotor = Rotor("I")
        rotor_mapping_one = get_rotor_mappings("I")
        self.assertEqual(rotor.mapping, rotor_mapping_one["mapping"])

    def test_encode_from_left_to_right(self):
        alphabet_uppercased = string.ascii_uppercase

        rotor_i = Rotor("I")
        self.assertEqual(
            rotor_i.encode_from_left_to_right(alphabet_uppercased.index("A")),
            alphabet_uppercased.index("U"),
        )

        rotor_ii = Rotor("II")
        self.assertEqual(
            rotor_ii.encode_from_left_to_right(alphabet_uppercased.index("U")),
            alphabet_uppercased.index("H"),
        )

        rotor_iii = Rotor("III")
        self.assertEqual(
            rotor_iii.encode_from_left_to_right(alphabet_uppercased.index("Z")),
            alphabet_uppercased.index("M"),
        )

        rotor_iv = Rotor("IV")
        self.assertEqual(
            rotor_iv.encode_from_left_to_right(alphabet_uppercased.index("H")),
            alphabet_uppercased.index("N"),
        )

        rotor_v = Rotor("V")
        self.assertEqual(
            rotor_v.encode_from_left_to_right(alphabet_uppercased.index("X")),
            alphabet_uppercased.index("P"),
        )

        rotor_beta = Rotor("Beta")
        self.assertEqual(
            rotor_beta.encode_from_left_to_right(alphabet_uppercased.index("G")),
            alphabet_uppercased.index("U"),
        )

        rotor_gamma = Rotor("Gamma")

        self.assertEqual(
            rotor_gamma.encode_from_left_to_right(alphabet_uppercased.index("P")),
            alphabet_uppercased.index("T"),
        )

    def test_encode_from_right_to_left(self):
        alphabet_uppercased = string.ascii_uppercase

        rotor_i = Rotor("I")
        self.assertEqual(
            rotor_i.encode_from_right_to_left(alphabet_uppercased.index("A")),
            alphabet_uppercased.index("E"),
        )

        rotor_ii = Rotor("II")
        self.assertEqual(
            rotor_ii.encode_from_right_to_left(alphabet_uppercased.index("U")),
            alphabet_uppercased.index("P"),
        )

        rotor_iii = Rotor("III")
        self.assertEqual(
            rotor_iii.encode_from_right_to_left(alphabet_uppercased.index("Z")),
            alphabet_uppercased.index("O"),
        )

        rotor_iv = Rotor("IV")
        self.assertEqual(
            rotor_iv.encode_from_right_to_left(alphabet_uppercased.index("H")),
            alphabet_uppercased.index("A"),
        )

        rotor_v = Rotor("V")
        self.assertEqual(
            rotor_v.encode_from_right_to_left(alphabet_uppercased.index("X")),
            alphabet_uppercased.index("E"),
        )

        rotor_beta = Rotor("Beta")
        self.assertEqual(
            rotor_beta.encode_from_right_to_left(alphabet_uppercased.index("G")),
            alphabet_uppercased.index("N"),
        )

        rotor_gamma = Rotor("Gamma")

        self.assertEqual(
            rotor_gamma.encode_from_right_to_left(alphabet_uppercased.index("P")),
            alphabet_uppercased.index("C"),
        )


class TestReflector(unittest.TestCase):
    def test_incorrect_mapping(self):
        with self.assertRaises(ReflectorError):
            Reflector("AKSDKJLASDJKLAKLJS")

    def test_standard_reflector_mapping(self):
        reflector = Reflector("A")
        reflector_mapping_a = get_standard_reflector_mapping("A")
        self.assertEqual(reflector.mapping, reflector_mapping_a)

    def test_custom_reflector_mapping(self):
        alphabet_uppercase_tuple = tuple(string.ascii_uppercase)
        reflector = CustomReflector(
            original_reflector_name="A", mapping=alphabet_uppercase_tuple
        )
        self.assertEqual(reflector.mapping, alphabet_uppercase_tuple)

    def test_custom_reflector_incorrect_mapping(self):
        alphabet_uppercase_tuple_double = tuple(string.ascii_uppercase * 2)

        with self.assertRaises(ReflectorError):
            CustomReflector(
                original_reflector_name="B", mapping=alphabet_uppercase_tuple_double
            )


class TestEnigmaMachine(unittest.TestCase):
    def test_invalid_rotor_cradle_added(self):
        lead = PlugLead("AG")
        lead_two = PlugLead("BD")
        plugboard = Plugboard()
        plugboard.add(lead)
        plugboard.add(lead_two)

        rotor = Rotor("I")
        rotor_two = Rotor("II")
        reflector = Reflector("A")

        rotor_cradle = RotorCradle()

        rotor_cradle.add_rotor(rotor)
        rotor_cradle.add_rotor(rotor_two)
        rotor_cradle.add_reflector(reflector)

        with self.assertRaises(EnigmaMachineError):
            EnigmaMachine(plugboard, rotor_cradle)

    def test_encoding(self):
        enigma_machine = EnigmaMachineFactory.create_enigma_machine(
            ["I", "II", "III"], ["1", "1", "1"], ["A", "A", "Z"], reflector_name="B"
        )

        self.assertEqual(enigma_machine.encode("A"), "U")

        enigma_machine = EnigmaMachineFactory.create_enigma_machine(
            ["I", "II", "III"], ["1", "1", "1"], ["A", "A", "A"], reflector_name="B"
        )

        self.assertEqual(enigma_machine.encode("A"), "B")

        enigma_machine = EnigmaMachineFactory.create_enigma_machine(
            ["I", "II", "III"], ["1", "1", "1"], ["Q", "E", "V"], reflector_name="B"
        )

        self.assertEqual(enigma_machine.encode("A"), "L")

        enigma_machine = EnigmaMachineFactory.create_enigma_machine(
            ["IV", "V", "Beta"], ["14", "9", "24"], ["A", "A", "A"], reflector_name="B"
        )

        self.assertEqual(enigma_machine.encode("H"), "Y")

        enigma_machine = EnigmaMachineFactory.create_enigma_machine(
            ["I", "II", "III", "IV"],
            ["7", "11", "15", "19"],
            ["Q", "E", "V", "Z"],
            reflector_name="C",
        )

        self.assertEqual(enigma_machine.encode("Z"), "V")

        enigma_machine = EnigmaMachineFactory.create_enigma_machine(
            ["I", "II", "III"],
            ["1", "1", "1"],
            ["A", "A", "Z"],
            lead_settings=["HL", "MO", "AJ", "CX", "BZ", "SR", "NI", "YW", "DG", "PK"],
            reflector_name="B",
        )

        self.assertEqual(enigma_machine.encode("HELLOWORLD"), "RFKTMBXVVW")

        enigma_machine = EnigmaMachineFactory.create_enigma_machine(
            ["IV", "V", "Beta", "I"],
            ["18", "24", "3", "5"],
            ["E", "Z", "G", "P"],
            lead_settings=["PC", "XZ", "FM", "QA", "ST", "NB", "HY", "OR", "EV", "IU"],
            reflector_name="A",
        )
        self.assertEqual(
            enigma_machine.encode(
                "BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI"
            ),
            "CONGRATULATIONSONPRODUCINGYOURWORKINGENIGMAMACHINESIMULATOR",
        )

    def test_invalid_encoding(self):
        enigma_machine = EnigmaMachineFactory.create_enigma_machine(
            ["I", "II", "III"], ["1", "1", "1"], ["A", "A", "Z"], reflector_name="B"
        )

        with self.assertRaises(EnigmaMachineError):
            enigma_machine.encode("EVERYTHINGISUPPERCASEEXCEPTFORthis")

        with self.assertRaises(EnigmaMachineError):
            enigma_machine.encode("Numbersgalore121123123123")

        with self.assertRaises(EnigmaMachineError):
            enigma_machine.encode("EVERYTHING IS UPPERCASE WITH SPACES IN IT")

    def test_machine_configurations_for_code_breaking(self):
        enigma_machine_code_one = EnigmaMachineFactory.create_enigma_machine(
            ["Beta", "Gamma", "V"],
            ["4", "2", "14"],
            ["M", "J", "M"],
            reflector_name="C",
            lead_settings=["KI", "XN", "FL"],
        )

        self.assertEqual(
            enigma_machine_code_one.encode(
                "DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ"
            ),
            "NICEWORKYOUVEMANAGEDTODECODETHEFIRSTSECRETSTRING",
        )

        enigma_machine_code_two = EnigmaMachineFactory.create_enigma_machine(
            ["Beta", "I", "III"],
            ["24", "2", "10"],
            ["J", "M", "G"],
            reflector_name="B",
            lead_settings=["VH", "PT", "ZG", "BJ", "EY", "FS"],
        )

        self.assertEqual(
            enigma_machine_code_two.encode(
                "CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH"
            ),
            "IHOPEYOUAREENJOYINGTHEUNIVERSITYOFBATHEXPERIENCESOFAR",
        )

        enigma_machine_code_three = EnigmaMachineFactory.create_enigma_machine(
            ["II", "Gamma", "IV"],
            ["24", "8", "20"],
            ["E", "M", "Y"],
            reflector_name="C",
            lead_settings=["FH", "TS", "BE", "UQ", "KD", "AL"],
        )

        self.assertEqual(
            enigma_machine_code_three.encode(
                "ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY"
            ),
            "SQUIRRELSPLANTTHOUSANDSOFNEWTREESEACHYEARBYMERELYFORGETTINGWHERETHEYPUTTHEIRACORNS",
        )

        enigma_machine_code_four = EnigmaMachineFactory.create_enigma_machine(
            ["V", "III", "IV"],
            ["24", "12", "10"],
            ["S", "W", "U"],
            reflector_name="A",
            lead_settings=["WP", "RJ", "VF", "HN", "CG", "BS", "AT", "IK"],
        )

        self.assertEqual(
            enigma_machine_code_four.encode(
                "SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW"
            ),
            "NOTUTORSWEREHARMEDNORIMPLICATEDOFCRIMESDURINGTHEMAKINGOFTHESEEXAMPLES",
        )

        enigma_machine_code_five = EnigmaMachineFactory.create_enigma_machine(
            ["V", "II", "IV"],
            ["6", "18", "7"],
            ["A", "J", "L"],
            reflector_name="Custom",
            custom_reflector_mapping={
                "original_reflector_name": "B",
                "mapping": tuple("PQUHRSLDYXNGOKMABEFZCWVJIT"),
            },
            lead_settings=["UG", "IE", "PO", "NX", "WT"],
        )

        self.assertEqual(
            enigma_machine_code_five.encode(
                "HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX"
            ),
            "YOUCANFOLLOWMYDOGONINSTAGRAMATTALESOFHOFFMANN",
        )


class TestEnigmaMachineFactory(unittest.TestCase):
    def test_no_reflector_settings(self):
        with self.assertRaises(EnigmaMachineFactoryError):
            EnigmaMachineFactory.create_enigma_machine(
                ["V", "II", "IV"],
                ["6", "18", "7"],
                ["A", "J", "L"],
                reflector_name=None,
                custom_reflector_mapping=None,
                lead_settings=["UG", "IE", "PO", "NX", "WT"],
            )

    def test_too_many_rotors_created(self):
        with self.assertRaises(EnigmaMachineFactoryError):
            EnigmaMachineFactory.create_enigma_machine(
                ["V", "II", "IV", "Gamma", "Beta"],
                ["6", "18", "7"],
                ["A", "J", "L"],
                reflector_name=None,
                custom_reflector_mapping=None,
                lead_settings=["UG", "IE", "PO", "NX", "WT"],
            )

    def test_incorrect_leads(self):
        with self.assertRaises(EnigmaMachineFactoryError):
            EnigmaMachineFactory.create_enigma_machine(
                ["V", "II", "IV", "Gamma", "Beta"],
                ["6", "18", "7"],
                ["A", "J", "L"],
                reflector_name=None,
                custom_reflector_mapping=None,
                lead_settings=["UG", "IE", "PO", "NX", "WT", "AI", "ZT", "MH", "QT"],
            )

    def test_enigma_machine_created_successfully(self):
        enigma_machine = EnigmaMachineFactory.create_enigma_machine(
            ["V", "II", "IV"],
            ["6", "18", "7"],
            ["A", "J", "L"],
            reflector_name="B",
            custom_reflector_mapping=None,
            lead_settings=["UG", "IE", "PO", "NX", "WT"],
        )

        self.assertEqual(str(enigma_machine), "V-6-A II-18-J IV-7-L B UG-IE-PO-NX-WT")


class TestEnigmaCodeCracker(unittest.TestCase):
    def test_cribs(self):
        with self.assertRaises(EnigmaCodeCrackerError):
            EnigmaCodeCracker(
                cribs=[],
                code="SUPERSECRETCODETHATISVERYOBVIOUS",
                rotor_names=[["V", "II", "IV"]],
                ring_settings=[["6", "18", "7"]],
                position_settings=[["A", "J", "L"]],
                reflectors=[{"name": "B"}],
                lead_settings=[["UG", "IE", "PO", "NX", "WT"]],
            )

        with self.assertRaises(EnigmaCodeCrackerError):
            EnigmaCodeCracker(
                cribs=["VALIDCRIB", "ANOTHERONE", "INvalid"],
                code="SUPERSECRETCODETHATISVERYOBVIOUS",
                rotor_names=[["V", "II", "IV"]],
                ring_settings=[["6", "18", "7"]],
                position_settings=[["A", "J", "L"]],
                reflectors=[{"name": "B"}],
                lead_settings=[["UG", "IE", "PO", "NX", "WT"]],
            )

        with self.assertRaises(EnigmaCodeCrackerError):
            EnigmaCodeCracker(
                cribs=["VALIDCRIB", "ANOTHERONE", "     "],
                code="SUPERSECRETCODETHATISVERYOBVIOUS",
                rotor_names=[["V", "II", "IV"]],
                ring_settings=[["6", "18", "7"]],
                position_settings=[["A", "J", "L"]],
                reflectors=[{"name": "B"}],
                lead_settings=[["UG", "IE", "PO", "NX", "WT"]],
            )

        with self.assertRaises(EnigmaCodeCrackerError):
            EnigmaCodeCracker(
                cribs=["VALIDCRIB", "ANOTHERONE", "1213123123"],
                code="SUPERSECRETCODETHATISVERYOBVIOUS",
                rotor_names=[["V", "II", "IV"]],
                ring_settings=[["6", "18", "7"]],
                position_settings=[["A", "J", "L"]],
                reflectors=[{"name": "B"}],
                lead_settings=[["UG", "IE", "PO", "NX", "WT"]],
            )

    def test_code(self):
        with self.assertRaises(EnigmaCodeCrackerError):
            EnigmaCodeCracker(
                cribs=["TESTING"],
                code="12123123",
                rotor_names=[["V", "II", "IV"]],
                ring_settings=[["6", "18", "7"]],
                position_settings=[["A", "J", "L"]],
                reflectors=[{"name": "B"}],
                lead_settings=[["UG", "IE", "PO", "NX", "WT"]],
            )

        with self.assertRaises(EnigmaCodeCrackerError):
            EnigmaCodeCracker(
                cribs=["TESTING"],
                code="TESTING SPACE",
                rotor_names=[["V", "II", "IV"]],
                ring_settings=[["6", "18", "7"]],
                position_settings=[["A", "J", "L"]],
                reflectors=[{"name": "B"}],
                lead_settings=[["UG", "IE", "PO", "NX", "WT"]],
            )

        with self.assertRaises(EnigmaCodeCrackerError):
            EnigmaCodeCracker(
                cribs=["TESTING"],
                code="TESTING!!!!",
                rotor_names=[["V", "II", "IV"]],
                ring_settings=[["6", "18", "7"]],
                position_settings=[["A", "J", "L"]],
                reflectors=[{"name": "B"}],
                lead_settings=[["UG", "IE", "PO", "NX", "WT"]],
            )

        with self.assertRaises(EnigmaCodeCrackerError):
            EnigmaCodeCracker(
                cribs=["TESTING"],
                code="TESTINGaSNEAKYLOWERCASE",
                rotor_names=[["V", "II", "IV"]],
                ring_settings=[["6", "18", "7"]],
                position_settings=[["A", "J", "L"]],
                reflectors=[{"name": "B"}],
                lead_settings=[["UG", "IE", "PO", "NX", "WT"]],
            )

        enigma_code_cracker = EnigmaCodeCracker(
            cribs=["TESTING"],
            code="TESTINGAGOODCASE",
            rotor_names=[["V", "II", "IV"]],
            ring_settings=[["6", "18", "7"]],
            position_settings=[["A", "J", "L"]],
            reflectors=[{"name": "B"}],
            lead_settings=[["UG", "IE", "PO", "NX", "WT"]],
        )

        self.assertGreaterEqual(len(enigma_code_cracker.valid_enigma_machines), 1)
