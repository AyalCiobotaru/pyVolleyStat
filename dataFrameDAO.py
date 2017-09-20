import pandas as pd

Stats = None

def getDataFrame(name):
    global Stats
    Stats = pd.read_pickle('Database/' + name + '.pickle')

def addOneStatDAO(level, sublevel, player):
    global Stats
    def addOne(x):
        """
        Returns 1 if x is np.NaN else x + 1
        """
        return 1 if pd.isnull(x) else x + 1
    Stats.set_value(player , (level, sublevel), addOne(Stats[level][sublevel][player]))

def printDataframe():
    global Stats
    print(Stats)

def applyFormulas():
    """
    Applies the hitting percentage formula and reception formula
    as well as reception total formulas
    """
    global Stats

    # Applies Hitting percentage
    hittingPercentage = (Stats['Attack']['Kill'] - Stats['Attack']['Err']) / Stats['Attack']['Att']
    Stats['Attack', 'Hit%'] = hittingPercentage

    receptionTotal = Stats['Reception']['0'] + Stats['Reception']['1'] + Stats['Reception']['2'] + Stats['Reception']['3']
    Stats['Reception', 'Tot'] = receptionTotal

    # Applies Passing numbers
    receptionAvg = (Stats['Reception']['1'] + Stats['Reception']['2']*2 + Stats['Reception']['3']*3) / Stats['Reception']['Tot']
    Stats['Reception', 'Avg'] = receptionAvg

    Stats = Stats.round(3)

def saveData(name):
    global Stats
    Stats.to_pickle('Database/' + name + '.pickle')
    Stats.to_csv('Database/' + name + '.csv')
