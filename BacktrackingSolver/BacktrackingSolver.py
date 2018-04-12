from enum import Enum

class FlightListing (object):
    def __init__(self, departure, arrival, distance):
        self.departure = departure
        self.arrival = arrival
        self.distance = distance
        self.seen = False

class FlightDatabase(object):
    listings = []
    def __init__(self):
        self.listings.append(FlightListing("New York", "Chicago", 1000))
        self.listings.append(FlightListing("Chicago", "Denver", 1000))
        self.listings.append(FlightListing("New York", "Toronto", 800))
        self.listings.append(FlightListing("New York", "Denver", 1900))
        self.listings.append(FlightListing("Toronto", "Calgary", 1500))
        self.listings.append(FlightListing("Toronto", "Los Angeles", 1800))
        self.listings.append(FlightListing("Toronto", "Chicago", 500))
        self.listings.append(FlightListing("Denver", "Urbana", 1000))
        self.listings.append(FlightListing("Denver", "Houston", 1500))
        self.listings.append(FlightListing("Houston", "Los Angeles", 1500))
        self.listings.append(FlightListing("Denver", "Los Angeles", 1000))

    def find(self, departure):
        return [listing  for listing in self.listings if (not listing.seen) and (listing.departure == departure)]

    def match(self, departure, arrival):
        for listing in self.listings:
            if (listing.departure == departure
                and listing.arrival == arrival):
                return listing
        return None

class TreeTraversalMode(Enum):
    DEPTH_FIRST = 1
    BREADTH_FIRST = 2

def findFlightRec(database, departure, arrival, stack, traversalMode):
    print("Checking for connection between: %s and %s" % (departure, arrival) )
    directConnection = database.match(departure, arrival)

    # Base Condition, if there exists a route between the two locations, add the route to the stack and return.
    if(directConnection != None):
        print("Connection found!")
        stack.append(directConnection)
        return

    # If no direct route exists, then find a possible connecting flight.
    nextPossibleFlights = database.find(departure)
    if(len(nextPossibleFlights) > 0):
        for flight in nextPossibleFlights:
            print("Connection between: %s and %s Found. Adding to stack." % ( flight.departure, flight.arrival ) )
        stack.extend(nextPossibleFlights)
        return findFlightRec(database, nextPossibleFlight.arrival, arrival, stack, traversalMode)

    # If no connecting flights exist, then backtrack to our last possible partial solution.
    elif( len(stack) > 0):
        print("No connections found. Backtracking...")
        if(traversalMode == TreeTraversalMode.DEPTH_FIRST):
            # popping from the end of the list (FIFO)
            backtrackFlight = stack.pop()
        else:
            # dequeue by popping from the front of the list (FILO)
            backtrackFlight = stack.pop(0)
        
        return findFlightRec(database, backtrackFlight.departure, arrival, stack, traversalMode)

if __name__ == "__main__":
    database = FlightDatabase()
    stack = []
    findFlightRec(database, "New York", "Los Angeles", stack, TreeTraversalMode.BREADTH_FIRST)
    if(len(stack) != 0):
        print("Flights Found:\r\n")
        distance = 0
        for flight in stack:
            print("%s -> %s" % (flight.departure, flight.arrival))
            distance += flight.distance
        print("\nTotal Distance: %d" % (distance))
    else:
        print('No Flights found')
