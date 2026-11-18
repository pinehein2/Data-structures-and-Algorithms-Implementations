import sys

def z_algo(input: str, reverse:bool = False) -> list[int]:
    """
    It takes in a string input and forms a Z-Array that identifies the 
    longest matching prefix starting at each index of the string.
    """
    input_len = len(input)
    z_array = [0] * input_len
    if reverse: #Z=algorithm but with suffixes
        z_array[-1] = input_len #Initialize the first index on the side it is starting with the length of the input
        l, r = input_len-1,input_len-1 #Initialize the indicators for the Z-box
        for i in range(input_len-2, -1, -1): #Iteration through each character in the input
            if i >= r: #If the current index is within a Z-box
                if z_array[i-r] < l-i+1: #Checks if there is no potentially longer pattern
                    z_array[i] = z_array[i-r] #Reuses the data from previous Z-boxes 
                else: #If there is a potentially longer pattern
                    r = i
                    while r < input_len and input[input_len - (r - l) - 1] == input[r]: #Marks the Z-box of the unnoticed longer pattern.
                        l -= 1
                    z_array[i] = r - l #Inputs the length of the matching pattern at this index
                    l += 1
            else: #If not in a Z-box
                l, r = i, i
                while l > -1 and input[input_len - (r - l) - 1] == input[l]: #Mark the Z-box if there is any matching at this index.
                    l -= 1
                z_array[i] = r - l #Inputs the length of the matching pattern at this index
                l += 1
    else: #Normal Z-algorithm from the front
        z_array[0] = input_len #Initialize the first index on the side it is starting with the length of the input
        l, r = 0, 0 #Initialize the indicators for the Z-box
        for i in range(1, input_len): #Iteration through each character in the input
            if i <= r: #If the current index is within a Z-box
                if z_array[i-l] < r-i+1: #Checks if there is no potentially longer pattern
                    z_array[i] = z_array[i-l] #Reuses the data from previous Z-boxes 
                else: #If there is a potentially longer pattern
                    l = i
                    while r < input_len and input[r - l] == input[r]: #Marks the Z-box of the unnoticed longer pattern.
                        r += 1
                    z_array[i] = r - l #Inputs the length of the matching pattern at this index
                    r -= 1
            else: #If not in a Z-box
                l, r = i, i
                while r < input_len and input[r - l] == input[r]: #Mark the Z-box if there is any matching at this index.
                    r += 1
                z_array[i] = r - l #Inputs the length of the matching pattern at this index
                r -= 1
    return z_array

def good_suffix(inp: str) -> list[int]:
    """
    Creates a table with the values to shift to the next occuring 
    substring before this current index. The given number can be used 
    to calculate how many shifts within the pattern to reach the next 
    good suffix.
    """
    m = len(inp)
    array = z_algo(inp, True) #Reversed Z-algorithm for the pattern
    suffix_arr = [0] * (m+1) #Initialize suffix array
    for i in range(m-1): #Loop through Z-array
        j = m - array[i] #Calculates which index in the suffix array to assign the index in the pattern to
        suffix_arr[j] = i #Assigns the index in the pattern to the suffix array
    
    return suffix_arr

def match_prefix(inp: str) -> list[int]:
    """
    Creates a table marking the longest matching prefix found at the 
    end of the pattern. The given number can be used to calculate how 
    many shifts within the pattern if the good suffix array does not 
    yield a proper result.
    """
    z_arr = z_algo(inp) #Z-algorithm for the pattern
    input_len = len(inp)
    mp_arr = [0] * (len(z_arr)+1) #Initializes the match prefix array
    for i in range(len(z_arr)-1, -1, -1): #Loops through the list backwards
        if z_arr[i] + i == input_len: #Checks if there is a matching prefix that reaches the end of the pattern
            mp_arr[i] = z_arr[i] #Assigns the current index in the mp_arr the value in the same index in the Z-array
        else:
            mp_arr[i] = mp_arr[i+1] #Assigns the current index in the mp_arr as the previous index in the mp_arr
    return mp_arr

def boyer_moore(text: str, pattern: str) -> list[int]:
    """
    Takes in the text and pattern and then finds all indexes where the
    pattern is a full match with the text by using the good suffix array
    and the match prefix array.
    """
    mp_arr = match_prefix(pattern) #Initializes the matched prefix array
    gs_arr = good_suffix(pattern) #Initializes the good suffix array

    n, m = len(text), len(pattern) #References for lengths of pattern and text
    shift = 0 #Initializing total shift value
    skip_l, skip_r = -1, -1 #Initializing the pointers for galil's optimization
    matches = [] #Output array
    while m-1 + shift < n:
        k = m - 1 #Initializes the current index to compare in both the pattern and text
        while k > -1 and text[k + shift] == pattern[k]: #Loops through and compares the pattern and text until either a mismatch or complete match
            if k == skip_r: #Checks if the current index reaches the range to skip
                k = skip_l #Skips the already known matching section
            k -= 1
        if k <= -1: #Checks if there is a complete match
            matches.append(k + shift + 2) #Appends the match into the output
            shift += m - mp_arr[1] #Adds to the total shift by the pattern according to the match prefix
            skip_l = 0 #Sets the skip ending position
            skip_r = mp_arr[1] #Sets the skip starting position
        else: #If there was a mismatch
            if gs_arr[k+1] == 0: #If the good suffix array shows a shift of 0
                shift += m - mp_arr[k+1] #Adds to the total shift by the length of the pattern minus the value given by the match prefix array
                skip_l = 0 #Sets the skip ending position
                skip_r = mp_arr[k + 1] #Sets the skip starting position
            else: #If the good suffix array shift value can be used
                shift += m - gs_arr[k+1] - 1 #Adds to the total shift by the pattern minus the value given by the match good suffix array
                skip_l = gs_arr[k+1] - m + k + 2 #Sets the skip ending position
                skip_r = gs_arr[k+1] + 1 #Sets the skip starting position
    return matches

def read_file(file_path: str) -> str:
    f = open(file_path, 'r')
    line = f.readline()
    f.close()

    return line

def write_file(matches) -> str:
    f = open("output_a1q2.txt", 'w')
    f.write("\n".join(matches))
    f.close()

if __name__ == '__main__':
    _, filename1, filename2 = sys.argv
    print("Number of arguments passed : ", len(sys.argv))

    print("First argument : ", filename1)
    print("Second argument : ", filename2)

    text = read_file(filename1)
    print("\nContent of first file : ", text)

    pattern = read_file(filename2)
    print("\nContent of second file : ", pattern)

    write_file(boyer_moore(text, pattern))
