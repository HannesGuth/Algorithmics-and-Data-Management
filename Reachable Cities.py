def getData():
    '''
    This function puts an SQL query to retrieve all necessary data from the database, here the city name, the country, the province, the longitude, the latitude, the river, the lake and the sea.
    It processes the incoming data such that all Null values will be replaced by "XXX", so it can be processed easier in the upcoming steps.
    Precondition: No data existed and other steps have been carried out before since this is the first step. It does not take any input values.
    Postcondition: The necessary data for all cities exists in a list of lists. Missing values, here Null values, are replaced by "XXX".
    :return: All necessary data as a list of lists with all Null values replaced by "XXX"
    '''
    from urllib.request import urlopen # import urlopen
    from urllib.parse import quote, urlencode # import quote
    q = "SELECT City.Name, City.Country, City.Province, City.Longitude, City.Latitude, located.River, located.Lake, located.Sea FROM City JOIN Country ON Country.Code = City.Country JOIN located ON located.City = City.Name ORDER BY City.Name" # put the query to select all necessary data, order it by City.Name to always get the same order
    eq = quote(q) # quote the previously created SQL query
    url = "http://kr.unige.ch/phpmyadmin/query.php?db=mondial&sql="+eq # combine the url from the database with the SQL query
    query_results = urlopen(url) # open the URL
    # iterate over the result rows
    data = list() # create an empty list (the list in which all entries will be saved later on)
    for line in query_results : # go through every line in the query result
        string_line = line.decode('utf-8').rstrip() # decode it using utf-8
        # if the query had a syntax error or if the result is empty
        # there is nevertheless one empty line, ignore it
        if len(string_line) > 0: # if the string is not empty
            # put the column values in columns
            liste = list() # create a new list for the current line in the query
            for i in range(8): # go through every element of the current line
                try: # try
                    if(string_line.split("\t")[i] != ""): # if the split is not empty (not a Null value)
                        liste.append(string_line.split("\t")[i]) # append this element to the newly created list "liste"
                    else: # if it is empty (Null value)
                        liste.append("XXX") # set it to "XXX"
                except: # except (Null value)
                    liste.append("XXX") # append "XXX"
            data.append(liste) # append the entry to the data variable

    return data # return all the data in an ordered way

def neighborhood(data, d, s):
    '''
    This function creates a kind of distance matrix for every city to any other city. At this stage, it will only be stated if 2 cities are neighbors (entry 1) or not (entry 1000)
    Two cities are neighbors when:
        - they are in the same province
        - they are adjacent to the same lake
        - they are adjacent to the same river
        - they are adjacent to the same sea and have distance less than s
        - they generally have a distance less than d without having anything else in common
    Precondition: The data retrieved from the query without knowing which cities are regarded as neighbors
    Postcondition: Knowledge about which cities are regarded as neighbors
    :param data: The blank information retrieved from the database in an ordered way and with "XXX" instead of Null values
    :param d: The distance two cities may have at maximum to be neighbors without having anything else in common
    :param s: The distance two cities may have at maxmimum to be neighbors when they only have the sea in common
    :return: The matrix of cities indicating if they are neighbors
    '''
    import numpy as np # import numpy as np
    neighbors = np.full((int(len(data)),int(len(data))), 1000) # create a numpy array with all entries equal to 1000, assuming that there are no neighbors. This will be checked and corrected for every combination of cities in the following

    for i in range(int(len(data))): # go through every line of the array
        for j in range(int(len(data))): # go through every column of the array
            dist = 100000 # set the initial variable dist to 100000
            sea = False # set sea for every combination initially to False
            if data[i][4] != "XXX" and data[i][3] != "XXX" and data[j][4] != "XXX" and data[j][3] != "XXX": # if none of the longitude and latitude data are "XXX" CHANGE
                try: # try (just to be very sure)
                    dist = abs(float(data[i][4]) - float(data[j][4])) + abs(float(data[i][3]) - float(data[j][3])) # calculate the manhattan distance
                except: # if an error is thrown
                    dist = 100000 # set dist to 100000
            province = data[i][2] == data[j][2] and data[i][2] != "XXX" # if both cities have the same province and neither is "XXX", set province to True
            river = data[i][5] == data[j][5] and data[i][5] != "XXX" # if both cities have the same river and neither is "XXX", set river to True
            lake = data[i][6] == data[j][6] and data[i][6] != "XXX" # if both cities have the same lake and neither is "XXX", set lake to True
            if dist < s: # if dist < s
                sea = data[i][7] == data[j][7] and data[i][7] != "XXX" # if both cities have the same sea and neither is "XXX", set sea to True
            if dist < d: # if dist < d
                distance = True # set distance to True
            else: # if dist >= d
                distance = False # set distance to False

            if province or lake or sea or river or distance: # if any of the neighborhood criteria for this combination of cities is fulfilled,
                neighbors[i][j] = 1 # replace 1000 by 1 for this combination
                if i == j: # except if i == j, then the cities are the same city
                    neighbors[i][j] = 0 # then the neighborhood distance is set to 0 for this combination
    # np.savetxt("neighbors.csv", neighbors, delimiter=",") # potentially save the neighbors matrix (initial matrix/array to start the Belman-Ford algorithm with)
    return(neighbors) # return the neighborhood matrix

