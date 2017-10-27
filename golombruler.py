#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

#Your backtracking function implementation
def BT(L, M):
    if L < 0 or M < 0:
        return -1,[]
    if M == 0:
        return -1,[]
    # Mask is used to hold our Golomb rulers Marks
    mask = dict()
    # First element in mask will be always zero, so we are not setting it by default
    mask[0] = 0

    # Call BTRecur to check the result, if result exist then check for L-1 and so on, till we are able to find the Marks for Golomb ruler.
    result =  BTRecur(mask, L, M, 1)
    if result:
        # Store the previous working Mask, this will be our output.
        previousMask = mask
        mask = dict()
        mask[0] = 0
        while(1):
            # Find the maximum value of L that is returned, now call the BTRecur for L-1
            L = max(previousMask.keys()) - 1
            # If result exists then we again call the BTRecur by reducing value of L by 1 and we keep on doing this till we can find the result.
            result = BTRecur(mask, L, M, 1)
            if result:
                previousMask = mask
                mask = dict()
                mask[0] = 0
            else:
                break

        # Return teh optimal Length for L and M
        return max(previousMask.keys()), sorted(previousMask.keys())
    else:
        return -1,[]

def BTRecur(mask, L, M, s):
    if len(mask) == M and max(mask.keys()) == L:
        return True
    # Try different values available for current mark
    for i in range(s,L + 1):
        mask[i] = i
        if not CSPChecker(mask):
            mask.pop(i, None)
        else:
            if len(mask) == M and max(mask.keys()) == L:
                return True
            res = BTRecur(mask, L, M, i + 1)
            if not res:
                mask.pop(i, None)
            else:
                return True

    return False

# Function to check if current state is violating constraint for Golomb Ruler or not.
# Check if all possible differences in values are unique or not
def CSPChecker(ruler):
    tmp = dict()
    rulerList = list(ruler.keys())
    for idx, i in enumerate(rulerList):
        for j in rulerList[(idx+1):]:
                diff = abs(j - i)
                if diff in tmp:
                    return False;

                tmp[diff] = diff
    return True


#Your backtracking+Forward checking function implementation
def FC(L, M):
    if L < 0 or M < 0:
        return -1,[]
    if M == 0:
        return -1,[]
    mask = dict()
    mask[0] = 0
    # Maintaining a domain list which keeps the possible legal values for remaing variables. All remaining variables can have legal domain of values so need only single array
    domain = list(range(1,L+1))
    result =  BTFCRecur(mask, L, M, 1, domain)
    if result:
        previousMask = mask
        while(1):
            # If ruler found for given L, then recursively checking for L - 1
            L = max(previousMask.keys()) - 1
            mask = dict()
            mask[0] = 0
            domain = list(range(1,L+1))
            result = BTFCRecur(mask, L, M, 1, domain)
            if result:
                previousMask = mask
            else:
                break
        return max(previousMask.keys()), sorted(previousMask.keys())
    else:
        return -1,[]

# Recursion function for BT + FP
def BTFCRecur(mask, L, M, s, domain):
    if len(mask) == M and max(mask.keys()) == L:
        return True
    if s == M:
    	return False
    for i in domain:
        # Only values greater than current values can be assigned to remaining variables to avoid duplicate reverse results
        if i < max(mask.keys()):
            continue
        mask[i] = i
        if not CSPChecker(mask):
            mask.pop(i, None)
        else:
            if len(mask) == M and max(mask.keys()) == L:
                return True
            updatedDomain = updateDomain(domain, mask)
            # If no legal values are left for remaining variables then pop the current value and try for others
            if not updatedDomain:
                mask.pop(i, None)
            else:
                res = BTFCRecur(mask, L, M, s + 1, updatedDomain)
                if not res:
                    mask.pop(i, None)
                else:
                    return True

    return False

# Update the domain for remaining variables according to the values assigned to markes
def updateDomain(domain, mask):
    keys = mask.keys()
    maxKey = max(keys)
    # Calculate all possible differences
    diffSet = set(abs(x - maxKey) for x in keys)
    # Check the values that we need to remove from domain
    res = set(x + y for x in list(diffSet) for y in keys)
    domain = list(set(domain) - set(res))
    if len(domain) == 0:
        return False
    return domain

# Backtracking + constraint propagation
def CP(L, M):
    if L < 0 or M < 0:
        return -1,[]
    if M == 0:
        return -1,[]
    mask = dict()
    mask[0] = 0
    domain = list()
    # Maintaining a list of domains for each variable. We need a list of list so that we can update all variables other then teh current variable
    domain.append([0])
    for i in range(1, M-1):
        domain.append(range(1,L+1))
    # Appending L at the end because L should be in the marks for it to be a ruler for given L
    domain.append([L])
    result =  BTCPRecur(mask, L, M, 1, domain)
    if result:
        previousMask = mask
        while(1):
            L = max(previousMask.keys()) - 1
            mask = dict()
            mask[0] = 0
            domain = list()
            domain.append([0])
            for i in range(1, M-1):
                domain.append(range(1,L+1))
            domain.append([L])
            result = BTCPRecur(mask, L, M, 1, domain)
            if result:
                previousMask = mask
            else:
                break
        return max(previousMask.keys()), sorted(previousMask.keys())
    else:
        return -1,[]

def BTCPRecur(mask, L, M, s, domain):
    if len(mask) == M and sorted(mask.keys())[-1] == L:
        return True
    if s == M:
        return False
    j = 0
    while(j < len(domain[s])):
        if j >= len(domain[s]):
            break
        i = domain[s][j]
        mask[i] = i
        if not CSPChecker(mask):
            mask.pop(i, None)
        else:
            if len(mask) == M and sorted(mask.keys())[-1] == L:
                return True
            # Domain a list of list so it is getting updated in updateDomain function So saving it and using again after fucntion ends
            preDomain = map(lambda x : list(x), domain)
            if not updateDomainForCP(domain, mask, len(mask)):
                mask.pop(i, None)
                domain = map(lambda x : list(x), preDomain)
            else:
                res = BTCPRecur(mask, L, M, s + 1, domain)
                if not res:
                    mask.pop(i, None)
                    domain = map(lambda x : list(x), preDomain)
                else:
                    return True
        j = j + 1
    
    return False

# Updating domain for BT + CP
def updateDomainForCP(domain, mask, s):
    keys = mask.keys()
    maxKey = max(keys)
    diffSet = set(abs(x - y) for x in keys for y in keys)
    res = set(x + y for x in list(diffSet) for y in keys)
    res = list(res.union(set(range(0,maxKey+1))))
    for i in range(s, len(domain)):
        domain[i] = [x for x in domain[i] if x not in res]
        if len(domain[i]) == 0:
            return False
    return True

import sys
if __name__ == "__main__":

    L = 6
    M = 4
    if len(sys.argv) > 2:
        L = int(sys.argv[1])  # Reading directory path from command line
        M = int(sys.argv[2])

    print BT(L, M)
    print FC(L, M)
    print CP(L, M)


