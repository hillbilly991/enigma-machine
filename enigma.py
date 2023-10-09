from errors import *
from enigma_helpers import *


class Plugboard:
    """
    Represents a plugboard in the enigma machine

    The plugboard houses plug leads and this class is used to both encode a character
    through the plug leads. It is also used tovalidate whether all the characters within
    the plug leads are unique and, also, limits the number of plug leads allowed in the
    enigma machine
    """

    def __init__(self):
        self.leads = []

    def encode(self, char):
        for lead in self.leads:
            encoded_char = lead.encode(char)
            if encoded_char != char:
                return encoded_char

        return char

    def add(self, PlugLead):
        if len(self.leads) > 10:
            raise PlugboardError("You are not allowed to add more than 10 leads")

        for lead in self.leads:
            if (
                lead.characters[0] in PlugLead.characters
                or lead.characters[1] in PlugLead.characters
            ):
                raise PlugboardError(
                    "You tried to add a lead to the plugboard which has one of its letters already taken",
                    lead.characters,
                    self.leads,
                )

        self.leads.append(PlugLead)

    def __str__(self):
        return f"{self.leads}"

    def __repr__(self):
        return f"{self.leads}"


class PlugLead:
    """
    Represents a plug lead in the enigma machine

    Plug leads connect two letters together so that if a signal from the
    keyboard is received (which will be a letter i.e 'I') and a plug lead
    contains that letter (i.e 'IE'), then the plug lead will emit a signal
    with the opposite character (in this example it would be 'E')
    """

    def __init__(self, mapping):
        if len(mapping) != 2:
            raise PlugLeadError("You must add 2 values to the PlugLead")

        if not mapping.isalpha():
            raise PlugLeadError("Character must be a letter in the alphabet")

        if mapping[0] == mapping[1]:
            raise PlugLeadError("Each character must be unique")

        self.characters = mapping.upper().strip()

    def encode(self, character):
        if character not in self.characters:
            return character

        return (
            self.characters[1]
            if self.characters[0] == character
            else self.characters[0]
        )

    def __str__(self):
        return f"{self.characters}"

    def __repr__(self):
        return f"{self.characters}"


class Reflector:
    """
    Represents a reflector of the enigma machine

    The reflector sits on the far left hand side of the rotors in the enigma machine
    and receives a signal from the rotor to its immediate right, encodes it, and then
    'reflects' it back to the same rotor
    """

    def __init__(self, reflector_name):
        self.name = reflector_name
        self.mapping = get_standard_reflector_mapping(reflector_name)

    def encode(self, pin):
        reflected_char = self.mapping[pin]

        return ord(reflected_char) - 65

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class CustomReflector(Reflector):
    """
    The is a special reflector which can be used to create a custom mapping for a
    standard Reflector
    """

    def __init__(self, mapping, original_reflector_name):
        if len(mapping) != 26:
            raise ReflectorError("The custom reflector mapping must be 26 letters long")

        self.name = "Custom"
        self.mapping = mapping
        self.original_reflector_name = original_reflector_name

    def __str__(self):
        return f"{self.original_reflector_name} {''.join(self.mapping)}"

    def __repr__(self):
        return f"{self.original_reflector_name} {''.join(self.mapping)}"


