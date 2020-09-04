import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fordisproject.settings")
django.setup()

#from firstapp.models import Seouldata

# CSV_PATH = '../Seouldataset2.csv'

#with open(CSV_PATH, newline='') as csvfile:
#    data_reader = csv.DictReader(csvfile)
 #   for row in data_reader:
  #      print(row)
   #     Seouldata.objects.create(
    #        sisulname = row['sisulname'],
     #       sisuladdr = row['sisuladdr'],
      #      tel = row['tel'],
       # )

from firstapp.models import Datalist

CSV_PATH = '../alldata.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        print(row)
        Datalist.objects.create(
            name = row['sisulname'],
            addr = row['sisuladdr'],
            tel = row['tel'],
            kind=row['kind'],
            lat = row['lat'],
            lng = row['lng'],
      )

