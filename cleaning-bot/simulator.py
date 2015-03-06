#!/usr/bin/python
#
# Author: Hannah Brock
# Class: CS 5300, Fall 2014
#
# For usage information, run: python simulator.py --help

from cleaning_bot import *
import argparse
import numpy
from scipy import stats

def confidence_interval(array, confidence=0.95):
    double_array = numpy.array(array) * 1.0
    mean = numpy.mean(double_array)
    std = numpy.std(double_array)
    stderr = stats.sem(double_array)
    interval = stderr * stats.t.ppf(confidence, len(double_array) - 1)
    return mean, interval, std

### MAIN ###
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--rows', type=int, required=True, help='number of rows for the grid')
parser.add_argument('-c', '--cols', type=int, required=True, help='number of columns for the grid')
parser.add_argument('-d', '--dirty', type=float, required=True, help='probability a given cell is dirty')
parser.add_argument('-a', '--agents', type=int, required=True, help='the number of agents')
parser.add_argument('-m', '--max', type=int, required=True, help='maximum time steps allowed')
parser.add_argument('-n', '--numruns', type=int, default=1, 
                    help='the number of runs for each data set (will run simulations x number of runs)')
parser.add_argument('-s', '--simulations', type=int, default=1, 
                    help='the number of simulation sets for each data set (will run simulations x number of runs)')
parser.add_argument('-t', '--time-delay', type=float, dest='delay', default=0.1,
                    help='visualization delay in seconds')
parser.add_argument('-v', '--visualize', dest='visualize', action='store_const', const=True,
                    default=False, help='visualize the simulator run')
parser.add_argument('-p', '--print-moves', dest='print_moves', action='store_const', const=True,
                    default=False, help='print the moves of each agent')

args = parser.parse_args()

if args.rows < 1:
    print 'The grid must have at least one row!'
    exit(1)
if args.cols < 1:
    print 'The grid must have at least one columns!'
    exit(1)
if args.agents < 1:
    print 'There must be at least one cleaning agent!'
    exit(1)
if args.dirty < 0:
    print 'Probability cannot be negative!'
    exit(1)
if args.delay <= 0:
    print 'Visualization delay must be greater than 0!'
    exit(1)
if args.visualize and args.numruns > 1:
    print 'Cannot visualize more than one run!'
    exit(1)

sim = CleaningSimulator(args.rows, args.cols, args.dirty, args.agents, args.visualize, args.delay,
                        args.print_moves, args.max)

steps = []
moves = []
clean = []
sims = args.simulations
if args.numruns == 1:
    sims = 1
for i in range(0, sims):
    steps_res = []
    moves_res = []
    clean_res = []
    for x in range(0,args.numruns):
        res = sim.run()
        steps_res.append(res[0])
        moves_res.append(res[1])
        clean_res.append(res[2])
        sim.reset()
    steps.append(steps_res)
    moves.append(moves_res)
    clean.append(clean_res)

if sims > 1:
    print 'Set\tMean Time\tMean Moves\t% Clean'
    mean_steps = []
    mean_moves = []
    mean_clean = []
    for x in range(0, sims):
        np_steps = numpy.array(steps[x])
        np_moves = numpy.array(moves[x])
        np_clean = numpy.array(clean[x])
        mean_steps.append(numpy.mean(np_steps))
        mean_moves.append(numpy.mean(np_moves))
        mean_clean.append(numpy.mean(np_clean))
        print str(x+1) + '\t' + str(mean_steps[x]) + '\t' + str(mean_moves[x]),
        print '\t'+ str(mean_clean[x])

    final_steps_mean, steps_interval, steps_std = confidence_interval(mean_steps)
    final_moves_mean, moves_interval, moves_std = confidence_interval(mean_moves)
    final_clean_mean, clean_interval, clean_std = confidence_interval(mean_clean)
    print '---\t----\t-----'
    print 'Mean\t' + str(final_steps_mean) + '\t' + str(final_moves_mean),
    print '\t' + str(final_clean_mean)
    print 'Conf Int\t' + str(steps_interval) + '\t' + str(moves_interval),
    print '\t' + str(clean_interval)
    print 'Std Dev\t' + str(steps_std) + '\t' + str(moves_std)
