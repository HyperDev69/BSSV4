import csv

class Characters:
    def getCharacterByName(self, name):
        
        brawler = None
        with open('Files/Assets/characters.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) 
            next(csv_reader)
            for count, row in enumerate(csv_reader, start=0):
                if row[0] == name:
                    return count
    def getBrawlers(self):
        BrawlersID = []
        with open('Files/Assets/characters.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:

                if line_count == 0 or line_count == 1:
                    line_count += 1
                else:
                    if row[18] == 'Hero' and row[1].lower() != 'true':
                        BrawlersID.append(line_count - 2)
                    line_count += 1

            return BrawlersID

    
