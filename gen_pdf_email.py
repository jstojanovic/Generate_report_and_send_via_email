#!/usr/bin/env python3
import os
import json
import reports
import emails

with open('car_sales.json') as file:
    Cars = json.load(file)
    file.close()

most_sold = ['','','', 0]
most_revenue = ['','','',0]
pop_year = {}
table = [['ID','Car','Price', 'Total Sales']]
l = []
for car in Cars:
    for it in car:
        l.append(car[it])  
    manufacturer = l[1]['car_make']
    model = l[1]['car_model']
    year = l[1]['car_year']
    sold = l[3]
    Id = l[0]
    price = float(l[2][1:])
    revenue = price * sold
    
    if most_sold[3] < sold:
        most_sold = [manufacturer, model, year, sold]
    if float(most_revenue[3]) < revenue:
        most_revenue = [manufacturer, model, year, "%0.2f" % revenue]
    
    pop_year[year] = pop_year.setdefault(year, 0) + sold 
    table.append([Id, manufacturer+' '+model+' ('+str(year)+')','$'+"%0.2f" % price,str(sold)])
    l = []
reports.generate("/tmp/report.pdf", "Sales summary for last month", "The "+most_revenue[0]+" "+most_revenue[1]+" ("+str(most_revenue[2])+") generated the most revenue: $"+str(most_revenue[3])+"<br/>The "+most_sold[0]+' '+most_sold[1]+' ('+str(most_sold[2])+') had the most sales: '+str(most_sold[3])+'<br/>The most popular year was '+str(max(pop_year, key=pop_year.get))+' with '+str(pop_year[max(pop_year, key=pop_year.get)])+' sales.', table)

sender = "automation@example.com"
receiver = "{}@example.com".format(os.environ.get('USER'))
subject = "Sales summary for last month"

body = "The "+most_revenue[0]+" "+most_revenue[1]+" ("+str(most_revenue[2])+") generated the most revenue: $"+str(most_revenue[3])+"\nThe "+most_sold[0]+' '+most_sold[1]+' ('+str(most_sold[2])+') had the most sales: '+str(most_sold[3])+'\nThe most popular year was '+str(max(pop_year, key=pop_year.get))+' with '+str(pop_year[max(pop_year, key=pop_year.get)])+' sales.'

message = emails.generate(sender, receiver, subject, body, "/tmp/report.pdf")
emails.send(message)
