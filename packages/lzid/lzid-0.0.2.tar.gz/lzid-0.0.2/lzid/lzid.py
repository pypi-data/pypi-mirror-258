import hashlib

def get_lz_id(input_string: str, return_odd: bool = True) -> int:
    """
    Generate a 4-digit number from the given string. This is done by hashing the string,
    converting the hash to an integer, and taking the modulus with respect to 10000.
    If return_odd is True, the function will return an odd number. Otherwise, it will return an even number.
    """
    hashed_value = hashlib.sha256(input_string.encode()).hexdigest()
    four_digit_number = abs(int(hashed_value, 16)) % 10000

    if return_odd and four_digit_number % 2 == 0:
        four_digit_number = (four_digit_number + 1) % 10000
    elif not return_odd and four_digit_number % 2 != 0:
        four_digit_number = (four_digit_number + 1) % 10000

    return four_digit_number