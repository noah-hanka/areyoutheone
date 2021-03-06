from person import *
from matchmake import *
import time as time
class Gameshow:
    def __init__(self, contestants=None):
        self._currentWeek = 1
        if not contestants:
            contestants = ["John","Rebecca","Steve","Emili","Janette","Robert","Sarah","Ellie","Alex","Thomas","Melissa","Billie","Leah","Alberto","Matt","Jennifer"]
        if contestants and len(contestants) % 2 == 0:
            C = [Person(contestant) for contestant in contestants]
            self._mm = MatchMaker(C)
        self._prevTruthBooths = set()
        self._currWeeksTruthBooth = (None, None, None)
    def truthBooth(self):
        results = False
        truthBoothChoice = self._mm.pickRandomPerson()
        while (truthBoothChoice.getName(), truthBoothChoice.getCurrentPartnerName()) in self._prevTruthBooths or (truthBoothChoice.getCurrentPartnerName(), truthBoothChoice.getName()) in self._prevTruthBooths:
            truthBoothChoice = self._mm.pickRandomPerson()
        self._prevTruthBooths.add((truthBoothChoice.getCurrentPartnerName(),truthBoothChoice.getName()))
        if truthBoothChoice.getCurrentPartnerName() == truthBoothChoice.getPerfectMatchName():
            self._mm.removeCouple(truthBoothChoice)
            results = True
        return truthBoothChoice._name, truthBoothChoice.getCurrentPartnerName(), results
    def getCurrentWeek(self):
        return self._currentWeek
    def simulateWeek(self):
        scrambled = False
        while self._mm.determineIfScramble() is True:
            scrambled = True
            self._mm.matchMakeParticipants()
        if self._mm.everyoneMatched() is True:
            rem = self._mm._numRemainingParticipants
            self._mm._numConfirmedPerfectlyMatched += rem
            for person, partner in self._mm._GUIcurrentPartners.items():
                self._mm._GUIconfirmedPerfectlyMatched[person] = partner
            self._mm._GUIcurrentPartners = dict()
            return self.endGame(rem)
        else:
            p1_name, p2_name, result = self.truthBooth()
            self._currWeeksTruthBooth = (p1_name,p2_name,result)
            if result is True:
                response = "and they were perfect matches for each other!"
            else:
                response = "and unfortunately it turns out they were not perfect matches for each other..."
            response= f"lovely couple of {p1_name} and {p2_name} were sent to the TRUTH BOOTH\n{response}\n" \
                   f"There are currently {self._mm._numRemainingParticipants} partipants still left.\n" \
                   f"Will they all find true love?\n"
            if scrambled: response = f"\nAfter some mingling this week,\nthe {response}"
            else: response = f"\nThe {response}"
            return response

    def endGame(self,remainder):
        s = ""

        s += f"\nThe remaining {remainder} participants all happen to be with their perfect match!\nEveryone has found their true love!\n\nThese were everyones matches:\n" \
             f"{self._mm.printPerfectMatches()}"
        return s
    def runGame(self,print_results=False,pauseEachWeek=False):
        self._mm.assignPerfectMatches()
        while not (self._mm.everyoneMatched()):
            if print_results:
                print(f'Week: {self.getCurrentWeek()}')
                print(self.simulateWeek())
            else:
                self.simulateWeek()
            if pauseEachWeek:
                input("Press ENTER to proceed to the next week\n")
            self._currentWeek += 1

if __name__ == "__main__":
    AreYouTheOne = Gameshow()
    AreYouTheOne.runGame(True)

