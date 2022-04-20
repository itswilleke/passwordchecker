import sys
import hashlib
import requests
import string
import random

#This section generates a random password
# characters for password
alphabets = list(string.ascii_letters)
digits = list(string.digits)
special_characters = list("!@#$%^&*()")
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")


def generate_random_password():
    # To set a length of the password
    length = int(input("Enter password length: "))
    alphabets_count = int(input("Enter alphabets count in password: "))
    digits_count = int(input("Enter digits count in password: "))
    special_characters_count = int(
        input("Enter special characters count in password: "))

    characters_count = alphabets_count + digits_count + special_characters_count

    if characters_count > length:
        print("Characters total count is greater than the password length")
        return

    password = []
    # Pick a random letter
    for i in range(alphabets_count):
        password.append(random.choice(alphabets))
    # Pick a random digit
    for i in range(digits_count):
        password.append(random.choice(digits))
    # Pick a random character
    for i in range(special_characters_count):
        password.append(random.choice(special_characters))

    if characters_count < length:
        random.shuffle(characters)
        for i in range(length - characters_count):
            password.append(random.choice(characters))

    # Shuffle the password
    random.shuffle(password)

    print("".join(password))


# Call the function
password = generate_random_password()

#This section checks for safety of the generated random password
def request_api_data(query_char):
    url = ' https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching: {res.status_code}, check the api and try again')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(
                f'{password} was found {count} times... you should probably change your password!')
        else:
            print(f'{password} was NOT found. Carry on!')
    return 'Your password can be safely used'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

