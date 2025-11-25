
import csv


def trainType(number):
    car = str(number).upper()
    try:
        if car.endswith("M"):
            car = car.rstrip(car[-1])
            try:
                car = int(car)
            except:
                return(f"Train type not found for {number}")
            # steamrail tait
            if car == 317 or car == 327 or car == 381 or car == 470:
                return "Tait"
            elif car >= 9001 and int(car) <= 9070 or int(car) >= 9101 and int(car) <= 9170 or int(car) >= 9201 and int(car) <= 9270 or int(car) >= 9301 and int(car) <= 9370 or int(car) >= 9701 and int(car) <= 9770 or int(car) >= 9801 and int(car) <= 9870 or int(car) >= 9901 and int(car) <= 9970:
                return "HCMT"
            elif car >= 561 and car <= 680:
                return "Alstom Comeng"
            elif car >= 301 and car <= 468:
                return "EDI Comeng"
            elif car >= 471 and car <= 554:
                return "EDI Comeng"
            if car >= 1 and car <= 288:
                return "X'Trapolis 100"
            if car >= 851 and car <= 986:
                return "X'Trapolis 100"
            if car >= 701 and car <= 844:
                return "Siemens Nexas"
            else:
                return(f"Train type not found for {number}")
        elif car.endswith("T"):
    
            car = car.rstrip(car[-1])
            try:
                car = int(car)
            except:
                return(f"Train type not found for {number}")
            # steamrail tait
            if car == 208 or car == 341:
                return "Tait"
            elif car >= 1131 and car <= 1190:
                return "Alstom Comeng"
            elif car >= 1001 and car <= 1084:
                return "EDI Comeng"
            elif car >= 1086 and car <= 1127:
                return "EDI Comeng"
            if car >= 1301 and car <= 1444:
                return "X'Trapolis 100"
            if car >= 1626 and car <= 1693:
                return "X'Trapolis 100"
            if car >= 851 and car <= 986:
                return "X'Trapolis100"
            if car >= 2501 and car <= 2572:
                return "Siemens Nexas"
            else:
                return(f"Train type not found for {number}")
            
        if car.startswith("N"):
            car = car.lstrip("N")
            try:
                car = int(car)
            except:
                return f"Train type not found for {number}"
            if 451 <= car <= 475:
                return "N Class"

            if car >= 451 and car <= 475:
                return "N Class"
            else:
                return(f"Train type not found for {number}")
            
        if car.startswith("K"):
            return("K Class")
        
        if car.startswith("Y"):
            return("Y Class")
        if car.startswith("T") and int(car[1:]) >= 320 and int(car[1:]) <= 413:
            return("T Class")
        if car.startswith("S"):
            number = int(car[1:])
            # Check if the number is between 300 and 317
            if 300 <= number <= 317:
                return("S Class (Diesel)")
        
        if car in ['IEV100', 'IEV102', 'EV120']:
            return 'Infrastructure evaluation vehicle'
        
        if car.startswith("TRAIN"):
            return("Error: TrainID sent")
            
        if int(car) >= 9001 and int(car) <= 9070 or int(car) >= 9101 and int(car) <= 9170 or int(car) >= 9201 and int(car) <= 9270 or int(car) >= 9301 and int(car) <= 9370 or int(car) >= 9701 and int(car) <= 9770 or int(car) >= 9801 and int(car) <= 9870 or int(car) >= 9901 and int(car) <= 9970:
            return "HCMT"
        if int(car) >= 8301 and int(car) <= 8325 or int(car) >= 8401 and int(car) <= 8425 or int(car) >= 8101 and int(car) <= 8125 or int(car) >= 8601 and int(car) <= 8625 or int(car) >= 8201 and int(car) <= 8225 or int(car) >= 8501 and int(car) <= 8525:
            return "X'Trapolis 2.0"
        if (1100 <= int(car) <= 1228) or (1230 <= int(car) <= 1328) or (1330 <= int(car) <= 1392) or (int(car) == 1399) or (1593 <= int(car) <= 1598) or (2100 <= int(car) <= 2132) or (2134 <= int(car) <= 2141) or (2200 <= int(car) <= 2232) or (2234 <= int(car) <= 2241) or (2300 <= int(car) <= 2332) or (2334 <= int(car) <= 2341):
            return "VLocity"
        if (7001 <= int(car) <= 7022):
            return "Sprinter"
        
        
        else:
            return(f"Train type not found for {number}")
    
    except Exception as e:
        print(f"Error: {e}")
        
