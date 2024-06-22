import copy
import logging
import pickle
import networkx as nx
from GT_utilities import User
from GT_utilities import generate_users
from GT_utilities import dictionary_update
from GT_utilities import brd
from GT_utilities import graph_thinner
from GT_utilities import lin_dist
from GT_utilities import halver
from GT_charts import sw_and_dist
from GT_charts import biggest_cost_reduction
from GT_charts import equlibra_chart
from GT_charts import biggest_costs



def brd_setup_and_run(filename, I, f, L2, slowmode, p, altr,altr_value,local_altruism,selection_mode,bc_threshold,ordering=None,calculate_social_optimum=False,preset_users=None):
    if ordering!=None:
        fp_exponent=-1  
        for list in reversed(ordering):
            for i in list:
                #print("assign fp exponent:{} to node {} with degree number{}".format(fp_exponent,i,degrees[i]))
                I.nodes[i]['fp-value']=fp_exponent
            fp_exponent-=1

    p_values={-1:0,-2:0,-3:0,-4:0,-5:0,-6:0,-7:0,-8:0,-9:0,-10:0,'none':0}
    User.altruist=0
    User.selfish=0
    User.cooperative=0
   #User.altruism_value_base=altr_value
    if preset_users==None:
        eu_users=generate_users(I,User,altr,L2,p,altr_coef=altr_value,selection_mode=selection_mode,bc_threshold=bc_threshold)
        users_original=copy.deepcopy(eu_users)
    else:
        eu_users=preset_users
        users_original=copy.deepcopy(eu_users)  
    # logging.debug("starting new cycle with:%d %d %d. Altrusim coefficent: %f",p,altr[0],altr[1],altr_value)
    # logging.info("run parameters: local altruism: %d selection mode: %d bc_threshold: %f",local_altruism,selection_mode,bc_threshold)
    dictionary_update(eu_users,p_values)
    p_values_start=p_values.copy()
           
    logging.info("number of altruist,cooperative and selfish users: %d %d %d",User.altruist,User.cooperative,User.selfish)

            #calculating 
    p_values,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users=brd(eu_users,I.number_of_edges(),f,p_values,slowmode,local_altruism,calculate_social_optimum)
    logging.debug("brd done")
            
            
    # if iterations>1:
    #     sw_and_dist((filename)+("slow" if slowmode else "fast")+str(p)+str(altr[0])+str(altr[1])+str(altr_value), p_values, p_values_start, iterations, social_welfare_array)
    #     biggest_costs(iterations,biggest_cost_array,(filename)+("slow" if slowmode else "fast")+str(p)+str(altr[0])+str(altr[1])+str(altr_value))
    #     biggest_cost_reduction(iterations,biggest_difference_array,(filename)+("slow" if slowmode else "fast")+str(p)+str(altr[0])+str(altr[1])+str(altr_value))
    #     logging.debug("printing pdfs done")
    # else:
    #     logging.info("no improvement could be made")
    return  p_values,p_values_start,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users,users_original
            
    
def run_all(results, I, f, L2):
    slowmode=results.slow
    filename=results.source_file.split(".")[0]
    altruism_threshold=results.altruism_threshold
    altruism_coeff=results.altruism_value
    p=-1
    while p>-11:
       
       
        
            p_values,p_values_start,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users\
                =brd_setup_and_run(filename, I, f, L2, slowmode, p, altruism_threshold,altruism_coeff)
            if iterations>1:
                fajl=open('run_results/{}'.format(filename+("slow" if slowmode else "fast")+str(p)+str(altruism_threshold[0])+str(altruism_threshold[1])),"wb")
                pickle.dump(p_values,fajl)
                pickle.dump(p_values_start,fajl)
                pickle.dump(iterations,fajl)
                pickle.dump(social_welfare_array,fajl)
                pickle.dump(biggest_cost_array,fajl)
                pickle.dump(biggest_difference_array,fajl)
                pickle.dump(users,fajl)
                fajl.close()                
            p-=1

def run_social(results, I, f, L2,social_p):
    slowmode=results.slow
    filename=results.source_file.split(".")[0]
    altruism_threshold=results.altruism_threshold
    altruism_coeff=results.altruism_value
    p=social_p
    #print(filename,f,L2,altruism_threshold,altruism_coeff)
    
    while altruism_coeff<=1.0:
            p_values,p_values_start,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users\
                =brd_setup_and_run(filename,I,f,L2,slowmode,p,altruism_threshold,altruism_coeff)
            if iterations>1:
                fajl=open('run_results/{}'.format(filename+("slow" if slowmode else "fast")+str(p)+str(altruism_threshold[0])+str(altruism_threshold[1])+str(altruism_coeff)),"wb")
                pickle.dump(p_values,fajl)
                pickle.dump(p_values_start,fajl)
                pickle.dump(iterations,fajl)
                pickle.dump(social_welfare_array,fajl)
                pickle.dump(biggest_cost_array,fajl)
                pickle.dump(biggest_difference_array,fajl)
                pickle.dump(users,fajl)
                fajl.close()
            altruism_coeff+=0.1   

