import re
import pandas as pd
from django.core.management.base import BaseCommand
from movies.models import MovieMetaModel
from movies.enums import GENRES_INV, MONTH_NAMES

# Because Heroku commands are run from the root folder, we need to specify the full
# path to the file. This also means this command must be run from the root package.
FILE_TO_READ = "backend/movies/populatordata/BechdelData.xlsx"


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


def convertImage(filename):
    return "posters/default.jpg" if pd.isna(filename) else "posters/" + filename + ".jpg"


# Run with:  python \backend\manage.py populator --year 2021 --force True
# https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/
class Command(BaseCommand):
    help = 'Populates the DB with movie data'

    def add_arguments(self, parser):
        parser.add_argument('--year', action='append', help='specifies the year to populate. Leave blank to update all years')
        parser.add_argument('--force', help='If specified will hard upsert all data, even if it already exists')
        parser.add_argument('--truncate', help='If specified will truncate all existing data. For testing purposes only!')

    def handle(self, *args, **options):
        years = options['year']
        shouldForce = options['force'] if options['force'] is not None else False
        shouldTruncate = options['truncate'] if options['force'] is not None else False

        # Read in all the Excel file sheets. If years is None, will read in everything
        sheets = pd.read_excel(FILE_TO_READ, sheet_name=years)
        
        # Loop all the sheets
        for sheetName, df in sheets.items():
            totalRows = 0
            totalCreated = 0
            totalModified = 0

            # A quirk of pandas. We replace all "NaN" (ie empty) elements with python None
            # df = df.replace({np.nan:None})

            # Truncate the data for the year (sheetName==year)
            if shouldTruncate:
                MovieMetaModel.objects.filter(releaseDate__year=sheetName).delete()

            for _, row in df.iterrows():
                title = row['Movie Title']
                releaseDate = row['Release Date'] #convertDate(row['Release Date'])
                genre = GENRES_INV.get(row['Genre'])
                gross = re.sub(r'[^\d.]+', '', str(row['Gross']))  # Remove all non numericals or '.' Returns a list so fetch the first element
                bechdelResult = strToBool(row['Does It Pass?'])
                image = convertImage(row['File Name'])

                # If we're forcing the update
                if (shouldForce):
                    _, created = MovieMetaModel.objects.update_or_create(
                        title=title,
                        defaults={
                            'releaseDate': releaseDate,
                            'genre': genre,
                            'gross': gross,
                            'image': image,
                            'bechdelResult': bechdelResult
                        },
                    )
                    if created:
                        totalCreated += 1
                    else:
                        totalModified += 1

                # Else we only create if the row DNE in the DB
                else:
                    _, created = MovieMetaModel.objects.get_or_create(
                            title=title,
                            releaseDate=releaseDate,  
                            genre=genre,
                            gross=gross,
                            image=image,
                            bechdelResult=bechdelResult
                    )
                    if created:
                        totalCreated += 1

                totalRows += 1

            self.stdout.write("loaded {sheetName} successfully: Total rows - {totalRows}, Updated - {totalModified}, Created - {totalCreated}".format(sheetName=sheetName, totalRows=totalRows, totalModified=totalModified, totalCreated=totalCreated))
        
        self.stdout.write("Terminating script. Bye, I love you!")