def apihelper(obj, pattern):
    matches = [att for att in dir(obj) if pattern in att]
    print(matches)
    return matches
