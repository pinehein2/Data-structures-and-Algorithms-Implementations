def buildSuffixArray(txt):
    n = len(txt)
  
    # Create a list of all suffixes
    suffixes = [txt[i:] for i in range(n)]
    
    # Sort the suffixes
    suffixes.sort()
    
    # Create the suffix array
    suffArr = [txt.index(suffix) for suffix in suffixes]
    return suffArr

def bwt(txt):
    suffixArray = buildSuffixArray(txt)
    bwtTxt = ""
    for x in suffixArray:
        bwtTxt += txt[x-1]
    
    return bwtTxt

def invertbwt(txt):
    def get_freq(letter, ind):
        freq = 0
        for x in range(0, ind):
            if txt[x] == letter:
                freq += 1
        return freq
    
    sortArr = sorted(txt)
    rank = {sortArr[0]:0}
    for x in range(1,len(sortArr)):
        if sortArr[x] not in rank:
            rank[sortArr[x]] = x

    newtxt = sortArr[0]
    current = sortArr[0]
    next = txt[rank[current]]
    ind = rank[current]
    while next is not sortArr[0]:
        current = next
        newtxt = sortArr[rank[current] + get_freq(current, ind)] + newtxt
        next = txt[rank[current] + get_freq(current, ind)]
        ind = rank[current] + get_freq(current, ind)
        
    return newtxt

if __name__ == '__main__':
    t = "rattatattat$"
    b = bwt(t)
    s = sorted(b)
    print(b)
    print(invertbwt(b))