def run_one(results, I, f, L2):
    slowmode=results.slow
    p=results.fp_exponent
    filename=results.source_file.split(".")[0]
    altruism_threshold=results.altruism_threshold
    altruism_coeff=results.altruism_value
    
    while altruism_coeff<=1.0:
            p_values,p_values_start,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users\
                =brd_setup_and_run(filename,I,f,L2,slowmode,p,altruism_threshold,altruism_coeff)
            if iterations>-1:
                fajl=open('run_results/{}'.format(filename+("slow" if slowmode else "fast")+str(p)+str(altruism_threshold[0])+str(altruism_threshold[1])+str(altruism_coeff)),"wb")
                pickle.dump(p_values,fajl)
                pickle.dump(p_values_start,fajl)
                pickle.dump(iterations,fajl)
                pickle.dump(social_welfare_array,fajl)
                pickle.dump(biggest_cost_array,fajl)
                pickle.dump(biggest_difference_array,fajl)
                pickle.dump(users,fajl)
                fajl.close()        
            altruism_coeff+=0.1
def run_once(arguments, I, f, L2):
            p = arguments.fp_exponent
            slowmode=arguments.slow
            filename=arguments.source_file.split(".")[0]
            altruism_threshold=arguments.altruism_threshold
            altruism_value=arguments.altruism_value
           
            p_values,p_values_start,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users\
                =brd_setup_and_run(filename,I,f,L2,slowmode,p,altruism_threshold,altruism_value)
            if iterations>1:
                fajl=open('run_results/{}'.format(filename+("slow" if slowmode else "fast")+str(p)+str(altruism_threshold[0])+str(altruism_threshold[1])),"wb")
                pickle.dump(p_values,fajl)
                pickle.dump(p_values_start,fajl)
                pickle.dump(iterations,fajl)
                pickle.dump(social_welfare_array,fajl)
                pickle.dump(biggest_cost_array,fajl)
                pickle.dump(biggest_difference_array,fajl)
                pickle.dump(users,fajl)
                fajl.close()
def run_equil(arguments, I, f, L2):
   
        slowmode=arguments.slow
        filename=arguments.source_file.split(".")[0]
        altruism_threshold=arguments.altruism_threshold
        altruism_value=arguments.altruism_value

        altr=altruism_value
        while altr<=1.0:
            p = -1
            p_values,p_values_start,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users\
                =brd_setup_and_run(filename,I,f,L2,slowmode,p,altruism_threshold,altr)
            write_results(slowmode, filename, altruism_threshold, altr, p, p_values, p_values_start, iterations, social_welfare_array, biggest_cost_array, biggest_difference_array, users)

            p=-10
            p_values,p_values_start,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users\
                =brd_setup_and_run(filename,I,f,L2,slowmode,p,altruism_threshold,altr)
            if iterations>1:
                fajl=open('run_results/{}'.format(filename+("slow" if slowmode else "fast")+str(p)+str(altruism_threshold[0])+str(altruism_threshold[1])+str(altr)),"wb")
                pickle.dump(p_values,fajl)
                pickle.dump(p_values_start,fajl)
                pickle.dump(iterations,fajl)
                pickle.dump(social_welfare_array,fajl)
                pickle.dump(biggest_cost_array,fajl)
                pickle.dump(biggest_difference_array,fajl)
                pickle.dump(users,fajl)
                fajl.close()
            altr+=0.1 

def write_results(slowmode, filename, altruism_threshold, altr, p, p_values, p_values_start, iterations, social_welfare_array, biggest_cost_array, biggest_difference_array, users):
    if iterations>1:
        fajl=open('run_results/{}'.format(filename+("slow" if slowmode else "fast")+str(p)+str(altruism_threshold[0])+str(altruism_threshold[1])+str(altr)),"wb")
        pickle.dump(p_values,fajl)
        pickle.dump(p_values_start,fajl)
        pickle.dump(iterations,fajl)
        pickle.dump(social_welfare_array,fajl)
        pickle.dump(biggest_cost_array,fajl)
        pickle.dump(biggest_difference_array,fajl)
        pickle.dump(users,fajl)
        fajl.close()

