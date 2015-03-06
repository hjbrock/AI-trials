#!/usr/bin/python
# Author: Hannah Brock
# Class: CS 5300, Fall 2014
# Assignment: A2

from towers_AStar import *
from towers_BFS import *
import argparse
from multiprocessing import Pool

def parse_args():
    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--numdisks', default=3, help='number of disks')
    parser.add_argument('-t', '--type', required=False, default='both',
                        help='type of search to perform (bfs, astar, or both)')
    parser.add_argument('-d', '--no-dups', dest='dups', action='store_const', 
                        const=True, default=False,
                        help='ignore duplicate nodes')
    parser.add_argument('-c', '--check-on-creation', dest='check_creation', 
                        action='store_const', const=True, default=False,
                        help='check for goal on node creation')
    parser.add_argument('-p', '--print', dest='print_tree', action='store_const', 
                        const=True, default=False,
                        help='print the search tree')
    return parser.parse_args()

def solution_str(solution):
    sol = ''
    for node in solution:
        sol += str(node.state)
        sol += ' -> '
    return sol[:len(sol)-4]

def run_search(solver, print_tree):
    path, created, expanded, solved = solver.search()
    if args.print_tree:
        solver.print_tree()
    print('Solution found: ' + str(solved))
    print('Solution length: ' + str(len(path) -1))
    print('Path: ' + solution_str(path))
    print('Nodes created: ' + str(created))
    print('Nodes expanded: ' + str(expanded))

args = parse_args()
bfs = (args.type == 'bfs')
astar = (args.type == 'astar')
if args.type == 'both':
    bfs = True
    astar = True

if bfs:
    pool = Pool(processes=4)
    print('Running BFS search')
    solver = TowersOfHanoiBFS(args.dups, int(args.numdisks), args.check_creation)
    pool.apply_async(run_search(solver, args.print_tree))
    pool.close()
    pool.join()
if astar:
    pool = Pool(processes=4)
    print('Running A* search')
    solver = TowersOfHanoiAStar(args.dups, int(args.numdisks), args.check_creation)
    pool.apply_async(run_search(solver, args.print_tree))
    pool.close()
    pool.join()
