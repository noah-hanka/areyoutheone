import random as random
class MatchMaker:
    def __init__(self, participants):
        self._remainingParticipants = participants
        self._numRemainingParticipants = len(participants)
        self._truePerfectMatches = dict()
        self._currentPartners = dict()
        self._numPerfectMatchedActivePlayers = 0
        self._confirmedPerfectlyMatched = set()
        self._numConfirmedPerfectlyMatched = 0
        self._GUIconfirmedPerfectlyMatched = dict()
        self._GUIcurrentPartners = dict()
    def assignPerfectMatches(self):
        participantPool = self._remainingParticipants.copy()
        while participantPool:
            p1, p2 = random.sample(participantPool,2)
            participantPool.remove(p1)
            participantPool.remove(p2)
            self._truePerfectMatches[p1._name] = p2
            self._truePerfectMatches[p2._name] = p1
            p1.setPerfectMatch(p2._name)
            p2.setPerfectMatch(p1._name)
        return self._truePerfectMatches
    def printPerfectMatches(self):
        s = ""
        count = 1
        l = list(self._truePerfectMatches.items())
        for i in range(0,len(l),2):
            person, partner = l[i]
            s += f"{count}. {person} and {partner.getName()} love eachother\n"
            count += 1
        return s
    def matchMakeParticipants(self):
        participantPool = self._remainingParticipants.copy()
        self._numPerfectMatchedActivePlayers = 0
        print("Matchmaking participants...\n")
        self._GUIcurrentPartners = dict()
        while participantPool:
            p1, p2 = random.sample(participantPool,2)
            participantPool.remove(p1)
            participantPool.remove(p2)
            self._currentPartners[p1._name] = p2
            self._currentPartners[p2._name] = p1

            #FOR GUI
            self._GUIcurrentPartners[p1._name] = p2._name

            p1.setCurrentPartner(p2._name)
            p2.setCurrentPartner(p1._name)
        for person in self._currentPartners.values():
            if person.getCurrentPartnerName() == person.getPerfectMatchName():
                self._numPerfectMatchedActivePlayers += 1
        return self._currentPartners
    def pickRandomPerson(self):
        return random.choice(self._remainingParticipants)
    def everyoneMatched(self):
        return self._numRemainingParticipants == self._numPerfectMatchedActivePlayers
    def determineIfScramble(self):
        averageNumOfActivePerfectMatches = (self._numRemainingParticipants / 2) / (self._numRemainingParticipants - 1)
        if (self._numPerfectMatchedActivePlayers / 2) < averageNumOfActivePerfectMatches:
            return True
        else:
            return False
    def removeCouple(self,person):
        partner = self._truePerfectMatches[person.getName()]
        self._numConfirmedPerfectlyMatched += 2
        self._numPerfectMatchedActivePlayers -= 2
        self._numRemainingParticipants -= 2
        self._confirmedPerfectlyMatched.add(person)
        self._confirmedPerfectlyMatched.add(partner)

        #For GUI
        self._GUIconfirmedPerfectlyMatched[person.getName()] = partner.getName()
        if person.getName() in self._GUIcurrentPartners:
            self._GUIcurrentPartners.pop(person.getName())
        else:
            self._GUIcurrentPartners.pop(person._perfectMatchName)
        #------------------------------------------------------------------------

        self._remainingParticipants.remove(person)
        self._remainingParticipants.remove(partner)
        self._currentPartners.pop(person._name)
        self._currentPartners.pop(partner._name)
        person.trueLove()
        partner.trueLove()