def run_random_subset(arguments, G, message_cost, privacy_loss_cost,graph_halve_type,run_iterations,local_altruism):
        filename=arguments.source_file.split(".")[0]
        altruism_value=arguments.altruism_value
        
        degree_thin=graph_thinner(G,1)
        graph=G
        graphname="original"
        if graph_halve_type==0:
            graph=degree_thin
            graphname="degree"
        M2 = graph.number_of_edges()
        # Get the node with the highest incoming degree
        highest_indegree_node = max(graph, key=lambda node: graph.in_degree[node], default=None)

        # Get the incoming degree of the node
        highest_indegree = graph.in_degree[highest_indegree_node]
        f = message_cost
        privacy_loss_cost = float(f*(M2-highest_indegree))+1.0
        
        run_random_iter(privacy_loss_cost, run_iterations, local_altruism, filename, altruism_value, graph, graphname, f)

def run_random_iter(privacy_loss_cost, run_iterations, local_altruism, filename, altruism_value, graph, graphname, f):
    for i in range(run_iterations):
        logging.info("run parameters:graph name: %s local altruism: %d selection mode: RANDOM p_exponent: random threshold_exists: no \
                             altruism_value: %f iteration: %d",
                            graphname,local_altruism,altruism_value,i)
        logging.info("calcluate social optimum: False")
        p_values,p_values_start,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users,users_original\
                                =brd_setup_and_run(filename,graph,f,privacy_loss_cost,True,-1,[0,0],altruism_value,
                                                local_altruism,2,0.0,calculate_social_optimum=False)
        if iterations>-1:
           fajl=open('run_results/{}slowlocal{}_altr{}_{}_random_iteration{}_soFalse.txt'.format(filename, str(local_altruism), altruism_value, graphname,i), "wb")
           pickle.dump(p_values,fajl)
           pickle.dump(p_values_start,fajl)
           pickle.dump(iterations,fajl)
           pickle.dump(social_welfare_array,fajl)
           pickle.dump(biggest_cost_array,fajl)
           pickle.dump(biggest_difference_array,fajl)
           pickle.dump(users,fajl)
           pickle.dump(users_original,fajl)
           fajl.close()
        logging.info("calcluate social optimum: True, using users from previous run")
        p_values,p_values_start,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users,users_original\
                                =brd_setup_and_run(filename,graph,f,privacy_loss_cost,True,-1,[0,0],altruism_value,
                                                local_altruism,2,0.0,calculate_social_optimum=True,preset_users=users_original)
        if iterations>-1:
           fajl=open('run_results/{}slowlocal{}_altr{}_{}_random_iteration{}_soTrue.txt'.format(filename, str(local_altruism), altruism_value, graphname,i), "wb")
           pickle.dump(p_values,fajl)
           pickle.dump(p_values_start,fajl)
           pickle.dump(iterations,fajl)
           pickle.dump(social_welfare_array,fajl)
           pickle.dump(biggest_cost_array,fajl)
           pickle.dump(biggest_difference_array,fajl)
           pickle.dump(users,fajl)
           pickle.dump(users_original,fajl)
           fajl.close() 
             

def run_random(arguments, G, message_cost, privacy_loss_cost,graph_halve_type,run_iterations):
        filename=arguments.source_file.split(".")[0]
        altruism_value=arguments.altruism_value
        degree_thin,bc_thin=graph_thinner(G)
        graph=G
        graphname="original"
        if graph_halve_type==0:
            graph=degree_thin
            graphname="degree"
        elif graph_halve_type==1:
            graph=bc_thin
            graphname="bc"

        M2 = graph.number_of_edges()
        # Get the node with the highest incoming degree
        highest_indegree_node = max(graph, key=lambda node: graph.in_degree[node], default=None)

        # Get the incoming degree of the node
        highest_indegree = graph.in_degree[highest_indegree_node]
        f = message_cost
        privacy_loss_cost = float(f*(M2-highest_indegree))+1.0
        for local_altruism in [True,False]:
            run_random_iter(privacy_loss_cost, run_iterations, local_altruism, filename, altruism_value, graph, graphname, f)

