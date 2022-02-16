from random import randrange
import numpy as np
import matplotlib.pyplot as plt

class Route:
    """
    Represents route over cities.
    """

    def __init__(self, route):
        """
        @arg route is a list of City objects.
        """
        self.route = route
        self.length = len(route)
        self.route_distance = None
        self.id = ""
        
 
                     
    def calculate_distance(self, tsp):
        self.route_distance = self.distance(tsp)


    def distance(self, tsp):
        """
        Calculates distance over route for given TSP instance.
        """
        route_distance = 0
        for i in range(1,len(self.route)+1):
            if i == (len(self.route)):
                route_distance += tsp.distance_matrix(self.route[i-1].city_number, self.route[0].city_number)
            else:
                route_distance += tsp.distance_matrix(self.route[i-1].city_number, self.route[i].city_number)

        return route_distance
    
    # def shortest_route(self, tsp, city):
    #     for i in range(len(tsp.dimension)):
    #         shortest(tsp[city][i])


    def two_opt(self): 
        """
        Swaps two random different cities (two_opt method).
        """
        assert len(self.route) >= 2

        index_1 = randrange(len(self.route))
        index_2 = randrange(len(self.route))
        
        while index_1 == index_2:
            index_2 = randrange(len(self.route))
        self.route[index_1], self.route[index_2] = self.route[index_2], self.route[index_1]

    
    def copy(self):
        new_route = Route(self.route.copy())
        return new_route

    def plot_routemap(self, file_name):
        positions = self.change_route_to_array(self.route)
        
        title_name_for_optimal_route = f"Optimal PPA Tour for Instance {file_name}"
        fig, ax = plt.subplots() 
        ax.set_title(title_name_for_optimal_route)          
        ax.scatter(positions[:, 0], positions[:, 1])             

        distance = 0.
    
        for i in range(len(positions)):
            if i == (len(positions)-1):
                start_pos = positions[len(positions)-1]
                end_pos = positions[0] 
            else:
                start_pos = positions[i]
                end_pos = positions[i+1]
                
            ax.annotate("", xy=start_pos, xytext=end_pos, arrowprops=dict(arrowstyle="-", color='lightcoral'))
            distance += np.sqrt((start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2)
        

        textstr = f"Cities: {len(positions)}  \nTotal length: {round(distance, 3)}"
        props = dict(boxstyle='round', alpha=0.1)
        ax.text(0.05, 0.95, textstr,transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
        plt.tight_layout()
        plt.show()
        # optimal_route_fig = f"optimal_tour_for_instance_{file_name}.png"
        # plt.savefig(optimal_route_fig)
        plt.close()
        plt.clf()
    
    @staticmethod
    def change_route_to_array(route):
        array = np.zeros((len(route), 2))
        for i in range(len(route)):
            array[i][0] = route[i].x
            array[i][1] = route[i].y     

        return array