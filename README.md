# Enigma machine

This project represents an enigma machine that was used during the Second World War to encrypt
military communications

## How to run this project

### Tests

1. First install pytest:

```py
pip install pytest
```

2. Then run:

```py
pytest tests.py
```

## How the Enigma machine works

### Keyboard

In order to encode characters, the person using the enigma machine would type their message on
a keyboard. Each character typed would pass through multiple encryption processes that are
detailed below. This is one of the reasons that the enigma machine was such a powerful tool
for encrypting military communications - it passed through multiple layers of encryption

### Plugboard and Plugleads

After a character is typed on the keyboard, this would fire off a signal and its first destination
was the plugboard, which housed plug leads

A plug lead is a wire that connects two letters together on a plugboard. If the signal from the
keyboard is 'A' and 'A' is connected to 'Z' via a plug lead, then the signal outputted from the
plugboard would be 'Z'

For example, you might have the following characters connected by different plug leads:

```py
[('A', 'Z'), ('B', 'F'), ('P', 'L')]
```

If, for example, the user typed in 'L' then the keyboard would send an 'L' signal to the plugboard,
and since 'L' is connected to 'P' via a plug lead, the plugboard would output a 'P' signal to the
rotor cradle

n.b: notice that there are no two characters that are repeated in different plug leads

### Rotor Cradle

A key component of the encryption process in the engima machine are the rotors and reflectors, which
sit within a rotor cradle

A rotor has pins and contacts on either side of it. When the signal arrives from the plugboard, it
goes through the right hand side of the first rotor, moves through the rotor's internal wiring and
exits via a contact on its left hand side. This happens across each rotor until it arrives at a
reflector, which sits on the far left hand side of the rotor cradle. The reflector then encodes a
character signal and 'reflects' it back across each rotor

The encryption is different after it hits the reflector since it now goes through the contacts on the
left hand side of each rotor and, again, moves through each rotor's internal wiring before exiting the
rotor on its right hand side (via a pin)

This is a very simplified version of a complex process. There are multiple characteristics of rotors,
depending on where they sit within the rotor cradle, and are probably best explained
in [this article](https://en.wikipedia.org/wiki/Enigma_rotor_details)

After the signal passes through the rotor cradle, it eventually returns to the plugboard, where the same
encryption process explained above begins again before it finally lights a bulb above the keyboard
