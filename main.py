import itertools
import copy
def solution_configs(holes,position,diglets,sol,result):
    if len(holes) == 1:
        sol[position] = copy.copy(diglets)
        result.append(copy.copy(sol))
    else:
        for combinaison in itertools.combinations(diglets,holes[0]):
            actual_diglets = set(combinaison)
            remaining_diglets = diglets.difference(actual_diglets)
            sol[position] = copy.copy(actual_diglets)
            next_holes = copy.copy(holes)
            next_holes.pop(0)
            solution_configs(next_holes,position+1,remaining_diglets,sol,result)
def hole_configs(to_save,number_of_holes,sol, pos,result):
    if pos == number_of_holes:
        if sum(sol) == to_save:
            result.append(copy.copy(sol))
    else:
        ensemble = {0,1,2}
        for element in ensemble:
            sol[pos] = element
            hole_configs(to_save,number_of_holes,sol, pos+1,result)
def distances_generation(number_of_diglets, number_of_holes, diglett_hole_matrix,time_to_dig):
    distances = {}
    for diglet in range(0,number_of_diglets):
        distances[diglet] = {}
        for diglet2 in range(diglet+1, number_of_diglets):
            distances[diglet][diglet2] = {}
            for hole in range(0, number_of_holes):
                faster = diglet2
                slower = diglet
                if diglett_hole_matrix[diglet][hole] <= diglett_hole_matrix[diglet2][hole]:
                    faster = diglet
                    slower = diglet2
                time= diglett_hole_matrix[faster][hole] + time_to_dig
                if time >= diglett_hole_matrix[slower][hole]:
                    distances[diglet][diglet2][hole] = time
                else:
                    distances[diglet][diglet2][hole] = diglett_hole_matrix[slower][hole]
    return distances
def evaluation_solution_config(solution_config,diglett_hole_matrix,couple_diglets_times):
    result = 0
    for index, element in enumerate(solution_config):
        toto = copy.copy(element)
        if len(toto) == 1:
            val = toto.pop()
            tmp = diglett_hole_matrix[val][index]
            if tmp > result:
                result = tmp
        elif len(toto) == 2:
            dig1 = toto.pop()
            dig2 = toto.pop()
            tmp = couple_diglets_times[dig1][dig2][index]
            if tmp > result:
                result = tmp
    return result
def solve_problem(m,n,l,t,diglett_hole_matrix):
    holes = []
    hole_init = []
    for val in range(0,m):
        hole_init.append(0)
    hole_configs(l,m,hole_init,0,holes)
    sols = []
    sol_init = []
    for val in range(0,m):
        sol_init.append(set())
    for hole_config in holes:
        for diglets in itertools.combinations(set(range(n)),l): 
            solution_configs(hole_config,0,set(diglets),sol_init,sols)
    sol_pos = None
    solution = None
    couple_diglets_times = distances_generation(n, m, diglett_hole_matrix,t)
    for possibilite in sols:
        sol_tmp = copy.copy(possibilite)
        if solution == None:
            sol_pos = copy.copy(sol_tmp)
            solution = evaluation_solution_config(possibilite,diglett_hole_matrix,couple_diglets_times)
        else:
            tmp = evaluation_solution_config(possibilite,diglett_hole_matrix,couple_diglets_times)
            if tmp < solution:
                sol_pos = copy.copy(sol_tmp)
                solution = tmp
    return solution
import os
def main_exec(input_path):
    input_file = open(input_path)
    print ()
    output_file = open(os.path.dirname(input_path)+'/output', 'w')
    content = input_file.readlines()
    k = int(content[0]) 
    next_start = 1
    for nombre_de_tests in range(0,k):
        data = list(content[next_start].split(' '))
        next_start += 1
        for index, number in enumerate(data):
            if len(number) > 0:
                data[index] = int(number) 
        m = data[0]
        n = data[1]
        l = data[2]
        t = data[3]
        diglett_hole_matrix = []
        for diglett in range(0,n):
            data = list(content[next_start].split(' '))
            next_start += 1
            for index, number in enumerate(data):
                if len(number) > 0:
                    data[index] = int(number)
            diglett_hole_matrix.append(copy.copy(data))
        output_file.write(str(solve_problem(m,n,l,t,diglett_hole_matrix))+'\n')
    output_file.close()
import sys
if __name__ == "__main__":
    if len(sys.argv)>1:
       main_exec(sys.argv[1])
