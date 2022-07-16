import csv
import glob
import re
from django.core.management.base import BaseCommand
from movies.models import MovieMetaModel
from movies.enums import GENRES_INV, MONTH_NAMES

# Because Heroku commands are run from the root folder, we need to specify the full
# path. This also means this command must be run from the root package.
dataFolder = "backend/movies/populatordata/"

def strToBool(str):
    if str == "y":
        return True
        
    elif str == "n":
        return False

    return None

# converts Strings of the form "17-Dec-21" to YYYY-MM-DD format
def convertDate(input):
    splitInput = input.split("-")

    day = splitInput[0]
    month = MONTH_NAMES.get(splitInput[1])
    year = "20" + splitInput[2]

    return year + "-" + month + "-" + day

# Run with:  python .\manage.py populator --year 2021
# https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/
class Command(BaseCommand):
    help = 'Populates the DB with movie data'

    def add_arguments(self, parser):
        parser.add_argument('--year', action='append', help='specifies the year to populate. Leave blank to update all years')

    def handle(self, *args, **options):
        filenames = []
        years = options['year']
        
        # If we passed in a list of years, only read those file
        if (years is not None and len(years) > 0):
            for year in years:
                filenames.append(dataFolder + year + ".csv")
            self.stdout.write("Attempting to load files: " + ' '.join(years))

        # Otherwise read every csv file in the directory
        else:
            filenames = glob.glob(dataFolder + "*.csv")
            self.stdout.write("Attempting to load all files")

        for filename in filenames:
            self.stdout.write("loading file: [" + filename + "].")
            with open(filename) as f:
                reader = csv.reader(f)
                totalRows = 0
                totalCreated = 0
                for row in reader:
                    _, created = MovieMetaModel.objects.get_or_create(
                            title=row[0],
                            releaseDate=convertDate(row[1]),  
                            genre=GENRES_INV.get(row[2]),
                            gross=re.sub(r'[^\d.]+', '', row[3]),  # Remove all non numericals or '.'
                            bechdelResult=strToBool(row[4])
                    )
                    totalRows += 1
                    if created: totalCreated += 1
            
                self.stdout.write("loaded succeeded: {totalCreated}/{totalRows} rows were new entries.".format(totalCreated=totalCreated, totalRows=totalRows))
        self.stdout.write("I love you! Bye!")