def bellman_ford_algorithm(neighbors):
    '''
    This function uses the Bellman-Ford algorithm to find the shortest path from any city to any other city.
    "Short" refers to the distance of two cities, here the number of steps for getting there.
    Precondition: Knowledge which cities are direct neighbors
    Postcondition: Knowledge how many steps need to be done for getting from any city to any other
    :param neighbors: It takes the information which cities are neighbours as input.
    :return: The matrix that tells how many steps to take to get fom any city to any other city
    '''
    import numpy as np # import numpy as np
    U1 = neighbors # set U1 to the neighbors to the np array containing information about the neighbourhood of two cities
    length = int(len(U1)) # set length to the number of rows in U1
    U1 = np.array(U1) # convert U1 to a numpy array
    vector = [0] * int(length) # set a vector of length "length" and 0s for all entries (needed for the algorithm to work)
    vector = np.array(vector) # make this vector a numpy array
    U1new = np.array(U1) # copy U1 and create U1new
    U1compare = np.array(U1) # copy U1 and create U1compare
    stp = False # set the stop variable stp to False
    counter = 0 # set counter to 0

    while not stp: # the stop variable is "False"
        stp = True # set stp initially to True, this will be changed if there was not found any improvement in this run
        counter = counter + 1 # increment counter by 1
        for k in range(length): # go through all rows
            print("Run", counter, ", k:", k, ", percent done:", round(100*((counter-1) * length + k)/(21*length),2), "%") # show the progress of the program, knowing that it will take 21 runs
            for l in range(length): # go through all columns
                min = U1compare[k,l] # set min to the initial value/distance of these two cities before the run. This value will be checked against a new candidate in this run.
                for i in range(length): # go through all rows and columns, respectively
                    vector[i] = U1compare[k,i] + U1[i,l] # fill the empty vector with the results fo the Bellmann-Ford multiplication
                if np.min(vector) < min: # if there is a value in this vector that is smaller than the minimum
                    U1new[k,l] = np.min(vector) # set the entry in the new array to this value
        if not np.array_equal(U1new, U1compare): # if the newly created array and the old array are not the same (at least one value could be improved)
            stp = False # set stp to False
            U1compare = np.array(U1new) # set the newly created array to U1compare, what is the array needed to check if the new U1new in the next run has changed compared to this run, so if any improvements have been found
    # np.savetxt("distances.csv", U1compare, delimiter=",") # potentially save the optimized distance matrix/array to save computational time for the next request when only the last function would need to be executed
    return(U1compare) # return the final array that could not have been improved anymore

def return_reachable_cities(neighbors, city, country, k):
    '''
    This function is the final function that finds the cities that are reachable from a given city in k steps.
    Precondition: Knowledge about the distance from every city to any other
    Postcondition: The reachable cities from the given city in k steps
    :param neighbors: The array with the distances
    :param city: The given city (starting point)
    :param country: The country, specifying the city closer
    :param k: k steps
    :return: Nothing but print out the reachable cities in k steps
    '''
    data = getData() # get the data again
    maxCountries = list() # create an empty list to save the countries later on that are reachable within a maximum of steps
    exactCountries = list() # create an empty list to save the countries later on that are reachable in exactly this number of steps
    stp = False # set stp to False
    i = 0 # set i to 0

    # finding the index of the starting city
    while not stp: # as long as stp is False
        i = i + 1 # increment i by 1
        if (city == data[i][0] and country == data[i][1]) or i == 905: # when the starting city is found or break if nothing is found after the length of the array
            index = i # set index to i
            stp = True # set stp to true

    for j in range(k+1): # go through all ks
        if j != 0: # if j does not refer to 0 steps what would give the starting city
            print("\n\nSteps:", j) # print the current steps
            maxCities = set() # create an empty set to store the reachable cities for which are at maximum k steps needed
            exactCities = set() # create an empty set to store the reachable cities for exactly this k
            for i in range(int(len(neighbors))): # go through all cities
                if neighbors[index][i] <= j and data[i][0] != city: # if the steps are lower or equal the current k/j and the city is not the same as the starting city
                    maxCities.add(str(data[i][0] + " (" + data[i][1] + ")")) # add this city to the maximum set
                    maxCountries.append(data[i][1]) # append the corresponding country to the max list
                if neighbors[index][i] == j and data[i][0] != city: # if the necessary steps are equal to the current k/j and the city is not the same as the starting city
                    exactCities.add(str(data[i][0] + " (" + data[i][1] + ")")) # add this city to the exact set
                    exactCountries.append(data[i][1]) # append the current country to the exact list
            print("Reachable cities with", j, "steps (", len(maxCities),"):", maxCities, "\n") # print the set for the at maximum reachable cities
            print("Exactly in", j, "steps reachable cities (", len(exactCities),"):", exactCities) # print the set for the exact reachable cities



def main() :
    n = "Geneva" # set the starting city's name
    c = "CH" # set the starting city's country
    k = 5 # set the number of desired steps
    s = 4 # set the distance that is allowed for cities on the same sea in order to be neighbors
    d = 2 # set the distance that is allowed for cities that are not on the same sea in order to be neighbors
    data = getData() # call getData to retrieve the data via sql from the database
    neighbors = neighborhood(data, d, s) # call neighborhood with data received from getData and the distances d for non-lake-adjacent and s for lake-adjacent
    shortest_distances = bellman_ford_algorithm(neighbors) # call bellman_for_algorithm with the result from neighborhood
    return_reachable_cities(shortest_distances, n, c, k) # call distances with the result from the previous code, given n, c and k


if __name__== "__main__":
    main()
