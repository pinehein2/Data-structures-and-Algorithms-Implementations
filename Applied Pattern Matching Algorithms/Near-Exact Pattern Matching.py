import sys

def z_algo(input: str, reverse:bool = False) -> list[int]:
    """
    It takes in a string input and forms a Z-Array that identifies the 
    longest matching prefix starting at each index of the string.
    """
    inpLen = len(input)
    zArr = [0] * inpLen
    if reverse: #Z=algorithm but with suffixes
        zArr[-1] = inpLen #Initialize the first index on the side it is starting with the length of the input
        l, r = inpLen-1,inpLen-1 #Initialize the indicators for the Z-box
        for i in range(inpLen-2, -1, -1): #Iteration through each character in the input
            if i >= r: #If the current index is within a Z-box
                if zArr[i-r] < l-i+1: #Checks if there is no potentially longer pattern
                    zArr[i] = zArr[i-r] #Reuses the data from previous Z-boxes 
                else: #If there is a potentially longer pattern
                    r = i
                    while r < inpLen and input[inpLen - (r - l) - 1] == input[r]: #Marks the Z-box of the unnoticed longer pattern.
                        l -= 1
                    zArr[i] = r - l #Inputs the length of the matching pattern at this index
                    l += 1
            else: #If not in a Z-box
                l, r = i, i
                while l > -1 and input[inpLen - (r - l) - 1] == input[l]: #Mark the Z-box if there is any matching at this index.
                    l -= 1
                zArr[i] = r - l #Inputs the length of the matching pattern at this index
                l += 1
    else: #Normal Z-algorithm from the front
        zArr[0] = inpLen #Initialize the first index on the side it is starting with the length of the input
        l, r = 0, 0 #Initialize the indicators for the Z-box
        for i in range(1, inpLen): #Iteration through each character in the input
            if i <= r: #If the current index is within a Z-box
                if zArr[i-l] < r-i+1: #Checks if there is no potentially longer pattern
                    zArr[i] = zArr[i-l] #Reuses the data from previous Z-boxes 
                else: #If there is a potentially longer pattern
                    l = i
                    while r < inpLen and input[r - l] == input[r]: #Marks the Z-box of the unnoticed longer pattern.
                        r += 1
                    zArr[i] = r - l #Inputs the length of the matching pattern at this index
                    r -= 1
            else: #If not in a Z-box
                l, r = i, i
                while r < inpLen and input[r - l] == input[r]: #Mark the Z-box if there is any matching at this index.
                    r += 1
                zArr[i] = r - l #Inputs the length of the matching pattern at this index
                r -= 1
    return zArr

def dl_distance(text:str, pattern:str) -> list[int]:
    """
    It takes in a text string and a pattern string then uses the 
    Z-Algorithm to find all indexes in the text where the pattern either
    matches or has a near match that can be solved either by a single edit
    of replace, swap, insert, or delete.
    """
    zarr1 = z_algo(pattern + "¿" + text)[-(len(text)):] #Gets the prefix Z-Array and trims the pattern and terminal character
    zarr2 = z_algo(text + "¿" + pattern, reverse=True)[:(len(text))] #Gets the suffix Z-Array and trims the patterna and terminal character

    output = []

    for i in range(len(zarr1)): #Iterates through the Z-Array
        if zarr1[i] == len(pattern): 
            #Case 1: Perfect Match, if the match length is the same as the length of the pattern.

            output.append((i+1, 0))

        elif i + len(pattern) - 1 < len(zarr1) \
            and zarr1[i] + zarr2[i + len(pattern)-1] == len(pattern)-1: 
            #Case 2: Replacement, if the amount of matches on each end of i, i + len(pattern) - 1 add up to the len(pattern) - 1 meaning only 1 character is not matching

            output.append((i+1, 1))

        elif i + len(pattern) - 1 < len(zarr1) \
            and zarr1[i] + zarr2[i + len(pattern)-1] == len(pattern)-2 \
            and text[i + zarr1[i]] == pattern[zarr1[i] + 1] \
            and text[i + zarr1[i] + 1] == pattern[zarr1[i]]: 
            #Case 3: Swapping, if the amount of matches on each end of i, i + len(pattern) - 1 add up to len(pattern) - 2 meaning 2 consecutives characters are not matching and those two characters will be checked to see if they can be swapped to form a match
                
            output.append((i+1, 1))

        elif i + len(pattern) - 2 < len(zarr1) \
            and zarr1[i] + zarr2[i + len(pattern)-2] >= len(pattern) - 1:
            #Case 4: Insertion, if the amount of matches on each end of i, i + len(pattern) - 2 add up to len(pattern) - 1 or more, the pattern is missing a character that will complete the match

            output.append((i+1, 1))

        elif i + len(pattern) < len(zarr1) \
            and zarr1[i] + zarr2[i + len(pattern)] >= len(pattern): 
            #Case 5: Deletion, if the amount of matches on each end of i, i + len(pattern) add up to len(pattern) or more, the pattern has an extra character that can be deleted to complete the match

            output.append((i+1, 1))
        
    return output

def read_file(file_path: str) -> str:
    f = open(file_path, 'r')
    line = f.readline()
    f.close()

    return line

def write_file(matches) -> str:
    f = open("output_a1q1.txt", 'w')
    f.write("\n".join(map(lambda tup: f"{tup[0]} {tup[1]}", matches)))
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

    write_file(dl_distance(text, pattern))