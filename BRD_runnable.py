#! /usr/bin/python

import argparse
import logging



import matplotlib.pyplot as plt
import networkx as nx


from GT_utilities import User
from GT_utilities import refresh_costs
from GT_utilities import generate_users
from GT_utilities import read_file
from GT_utilities import social_welfare_central
from GT_running_modes import run_all, run_equil, run_random_subset
from GT_running_modes import run_social, run_test
from GT_running_modes import run_one
from GT_running_modes import run_once
from GT_running_modes import run_random
from GT_running_modes import run_some
from GT_charts import central_distr



if __name__ == '__main__':


    parser = argparse.ArgumentParser(
        description='Calculating e-PNE by using the best response dynamic',
    )
    parser.add_argument('-p', action='store',
                        dest='fp_exponent',
                        type=int,
                        default=-6,
                        help='Set the exponent of the false positive rate. Ranges from -1 to -10. Not \
                            all modes use this value. default:-6')
    parser.add_argument('-f', action='store',
                        dest='source_file',
                        default='email-Eu-core-temporal.txt',
                        help='source file name within datasets folder, default:eu-server',
    )
    parser.add_argument('-t', action='store',
                        dest='altruism_threshold',
                        type=int,
                        nargs=2,
                        default=[4,4],
                        help='users incoming messages from which he is altruistic. Second value not in use, set both for the same value. Default:4')
    parser.add_argument('-a', '--altruism',
                        action='store',
                        dest='altruism_value',
                        type=float,
                        default=0.1,
                        help='The coefficent for the social cost used at calculating the cost of altruistic users. Default:0.1')                    
    parser.add_argument('-m', '--mode',
                        action='store',
                        dest='running_mode',
                        type=int,
                        default=1,
                        help='The running mode changes the amount of tests to be performed. It has the following options:   \
                                1->Runs the whole simulation on the whole range of starting p_values with the given altruism thresholds and coefficient\
                                2->Runs the test at p_value=social_opt with the given thresholds and with increasing altruism coefficents up until 1.0    \
                                3->Runs the test at the selected p_value with the given altruism thresholds and with increasing altruism coefficents up until 1.0    \
                                4->Runs the selected test with the given altruism thresholds and with the given coefficient \
                                5->Runs a test from -1 and -10 with increasing altruism coefficient to test NEs \
                                6->Runs several test based on selection mode and graph halving method \
                                7->Runs the the test with random fp_values for everyone in iterations number of times*2(due to local//global altruism altruism) ')                        
    parser.add_argument('-s', '--slow',
                        action='store_true',
                        dest='slow',
                        help="Changes how the brd calculation is made, if given, the algorithm searches for the player with highest "\
                        "achievable cost decrease. Otherwise it chooses the player with the highest cost."
                        )
    parser.add_argument('-i', '--iterations',
                        action='store',
                        dest='iterations',
                        type=int,
                        default=1,
                        help="How many times the simulation is run for the random mode. Default:1"
                        )
    parser.add_argument('-hv', '--halving',
                        action='store',
                        dest='halving',
                        type=int,
                        default=1,
                        help="Type of halving used in the simulation. \
                            0->halves the graph based on the highest degree \
                            1->halves the graph based on the highest betweenness centrality . Default:1")
    parser.add_argument('-d', '--draw',
                        action='store_true',
                        dest='draw',
                        help="If given, makes a png image of the graph before running the simulation"
                        )
    parser.add_argument('-l', '--local',
                    action='store_true',
                    dest='local_altruism',
                    help="If given, will run the simulation with local altruism, otherwise global altruism is used"
                    )
    parser.add_argument('-so', '--socialopt',
                action='store_true',
                dest='calculate_social_opt',
                help="If given, will calculate a social optimum approximation for the given graph, instead of running the NE search algorithm"
                )

    results = parser.parse_args()
    #print(results.altruism_threshold)

    logging.basicConfig(filename='{}_BRD.log'.format(results.source_file.split(".")[0]), filemode='w', format='%(asctime)s - %(name)s - %(threadName)s - %(thread)d - %(levelname)s - %(message)s'
                        ,datefmt='%d-%b-%y %H:%M:%S',level=logging.DEBUG)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)

        
    
    logging.debug("True brd algorithm is enabled: %s",results.slow)
    
    
    filename='datasets/{}'.format(results.source_file)
    logging.debug("reading from file: %s",filename)
    I = read_file(filename)


    inDegrees2 = []


    for k, v in I.in_degree():
        inDegrees2.append(v)


    degree_sequence2A = sorted(inDegrees2, reverse=True)



    
    # Theorem 4. The SO of the FMD-RA Game is not the trivial NE and corresponds to higher overall utilities if f · (M − maxu(in(u))) < L.
    # we assume the users
    # suffer from a privacy breach if relationship anonymity is not ensured, i.e., they
    # uniformly lose L when the recipient u can be linked to any sender via any message between them.

    M2 = I.number_of_edges()
    max_incoming2 = degree_sequence2A[0]
    f = 1.0
    L2 = float(f*(M2-max_incoming2))+1.0
   

    #making an image of the currently loaded graph
    draw=results.draw
    if draw:
        logging.debug("attempting to draw graph")
        fak=plt.figure()
        nx.draw(I, connectionstyle='arc3, rad = 0.1',ax=fak.add_subplot(111))
        fak.savefig("{}_graph.png".format(results.source_file.split(".")[0]),dpi=150)


    
    # #minden p exponense egy social cost tarolva, kozponti iranyitas
    # best_p_values=social_welfare_central(User,I,L2,[-1,-1],True)
    # optimal_p=max(best_p_values,key=best_p_values.get)
    # logging.info("the optimal p value when everyone is altruist:%d",optimal_p)
    
    # centralized_solution=max(best_p_values.values())

    # logging.info("Centrailzed solution done: %f",max(best_p_values.values()))
    # central_distr(best_p_values,results.source_file.split(".")[0])


    running_mode=results.running_mode
    if running_mode==1:
        logging.info("Entering running mode: every false_positive rate start with every altruism possibility")
        run_all(results, I, f, L2)
    # elif running_mode==2:
    #     logging.info("Entering running mode: Testing results at predicted best false positive rate")
    #     run_social(results, I, f, L2, optimal_p )
    elif running_mode==3:
        logging.info("Entering running mode: Testing desired false positive rate with every altruism posibbility")
        run_one(results, I, f, L2)
    elif running_mode==4:
        logging.info("Entering running mode: Testing single fp_value with single altruism preset")
        run_once(results, I, f, L2)
    elif running_mode==5:
        logging.info("Entering running mode: Testing both -1 and -10 for NE")
        run_equil(results, I, f, L2)
    elif running_mode==6:
        logging.info("TEST MODE FOR DEGREE AND BC THRESHOLDS")
        run_some(results, I, f, L2,results.halving,0,results.calculate_social_opt)
    elif running_mode==7:
        logging.info("TEST MODE FOR LIN AND EXP THRESHOLDS")
        run_some(results, I, f, L2,results.halving,3,results.calculate_social_opt)
    elif running_mode==8:
        logging.info("TEST MODE FOR RANDOM DISTRIBUTION WITH SOCIAL OPTIMUM")
        run_random_subset(results, I, f, L2,results.halving,results.iterations,results.local_altruism)
    else:
        print("Invalid running mode")


