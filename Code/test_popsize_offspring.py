import numpy as np
import time
import matplotlib.pyplot as plt
from scipy import stats
import tsp_30_times_v1 as instance_list 
from tsp import TSP
from ppa import PPA

def main():
    # loop for solving all instances
    statistics = ""
    
    number = 30

    name_of_file_name = f"tsp_instance_{number}_offspring_popsize_v2.py"
    instance_name = f"../Data/tsp_instance_30_{number}.txt"
    tsp = TSP(instance_name)     
    n_pop_size = 50 
    n_offspring = 50
    n_evaluations = 5000
    n_mutations = 10
    n_runs = 50
    start_all_pop = 1
    start_all_max = 1
    print(number)

    all_best_routes = []
    all_worst_routes = []

    

    
    statistics += f"instance_{number}_offspring_popsize = ["
    
    optimal_route = instance_list.list_of_instances[number-1]["optimal_tour"]
    arr = np.zeros((n_pop_size-start_all_pop+1 , n_offspring-start_all_max+1))
    
    for pop_size_i, pop_size in enumerate(range(start_all_pop, n_pop_size + 1)):
        statistics += "["
        for offspring_i, max_offspring in enumerate(range(start_all_max, n_offspring + 1)):

            route_distance_list = []
            route_distance_text = "["
            runtime_distance_text = "["
            route_list = []
            list_runtimes = []
            for run in range(n_runs):
                start = time.time()
                ppa = PPA(n_evaluations, pop_size, max_offspring, n_mutations, tsp)
                distance_ppa, route_ppa  = ppa.evaluate(number, run, pop_size_i, offspring_i)
                end = time.time()

                route_distance_list.append(distance_ppa)
                route_list.append(route_ppa)
                ppa_runtime = round(end - start, 3)
                list_runtimes.append(ppa_runtime)

                route_distance_text += f"{distance_ppa/optimal_route}"
                runtime_distance_text += f"{ppa_runtime}"
                
                if run != n_runs-1:
                    route_distance_text += ","
                    runtime_distance_text += ","
                
                
            print(f"Population size: {pop_size}, max offspring: {max_offspring}")
            route_distance_text += "]"
            runtime_distance_text += "]"
            
            mean_route_distnace_of_n_runs = np.mean(route_distance_list)/optimal_route
            mean_runtime_50_runs = np.mean(list_runtimes)/n_runs
            bestroute = sorted(route_list, key=lambda route: route.route_distance)[0]
            # worstroute = sorted(route_list, key=lambda route: route.route_distance)[-1]
            # the route 
            # which offspring and popsize 
            tsp_route = "["
            for i, route in enumerate(route_list):
                tsp_route += "["
                for j, city in enumerate(route.route):
        
                    tsp_route += f"({city.city_number}, {city.x}, {city.y})"
                    if j != len(route.route)-1:
                        tsp_route += ","
                tsp_route += "]"
                if i != len(route_list)-1:
                    tsp_route += ","
            tsp_route += "]"
            all_best_routes.append(bestroute)
            # all_worst_routes.append(worstroute)
            arr[pop_size_i, offspring_i] = mean_route_distnace_of_n_runs
            W, p = stats.shapiro(route_distance_list)
            statistics += f"{{'instance': {number}, 'optimal': {optimal_route}, 'x': {pop_size}, 'y':{max_offspring},  'shaprio': {p},'stdv': {round(np.std(route_distance_list),3)}, 'mean': {round(np.mean(route_distance_list), 3)}, 'max': {round(np.max(route_distance_list), 3)}, 'min': {round(np.min(route_distance_list), 3)}, 'runtime': {mean_runtime_50_runs}, 'values': {route_distance_text},  'tsp_runtimes':{runtime_distance_text},'route':{tsp_route}}}"     
            
            file = open(name_of_file_name, "w") 
            file.write(statistics) 
            file.close() 
            
            if offspring_i != n_offspring-start_all_max:
                    statistics += ",\n"
        statistics += "]"       
        if pop_size_i != n_pop_size-start_all_pop:
            statistics += ",\n"
    statistics += "] \n"


    
    thesbestroute = sorted(all_best_routes, key=lambda route: route.route_distance)[0]
    # thesworstroute = sorted(all_worst_routes, key=lambda route: route.route_distance)[-1]
    name_map_best = f"{number} ppa divided by little {round(thesbestroute.route_distance/optimal_route, 2)} (best case)"
    # name_map_worst = f"{number} ppa divided by little {round(thesworstroute.route_distance/optimal_route, 2)} (worst case)"
    
    thesbestroute.plot_routemap(name_map_best)
    # thesworstroute.plot_routemap(name_map_worst)
    
    plt.figure(figsize=(10, 10))
    plt.pcolormesh(arr)
    resolution = ""
    if number <= 10:
        resolution = " 30x24 "
    elif 10 < number <= 20:
        resolution = " 36x20  "
    elif 20 < number <= 30:
        resolution = " 40x18 "

    title_heatmap = f"Mean tour instance {number}, 30 cities & map resolution {resolution} "

    plt.title(title_heatmap, fontsize=16)
    plt.ylabel('popSize', fontsize=14)
    plt.xlabel('max offspring', fontsize=14)
    plt.tight_layout()
    cbar = plt.colorbar(orientation='vertical')
    label_name_bar = f"mean optimal ppa tour of {n_runs} runs / exact optimal tour"
    cbar.set_label(label_name_bar, fontsize=14)
    name_heatmap_file = f"heatmap_instance_{number}_runs_{n_runs}_mutations_{n_mutations}_v2.png"
    plt.show()
    plt.savefig(name_heatmap_file)
    plt.close()
    plt.clf()

    file = open(name_of_file_name, "w") 
    file.write(statistics) 
    file.close() 
if __name__ == '__main__':
    main()