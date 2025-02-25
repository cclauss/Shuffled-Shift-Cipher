import random
import string


class shuffled_shift_cipher(object):
    """
    This algorithm uses the Caeser Cipher algorithm but removes the option to
    use brute force to decrypt the message.

    The passcode is a a random password from the selection buffer of
    1. uppercase letters of the English alphabet
    2. lowercase letters of the English alphabet
    3. digits from 0 to 9

    Using unique characters from the passcode, the normal list of characters,
    that can be allowed in the plaintext, is pivoted and shuffled. Refer to docstring
    of __make_key_list() to learn more about the shuffling.

    Then, using the passcode, a number is calculated which is used to encrypt the
    plaintext message with the normal shift cipher method, only in this case, the
    reference, to look back at while decrypting, is shuffled.

    Each cipher object can possess an optional argument as passcode, without which a
    new passcode is generated for that object automatically.
    cip1 = shuffled_shift_cipher('d4usr9TWxw9wMD')
    cip2 = shuffled_shift_cipher()
    """

    def __init__(self, passkey=None):
        """
        Initializes a cipher object with a passcode as it's entity
        Note: No new passcode is generated if user provides a passcode
        while creating the object
        """
        if passkey == None:
            self.__passcode = self.__passcode_creator()
        else:
            self.__passcode = passkey
        self.__key_list = self.__make_key_list()
        self.__shift_key = self.__make_shift_key()

    def __str__(self):
        """
        :return: passcode of the cipher object
        """
        return "Passcode is: " + "".join(self.__passcode)

    def __sum_of_digits(self, num):
        """
        Calculates the sum of all digits in 'num'

        :param num: a positive natural number
        :return: an integer which stores the sum of digits
        """
        sum_ = sum(map(int, str(num)))
        return sum_

    def __make_one_digit(self, digit):
        """
        Implements an algorithm to return a single digit integer
        Doesn't keep the value of input 'digit' intact

        :param digit: takes in a positive number
        :return: the number itself; if its single digit
                 else, converts to single digit and returns
        """
        while digit > 10:
            digit = self.__sum_of_digits(digit)
        return digit

    def __neg_pos(self, iterlist):
        """
        Mutates the list by changing the sign of each alternate element

        :param iterlist: takes a list iterable
        :return: the mutated list
        """
        for i in range(1, len(iterlist), 2):
            iterlist[i] *= -1
        return iterlist

    def __passcode_creator(self):
        """
        Creates a random password from the selection buffer of
        1. uppercase letters of the English alphabet
        2. lowercase letters of the English alphabet
        3. digits from 0 to 9

        :rtype: list
        :return: a password of a random length between 10 to 20
        """
        choices = string.ascii_letters + string.digits
        password = [random.choice(choices) for i in range(random.randint(10, 20))]
        return password

    def __make_key_list(self):
        """
        Shuffles the ordered character choices by pivoting at breakpoints
        Breakpoints are the set of characters in the passcode

        eg:
            if, ABCDEFGHIJKLMNOPQRSTUVWXYZ are the possible characters
            and CAMERA is the passcode
            then, breakpoints = [A,C,E,M,R] # sorted set of characters from passcode
            shuffled parts: [A,CB,ED,MLKJIHGF,RQPON,ZYXWVUTS]
            shuffled __key_list : ACBEDMLKJIHGFRQPONZYXWVUTS

        Shuffling only 26 letters of the english alphabet can generate 26!
        combinations for the shuffled list. In the program we consider, a set of
        97 characters (including letters, digits, punctuation and whitespaces),
        thereby creating a possibility of 97! combinations (which is a 152 digit number in itself),
        thus diminishing the possibility of a brute force approach. Moreover,
        shift keys even introduce a multiple of 26 for a brute force approach
        for each of the already 97! combinations.
        """
        # key_list_options contain nearly all printable except few elements from string.whitespace
        key_list_options = (
            string.ascii_letters + string.digits + string.punctuation + " \t\n"
        )

        keys_l = []

        # creates points known as breakpoints to break the key_list_options at those points and pivot each substring
        breakpoints = sorted(set(self.__passcode))
        temp_list = []

        # algorithm for creating a new shuffled list, keys_l, out of key_list_options
        for i in key_list_options:
            temp_list.extend(i)

            # checking breakpoints at which to pivot temporary sublist and add it into keys_l
            if i in breakpoints or i == key_list_options[-1]:
                keys_l.extend(temp_list[::-1])
                temp_list = []

        # returning a shuffled keys_l to prevent brute force guessing of shift key
        return keys_l

    def __make_shift_key(self):
        """
        sum() of the mutated list of ascii values of all characters where the 
        mutated list is the one returned by __neg_pos()
        """
        num = sum(self.__neg_pos(list(map(ord, self.__passcode))))
        return num if num > 0 else len(self.__passcode)

    def decrypt(self, encoded_message):
        """
        Performs shifting of the encoded_message w.r.t. the shuffled __key_list
        to create the decoded_message
        """
        decoded_message = ""

        # decoding shift like caeser cipher algorithm implementing negative shift or reverse shift or left shift
        for i in encoded_message:
            position = self.__key_list.index(i)
            decoded_message += self.__key_list[
                (position - self.__shift_key) % -len(self.__key_list)
            ]

        return decoded_message

    def encrypt(self, plaintext):
        """
        Performs shifting of the plaintext w.r.t. the shuffled __key_list
        to create the encoded_message
        """
        encoded_message = ""

        # encoding shift like caeser cipher algorithm implementing positive shift or forward shift or right shift
        for i in plaintext:
            position = self.__key_list.index(i)
            encoded_message += self.__key_list[
                (position + self.__shift_key) % len(self.__key_list)
            ]

        return encoded_message


if __name__ == "__main__":
    # cip1 = shuffled_shift_cipher('d4usr9TWxw9wMD')
    cip1 = shuffled_shift_cipher()
    cipher = cip1.encrypt("Hello, this is like a modified caeser cipher")
    print(cipher)
    print(cip1)
    print(cip1.decrypt(cipher))
