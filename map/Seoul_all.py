import csv

Seoul_all = []
rownum = 0
rownum_acc = 0
rownum_food = 0
rownum_tour = 0

with open("Seoul_School.csv", 'r', encoding ="utf-8") as s_school:
    seoul_school_data = csv.reader(s_school)
    for row in seoul_school_data:
        washroom = row[11]
        if washroom.find("Y")!=-1:
            Seoul_all.append(row)
        rownum += 1

with open("Seoul_acc.csv", "r", encoding="utf-8") as s_acc:
    seoul_acc_data = csv.reader(s_acc)
    for row_acc in seoul_acc_data:
        washroom1 = row_acc[9]
        if washroom1.find("Y") != -1:
            Seoul_all.append(row_acc)
        rownum_acc += 1

with open("Seoul_food.csv", "r", encoding="utf-8") as s_food:
    seoul_food_data = csv.reader(s_food)
    for row_food in seoul_food_data:
        washroom2 = row_food[9]
        if washroom2.find("Y") != -1:
            Seoul_all.append(row_food)
        rownum_food += 1


with open("Seoul_tour.csv", "r", encoding="utf-8") as s_tour:
    seoul_tour_data = csv.reader(s_tour)
    for row_tour in seoul_tour_data:
        washroom3 = row_tour[9]
        if washroom3.find("Y") != -1:
            Seoul_all.append(row_tour)
        rownum_tour += 1


with open("Seoul_all.csv", "w", encoding="utf8") as s_s_n:
    writer = csv.writer(s_s_n, delimiter=',')
    for row in Seoul_all:
        mynewrow = row[1:2] + row[3:5]
        writer.writerow(mynewrow)


