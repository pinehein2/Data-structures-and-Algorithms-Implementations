def z_algo(input: str) -> list[int]:
    """
    It takes in a string input and forms a Z-Array that identifies the 
    longest matching prefix starting at each index of the string.
    """
    inpLen = len(input)
    zArr = [0] * inpLen
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

def sparray(input: str) -> list[int]:
    zArr = z_algo(input)
    kmpArr = [0] * len(input)
    for i in range(len(input)-1, 0, -1):
        kmpArr[i + zArr[i]-1] = zArr[i]

    return kmpArr

if __name__ == "__main__":
    print(z_algo("abcdabcdabcdabcdabcdabcd"))