class Rotor:
    """
    Represents a fundamental element of the Enigma machine - a rotor

    This class represents the behaviour of a single rotor. A rotor sits within a cradle
    (represented by RotorCradle) and receives signals through pins (which sit on the
    right hand side of the Rotor) and contacts (which site on the left hand side of a
    Rotor). Depending on which way the signal is travelling, a rotor will first receive
    a signal on a pin or a contact (see encode_from_right_to_left and
    encode_from_left_to_right)

    The internal wiring of a rotor moves when the position of the rotor changes, and is
    offset by the ring setting of the rotor. These two determine where a signal enters
    and exits a rotor (see methods encode_from_right_to_left and encode_from_left_to_right
    for more details)
    """

    def __init__(self, name, position_setting="A", ring_setting=1):
        rotor_setting = get_rotor_mappings(name)
        self.name = name
        self.mapping = rotor_setting["mapping"]
        self.notch = rotor_setting["notch"]
        self.position = ord(position_setting) - 65
        self.ring_setting = ring_setting - 1
        self.initial_position = position_setting

    def step(self):
        self.position = self.position + 1 if self.position != 25 else 0

    def encode_from_right_to_left(self, initial_pin):
        """
        Mimics the behaviour of how a rotor receives a signal on its right side.

        On the right hand side of each rotor there is a pin. Initially, a signal
        hits a pin on the right hand side of the rotor (initial_pin), and this
        then passes a signal through the rotor's internal wiring to exit the
        rotor through a contact on its left hand side (exit_contact). The route
        the signal takes through the internal wiring is determined by the
        difference between its current position and the ring setting, which is
        the offset
        """
        offset = self.__get_offset__()
        # whatever contact is at the adjusted pin index will have a
        # corresponding exit contact, which is where the signal will exit
        # the rotor from from the left hand side
        adjusted_pin_index = (initial_pin + offset) % 26
        # we find the offset exit contact by first finding what the position
        # of the contact would be if the internal wiring hadn't changed (i.e
        # if the position and ring setting hadn't been adjusted), and then use
        # the offset (which is the difference between the current position and
        # the ring setting) to determine which contact the signal will exit
        # from out of the rotor
        label_index = ord(self.mapping[adjusted_pin_index]) - 65
        exit_contact = (label_index - offset) % 26

        return exit_contact

    def encode_from_left_to_right(self, first_contact):
        """
        Mimics the behaviour of how a rotor receives a signal on its left side.

        On the left hand side of each rotor there is a contact. The first thing
        that happens is a contact receives a signal (first_contact) which then
        passes a signal through the rotor's internal wiring to exit the rotor
        through a pin on its right hand side (exit_pin). The route the signal
        takes through the internal wiring is determined by the difference between
        its current position and the ring setting, which is the offset
        """
        offset = self.__get_offset__()
        # when the signal enters the rotor from the left, it will first hit a
        # contact, which will be adjusted according to the rotor's current
        # position and ring setting
        adjusted_contact = (first_contact + offset) % 26
        # we then need to get that character and then find it within the
        # the mapping in order to pass the signal from the left hand side to
        # the right hand side
        char_from_contact = chr(65 + adjusted_contact)
        pin_index = self.mapping.index(char_from_contact)
        # and we adjust the exit pin because we want to make sure that it hits
        # the correct adjusted contact on the rotor to the right hand side, or
        # the plugboard
        exit_pin = (pin_index - offset) % 26

        return exit_pin

    def __get_offset__(self):
        """
        Influences the route that the signal takes through the internal wiring
        of the rotor
        """
        return self.position - self.ring_setting

    def is_on_notch(self):
        return self.notch == self.position

    def __str__(self):
        return f"{self.name}-{self.ring_setting + 1}-{self.initial_position}"

    def __repr__(self):
        return f"{self.name}-{self.ring_setting + 1}-{self.initial_position}"


class RotorCradle:
    """
    Represents where a reflector and rotor are housed within an enigma machine

    A RotorCradle makes sure that the rotors are stepped forward before a signal
    is sent through the rotors and reflector. It also makes sure that signals are
    sent to the correct pins and contacts on the rotors and reflector, and
    validates whether the number of rotors and reflectors are within the limit of
    what is needed to encode a text in an enigma machine
    """

    def __init__(self):
        self.rotors = []
        self.reflector = None

    def add_rotor(self, Rotor):
        if len(self.rotors) >= 4:
            raise RotorCradleError("You are allowed a maximum of 4 rotors")

        self.rotors.append(Rotor)

    def add_reflector(self, Reflector):
        if self.reflector != None:
            raise RotorCradleError("You are only allowed one reflector")

        self.reflector = Reflector

    def step_rotors(self):
        """
        Steps rotors forward if they need to be before a signal is sent through
        the rotor cradle
        """
        prev_rotor_turned_on_notch = False

        for i, rotor in enumerate(self.rotors):
            first_rotor = i == 0
            first_or_second_rotor = first_rotor or i == 1
            second_or_third_rotor = i == 1 or i == 2
            if rotor.is_on_notch() and first_or_second_rotor:
                rotor.step()
                prev_rotor_turned_on_notch = True
            elif prev_rotor_turned_on_notch and second_or_third_rotor:
                rotor.step()
                prev_rotor_turned_on_notch = False
            elif first_rotor:
                rotor.step()

    def encode(self, input_character):
        """
        Steps rotors and then encodes a character from the right hand side of the
        rotor cradle to the left and then back again
        """
        self.step_rotors()
        pin_to_connect_to = ord(input_character) - 65

        for rotor in self.rotors:
            pin_to_connect_to = rotor.encode_from_right_to_left(pin_to_connect_to)

        contact_to_connect_to = self.reflector.encode(pin_to_connect_to)

        for i in range(-1, -len(self.rotors) - 1, -1):
            contact_to_connect_to = self.rotors[i].encode_from_left_to_right(
                contact_to_connect_to
            )

        input_character_encrypted = chr(contact_to_connect_to + 65)

        return input_character_encrypted

    def __str__(self):
        return f"{self.rotors} {self.reflector}"

    def __repr__(self):
        return f"{self.rotors} {self.reflector}"


