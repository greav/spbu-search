from bitstring import BitArray


def elias_gamma_encode(number):
    reduced_binary_code = bin(number)[3:]
    return inverted_unary(len(reduced_binary_code)) + reduced_binary_code


def elias_gamma_encode_sequence(numbers):
    return BitArray(bin="".join(elias_gamma_encode(number) for number in numbers))


def elias_delta_encode(number):
    bin_n = bin(number)[2:]
    n_sign_bits = len(bin_n)
    encoded_sign_bits = elias_gamma_encode(n_sign_bits)
    return encoded_sign_bits + bin_n[1:]


def elias_delta_encode_sequence(numbers):
    return BitArray(bin="".join(elias_delta_encode(number) for number in numbers))


def inverted_unary(number):
    return "0" * number + "1"


def elias_gamma_decode(encoded_numbers):
    decoded_numbers = []
    n_zeros = 0
    i = 0
    while i < len(encoded_numbers):
        if not encoded_numbers[i]:  # bit == 0
            n_zeros += 1
            i += 1
        else:  # bit == 1
            if n_zeros == 0:
                number = 1
            else:
                number = (
                    int(encoded_numbers[i + 1 : i + n_zeros + 1].bin, base=2)
                    + 2 ** n_zeros
                )
            decoded_numbers.append(number)
            i += n_zeros + 1
            n_zeros = 0
    return decoded_numbers


def elias_delta_decode(encoded_numbers):
    decoded_numbers = []
    n_zeros = 0
    i = 0
    while i < len(encoded_numbers):
        if not encoded_numbers[i]:  # bit == 0
            n_zeros += 1
            i += 1
        else:  # bit == 1
            if n_zeros == 0:
                k = 1
                number = 1
            else:
                k = (
                    int(encoded_numbers[i + 1 : i + n_zeros + 1].bin, base=2)
                    + 2 ** n_zeros
                )
                number = 2 ** (k - 1) + int(
                    encoded_numbers[i + 1 + n_zeros : i + n_zeros + k].bin, base=2
                )
            decoded_numbers.append(number)
            i += n_zeros + k
            n_zeros = 0

    return decoded_numbers
