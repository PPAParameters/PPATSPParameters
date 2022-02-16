import random
import numpy as np
import matplotlib.pyplot as plt

from route import Route



class PPA:


    def __init__(self, evaluations, pop_size, n_max, s_max, instance):
        self.instance = instance
        self.evaluations = evaluations
        self.number_evaluations = 0 
        self.pop_size = pop_size
        self.n_max = n_max
        self.s_max = s_max
        self.route_matrix = instance.matrix
        self.population = self.initialize_population(pop_size)
        self.population_offspring = []
        self.generations = 0
        self.x_max = 0
        self.x_min = np.inf 
        self.end_generation = True
        self.best_route = None
        self.list_of_best_routes = []
        
    
    def initialize_population(self, pop_size):
        route = Route(self.instance.cities)
        initial_pop = [Route(random.sample(route.route, route.length)) for n in range(self.pop_size)]
        for i, route in enumerate(initial_pop):
            route.calculate_distance(self.instance )
            route.id = "start:" +str(i+1)
            self.number_evaluations += 1
            
        return initial_pop        
    

    def fitness(self, route):
        """
        Normalize and calculate the fitness,
        f(xi) within an interval between [0,1] with 
        z_x_i = (f(x_max)-f(x_i))/(f(x_max)-f(x_min)) 
        """
        normalized_fitness = (self.x_max - route.route_distance) / (self.x_max - self.x_min)
        F_xi = 0.5 * (np.tanh(4 * (normalized_fitness) - 2) + 1)
        return F_xi
    

    def assign_offspring(self, F_xi):
        offspring = int(np.ceil(self.n_max * F_xi * random.random()))
        return offspring
    

    def mutation(self, F_xi):
        mutations = int(np.ceil(self.s_max * random.random() * (1 - F_xi)))  
        return mutations  

    # def assign_offspring(self, F_xi):
    #     offspring = int(np.ceil(self.n_max * F_xi ))
    #     return offspring
    

    # def mutation(self, F_xi):
    #     mutations = int(np.ceil(self.s_max *  (1 - F_xi)))  
    #     return mutations  


    def create_new_offspring(self, route, number_offspring, number_mutation):
        for offspring_id in range(1, number_offspring + 1):   
            offspring_route = route.copy()
            assert id(offspring_route) != id(route)

            for _ in range(number_mutation):
                offspring_route.two_opt()
            offspring_route.calculate_distance(self.instance)
            
            self.population_offspring.append(offspring_route)
            self.number_evaluations += 1

     
    def evaluate(self, file_name, round, a, b):
        """
        Evaluate while that there wont be more evaluations that 
        specified but if the eveluation is busy it will finish it.
        """
        
        while self.end_generation:
           
            sorted_route_list = sorted([x.route_distance for x in self.population])  
            self.x_max = sorted_route_list[-1]
            self.x_min = sorted_route_list[0]

            for route in self.population:
                if  self.number_evaluations >= self.evaluations:
                    self.end_generation = False
                
                # The fitness is calculated for eacht route. 
                # If the X_max is equal to the X_min than all 
                # the fitness values will be 0.5
                if(self.x_max == self.x_min):
                    F_xi = 0.5
                else: 
                    F_xi = self.fitness(route)
                
                number_offspring = self.assign_offspring(F_xi)
                number_mutation = self.mutation(F_xi)     
                self.create_new_offspring(route, number_offspring, number_mutation)
                
        
            self.population = self.population + self.population_offspring
            self.population = sorted(self.population, key=lambda route: route.route_distance)[:self.pop_size]
        
            self.population_offspring = []

            # Save the best route and update if there is a better route.
            if self.best_route is None:
                self.best_route = self.population[0]
            elif self.best_route.route_distance > self.population[0].route_distance:
                self.best_route = self.population[0]
                self.list_of_best_routes.append(self.best_route)
            
            
        # tsp_route_1 = Route.change_route_to_array(self.best_route.route) 
        # fig, ax = plt.subplots()         
        # ax.set_title('Optimized tour')          
        # ax.scatter(tsp_route_1[:, 0], tsp_route_1[:, 1], color="lightcoral")   
        
        # for route in self.list_of_best_routes:
        #     plt.cla()
        #     ax.set_title('Optimized tour')          
        #     ax.scatter(tsp_route_1[:, 0], tsp_route_1[:, 1], color="lightcoral")  
        #     positions = Route.change_route_to_array(route.route) 
        #     distance = 0.0
        #     for i in range(len(positions)):
        #         if i == (len(positions)-1):
        #             start_pos = positions[len(positions)-1]
        #             end_pos = positions[0] 
        #         else:
        #             start_pos = positions[i]
        #             end_pos = positions[i+1]
            
            
        #         ax.annotate("", xy=start_pos, xytext=end_pos, arrowprops=dict(arrowstyle="-", color='lightcoral'))
        #         distance += np.sqrt((start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2)
        

        #     textstr = f"N Cities: {len(positions)}\nTotal length: {int(distance)}"
        #     props = dict(boxstyle='round', alpha=0.1)
        #     ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)

        #     plt.tight_layout()
        #     plt.pause(0.05)
        # print(round, a, b)

        # code to show the optimal route 
        # if round == 2 and a == 5 and b == 5:
        #     self.best_route.plot_routemap(file_name)
        return self.best_route.route_distance, self.best_route



    

