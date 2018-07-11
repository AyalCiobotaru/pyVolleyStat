
class lastAction(object):
    def __init__(self, level, sublevel, player):
        self.level = level
        self.sublevel = sublevel
        self.player = player

        if self.level == "initial":
            self.message = "Awaiting Player Select"
        else:
            self.message = self.player

        if self.level == "Attack":
            if self.sublevel == "Att":
                self.message += " got an attempt"
            elif self.sublevel == "Kill":
                self.message += " got a kill"
            else:
                self.message += " got a hitting error"
        elif self.level == "Serve":
            if self.sublevel == "Tot":
                self.message += " served the ball in"
            elif self.sublevel == "Ace":
                self.message += " got an ace"
            else:
                self.message += " got a service error"
        elif self.level == "Dig":
            self.message += " got a dig"
        elif level == "Block":
            if sublevel == "Err":
                self.message += " got tooled"
            else:
                self.message += " got a block"
        else: # Reception
            if self.sublevel == "0":
                self.message += " got aced"
            if self.sublevel == "1":
                self.message += " passed a 1"
            if self.sublevel == "2":
                self.message += " passed a 2"
            if self.sublevel == "3":
                self.message += " passed a 3"
        self.removeMessage = "%s's %s stat was removed" % (player, level)

    def getMessage(self):
        return self.message

    def getPlayer(self):
        return self.player

    def getLevel(self):
        return self.level

    def getSublevel(self):
        return self.sublevel

    def getRemoveMessage(self):
        return self.removeMessage