class EnigmaMachine:
    """
    Represents the enigma machine

    EnigmaMachine houses a plugboard and rotor cradle (see Plugboard and RotorCradle)
    """

    def __init__(self, Plugboard, RotorCradle):
        if len(RotorCradle.rotors) < 3 or len(RotorCradle.rotors) > 4:
            raise EnigmaMachineError(
                "You must have either 3 or 4 Rotors in order to run the enigma machine"
            )

        self.plugboard = Plugboard
        self.rotor_cradle = RotorCradle

    def encode(self, string):
        """
        encodes a string in the enigma machine by passing it through the plugboard first,
        then through the rotors and reflector in the rotor cradle, before finally
        passing it back through the plugboard
        """
        if not is_valid_enigma_input_string(string):
            raise EnigmaMachineError(
                "Input must be uppercase letters of the alphabet only with no spaces"
            )

        encoded_string = []
        for character in string:
            plugboard_output = self.plugboard.encode(character)
            rotor_cradle_output = self.rotor_cradle.encode(plugboard_output)

            encoded_string.append(self.plugboard.encode(rotor_cradle_output))

        return "".join(encoded_string)

    def __str__(self):
        rotors = " ".join([str(rotor) for rotor in reversed(self.rotor_cradle.rotors)])
        reflector = self.rotor_cradle.reflector
        plugboard = "-".join([str(pluglead) for pluglead in self.plugboard.leads])

        return f"{rotors} {reflector} {plugboard}"

    def __repr__(self):
        rotors = " ".join([str(rotor) for rotor in reversed(self.rotor_cradle.rotors)])
        reflector = self.rotor_cradle.reflector
        plugboard = "-".join([str(pluglead) for pluglead in self.plugboard.leads])

        return f"{rotors} {reflector} {plugboard}"


class EnigmaMachineFactory:
    """
    Creates an enigma machine from preconfigured settings
    """

    def create_enigma_machine(
        rotor_names,
        ring_settings,
        position_settings,
        reflector_name=None,
        custom_reflector_mapping=None,
        lead_settings=[],
    ):
        rotor_cradle = RotorCradle()
        plugboard = Plugboard()

        rotor_settings_together = list(
            zip(rotor_names, ring_settings, position_settings)
        )

        # We reverse these settings since the rotors names, ring settings and position
        # settings are all sent to this method in the order in which the rotors appear
        # when looking at the rotor cradle in real life
        # In reality, the signal is sent through the right most rotor first, and goes
        # through each rotor to the left of it before being reflected back again. To mimic
        # this behaviour, we reverse the settings so that when a signal is sent through a
        # RotorCradle, it is done so in the correct order (from right to left)
        for rotor_name, ring_setting, position_setting in reversed(
            rotor_settings_together
        ):
            rotor = Rotor(
                rotor_name,
                ring_setting=int(ring_setting),
                position_setting=position_setting,
            )
            rotor_cradle.add_rotor(rotor)

        if custom_reflector_mapping:
            reflector = CustomReflector(
                custom_reflector_mapping["mapping"],
                custom_reflector_mapping["original_reflector_name"],
            )
        elif reflector_name:
            reflector = Reflector(reflector_name)
        else:
            raise EnigmaMachineFactoryError(
                "You must add a reflector name or custom reflector mapping to create an enigma machine"
            )

        rotor_cradle.add_reflector(reflector)

        for lead_setting in lead_settings:
            lead = PlugLead(lead_setting)
            plugboard.add(lead)

        enigma_machine = EnigmaMachine(plugboard, rotor_cradle)

        return enigma_machine
