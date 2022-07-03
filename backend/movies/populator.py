#!/usr/bin/python

import sys
import csv
import glob
from models import MovieMetaModel

# This script can be run to populate movie data from my downloaded CSV files
def main():
    filenames = []

    if (len(sys.argv) > 2):
        print("only one or no args allowed ya bimbo")
        sys.exit(0)
    
    # If we passed in the year, only read that file
    elif (len(sys.argv) == 2):
        filenames.append(sys.argv[1] + ".csv")

    # Otherwise read every csv file in the directory
    else:
        filenames = glob.glob("*.csv")

    for filename in filenames:
        with open(filename) as f:
            reader = csv.reader(f)
            totalRows = 0
            totalCreated = 0
            for row in reader:
                _, created = MovieMetaModel.objects.get_or_create(
                        title=row[0],
                        releaseDate=row[1],
                        genre=row[2],
                        gross=row[3],
                        bechdelResult=row[4]
                )
                totalRows += 1
                if created: totalCreated += 1
        
            print("loaded file: [" + filename + "]. " + totalCreated + "/" + totalRows + " rows were new entries.")
    print("I love you! Bye!")


if __name__ == "__main__":
    main()