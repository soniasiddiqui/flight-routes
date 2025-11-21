# File: Flights.py
# Student: Sonia Siddiqui
# UT EID: sas9583
# Course Name: CS303E
# Description of Program:
# This program takes information in a file about flights between a number of
# cities, stores the information into a useful form, and permits the user to
# ask various questions about the information.

import os.path

class Flights:

    def __init__(self):
        # Accept from the user the name of a file containing the data.
        # If no file of that name exists, print an error message and quit.
        f1 = input("Enter the name of a file: ")
        if not os.path.isfile(f1):
            print("File does not exist")
            return

        self.__cityNames = []
        self.__flightInfo = {}

        infile = open(f1, "r")

        # Splitting first line, stripping extra space, and assigning each element to list attribute
        cityNames = infile.readline().strip()
        self.__cityNames = cityNames.split(", ")

        # Initialize flight dictionary
        self.__flightInfo = {city: [] for city in self.__cityNames}

        # Read rest of lines for flight info
        for line in infile:
            elements = line.strip().split(", ")
            cityA = elements[0].strip()
            cityB = elements[1].strip()
            price = int(elements[2].strip())

            self.__flightInfo[cityA].append((cityB, price))
            self.__flightInfo[cityB].append((cityA, price))

        infile.close()


    def getCities(self):
        return self.__cityNames


    def getFlights(self):
        return self.__flightInfo


    def __str__(self):
        result = "Cities: " + str(self.__cityNames) + "\nFlights:\n"
        for city, flights in self.__flightInfo.items():
            result += " ('{}', {})\n".format(city, flights)
        return result


    def getNeighboringCities(self, city):
        if city not in self.__cityNames:
            print("City", city, "not found")
        else:
            neighboringCities = set()
            for destination, _ in self.__flightInfo.get(city, []):
                neighboringCities.add(destination)
            return neighboringCities


    def getRoute(self, startCity, endCity):
        # add startCity to the set of cities visited
        visitedCities = set()
        return self.getRouteHelper(startCity, endCity, visitedCities)


    def getRouteHelper(self, startCity, endCity, visitedCities):
        if startCity not in self.__cityNames or endCity not in self.__cityNames:
            print("City", startCity if startCity not in self.__cityNames else endCity, "not found")
            return []

        elif startCity == endCity:
            return [startCity]

        visitedCities.add(startCity)

        if startCity in self.__flightInfo:
            for cityB, _ in self.__flightInfo[startCity]:
                if cityB not in visitedCities:
                    # recursively find a route from cityB to endCity
                    route_from_cityB = self.getRouteHelper(cityB, endCity, visitedCities)
                    if route_from_cityB:
                        # add startCity to the front of the route
                        return [startCity] + route_from_cityB

        return []


    def getRoutePrice(self, route):
        if not route:
            return -1

        total_price = 0
        for i in range(len(route) - 1):
            city_now = route[i]
            city_next = route[i + 1]
            for destination, price in self.__flightInfo[city_now]:
                if destination == city_next:
                    total_price += price
                    break

        return total_price


    def getPrice(self, cityA, cityB):
        if cityA not in self.__cityNames or cityB not in self.__cityNames:
            print("City", cityA if cityA not in self.__cityNames else cityB, "not found")
            return -1

        route = self.getRoute(cityA, cityB)
        return self.getRoutePrice(route)

if __name__ == "__main__":
    flights = Flights()   # creates the object and loads the file

    # Print something so you can see output
    print("\nLoaded cities:")
    print(flights.getCities())

    print("\nFlight connections:")
    print(flights.getFlights())

    # Try a sample route (optional)
    print("\nExample route from New York to Dallas:")
    route = flights.getRoute("New York", "Dallas")
    print("Route:", route)
    print("Route price:", flights.getRoutePrice(route))