# trams
def tramType(number):
    try:
        car = int(number)
    except:
        return(f"Tram type not found for {number}")
    
    if car >= 116 and car <= 230:
        return('Z-Class')
    elif car >= 231 and car <= 300:
        return('A-Class')
    elif car >= 2003 and car <= 2132:
        return('B-Class')
    elif car >= 3001 and car <= 3036:
        return('C1-Class')
    elif car >= 3501 and car <= 3538:
        return('D1-Class')
    elif car >= 5001 and car <= 5021:
        return('D2-Class')
    elif car in [5103, 5106, 5111, 5113, 5123]:
        return('C2-Class')
    elif car >= 6001 and car <= 6050:
        return('E1-Class')
    elif car in [856, 888, 925, 928, 946, 957, 959, 961, 981, 983, 1000, 1010]:
        return('W8-Class')
    elif car >= 6051 and car <= 6100:
        return('E2-Class')
    else:
        print(f"Tram type not found for {number}")
        return(None)
    
    
# Convert PTV Run ID to TDN
def RunIDtoTDN(runID):
        aski1 = runID[1]
        aski2 = runID[2]
        letter = chr(int(str(aski1) + str(aski2)))
        final = letter + runID[3:]
        return(final)

# Convert TDN to PTV Run ID
def TDNtoRunID(tdn):
    aski = ord(tdn[0])
    aski1 = str(aski)[0]
    aski2 = str(aski)[1]
    final = aski1 + aski2 + tdn[1:]
    return(final)

async def cleanAPITrainNumber(number:str):
    """
    This function will clean up the train number if its a hcmt and also it will return the train type better than the api provides such as differentitating between EDI and Alstom Comengs.
    """
    if "-" in str(number):
        cars = number.split("-")
        split = []
        for car in cars:
            split.append(car)
            Type = trainType(car)        

        for carriage in split:
            print(f'splitted carriage: {carriage}')
            if len(carriage) == 5 and carriage.endswith("M"): # filter HCMT carriages
                car = carriage[:-1]
                Type = "HCMT"
                return Type, car
            else:
                return Type, number
                
    return '', '' # if no type is found return None

def sydneyTrainType(setNumber):
    # figure out the train type
        if setNumber.startswith('AM'):
            trainType = 'Alstom Metropolis'
        elif setNumber.startswith('A'):
            trainType = 'Waratah A set'
        elif setNumber.startswith('B'):
            trainType = 'Waratah B set'
        elif setNumber.startswith('H'):
            trainType = 'OSCar'
        elif setNumber.startswith('J'):
            trainType = 'Hunter'
        elif setNumber.startswith('K'):
            trainType = 'K Set'
        elif setNumber.startswith('M'):
            trainType = 'Millenium'
        elif setNumber.startswith('N'):
            trainType = 'Endeavour'
        elif setNumber.startswith('T'):
            trainType = 'Tangara'
        elif setNumber.startswith('V'):
            trainType = 'V Set'
        elif setNumber.startswith('XP'):
            trainType = 'XPT'    
        elif setNumber.startswith('P'):
            trainType = 'Xplorer'
        elif int(setNumber) >= 4801 and int(setNumber) <= 4863 or int(setNumber) >= 4865 and int(setNumber) <= 48165 or int(setNumber) >= 48208 and int(setNumber) <= 48209 or int(setNumber)== 48216:
            trainType = '48 Class'
        
        else:
            trainType = 'Unknown'
            
        return trainType
        
def getSydneySetNumber(number):
    with open('utils/datalists/nsw-trains.csv', 'r') as file:
        csv_reader = csv.reader(file)
        train_info = None
        for row in csv_reader:
            if row[0] == number:
                train_info = {
                    'Set Number': row[0],
                    'Carriages': row[1],
                    'Status': row[2],
                    'Livery': row[3],
                    'Note': row[4],
                    'Operator': row[5],
                    'EnteredService': row[6],
                    'Gauge': row[7],
                }
        if not train_info:
            train_info = None
            file.seek(0)
            for row in csv_reader:
                carriages = row[1].split('-')
                if number in carriages:
                    train_info = {
                        'Set Number': row[0],
                        'Carriages': row[1],
                    }
                    break
            if not train_info:
                return None
            else:
                return train_info['Set Number']