class Person:
    def __init__(self, name):
        self._name = name
        self._hasPartner = False
        self._perfectMatchName = None
        self._currentPartnerName = None
        self._foundTrueLove = False
    def getName(self):
        return self._name
    def getCurrentPartnerName(self):
        return self._currentPartnerName
    def getPerfectMatchName(self):
        return self._perfectMatchName
    def setCurrentPartner(self, currentPartner):
        self._currentPartnerName = currentPartner
        return f"{self._name} is now partnered up with {self._currentPartnerName}..."
    def setPerfectMatch(self, perfectMatch):
        self._perfectMatchName = perfectMatch
        return f"{self._name}'s secret perfect match is {self._perfectMatchName}!"
    def trueLove(self):
        self._foundTrueLove = True
    def __str__(self):
        if self._foundTrueLove is True:
            return f"{self._name} has found true love with {self._perfectMatchName}, they are now living happily " \
                   f"forever after"
        elif self._currentPartnerName == self._perfectMatchName:
            return f"{self._name} is currently matched with their PERFECT match, but they do not know it yet!"
        else:
            return f"{self._name} is still in the search of true love. Are they destined for loneliness?"