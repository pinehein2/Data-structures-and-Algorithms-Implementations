def encoder_lz77(text: str, max_search:int, max_lookahead:int):
    middle_bound = 0
    output = []
    while middle_bound < len(text):
        offset = 0
        length = 0
        for i in range(max(middle_bound - min(max_search, max_lookahead), 0), middle_bound):
            if text[i] == text[middle_bound]:
                offset = middle_bound - i
                break
        if offset > 0:
            while text[middle_bound + length] == text[middle_bound-offset+length] and length < max_lookahead and middle_bound+length < len(text)-1:
                length += 1
        output.append((offset, length, text[middle_bound+length]))
        middle_bound += length + 1
    return output

def decoder_lz77(code):
    decoded = ""
    for offset, length, next_char in code:
        if offset > 0 and length > 0:
            for i in range(length):
                decoded += decoded[0-offset+i]
                offset += 1
        decoded += next_char
    return decoded

def encoder(text, max_search:int, max_lookahead:int):
    pass


if __name__ == "__main__":
    text = "aacaacabcabaaac"
    m = encoder(text, 6, 4)
    n = decoder_lz77([(0,0,'p'),(0,0,'q'),(0,0,'r'),(3,3,'s'),(7,6,'t')])
    print(n)