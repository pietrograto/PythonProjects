from art import logo

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

print(logo)

# def caesar_cipher(plain_text, shift_amount, direction):
#     cipher_text = ""
#     for letter in plain_text:
#         if letter in alphabet:
#             position = alphabet.index(letter)
            
#             if direction == "encode":
#                 new_position = (position + shift_amount) % len(alphabet)
#             elif direction == "decode":
#                 new_position = (position - shift_amount) % len(alphabet)
            
#             new_letter = alphabet[new_position]
#             cipher_text += new_letter
#         else:
#             cipher_text += letter 
#     return cipher_text

# result = caesar_cipher(text,  shift, direction)
# print(f"The encoded message is {result}") 

def caesar_cipher(plain_text, shift_amount, direction):
    cipher_text = ""
    if direction == "decode":
        shift_amount *= -1  # Negate the shift for decoding
    for letter in plain_text:
        if letter in alphabet:
            position = alphabet.index(letter)
            new_position = (position + shift_amount) % len(alphabet)
            new_letter = alphabet[new_position]
            cipher_text += new_letter
        else:
            cipher_text += letter  # Keep non-alphabetic characters unchanged
    return cipher_text

should_end = False
while not should_end:

    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
    text = input("type your message: \n").lower()
    shift = int(input("Type the shift number:\n"))

    result = caesar_cipher(text,  shift, direction)
    print(f"The encoded message is {result}") 

    restart = input("Type 'yes' if you want to go again. Otherwise type 'no'.\n")
    if restart == "no":
        should_end = True
        print("Goodbye")
        
