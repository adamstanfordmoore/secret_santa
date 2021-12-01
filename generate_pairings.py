#!/usr/bin/env python3

"""
Secret Santa: generate pairings
@author Adam Stanford-Moore
@version 2017-12-14 
The script generates the secret santa pairings taking into account several factors:
1.  No pairing with immediate family
2.  No pairing with someone you had in the last two years
3.  modification from backdoor
The program reads in the people to be included and creates a dictionary of people with their
possible pairs, then generates a Hamiltonian cycle 
"""
import smtplib
import datetime
import random
from copy import deepcopy
import signal

YEAR = datetime.datetime.now().year


class TimeoutError(Exception):
    pass

def handler(signum, frame):
    raise TimeoutError()

#returns dictionary of {person: has_this_person}
def get_pairing(filename):
    pairing = dict();
    names = [] 
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.rstrip('\n'))   
    
    first_name = names[0]            
    for i in range(len(names)):
        if (names[i] == '-'): 
            continue
        elif (i == len(names) - 1):
            pairing[names[i]] = first_name   
        elif (names[i+1] == '-'):
            pairing[names[i]] = first_name
            first_name = names[i+2] 
        else:
            pairing[names[i]] = names[i+1]
            
    return pairing

"""
Return a dictionary of 'name':'family_ID_#'
"""
def get_family_ID(filename):
    contacts = dict()

    with open(filename, mode='r', encoding='utf-8') as names_file:
        for a_name in names_file:
            if (a_name == '\n'):
                continue
            contacts[a_name.split()[0]] = a_name.split()[1]
    return contacts

#takes in a list where each person is paired with the next person.  Writes it to file in same order    
def write_pairings(pairing_list):
    file_name = 'secret_pairings_' + str(YEAR) + '.txt'
    f= open(file_name,"w")    
    # iterate through
    
    for i in range(len(pairing_list)):
        if (i == len(pairing_list) - 1):
            f.write(pairing_list[i]) 
        else:
            f.write(pairing_list[i]+'\n')


"""
Times out the find_cycle method in case it is stuck down a certain path, and restarts
the search.  Necessary if there are many specifications 
"""
def timed_find_cycle(graph,list):
    # set the timeout handler
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(15)  #timeout duration
    try:
        result = find_cycle(graph,list)
    except TimeoutError as exc:
        result = timed_find_cycle(graph,list)
    finally:
        signal.alarm(0)

    return result


""" 
To find a person with fewer or equal to num options to speed process.  Allows recursion to
start with a person who has few options.  
"""
def few_options(graph, num):
    keys = list(graph.keys())
    for key in keys:
        if (len(graph[key]) <= num):
            return key
    return few_options(graph, num + 5)

"""
Recursive backtracking function to find Hamiltonian path. It starts by adding a random 
person to cur_list and then tries to find path with another person added on.  If no path is found,
then a different person is added.
""" 
def find_cycle(graph, cur_list):
    print(cur_list)
    if (len(cur_list) == len(graph) and cur_list[0] in graph[cur_list[-1]]):
        return cur_list
    curr = cur_list[-1];
    possible = graph[curr]
    random.shuffle(possible)
    
    for i in range(len(possible)):
        if len(graph[possible[i]]) < 3:
            possible[0], possible[i] = possible[i], possible[0]
            break
            
    for next in possible:
        if (next not in cur_list):
            new_list = deepcopy(cur_list)
            new_list.append(next)
            new = find_cycle(graph,new_list)
            if (new):
                return new               
    return None    

"""
{a:[x,y,z]} allows me to remove xyz from possible candidates for a or allows me to
change candidates for a to exactly xyz 
"""
def backdoor(graph, last, before_last):
    change = {}
    remove = {'Adam':['Lorena','Younmi']}
    remove['Mignon'] = [last['Rory'],before_last['Rory']] #because Mignon shops for both
    remove['Rory'] = [last['Mignon'],before_last['Mignon']]
    for key in change:
        if key in graph:
            graph[key] = change[key]
    for key2 in remove:
        if key2 in graph:   #only if the person is in the pairing can we remove
            new = graph[key2]
            for p in remove[key2]:
                try:
                    new.remove(p)
                except:
                    continue
            graph[key2] = new
    return graph
        
            
def main():
    # set up graph as a dictionary
    graph = dict()
    family_ID = get_family_ID('INCLUDED_IN_DRAW.txt') # read contacts
    last_pairing = get_pairing('secret_pairings_' + str(YEAR - 1) + '.txt')
    before_last_pairing = get_pairing('secret_pairings_' + str(YEAR - 2) + '.txt')
    
    #populate graph with allowed pairs
    for person in family_ID:
        for possible_pair in family_ID:
            if (family_ID[person] != family_ID[possible_pair]): #not in same family
                if (person not in last_pairing or last_pairing[person] != possible_pair):
                    if (person not in before_last_pairing or before_last_pairing[person] != possible_pair):
                        
                        #add connection from person to possible_pair                
                        if (person in graph):
                            graph[person].append(possible_pair)
                        else:
                            graph[person] = [possible_pair]
    
    #modify graph with extra specifications
    graph = backdoor(graph, last_pairing, before_last_pairing)  

    #find pairings
    pairing_list = timed_find_cycle(graph,[few_options(graph,1)]) 

    write_pairings(pairing_list)
    print(pairing_list)
        
        
    
if __name__ == '__main__':
    main()