def run_some(arguments, G, message_cost, privacy_loss_cost,graph_halve_type,selection,calculate_social_optimum=False):
        filename=arguments.source_file.split(".")[0]
        altruism_value=arguments.altruism_value
        degree_thin,bc_thin=graph_thinner(G)
        graph=G
        graphname="original"
        if graph_halve_type==0:
            graph=degree_thin
            graphname="degree"
        elif graph_halve_type==1:
            graph=bc_thin
            graphname="bc"

        M2 = graph.number_of_edges()

        # Get the node with the highest incoming degree
        highest_indegree_node = max(graph, key=lambda node: graph.in_degree[node], default=None)

        # Get the incoming degree of the node
        highest_indegree = graph.in_degree[highest_indegree_node]
        
        f = message_cost
        privacy_loss_cost = float(f*(M2-highest_indegree))+1.0
        bc_threshold=0.0
        threshold=[0,0]


        for local_altruism in [True,False]:
            if selection==0 or selection==1:

            
                for selection_mode in [0,1]:
                    for p_exponent in [-1,-10]:
                        for threshold_exist in [True,False]:

                            if selection_mode==0 and threshold_exist==True:
                                    threshold=[4,4]
                            elif selection_mode==1 and threshold_exist==True:
                                    bc_threshold=0.01
                            elif selection_mode==1 and threshold_exist==False:
                                    bc_threshold=0.0
                            elif selection_mode==0 and threshold_exist==False:
                                    threshold=[0,0]

                            
                            logging.info("run parameters:graph name: %s local altruism: %d selection mode: %d p_exponent: %d threshold_exists: %d altruism_value: %f",
                                            graphname,local_altruism,selection_mode,p_exponent,threshold_exist,altruism_value)
                            logging.info("calcluate social optimum: %s",str(calculate_social_optimum))
                            p_values,p_values_start,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users,asd\
                                    =brd_setup_and_run(filename,graph,f,privacy_loss_cost,True,p_exponent,threshold,altruism_value,
                                                    local_altruism,selection_mode,bc_threshold,calculate_social_optimum=calculate_social_optimum)
                            if iterations>-1:
                                fajl=open('run_results/{}slowlocal{}_altr{}_{}_Threshold{}_{}_{}_so{}.txt'.format(filename, str(local_altruism), altruism_value, graphname, 
                                                                                                                  str(threshold_exist), p_exponent, selection_mode,str(calculate_social_optimum)), "wb")
                                pickle.dump(p_values,fajl)
                                pickle.dump(p_values_start,fajl)
                                pickle.dump(iterations,fajl)
                                pickle.dump(social_welfare_array,fajl)
                                pickle.dump(biggest_cost_array,fajl)
                                pickle.dump(biggest_difference_array,fajl)
                                pickle.dump(users,fajl)
                                fajl.close()
            elif selection==3:
                degrees = dict(graph.degree())
                sorted_nodes_degree = sorted(degrees, key=lambda x: degrees[x],reverse=False)
                degree_lin=lin_dist(sorted_nodes_degree)
                degree_exp=halver([],sorted_nodes_degree)
                bc=nx.betweenness_centrality(graph)
                sorted_nodes_bc=sorted(bc,key=lambda x: bc[x],reverse=False)
                bc_lin=lin_dist(sorted_nodes_bc)
                bc_exp=halver([],sorted_nodes_bc)
                for ordering,name in zip([degree_lin,degree_exp,bc_lin,bc_exp],["degree_lin","degree_exp","bc_lin","bc_exp"]):
                    logging.info("run parameters:graph name: %s local altruism: %d selection mode: ordering %s threshold_exists: no altruism_value: %f",
                                graphname,local_altruism,name,altruism_value)
                    logging.info("calcluate social optimum: %s",str(calculate_social_optimum))
                    
                    p_values,p_values_start,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users,asd\
                                =brd_setup_and_run(filename,graph,f,privacy_loss_cost,True,-1,threshold,altruism_value,
                                                local_altruism,3,bc_threshold,ordering,calculate_social_optimum=calculate_social_optimum)
                    if iterations>-1:
                        fajl=open('run_results/{}slowlocal{}_altr{}_{}_ordering_{}_so{}.txt'.format(filename, str(local_altruism), altruism_value, graphname,name,str(calculate_social_optimum)), "wb")
                        pickle.dump(p_values,fajl)
                        pickle.dump(p_values_start,fajl)
                        pickle.dump(iterations,fajl)
                        pickle.dump(social_welfare_array,fajl)
                        pickle.dump(biggest_cost_array,fajl)
                        pickle.dump(biggest_difference_array,fajl)
                        pickle.dump(users,fajl)
                        fajl.close()


