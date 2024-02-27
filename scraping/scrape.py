# import xml.etree.ElementTree as ET
#
# tree = ET.parse('RS_Via-3.xml')
# root = tree.getroot()
# some_names = root.find('PricedItineraries').findall('Flights')
# i = 0
# for some_name in some_names:
#     flights_onward = some_name.find('OnwardPricedItinerary').find('Flights').findall('Flight')
#     flights_return = some_name.find('ReturnPricedItinerary').find('Flights').findall('Flight')
#     print('Itinerary No: ', i, '\n')
#     for flight_onward in flights_onward:
#         print("Flight No: ", flight_onward.find('FlightNumber').text, 'Onward')
#         print("Company: ", flight_onward.find('Carrier').text)
#         print("Destination from: ", flight_onward.find('Source').text)
#         print("Destination to: ", flight_onward.find('Destination').text)
#         print("Departure time:", flight_onward.find('DepartureTimeStamp').text)
#         print("Arrival time:", flight_onward.find('ArrivalTimeStamp').text)
#         print()
#     for flight_return in flights_return:
#         print("Flight No: ", flight_return.find('FlightNumber').text, 'Return')
#         print("Company: ", flight_return.find('Carrier').text)
#         print("Destination from: ", flight_return.find('Source').text)
#         print("Destination to: ", flight_return.find('Destination').text)
#         print("Departure time:", flight_return.find('DepartureTimeStamp').text)
#         print("Arrival time:", flight_return.find('ArrivalTimeStamp').text)
#         print()
#     print('\n\n')
#
#     i += 1


import xml.etree.ElementTree as ET
import pandas

tree = ET.parse('scraping/RS_Via-3.xml')
root = tree.getroot()
some_names = root.find('PricedItineraries').findall('Flights')

flight_numbers = []
companies = []
destinations_from = []
destinations_to = []

departure_time = []
arrival_time = []

onward_or_return = []
ticket_type = []
classes = []

currency = []
base_fare = []
airline_taxes = []
total_amount = []

for some_name in some_names:
    flights_onward = some_name.find('OnwardPricedItinerary').find('Flights').findall('Flight')
    flights_return = some_name.find('ReturnPricedItinerary').find('Flights').findall('Flight')

    pricing = some_name.find('Pricing')
    i = 0

    for flight_onward in flights_onward:
        onward_or_return.append('Onward')
        flight_numbers.append(flight_onward.find('FlightNumber').text)

        companies.append(flight_onward.find('Carrier').text)
        destinations_from.append(flight_onward.find('Source').text)
        destinations_to.append(flight_onward.find('Destination').text)

        departure_time.append(flight_onward.find('DepartureTimeStamp').text)
        arrival_time.append(flight_onward.find('ArrivalTimeStamp').text)

        ticket_type.append(flight_onward.find('TicketType').text)
        classes.append(flight_onward.find('Class').text)
        i += 1

    for flight_return in flights_return:
        onward_or_return.append('Return')
        flight_numbers.append(flight_return.find('FlightNumber').text)

        companies.append(flight_return.find('Carrier').text)
        destinations_from.append(flight_return.find('Source').text)
        destinations_to.append(flight_return.find('Destination').text)

        departure_time.append(flight_return.find('DepartureTimeStamp').text)
        arrival_time.append(flight_return.find('ArrivalTimeStamp').text)
        ticket_type.append(flight_return.find('TicketType').text)
        classes.append(flight_return.find('Class').text)
        i += 1

    for j in range(i):
        currency.append(pricing.attrib.get('currency'))
        base_fare.append(float(pricing.find("./ServiceCharges[@ChargeType='BaseFare']").text))
        airline_taxes.append(float(pricing.find("./ServiceCharges[@ChargeType='AirlineTaxes']").text))
        total_amount.append(float(pricing.find("./ServiceCharges[@ChargeType='TotalAmount']").text))


df = pandas.DataFrame({"Flight Number": flight_numbers, 'Onward/Return': onward_or_return, 'Companies': companies,
                       "Destination From": destinations_from, 'Destination to': destinations_to,
                       "Departure time": departure_time, 'Arrival Time': arrival_time,
                       'Ticket Type': ticket_type, "Class": classes, 'Currency': currency,
                       "Base Fare": base_fare, 'Airline Taxes': airline_taxes, 'Total Amount': total_amount
                       }
                      )


df.to_csv('scraping/flightsRS_Via_3.csv')
df.to_excel('scraping/flightsRS_Via_3.xlsx')
