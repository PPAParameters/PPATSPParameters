import random 
import numpy as np
import matplotlib.pyplot as plt


matrix_list =[]
def generate_tsp_instances(number_cities, number_instances,  number_of_kind, list_of_vertical, list_of_horizontal,increment=0):
    
    document = "import numpy as np \n\n"
    name_of_file_name = f"tsp_instance_{number_cities}_matrix_little.py"
    instance_number_index = 0
    vertical =  list_of_vertical[instance_number_index]
    horizontal = list_of_horizontal[instance_number_index]
    
    for instance_number in range(1, number_instances+1):
        # if (instance_number % (number_of_kind+1) == 0):
        #     # instance_number_index += 1
        #     # vertical =  list_of_vertical[instance_number_index]
        #     # horizontal = list_of_horizontal[instance_number_index]


        name_of_file = f"tsp_instance_{number_cities}_{instance_number}.txt"
        keywords = f"AME : levi{number_cities}_{instance_number}\n"
        keywords = keywords + f"COMMENT : {number_cities}: {vertical}x{horizontal} -city problem (levikoppenhol)\n"
        keywords = keywords + f"TYPE : TSP\n"
        keywords = keywords + f"DIMENSION : {number_cities}\n"
        keywords = keywords + f"EDGE_WEIGHT_TYPE : EUC_2D\n"
        keywords = keywords + f"NODE_COORD_SECTION\n"
        cities_for_instance = generate_city(number_cities, vertical, horizontal)
        keywords = keywords + cities_for_instance 
        file = open(name_of_file, "w") 
        file.write(keywords) 
        file.close() 
        dimension, cities = read_tsp_problem(name_of_file)
        # plot_routemap(cities)
        matrix = route_to_matrix(dimension, cities)
        matrix_list.append(matrix)
#         
        mat = np.matrix(matrix)
        name_of_file_py = f"# dimensions {vertical}x{horizontal} \ntsp_instance_{number_cities}_{instance_number}_city_list = {cities} \ntsp_instance_{number_cities}_{instance_number}"
        
        document = document + f"{name_of_file_py} = np.matrix([\n"
        
        for i in range(mat.shape[0]):
            document = document + "["
            for j in range(mat.shape[1]):
                if 0 != j:
                    document = document + f","
                if mat[i, j] == -1:     
                    document = document + f"np.inf "
                else:
                    document = document + f"{mat[i, j]} " 
            if i == mat.shape[0]-1:
                document = document + "]\n"
            else:    
                document = document + "],\n"   
        document = document + "])\n\n"            
        number_cities = number_cities - increment
    file = open(name_of_file_name, "w") 
    file.write(document) 
    file.close() 
        
        
        
        
        
def route_to_matrix(dimension, city_list):
    route_matrix = np.zeros((int(dimension), int(dimension)))  
    for x in range(dimension):     
        for y in range(x, dimension):
            if x == y:
                route_matrix[x, y] = -1
            else:
                route_matrix[x, y] = distance(city_list[x], city_list[y])
                route_matrix[y, x] = route_matrix[x,y]
    return route_matrix
        
        
def distance(city1, city2):
    """
    Calculates Euclidean distance.
    """
    return np.sqrt((city1[1] - city2[1])**2 + (city1[2] - city2[2])**2)

def read_numbered_city_line(words):
    city_number = int(words[0])
    x = float(words[1])
    y = float(words[2])
    return (city_number, x, y)
    
def read_cities_problem(tspfile):
    # Read dimension.
    dimension = None
    for line in tspfile:
        if 'DIMENSION' in line:
            dimension = int(line.split()[-1])
        elif 'TOUR_SECTION' in line or 'NODE_COORD_SECTION' in line:
            assert dimension is not None
            break 
    assert dimension is not None
    
    # Read cities.
    cities = []  
    for _ in range(dimension):
        line  = tspfile.readline()
        words = line.split()
        cities.append(read_numbered_city_line(words))
    return dimension, cities
        
def read_tsp_problem(path):
    with open(path,'r') as tspfile:
        dimension, cities = read_cities_problem(tspfile)
        return dimension, cities
    assert False
        
def generate_city(number_cities, vertical, horizontal):
    text = ""

    for i in range(1, number_cities+1):
        x = random.randint(0,horizontal)
        y = random.randint(0,vertical)
        text = text + f"{i} {x} {y}\n"
    
    text = text + "EOF"
    return text


def plot_routemap(route):
    positions = change_route_to_array(route)
    
    fig, ax = plt.subplots()         
    ax.set_title('Map')          
    ax.scatter(positions[:, 0], positions[:, 1])   
    plt.tight_layout()
    plt.show()

def change_route_to_array(route):
    
    array = np.zeros((len(route), 2))
    for i in range(len(route)):
        array[i][0] = route[i][1]
        array[i][1] = route[i][2]     

    return array

def main():
    
    generate_tsp_instances(30,30,  1, [30], [24], 0)
    
if __name__ == '__main__':
    main()

    