def run_test(arguments,G,f,privacy_loss_cost):
        filename=arguments.source_file.split(".")[0]
        altruism_value=arguments.altruism_value
        degree_thin,bc_thin=graph_thinner(G)
        for graph,graphname in zip([degree_thin,bc_thin],["degree","bc"]):
            M2 = graph.number_of_edges()
            # Get the node with the highest incoming degree
            highest_indegree_node = max(graph, key=lambda node: graph.in_degree[node], default=None)

            # Get the incoming degree of the node
            highest_indegree = graph.in_degree[highest_indegree_node]
            f = 1.0
            privacy_loss_cost = float(f*(M2-highest_indegree))+1.0
            bc_threshold=0.0
            threshold=[0,0]

            degrees = dict(graph.degree())
            sorted_nodes_degree = sorted(degrees, key=lambda x: degrees[x],reverse=False)
            degree_lin=lin_dist(sorted_nodes_degree)
            degree_exp=halver([],sorted_nodes_degree)
            bc=nx.betweenness_centrality(graph)
            sorted_nodes_bc=sorted(bc,key=lambda x: bc[x],reverse=False)
            bc_lin=lin_dist(sorted_nodes_bc)
            bc_exp=halver([],sorted_nodes_bc)
            
            for local_altruism in [True,False]:
                for selection_mode in [0,1]:
                    for p_exponent in [-1,-10]:
                       for threshold_exist in [True,False]:

                            if selection_mode==0 and threshold_exist==True:
                                 threshold=[4,4]
                            elif selection_mode==1 and threshold_exist==True:
                                 bc_threshold=0.01
                            elif selection_mode==1 and threshold_exist==False:
                                 bc_threshold=0.0
                            elif selection_mode==0 and threshold_exist==False:
                                 threshold=[0,0]

                            
                            logging.info("run parameters:graph name: %s local altruism: %d selection mode: %d p_exponent: %d threshold_exists: %d altruism_value: %f",
                                         graphname,local_altruism,selection_mode,p_exponent,threshold_exist,altruism_value)
                            p_values,p_values_start,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users\
                                    =brd_setup_and_run(filename,graph,f,privacy_loss_cost,True,p_exponent,threshold,0.5,
                                                    local_altruism,selection_mode,bc_threshold)
                            if iterations>1:
                                fajl=open('run_results/{}'.format(filename+("slow")+str("local:",local_altruism)+str(altruism_value)+(graphname)+("Threshold:",threshold_exist)
                                                                    +str(p_exponent)+(selection_mode)),"wb")
                                pickle.dump(p_values,fajl)
                                pickle.dump(p_values_start,fajl)
                                pickle.dump(iterations,fajl)
                                pickle.dump(social_welfare_array,fajl)
                                pickle.dump(biggest_cost_array,fajl)
                                pickle.dump(biggest_difference_array,fajl)
                                pickle.dump(users,fajl)
                                fajl.close()
                            #print("Running: ",filename,graph,f,privacy_loss_cost,True,p_exponent,threshold,0.5,local_altruism,selection_mode,bc_threshold)
                logging.info("run parameters:graph name: %s local altruism: %d selection mode: random p_exponent: random threshold_exists: no altruism_value: %f",
                            graphname,local_altruism,altruism_value)
                p_values,p_values_start,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users\
                                =brd_setup_and_run(filename,graph,f,privacy_loss_cost,True,-1,threshold,altruism_value,
                                                local_altruism,2,bc_threshold)
                if iterations>1:
                        fajl=open('run_results/{}'.format(filename+("slow")+str("local:",local_altruism)+str(altruism_value)+(graphname)+("random")),"wb")
                        pickle.dump(p_values,fajl)
                        pickle.dump(p_values_start,fajl)
                        pickle.dump(iterations,fajl)
                        pickle.dump(social_welfare_array,fajl)
                        pickle.dump(biggest_cost_array,fajl)
                        pickle.dump(biggest_difference_array,fajl)
                        pickle.dump(users,fajl)
                        fajl.close()
                for ordering,name in zip([degree_lin,degree_exp,bc_lin,bc_exp],["degree_lin","degree_exp","bc_lin","bc_exp"]):
                    logging.info("run parameters:graph name: %s local altruism: %d selection mode: ordering p_exponent: %s threshold_exists: no altruism_value: %f",
                                graphname,local_altruism,name,altruism_value)
                    
                    p_values,p_values_start,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,users\
                                =brd_setup_and_run(filename,graph,f,privacy_loss_cost,True,-1,threshold,altruism_value,
                                                local_altruism,3,bc_threshold,ordering)
                    if iterations>1:
                        fajl=open('run_results/{}'.format(filename+("slow")+str("local:",local_altruism)+str(altruism_value)+(graphname)+(name)),"wb")
                        pickle.dump(p_values,fajl)
                        pickle.dump(p_values_start,fajl)
                        pickle.dump(iterations,fajl)
                        pickle.dump(social_welfare_array,fajl)
                        pickle.dump(biggest_cost_array,fajl)
                        pickle.dump(biggest_difference_array,fajl)
                        pickle.dump(users,fajl)
                        fajl.close()