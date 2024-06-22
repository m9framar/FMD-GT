
from collections import defaultdict
import copy
import pickle

from matplotlib import ticker
import GT_charts as charts
import numpy as np
from GT_utilities import User, read_file, social_welfare_central
from GT_utilities import graph_thinner
import networkx as nx
import argparse
import matplotlib.pyplot as plt


helptext="  Press 1 for social welfare and simple fp-value distribution|    \
            Press 2 for display of selected users biggest cost over time|   \
            Press 3 for display of biggest achievable reduction in each iteration|  \
            Press 4 comparision of PoA/PoS| \
            Press 5 for display of final exponent rates based on incoming messages."


def graph_comparision():
    filename=input("Enter the name of the graph: ")
    filename='datasets/{}'.format(filename)
    graph1=read_file(filename)
    graph2=graph_thinner(graph1,1)
    filename=input("Enter the name of the graph: ")
    filename='datasets/{}'.format(filename)
    graph3=read_file(filename)
    graph4=graph_thinner(graph3,1)
    with open("priv_loss.txt","w") as file:
        f=1
        M=graph2.number_of_edges()
        highest_indegree=max(dict(graph2.in_degree()).values())
        privacy_loss_cost = float(f*(M-highest_indegree))+1.0
        file.write("Privacy loss cost for graph College halved: {}\n".format(privacy_loss_cost))
        M=graph4.number_of_edges()
        highest_indegree=max(dict(graph4.in_degree()).values())
        privacy_loss_cost = float(f*(M-highest_indegree))+1.0
        file.write("Privacy loss cost for graph EU halved: {}\n".format(privacy_loss_cost))

    # Transform the graphs to simple digraphs
    digraph1 = nx.DiGraph(graph1)
    digraph2 = nx.DiGraph(graph2)
    digraph3 = nx.DiGraph(graph3)
    digraph4 = nx.DiGraph(graph4)

    # Calculate pagerank and betweenness centrality for each graph
    pr1 = nx.pagerank(graph1)
    pr2 = nx.pagerank(graph2)
    pr3 = nx.pagerank(graph3)
    pr4 = nx.pagerank(graph4)

    bc1 = nx.betweenness_centrality(digraph1)
    bc2 = nx.betweenness_centrality(digraph2)
    bc3 = nx.betweenness_centrality(digraph3)
    bc4 = nx.betweenness_centrality(digraph4)

    # Calculate additional graph metrics
    density1 = nx.density(graph1)
    density2 = nx.density(graph2)
    density3 = nx.density(graph3)
    density4 = nx.density(graph4)

    cc1 = nx.average_clustering(digraph1)
    cc2 = nx.average_clustering(digraph2)
    cc3 = nx.average_clustering(digraph3)
    cc4 = nx.average_clustering(digraph4)

    deg1 = nx.degree_assortativity_coefficient(graph1)
    deg2 = nx.degree_assortativity_coefficient(graph2)
    deg3 = nx.degree_assortativity_coefficient(graph3)
    deg4 = nx.degree_assortativity_coefficient(graph4)

    # Get the number of nodes and edges for each graph
    nodes1 = len(graph1.nodes())
    nodes2 = len(graph2.nodes())
    nodes3 = len(graph3.nodes())
    nodes4 = len(graph4.nodes())

    edges1 = len(graph1.edges())
    edges2 = len(graph2.edges())
    edges3 = len(graph3.edges())
    edges4 = len(graph4.edges())

    # Get the top 10 nodes for each metric in each graph
    pr1_top10 = sorted(pr1.items(), key=lambda x: x[1], reverse=True)[:10]
    pr2_top10 = sorted(pr2.items(), key=lambda x: x[1], reverse=True)[:10]
    pr3_top10 = sorted(pr3.items(), key=lambda x: x[1], reverse=True)[:10]
    pr4_top10 = sorted(pr4.items(), key=lambda x: x[1], reverse=True)[:10]

    bc1_top10 = sorted(bc1.items(), key=lambda x: x[1], reverse=True)[:10]
    bc2_top10 = sorted(bc2.items(), key=lambda x: x[1], reverse=True)[:10]
    bc3_top10 = sorted(bc3.items(), key=lambda x: x[1], reverse=True)[:10]
    bc4_top10 = sorted(bc4.items(), key=lambda x: x[1], reverse=True)[:10]

    # Calculate the summed pagerank and betweenness centrality of the rest of the graph for each graph
    pr1_rest_sum = sum([pr for node, pr in pr1.items() if node not in [n for n, pr in pr1_top10]])
    pr2_rest_sum = sum([pr for node, pr in pr2.items() if node not in [n for n, pr in pr2_top10]])
    pr3_rest_sum = sum([pr for node, pr in pr3.items() if node not in [n for n, pr in pr3_top10]])
    pr4_rest_sum = sum([pr for node, pr in pr4.items() if node not in [n for n, pr in pr4_top10]])

    bc1_rest_sum = sum([bc for node, bc in bc1.items() if node not in [n for n, bc in bc1_top10]])
    bc2_rest_sum = sum([bc for node, bc in bc2.items() if node not in [n for n, bc in bc2_top10]])
    bc3_rest_sum = sum([bc for node, bc in bc3.items() if node not in [n for n, bc in bc3_top10]])
    bc4_rest_sum = sum([bc for node, bc in bc4.items() if node not in [n for n, bc in bc4_top10]])

    # Create the table

    headers = ['College', 'College halved', 'EU', 'EU halved']
    rows = [    'Summed PageRank of top 10 nodes',
                'Summed betweenness centrality of top 10 nodes',
                'Summed PageRank of rest of graph',
                'Summed betweenness centrality of rest of graph',
                'Graph density',
                'Average clustering coefficient',
                'Degree assortativity coefficient',
                'Number of nodes',
                'Number of edges']
    data = [[round(sum([pr for node, pr in pr1_top10]), 4), round(sum([pr for node, pr in pr2_top10]), 4), round(sum([pr for node, pr in pr3_top10]), 4), round(sum([pr for node, pr in pr4_top10]), 4)],
        [round(sum([bc for node, bc in bc1_top10]), 4), round(sum([bc for node, bc in bc2_top10]), 4), round(sum([bc for node, bc in bc3_top10]), 4), round(sum([bc for node, bc in bc4_top10]), 4)],
        [round(pr1_rest_sum, 4), round(pr2_rest_sum, 4), round(pr3_rest_sum, 4), round(pr4_rest_sum, 4)],
        [round(bc1_rest_sum, 4), round(bc2_rest_sum, 4), round(bc3_rest_sum, 4), round(bc4_rest_sum, 4)],
        [round(density1, 4), round(density2, 4), round(density3, 4), round(density4, 4)],
        [round(cc1, 4), round(cc2, 4), round(cc3, 4), round(cc4, 4)],
        [round(deg1, 4), round(deg2, 4), round(deg3, 4), round(deg4, 4)],
        [nodes1, nodes2, nodes3, nodes4],
        [edges1, edges2, edges3, edges4]]
    charts.table_all(data,rows,headers,"Graph Metrics Comparision","graphs")


    
def read_equilibra(file_name,poa_array,pos_array,social_p):
        dataset,delim,metadata=file_name.rpartition("-")
        # print(dataset)
        #print(metadata)
        szam=metadata[-3:]
        #print(szam)
        altruism_coeff=float(szam)
        #print(altruism_coeff)
        others=metadata[-5:-3]
        #print(others)
        try:
            newstring=dataset+str(social_p)+others+str(altruism_coeff)
            objects = read_binary(newstring)
            social_optimum=objects[3][-1]

            newstring=dataset+"-1"+others+str(altruism_coeff)
            objects = read_binary(newstring)
            #left=objects[3][-1]
            #print("left",left)
            pos=objects[3][-1]/social_optimum
            
            newstring=dataset+"-10"+others+str(altruism_coeff)
            objects = read_binary(newstring)
            #right=objects[3][-1]
            #print("right:",right)
            #print("left" if left>right else "right")
            poa=objects[3][-1]/social_optimum

            poa_array.append(poa)
            pos_array.append(pos)
        except IndexError:
            print("Indexing error, returning")
            return
        altruism_coeff+=0.1
        altr=round(altruism_coeff,1)
        if altr>1.0:
            return
        newstring=dataset+"-10"+others+str(altr)    
        read_equilibra(newstring,poa_array,pos_array,social_p)
#HA RÁNÉZÖNK EGY GRAFÁRA AKKOR A MTERIKÁI ALAPJÁN MEG LEHET-E HATÁROZNI HOGY MELY CSUCSOKNAK KELL ALTRUIZMUST ADNI
def read_binary(newstring):
    print("Reading from: "+newstring)
    objects=[]
    try:
        with open("run_results/{}".format(newstring),"rb") as file:
            while True:
                try:
                    objects.append(pickle.load(file))
                except EOFError:
                    break
        if len(objects)==0:
            print('Could not parse objects in binary')
    except FileNotFoundError:
        print("file not found")
    
    return objects
def compare_group(objects,graph,exponent):
    number_of_edges=graph.number_of_edges()
    sum_priv_cost=0
    sum_bw_cost=0
    active_users=0
    inactive_users=0
    p_values={-1:0,-2:0,-3:0,-4:0,-5:0,-6:0,-7:0,-8:0,-9:0,-10:0,"none":0}
    for i in objects[6]:
        if i.inactive==False or i.p_exponent==-1:
            active_users+=1
        else:
           
            inactive_users+=1
        sum_priv_cost+=i.priv_cost
        sum_bw_cost+=- 1*(i.incoming+i.p*(number_of_edges-i.incoming))
    for i in objects[6]:
        if i.p_exponent<=-1 and i.p_exponent>=-10:
            p_values[i.p_exponent]+=i.priv_cost
        else:
            p_values["none"]+=i.priv_cost
    for key,values in p_values.items():

        if objects[0][key]!=0:
            p_values[key]=values/objects[0][key]
    sum_of_values = sum(value for k, value in p_values.items() if k != exponent)

    # Create a list of keys where the value is more than 0
    keys_with_value_more_than_zero = [key for key, value in p_values.items() if value < 0]

    # Count the number of keys in the list
    num_keys_with_value_more_than_zero = len(keys_with_value_more_than_zero)
    
    if num_keys_with_value_more_than_zero>1 and p_values[exponent]!=0:
        denonimator=np.float64(sum_of_values/(num_keys_with_value_more_than_zero - 1))
        numerator=np.float64(p_values[exponent])
        comparison_result = numerator/denonimator
        if comparison_result<1:
            print("something is wrong")
            print("comparison_result",comparison_result)
            print("denonimator",denonimator)
            print("numerator",numerator)
            print("sum of values",sum_of_values)
            print("num keys",num_keys_with_value_more_than_zero)
            print("p_values",p_values)
            print("number os users",objects[0])
        p_values = {k: 0 for k in p_values}
    
        return comparison_result
    else:
        p_values = {k: 0 for k in p_values}
        print("No comparison possible")
        return 0
    
def read_m6_full(top_comparision,graph_name,altr_value,graph):
    run_results_list=[]
    graphname="degree"
    for string_local in ["True","False"]:
        for selection_mode in [0,1]:                  
            for threshold_exist in [True,False]:
                for p_exponent in [-1,-10]:
                    for calculate_social_optimum in [True,False]:
                            file_string='{}slowlocal{}_altr{}_{}_Threshold{}_{}_{}_so{}.txt'.format(graph_name, string_local, altr_value, graphname, 
                                                                                                                str(threshold_exist), p_exponent, selection_mode,str(calculate_social_optimum))
                            objects=read_binary(file_string)
                            selection_string="degree" if selection_mode==0 else "bc"
                            threshold_string="Threshold" if threshold_exist==True else "No Threshold"
                            p_exponent_string="all from -1" if p_exponent==-1 else "all from -10"
                            run_results_list.append([objects,"NE" if calculate_social_optimum==False else "SO",string_local,[selection_string,threshold_string,p_exponent_string]])
                            
                            comparision=compare_group(objects,graph,-1)
                            if comparision!=0:
                                string_of_key="NE" if calculate_social_optimum==False else "SO"
                                #     print("adding value to top comparision",comparision)
                                top_comparision[string_of_key].append(comparision)
    return run_results_list
def read_m7_full(top_comparision,graph_name,altr_value,graph):
    graphname="degree"
    run_results_list=[]   
    for string_local in ["True","False"]:
        for name in ["degree_lin","degree_exp","bc_lin","bc_exp"]:
            for calculate_social_optimum in [True,False]: 
                file_string="{}slowlocal{}_altr{}_{}_ordering_{}_so{}.txt".format(graph_name, string_local, altr_value, graphname,name,str(calculate_social_optimum))
                objects=read_binary(file_string)
                run_results_list.append([objects,"NE" if calculate_social_optimum==False else "SO",string_local,name])
                comparision=compare_group(objects,graph,-1)
                if comparision!=0:
                    string_of_key="NE" if calculate_social_optimum==False else "SO"
                    #     print("adding value to top comparision",comparision)
                    top_comparision[string_of_key].append(comparision)
    return run_results_list
def read_m8_full(top_comparision,graph_name,altr_value,graph,iteration_start,iteration_end):
    graphname="degree"
    run_results_list=[]
    for iteration in range(int(iteration_start),int(iteration_end)+1):
        for local in ["True","False"]:
            for calculate_social_optimum in [True,False]:
                file_string="{}slowlocal{}_altr{}_{}_random_iteration{}_so{}.txt".format(graph_name, local, altr_value, graphname,iteration,str(calculate_social_optimum))
                objects=read_binary(file_string)

                if len(objects)>0:
                    run_results_list.append([objects,"NE" if calculate_social_optimum==False else "SO",local,"random_{}".format(iteration)])
                    comparision=compare_group(objects,graph,-1)
                    if comparision!=0:
                        string_of_key="NE" if calculate_social_optimum==False else "SO"
                        #     print("adding value to top comparision",comparision)
                        top_comparision[string_of_key].append(comparision)
    return run_results_list
def get_dimensions(lst):
    if isinstance(lst, list):
        return [len(lst)] + get_dimensions(lst[0])
    else:
        return []
def calulate_equilibrium_meausure(objects):
    ne_local = [sublist[0] for sublist in objects if sublist[1] == "NE" and sublist[2]=="True"]
    sw_ne_local=[]
    for run in ne_local:
        sw_ne_local.append(run[3][-1])
   
    ne_local_min=min(sw_ne_local)
    ne_local_max=max(sw_ne_local)

    so_local = [sublist[0] for sublist in objects if sublist[1] == "SO" and sublist[2]=="True"]
    sw_so_local=[]
    for run in so_local:
        sw_so_local.append(run[3][-1])
    so_local_max=max(sw_so_local)
    PoA_local=ne_local_min/so_local_max
    PoS_local=ne_local_max/so_local_max


    ne_global = [sublist[0] for sublist in objects if sublist[1] == "NE" and sublist[2]=="False"]
    sw_ne_global=[]
    for run in ne_global:
        sw_ne_global.append(run[3][-1])
    ne_global_min=min(sw_ne_global)
    ne_global_max=max(sw_ne_global)

    so_global = [sublist[0] for sublist in objects if sublist[1] == "SO" and sublist[2]=="False"]
    sw_so_global=[]
    for run in so_global:
        sw_so_global.append(run[3][-1])
    so_global_max=max(sw_so_global)
    PoA_global=ne_global_min/so_global_max
    PoS_global=ne_global_max/so_global_max

    return [PoA_local,PoS_local,PoA_global,PoS_global]
def display_equilibria(graph_name, altr_value, results_m6,filename):
    equilibria=calulate_equilibrium_meausure(results_m6)
    equilibria_dict={
            "PoA":[equilibria[0],equilibria[2]],
            "PoS":[equilibria[1],equilibria[3]],
        }
    names_list=["Local","Global"]
    charts.barchart_comparision(equilibria_dict,names_list,
                                    "Comparison of PoA and PoS \n for local and global altruism models\nfor {} graph with altruism value:{}".format(graph_name,altr_value),
                                    "Equilibira measure value",
                                    filename,
                                    "Altruism model")
def sum_usercost(userlist,graph,message_cost=1):
    sum_bw_cost=0
    sum_priv_cost=0
    number_of_edges=graph.number_of_edges()
    for i in userlist:
        sum_priv_cost+=i.priv_cost
        sum_bw_cost+=- message_cost*(i.incoming+i.p*(number_of_edges-i.incoming))
    return [sum_priv_cost,sum_bw_cost]
def compare_setups(objects,graph,socialopt=False):
    best_run_local=[]
    best_run_global=[]
    best_run_value_local=0
    best_run_value_global=0
    
    ne_local = [[sublist[0], sublist[3]] for sublist in objects if sublist[1] == ("NE" if socialopt==False else "SO") and sublist[2]=="True"]
    ne_global = [[sublist[0], sublist[3]] for sublist in objects if sublist[1] == ("NE" if socialopt==False else "SO") and sublist[2]=="False"]

    for run in ne_local:      
        sumusercost=abs(sum(sum_usercost(run[0][6],graph)))
        best_run_local.append([round(sumusercost, 0),run[0][2],run[1]])

    best_run_local = sorted(best_run_local, key=lambda x: x[0])

    best_run_value_local = best_run_local[0][0]

    best_run_value_local_iter=best_run_local[0][1]




    for run in ne_global:  
        sumusercost=abs(sum(sum_usercost(run[0][6],graph)))
        best_run_global.append([round(sumusercost, 0),run[0][2],run[1]])

    best_run_global = sorted(best_run_global, key=lambda x: x[0])

    best_run_value_global = best_run_global[0][0]
    best_run_value_global_iter=best_run_global[0][1]


    # Store every run as a percentage of the best run value
    for run in best_run_local:
        run.append(round(best_run_value_local/run[0]*100, 2))
        run.append(round(run[1]/best_run_value_local_iter*100, 2))
    best_run_local = sorted(best_run_local, key=lambda x: x[1])

    for run in best_run_global:
        run.append(round(best_run_value_global/run[0]*100, 2))
        run.append(round(run[1]/best_run_value_global_iter*100, 2))
    best_run_global = sorted(best_run_global, key=lambda x: x[1])    

    return [best_run_local,best_run_global]


def user_analysis(runs, graph):
    # Find the top 10 nodes by betweenness centrality
    centrality = nx.betweenness_centrality(graph,normalized=True)
    top_nodes = sorted(centrality, key=centrality.get, reverse=True)[:10]
    bc_at_exponents_by_run={}
    top_users_by_bc_by_run={}
    users_at_exponents_by_run={}
    
    # Find the corresponding users for each run
    for run in runs:
        bc_at_exponents={-1:0,-2:0,-3:0,-4:0,-5:0,-6:0,-7:0,-8:0,-9:0,-10:0,"none":0}
        users_at_exponents={-1:[],-2:[],-3:[],-4:[],-5:[],-6:[],-7:[],-8:[],-9:[],-10:[],"none":[]}
        top_users_by_bc=[]
        #print("Run:", run[1:4])
        for user in run[0][6]:
            run_string = "Run: {}, {}, {}".format(run[1], run[2], run[3])
            #run_string = [run[1], run[2], run[3]]
            
            if user.p_exponent<=-1 and user.p_exponent>=-10:
                bc_at_exponents[user.p_exponent]+=centrality[user.id]
                users_at_exponents[user.p_exponent].append(user)
            else:
                bc_at_exponents["none"]+=centrality[user.id]
                users_at_exponents["none"].append(user)

            if user.id in top_nodes:
                top_users_by_bc.append(user)
            
        bc_at_exponents_by_run[run_string] = [bc_at_exponents,[run[1], run[2], run[3]]]
        top_users_by_bc_by_run[run_string]=[top_users_by_bc,[run[1], run[2], run[3]]]
        users_at_exponents_by_run[run_string]=users_at_exponents
    return bc_at_exponents_by_run,top_users_by_bc_by_run,users_at_exponents_by_run
#ordering users by exponents, and then observing a certain metric for each x-th percentile
def bc_division_by_precentile(users_at_exponents_by_run,graph,percentile=10):
    result_list=[]
    betweenness_centrality = nx.betweenness_centrality(graph)
    for run_string, user_dict in users_at_exponents_by_run.items():
        #print(run_string)
        #users in user_dict ordered into a list with lowest highest exponent first and "none" last
        users = [user_list for exponent, user_list in user_dict.items()]
        # Flatten the 'users' list
        users = [user for user_list in users for user in user_list]
        #taking the sum of the betweenness centrality of the users in the list for the first xth percentile
        percentile_list=[]
        for i in range(percentile, 101, percentile):
            end_index = i * len(users) // 100
            result=sum(betweenness_centrality[user.id] for user in users[:end_index])
            #print(f"Percentile {i}%:", result)
            percentile_list.append([i,result])
        result_list.append([run_string,percentile_list])
    return result_list



def sort_by_user_metrics(bc_at_exponents_by_run, top_users_by_bc_by_run):
    sorted_runs_exponents = sorted(bc_at_exponents_by_run.items(), key=lambda x: x[1][0][-1], reverse=True)
    # for run_string, bc_dict in sorted_runs_exponents:
    #     print(run_string)
        # for exponent, bc_value in bc_dict.items():
        #     print(f"Exponent {exponent}: {bc_value:.2f}")
        # print("\n")

    top_users_by_bc_by_run_with_count = {}
    for run_string, user_list in top_users_by_bc_by_run.items():
        count = 0
        for user in user_list[0]:
            if user.p_exponent == -1:
                count += 1
        top_users_by_bc_by_run_with_count[run_string] = [user_list, count]
    
    sorted_runs_topusers = sorted(top_users_by_bc_by_run_with_count.items(), key=lambda x: x[1][1], reverse=True)
                        

    # print("amount of tops users with exponent -1\n")
    # for run_string, top_users in sorted_runs_topusers:
    #      print(run_string+" "+str(top_users[1]))
        #  for user in top_users[0]:
        #      print(f"User {user.id}: {user.p_exponent}")
        #  print("\n")
    return sorted_runs_exponents, sorted_runs_topusers       
def user_metrics_boxplots(graph_name,altr_value,sorted_runs_exponents, sorted_runs_topusers,filename):
    bc_by_runtype = {
        "NE_local": [],
        "SO_local": [],
        "NE_global": [],
        "SO_global": []
    }
    numberof_topusers_at_exponent = {
        "NE_local": [],
        "SO_local": [],
        "NE_global": [],
        "SO_global": []
    }
    for run_string,topusers in sorted_runs_topusers:
        if topusers[0][1][0]=="NE":
            if topusers[0][1][1]=="True":
                numberof_topusers_at_exponent["NE_local"].append(topusers[1])
            else:
                numberof_topusers_at_exponent["NE_global"].append(topusers[1])
        else:
            if topusers[0][1][1]=="True":
                numberof_topusers_at_exponent["SO_local"].append(topusers[1])
            else:
                numberof_topusers_at_exponent["SO_global"].append(topusers[1])

    for run_string,bc_dict in sorted_runs_exponents:
        
        if bc_dict[1][0]=="NE":
            if bc_dict[1][1]=="True":
                bc_by_runtype["NE_local"].append(bc_dict[0][-1])
            else:
                bc_by_runtype["NE_global"].append(bc_dict[0][-1])
        else:
            if bc_dict[1][1]=="True":
                bc_by_runtype["SO_local"].append(bc_dict[0][-1])
            else:
                bc_by_runtype["SO_global"].append(bc_dict[0][-1])
    charts.boxchart_comparision([bc_by_runtype["NE_local"],bc_by_runtype["NE_global"],bc_by_runtype["SO_local"],bc_by_runtype["SO_global"]],
                                ["NE_local","NE_global","SO_local","SO_global"],
                                "[{}][{}]Betweenness centrality of -1 strategy users".format(graph_name,altr_value),
                                "Betweenness centrality\n nomrmalized and summed",
                                "Run type",
                                filename+"sumbctop")
    charts.boxchart_comparision([numberof_topusers_at_exponent["NE_local"],numberof_topusers_at_exponent["NE_global"],numberof_topusers_at_exponent["SO_local"],numberof_topusers_at_exponent["SO_global"]],
                                ["NE_local","NE_global","SO_local","SO_global"],
                                "[{}][{}]Number of top users with exponent -1".format(graph_name,altr_value),
                                "Number of top users with exponent -1",
                                "Run type",
                                filename+"numoftopusers")
    return bc_by_runtype,numberof_topusers_at_exponent
def read_runs(graph_name,altr_value_string,mode):
    filename=graph_name
    filename2='datasets/{}'.format(filename)
    graph=read_file(filename2)
    thin_graph=graph_thinner(graph,1)
    graph_name=filename.split(".")[0]
    altr_value=altr_value_string
    
    top_comparision={
        "NE":[],
        "SO":[],
    }
    if mode=="6":
        results_m6=read_m6_full(top_comparision,graph_name,altr_value,thin_graph)
        display_equilibria(graph_name, altr_value, results_m6,"m6_equilibira_{}_{}".format(graph_name,altr_value))
        compare_setups(results_m6,thin_graph)
        bc_at_exponents_by_run,top_users_by_bc_by_run,users_at_exponents_by_run = user_analysis(results_m6, thin_graph)
        sorted_exponent, sorted_top = sort_by_user_metrics(bc_at_exponents_by_run, top_users_by_bc_by_run)   
    if mode=="7":
        results_m7=read_m7_full(top_comparision,graph_name,altr_value,thin_graph)
    if mode=="8":
        results_m8=read_m8_full(top_comparision,graph_name,altr_value,thin_graph,0,9)
    if mode=="all":
        results_m6,results_m7,results_m8=[],[],[]
        results_m6=read_m6_full(top_comparision,graph_name,altr_value,thin_graph)
        print("dimensions of results_m6:",get_dimensions(results_m6))
        display_equilibria(graph_name, altr_value, results_m6,"m6_equilibira_{}_{}".format(graph_name,altr_value))
        results_m7=read_m7_full(top_comparision,graph_name,altr_value,thin_graph)
        print("dimensions of results_m7:",get_dimensions(results_m7))
        display_equilibria(graph_name, altr_value, results_m7,"m7_equilibira_{}_{}".format(graph_name,altr_value))
        results_m8=read_m8_full(top_comparision,graph_name,altr_value,thin_graph,0,9)
        if len(results_m8)>0:
            print("dimensions of results_m8:",get_dimensions(results_m8))
            display_equilibria(graph_name, altr_value, results_m8,"m8_equilibira_{}_{}".format(graph_name,altr_value))
            results_m6.extend(results_m8)
        results_m6.extend(results_m7)
        
        print("dimensions of results_m6:",get_dimensions(results_m6))

        display_equilibria(graph_name, altr_value, results_m6,"all_equilibira_{}_{}".format(graph_name,altr_value))
        for socialopt in [True,False]:
            NE_runs=compare_setups(results_m6,thin_graph,socialopt=socialopt)
            # for run in results_m6:
            #     print(run[1],run[2],run[3])
            #     print(abs(sum(sum_usercost(run[0][6],thin_graph))))

            
            bc_at_exponents_by_run,top_users_by_bc_by_run,users_at_exponents_by_run = user_analysis(results_m6, thin_graph)
            with open("{}_{}.txt".format(graph_name, altr_value), "w") as file:
                for run_string, user_dict in users_at_exponents_by_run.items():
                    file.write(run_string + "\n")
                    for user_list in user_dict[-1]:
                        file.write(f"Exponent {user_list.p_exponent}: {user_list.id}\n")
                    file.write("\n")
            bc_division_by_precentile(users_at_exponents_by_run,thin_graph)
            sorted_exponent, sorted_top = sort_by_user_metrics(bc_at_exponents_by_run, top_users_by_bc_by_run)
            for run_string, bc_dict in sorted_exponent:
                if bc_dict[1][0]==("NE" if socialopt==False else "SO"):
                    for run in NE_runs[0]:
                        if bc_dict[1][2]==run[2]  and bc_dict[1][1]=="True":
                            run.append(round(bc_dict[0][-1], 2))
                            #break
                    for run in NE_runs[1]:
                        if bc_dict[1][2]==run[2]  and bc_dict[1][1]=="False":
                            run.append(round(bc_dict[0][-1], 2))
                            #break
            for run_string, top_users in sorted_top:
                
                if top_users[0][1][0]==("NE" if socialopt==False else "SO"):
                    for run in NE_runs[0]:
                        if top_users[0][1][2]==run[2]  and top_users[0][1][1]=="True":
                            run.append(top_users[1])
                            #break
                    for run in NE_runs[1]:
                        if top_users[0][1][2]==run[2]  and top_users[0][1][1]=="False":
                            run.append(top_users[1])
                            #break
            
            NE_runs[0].sort(key=lambda x: x[3],reverse=True)
            NE_runs[1].sort(key=lambda x: x[3],reverse=True)


            rundata=[]
            collabels=["Sumcost","Iterations","SW %","Iter %","Sum of bc at -1","# of top10 at -1"]
            rowlabels=[]
            for run in NE_runs[0]:
                rowlabels.append("{}".format(run[2]))
                rundata.append([run[0],run[1],run[3],run[4],run[5],run[6]])
            charts.table_all(rundata,rowlabels,collabels, 
                            "{}[{}]_{}_local".format(graph_name,altr_value,("NE" if socialopt==False else "SO")),
                            "[{}][All][{}][{}]_local".format(graph_name,altr_value,("NE" if socialopt==False else "SO")))
            data_to_latex(rundata, rowlabels, collabels, "output_{}_{}_{}_{}.txt".format(graph_name,altr_value,("NE" if socialopt==False else "SO"),"local"))
            rundata=[]
            collabels=["Sumcost","Iterations","SW %","Iter %","Sum of bc at -1","# of top10 at -1"]
            rowlabels=[]
            for run in NE_runs[1]:
                rowlabels.append("{}".format(run[2]))
                rundata.append([run[0],run[1],run[3],run[4],run[5],run[6]])
            charts.table_all(rundata,rowlabels,collabels, 
                            "{}[{}]_{}_global".format(graph_name,altr_value,("NE" if socialopt==False else "SO")),
                            "[{}][All][{}][{}]_global".format(graph_name,altr_value,("NE" if socialopt==False else "SO")))
            data_to_latex(rundata, rowlabels, collabels, "output_{}_{}_{}_{}.txt".format(graph_name,altr_value,("NE" if socialopt==False else "SO"),"global"))
            

            charts.scatterplots_NE( graph_name,altr_value,
                                    NE_runs,
                                    "{}[{}]".format(graph_name,altr_value),
                                    socialopt)
            

        metrics_result=user_metrics_boxplots(graph_name,altr_value,
                                            sorted_exponent,sorted_top,
                                            "[{}][All][{}]_usermetrics_boxchart".format(graph_name,altr_value))
        charts.boxchart_comparision([top_comparision["NE"],top_comparision["SO"]],["NE","SO"],
                                 "[{}][All][{}] Comparison of -1 strategy priv.loss\n to the average of other strategies between NE and SO".format(graph_name,altr_value),
                                 "Ratio of -1 strategy priv.loss\n to the average of other strategies",
                                 "Difference between NE and SO ",
                                 "[{}][All][{}]_-1comp_boxchart".format(graph_name,altr_value))
def compare_datasets_across_runs(graph_name_1,graph_name_2):
    print("Comparing datasets")
    graph_1=read_file('datasets/{}'.format(graph_name_1))
    thin_graph_1=graph_thinner(graph_1,1)
    graph_name_1=graph_name_1.split(".")[0]
    graph_2=read_file('datasets/{}'.format(graph_name_2))
    thin_graph_2=graph_thinner(graph_2,1)
    graph_name_2=graph_name_2.split(".")[0]
    top_comparision={
        "NE":[],
        "SO":[],
    }
    all_runs={
        graph_name_1:{
            0.1:[],
            1.0:[],
        },
        graph_name_2:{
            0.1:[],
            1.0:[],
        }
    }
    all_runs_data=copy.deepcopy(all_runs)
    for graph_name in [graph_name_1,graph_name_2]:
        thin_graph=thin_graph_1 if graph_name==graph_name_1 else thin_graph_2
        for altruism_value in [0.1,1.0]:
            all_runs[graph_name][altruism_value].extend(read_m6_full(top_comparision,graph_name,str(altruism_value),thin_graph))
            all_runs[graph_name][altruism_value].extend(read_m7_full(top_comparision,graph_name,str(altruism_value),thin_graph))
            all_runs[graph_name][altruism_value].extend(read_m8_full(top_comparision,graph_name,str(altruism_value),thin_graph,0,9))
    #printing the sw_and_dist graph for every run stored
    # for dataset in [graph_name_1, graph_name_2]:
    #     for altruism in [0.1,1.0]:
    #         runs = all_runs[dataset][altruism]
    #         for run in runs:
    #             name = "{}_{}_{}_{}_{}".format(dataset, altruism, run[1], "Local" if run[2] == "True" else "Global", run[3])
    #             title = "{}[{}]_{}_{}\n{}".format(dataset, altruism, run[1], "Local" if run[2] == "True" else "Global", run[3])
    #             charts.sw_and_dist(name,run[0][0],run[0][1],run[0][2],run[0][3],title)
    
    # # get the list of runs for a guven dataset and altruism value
    # for dataset in [graph_name_1, graph_name_2]:
    #     for altruism in [0.1, 1.0]:
    #         #run a user analysis and a division by percentile scan
    #         bc_at_exponents_by_run,top_users_by_bc_by_run,users_at_exponents_by_run = user_analysis(all_runs[dataset][altruism], thin_graph_1 if dataset==graph_name_1 else thin_graph_2)
    #         all_runs_data[dataset][altruism]=bc_division_by_precentile(users_at_exponents_by_run,thin_graph_1 if dataset==graph_name_1 else thin_graph_2)
    #storing the best run data for each type
    best_runs = {
        graph_name_1: {
            0.1: {
                "SO": None,
                "NE": None
            },
            1.0: {
                "SO": None,
                "NE": None
            }
        },
        graph_name_2: {
            0.1: {
                "SO": None,
                "NE": None
            },
            1.0: {
                "SO": None,
                "NE": None
            }
        }
    }
    best_runs_data=copy.deepcopy(best_runs)
    #finding the best data for each type, for each dataset
    #opening a file for debugging
    with open("best_runs_search.txt", "w") as file:
        for altruism in [0.1, 1.0]:
            for solution in ["SO", "NE"]:
                for dataset in [graph_name_1, graph_name_2]:
                    best_run = None
                    best_value = float("inf")
                    for run in all_runs[dataset][altruism]:
                        if run[1] == solution:
                            sumusercost=abs(sum(sum_usercost(run[0][6],thin_graph_1 if dataset==graph_name_1 else thin_graph_2)))
                            #writing all the data to a file for debugging
                            file.write("Dataset: {}, Altruism: {}, Solution: {}\n".format(dataset, altruism, solution))
                            file.write("{} {} {}\n".format(run[1],run[2],run[3]))
                            file.write("Priv cost: {}, BW cost: {}\n".format(*sum_usercost(run[0][6],thin_graph_1 if dataset==graph_name_1 else thin_graph_2)))
                            file.write("Sumusercost: {}\n".format(sumusercost))


                            if sumusercost < best_value:
                                best_value = sumusercost
                                best_run = run
                    best_runs[dataset][altruism][solution] = best_run
    
    # query each run from best runs and run a user analysis and a division by percentile scan
    tabledata=[]
    rowlabels=[]
    with open("percentile_table_25.txt","w") as file:
        for dataset in [graph_name_1, graph_name_2]:
            for altruism in [0.1, 1.0]:
                for solution in ["SO", "NE"]:
                    run = best_runs[dataset][altruism][solution]
                    file.write("Dataset: {}, Altruism: {}, Solution: {}\n".format(dataset, altruism, solution))
                    if run is not None:
                        priv_cost, bw_cost = sum_usercost(run[0][6], thin_graph_1 if dataset==graph_name_1 else thin_graph_2)
                        bc_at_exponents_by_run,top_users_by_bc_by_run,users_at_exponents_by_run = user_analysis([run], thin_graph_1 if dataset==graph_name_1 else thin_graph_2)
                        bcpercentile=bc_division_by_precentile(users_at_exponents_by_run,thin_graph_1 if dataset==graph_name_1 else thin_graph_2)
                        bcpercentile_value=[round(float(value), 4) for percentage, value in bcpercentile[0][1]]
                        #for 25th, 50th and 75th percentile
                        bcpercentile_25=bc_division_by_precentile(users_at_exponents_by_run,thin_graph_1 if dataset==graph_name_1 else thin_graph_2,25)
                        bcpercentile_value_25=[round(float(value), 4) for percentage, value in bcpercentile_25[0][1]]
                        
                        best_runs_data[dataset][altruism][solution] = [bcpercentile_value,priv_cost,bw_cost,run[1],run[2],run[3]]
                        tabledata.append(bcpercentile_value+[round(float(priv_cost), 2),round(float(bw_cost), 2)]+["Local" if run[2]=="True" else "Global" ,run[3]])
                        file.write("percentile values: {}\n".format(bcpercentile_value_25))
                        file.write("Priv cost: {}, BW cost: {}\n".format(priv_cost, bw_cost))
                        file.write("Run: {}, {}, {}\n".format(run[1], "Local" if run[2]=="True" else "Global", run[3]))
                        #print(tabledata[-1])
                        
                        
                        rowlabels.append("{} {} {}".format(dataset,altruism,solution))
    #making a table of the best run data
    
    collabels=["BC 10th%","BC 20th%","BC 30th%","BC 40th%","BC 50th%","BC 60th%","BC 70th%","BC 80th%","BC 90th%","BC 100th%","Priv cost","BW cost","Altruism model","Selection mode"]
    charts.table_all(tabledata,rowlabels,collabels,
                        "Best runs comparison",
                        "Best runs comparison")
    #taking the first 10 items of each tabledata row and making a graph 
    # Define the percentiles
    percentiles = [f"{p}%" for p in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]]

    # Create a new figure and axis
    fig, ax = plt.subplots()
    ax.set_xlabel('Xth percentile')
    ax.set_ylabel('Summed BC of ordered users')
    ax.set_title('BC percentile change of the best runs')
    markers=["*","o","s","^","D","P","X","H","v","<"]
    # Iterate over the best runs
    for dataset in [graph_name_1, graph_name_2]:
        for altruism in [0.1, 1.0]:
            for solution in ["SO", "NE"]:
                # Get the bcpercentile data for the current best run
                bcpercentile = best_runs_data[dataset][altruism][solution][0]

                # Add a plot to the axis for the current best run
                linestyle = '--' if solution == "SO" else '-'
                marker = '*' if dataset == graph_name_1 else None
                ax.plot(percentiles, bcpercentile, linestyle=linestyle, marker=markers.pop(), label=f"{dataset} {altruism} {solution}")

    # Add a legend
    ax.legend()

    # Show the plot
    plt.savefig("best_runs_bcpercentile.png")
        
    
    



    
    #print the priv and bw cost of the best runs
    # for dataset in [graph_name_1, graph_name_2]:
    #     for altruism in [0.1, 1.0]:
    #         for solution in ["SO", "NE"]:
    #             if best_runs[dataset][altruism][solution] is not None:
    #                 print("Dataset: {}, Altruism: {}, Solution: {}".format(dataset, altruism, solution))
    #                 print("Priv cost: {}, BW cost: {}".format(*sum_usercost(best_runs[dataset][altruism][solution][0][6],thin_graph_1 if dataset==graph_name_1 else thin_graph_2)))
    
    

    # Define the datasets, altruism values, and solutions
    datasets = [graph_name_1, graph_name_2]
    altruism_values = [0.1, 1.0]
    solutions = ["SO", "NE"]

    # Initialize the figure and the axes with a larger size
    fig, ax = plt.subplots(figsize=(20, 12))

    # Define the color palettes for the two datasets
    colors = [['blue', 'lightblue'], ['orange', 'peachpuff']]
    altruism_ticks=[]
    solution_ticks=[]
    multiplier = 0
    bar_width = 0.25
    # Iterate over the datasets and altruism values
    for i, dataset in enumerate(datasets):
        for j, altruism in enumerate(altruism_values):
            for k, solution in enumerate(solutions):
                # Extract the best run
                best_run = best_runs[dataset][altruism][solution]
                
                # Calculate the private cost and bandwidth cost
                priv_cost, bw_cost = sum_usercost(best_run[0][6], thin_graph_1 if dataset == graph_name_1 else thin_graph_2)
                
                # Calculate the total cost
                total_cost = priv_cost + bw_cost
                
                # Calculate the percentage values
                priv_cost_perc = priv_cost / total_cost * 100
                bw_cost_perc = bw_cost / total_cost * 100
                
                # Calculate the adjusted bar position for the current solution
                
                
                # Create the stacked bar with specified colors
                rects_priv = ax.bar(multiplier, priv_cost_perc, width=bar_width, color=colors[i][0], 
                                    hatch='x' if i == 1 else None)
                
                rects_bw = ax.bar(multiplier, bw_cost_perc, bottom=priv_cost_perc, width=bar_width, color=colors[i][1])
                
                ax.bar_label(rects_priv, padding=3, labels=[f"{priv_cost_perc:.2f}%"],fontsize=20)
                
                altruism_ticks.append(multiplier + bar_width / 2)
                solution_ticks.append(multiplier )
                multiplier +=bar_width
            multiplier+=0.3
                
    ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    ax.set_xticks(solution_ticks)
    ax.set_xticklabels(["SO", "NE"] * len(datasets)*len(altruism_values))
    ax.set_xlabel("Solution type")
    secax = ax.secondary_xaxis(-0.1)
    secax.set_xticks(altruism_ticks[::2])
    secax.set_xticklabels(["0.1", "1.0"] * len(datasets))
    secax.set_xlabel("Altruism value")

    ax.set_ylabel("Percentage of total cost")
    ax.set_title("Comparison of private and bandwidth costs for the best runs")
    labels = ['DS1_priv', 'DS1_bw', 'DS2_priv', 'DS2_bw']

    handles = []
    
    colors_flat = [color for sublist in colors for color in sublist]
    for i, color in enumerate(colors_flat):
        handles.append(plt.Rectangle((0,0),1,1, color=color, hatch='x' if i==2 else None, ec='black'))

    # Add the legend
    ax.legend(handles, labels, loc='upper left',bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    fig.tight_layout()

    plt.savefig("cost_comparison.png")
    
    # ne_runs_0_1 = []
    # for run in run_data_all[0.1]:
    #     if run[1] == "NE":
    #         for key, values in run[0][1].items():
    #             if key != -1 and key != "none" and values > 0:
    #                 ne_runs_0_1.append(run)
    #                 break

    # ne_runs_1_0 = []
    # for run in run_data_all[1.0]:
    #     if run[1] == "NE":
    #         for key, values in run[0][1].items():
    #             if key != -1 and key != "none" and values > 0:
    #                 ne_runs_1_0.append(run)
    #                 break

    # for run_0_1, run_1_0 in zip(ne_runs_0_1, ne_runs_1_0):
    #     fp_values_0_1 = run_0_1[0][1]
    #     fp_values_1_0 = run_1_0[0][1]
    #     print("Run 0.1:", run_0_1[1], run_0_1[2], run_0_1[3])
    #     print(fp_values_0_1)
    #     print("Run 1.0:", run_1_0[1], run_1_0[2], run_1_0[3])
    #     print(fp_values_1_0)
def sw_central_calculation(graphs,altr_value):
    if altr_value==0.0:
        p_values_dict={}
        for graph in graphs:
            filename='datasets/{}'.format(graph)
            graph=read_file(filename)
            thin_graph=graph_thinner(graph,1)
            graph_name=filename.split("/")[1]
            graph_name=graph_name.split(".")[0]
            f=1
            M=graph.number_of_edges()
            highest_indegree=max(dict(graph.in_degree()).values())
            privacy_loss_cost = float(f*(M-highest_indegree))+1.0
            p_values=social_welfare_central(User,thin_graph,privacy_loss_cost,[0,0],f)
            p_values_dict[graph_name]=p_values
        #plotting the two datasets p values
        with open("p_values.txt", "w") as file:
            file.write(str(p_values_dict))
        charts.central_distr(p_values_dict,"eu_vs_college")
    else:
        for graph in graphs:
            filename='datasets/{}'.format(graph)
            graph=read_file(filename)
            thin_graph=graph_thinner(graph,1)     
def data_to_latex(rundata, rowlabels, collabels, filename):
    def escape_underscores(s):
        """Escape underscores in strings for LaTeX compatibility."""
        return s.replace("_", r"\_")
    with open(filename, 'w') as f:
        # Begin table and specify alignment for each column
        f.write("\\begin{tabular}{" + "l" * (len(collabels) + 1) + "}\n")
        f.write("\\hline\n")
        
        # Column labels
        f.write(" & ".join(collabels) + " \\\\\n")
        f.write("\\hline\n")
        
        # Data rows
        for label, row in zip(rowlabels, rundata):
            label = escape_underscores(label)
            row_str = [str(item) for item in row]
            f.write(label + " & " + " & ".join(row_str) + " \\\\\n")
            f.write("\\hline\n")
        
        f.write("\\hline\n")
        f.write("\\end{tabular}")

if __name__=="__main__":
    # file_name=input("Select data file to read:")
    # objects=[]
    # with open("run_results/{}".format(file_name),"rb") as file:
    #     while True:
    #         try:
    #             objects.append(pickle.load(file))
    #         except EOFError:
    #             break
    # if len(objects)==0:
    #     print('Could not parse objects in binary')
    #printmode=input("Select graph number to print or press h for help:")

    parser = argparse.ArgumentParser(description="Prints various features and data for the given graph and runs")
    parser.add_argument("-g", "--graph_name", nargs='+', type=str, help="The name(s) of the graph")
    parser.add_argument("-a", "--altr_value", type=str, help="The altruism value")
    parser.add_argument("printmode",type=str,help="data analysis mode")
    parser.add_argument("--mode", help="which running mode to analyze? 6/7/8/all", default="all")
    args = parser.parse_args()
    printmode=args.printmode
    
    if str.lower(printmode)=='h':
        print(helptext)
    elif int(printmode)==1:
        file_name=input("Select data file to read:")
        objects=read_binary(file_name)
        suptitle=input("Select suptitle:")
        charts.sw_and_dist(file_name,objects[0],objects[1],objects[2],objects[3],suptitle)
    elif int(printmode)==2:
        file_name=input("Select data file to read:")
        objects=read_binary(file_name)
        charts.biggest_costs(objects[2],objects[4],file_name) 
    elif int(printmode)==3:
        file_name=input("Select data file to read:")
        objects=read_binary(file_name)
        charts.biggest_cost_reduction(objects[2],objects[5],file_name)
    elif int(printmode)==4:
        file_name=input("Select data file to read:")
        social_p=input("social optimum run result staring p value:")
        poa_array=[]
        pos_array=[]
        read_equilibra(file_name,poa_array,pos_array,social_p)
        print(pos_array)
        print(poa_array)
        dataset,delim,metadata=file_name.rpartition("-")
        file_name=dataset
        charts.equlibra_chart(poa_array,pos_array,file_name)
             
    elif int(printmode)==5:
        file_name=input("Select data file to read:")
        objects=read_binary(file_name)
        cutoff1,cutoff2=input("Select cutoff point 1 and 2:").split()
        charts.dist_indegree(objects[6],objects[0],cutoff1,cutoff2,file_name)
    elif int(printmode)==6:
        file_name=input("Select data file to read:")
        objects=read_binary(file_name)
        filename=input("Select graph name:")
        filename2='datasets/{}'.format(filename)
        graph=read_file(filename2)
        thin_graph=graph_thinner(graph,1)
        number_of_edges=thin_graph.number_of_edges()
        print("total messages:",number_of_edges)
        sum_priv_cost=0
        sum_bw_cost=0
        print("final social welfare:",objects[3][-1])
        print("final-1 social welfare:",objects[3][-2])
        print("initial social welfare:",objects[3][0])
        print("initial+1 social welfare:",objects[3][1])
        print("final user setup at -1:")        
        for i in objects[6]:
            sum_priv_cost+=i.priv_cost
            sum_bw_cost+=- 1*(i.incoming+i.p*(number_of_edges-i.incoming))
            
            if i.p_exponent==-1:
                print(i.incoming,i.outgoing,i.cost)
        print("sum of private costs:",sum_priv_cost)
        print("sum of bandwidth costs:",sum_bw_cost)
    elif int(printmode)==7:
        graph_name=input("Select graph name:")
        altr_value=input("Select altruism value:")
        graph_halve=input("graph halving method:")
        iteration_start=input("Select iteration start:")
        iteration_end=input("Select iteration end:")
        i=int(iteration_start)
        array_local_altr=[]
        array_global_altr=[]
        while i<int(iteration_end)+1:
            filename='{}slowlocal{}_altr{}_{}_random_iteration{}.txt'.format(graph_name, "True", altr_value, graph_halve,i)
            objects=read_binary(filename)
            array_local_altr.append(objects[3][-1])
            print("local:",objects[3][-1])
            filename='{}slowlocal{}_altr{}_{}_random_iteration{}.txt'.format(graph_name, "False", altr_value, graph_halve,i)
            objects=read_binary(filename)
            array_global_altr.append(objects[3][-1])
            print("global:",objects[3][-1])
           
            i+=1
        filename="{}_{}_{}_{}_{}".format(graph_name,graph_halve,altr_value,iteration_start,iteration_end)
        charts.random_run_comparison((int(iteration_end)-int(iteration_start)),array_local_altr,array_global_altr,filename)
    elif int(printmode)==8:
        data=[]
        filename=input("Select graph name:")
        filename2='datasets/{}'.format(filename)
        graph=read_file(filename2)
        thin_graph=graph_thinner(graph,1)
        number_of_edges=thin_graph.number_of_edges()
        graph_name=filename.split(".")[0]
        altr_value=input("Select altruism value:")
        graphname="degree"
        question_social=input("Select social optimum? (True/False)")
        if str.lower(question_social)=="true":
            calculate_social_optimum=True
        else:
            calculate_social_optimum=False
        run_array={
            -1:[],
            -10:[],
        }


        names_list=[]
        for string_local in ["True","False"]:
            for selection_mode in [0,1]:                  
                for threshold_exist in [True,False]:
                    for p_exponent in [-1,-10]:
                            file_string='{}slowlocal{}_altr{}_{}_Threshold{}_{}_{}_so{}.txt'.format(graph_name, string_local, altr_value, graphname, 
                                                                                                                  str(threshold_exist), p_exponent, selection_mode,str(calculate_social_optimum))
                            objects=read_binary(file_string)
                            
                            sum_priv_cost=0
                            sum_bw_cost=0
                            active_users=0
                            inactive_users=0
                            for i in objects[6]:
                                if i.inactive==False or i.p_exponent==-1:
                                    active_users+=1
                                else:
                                    inactive_users+=1
                                sum_priv_cost+=i.priv_cost
                                sum_bw_cost+=- 1*(i.incoming+i.p*(number_of_edges-i.incoming))

                            run_array[p_exponent].append(abs(sum_priv_cost+sum_bw_cost))


                            data.append({"local":("Local" if string_local=="True" else "Global"),
                                         "selection_mode":("degree" if selection_mode==0 else "bc"),
                                         "start_p":str(p_exponent),
                                         "threshold_set":str(threshold_exist),
                                         "final_social":str(int(objects[3][-1])),
                                         "sum_priv_cost":str(int(sum_priv_cost)),
                                         "sum_bw_cost":str(int(sum_bw_cost)),
                                         "active_users":str(active_users),
                                         "inactive_users":str(inactive_users)})
                    string="{}\n{}\n{}".format(("Local" if string_local=="True" else "Global"),
                            ("degree" if selection_mode==0 else "bc"),
                            ("Thrshld_yes" if threshold_exist==True else "Thrshld_no"))
                    names_list.append(string)
        charts.table_m6(data,"{}_{}_{}".format(graph_name,altr_value,("NE" if calculate_social_optimum==False else "SO")))
        charts.barchart_comparision(run_array,names_list)

    elif int(printmode)==9:
        data=[]
        filename=input("Select graph name:")
        filename2='datasets/{}'.format(filename)
        graph=read_file(filename2)
        thin_graph=graph_thinner(graph,1)
        number_of_edges=thin_graph.number_of_edges()
        graph_name=filename.split(".")[0]
        altr_value=input("Select altruism value:")
        graphname="degree"
        p_values={-1:0,-2:0,-3:0,-4:0,-5:0,-6:0,-7:0,-8:0,-9:0,-10:0,"none":0}
        for calculate_social_optimum in [True,False]:     
            for string_local in ["True","False"]:
                for name in ["degree_lin","degree_exp","bc_lin","bc_exp"]:
                    file_string="{}slowlocal{}_altr{}_{}_ordering_{}_so{}.txt".format(graph_name, string_local, altr_value, graphname,name,str(calculate_social_optimum))
                    objects=read_binary(file_string)
                    sum_priv_cost=0
                    sum_bw_cost=0
                    active_users=0
                    inactive_users=0
                    for i in objects[6]:

                        p_values[i.p_exponent]+=i.priv_cost
                        if i.inactive==False or i.p_exponent==-1:
                            active_users+=1
                        else:
                            p_values["none"]+=1
                            inactive_users+=1
                        sum_priv_cost+=i.priv_cost
                        sum_bw_cost+=- 1*(i.incoming+i.p*(number_of_edges-i.incoming))
                    data.append({   "local":("Local" if string_local=="True" else "Global"),
                                    "ordering":name,
                                    "final_social":str(int(objects[3][-1])),
                                    "sum_priv_cost":str(int(sum_priv_cost)),
                                    "sum_bw_cost":str(int(sum_bw_cost)),
                                    "active_users":str(active_users),
                                    "inactive_users":str(inactive_users)    })
                    #reset p_values
                    p_values = {k: 0 for k in p_values}
            charts.table_m7(data,"{}_{}_{}".format(graph_name,altr_value,("NE" if calculate_social_optimum==False else "SO")))
    elif int(printmode)==10:
        data_NE=[]
        data_SO=[]
        filename=input("Select graph name:")
        filename2='datasets/{}'.format(filename)
        graph=read_file(filename2)
        thin_graph=graph_thinner(graph,1)
        number_of_edges=thin_graph.number_of_edges()
        graph_name=filename.split(".")[0]
        altr_value=input("Select altruism value:")
        graphname="degree"
        local=input("Select local mode (True/False):")
        iteration_start=input("Select iteration start:")
        iteration_end=input("Select iteration end:")

        run_array={
            "NE":[],
            "SO":[],
        }
        #p_values stores the sum of priv_cost for each p_exponent and then averages it
        p_values={-1:0,-2:0,-3:0,-4:0,-5:0,-6:0,-7:0,-8:0,-9:0,-10:0,"none":0}
        p_values_list_NE={}
        #how does the -1 strategy compare to the others in regards to the sum of priv_cost
        top_comparision={
            "NE":[],
            "SO":[],
        }
        p_values_list_SO={}
        names_list=[]
        for iteration in range(int(iteration_start),int(iteration_end)+1):
            file_string="{}slowlocal{}_altr{}_{}_random_iteration{}_so{}.txt".format(graph_name, local, altr_value, graphname,iteration,str(False))
            objects_NE=read_binary(file_string)
            sum_priv_cost=0
            sum_bw_cost=0
            active_users=0
            inactive_users=0
            for i in objects_NE[6]:
                p_values[i.p_exponent]+=i.priv_cost
                if i.inactive==False or i.p_exponent==-1:
                    active_users+=1
                else:
                    p_values["none"]+=1
                    inactive_users+=1
                sum_priv_cost+=i.priv_cost
                sum_bw_cost+=- 1*(i.incoming+i.p*(number_of_edges-i.incoming))
            run_array["NE"].append(abs(sum_priv_cost+sum_bw_cost))
            data_NE.append({   "local":("Local" if local=="True" else "Global"),
                            "run_number":iteration,
                            "final_social":str(int(objects_NE[3][-1])),
                            "sum_priv_cost":str(int(sum_priv_cost)),
                            "sum_bw_cost":str(int(sum_bw_cost)),
                            "active_users":str(active_users),
                            "inactive_users":str(inactive_users)    })
            #calculate average priv_cost for each p_exponent
            for key,values in p_values.items():
                
                if objects_NE[0][key]!=0:
                    p_values[key]=values/objects_NE[0][key]
                
            p_values_list_NE[iteration] = p_values
            sum_of_values = sum(value for k, value in p_values.items() if k != -1)
            # Create a list of keys where the value is more than 0
            keys_with_value_more_than_zero = [key for key, value in p_values.items() if value < 0]

            # Count the number of keys in the list
            num_keys_with_value_more_than_zero = len(keys_with_value_more_than_zero)
            # print("num_keys_with_value_more_than_zero: ",num_keys_with_value_more_than_zero)
            # print("-1 strategy: ",p_values[-1])
            # print("sum of other strategies: ",sum_of_values)
            # print("avgerge of sum of other strategies: ",sum_of_values/(num_keys_with_value_more_than_zero - 1))
            comparision = p_values[-1]/(sum_of_values/(num_keys_with_value_more_than_zero - 1))
            print("-1 compared to average of others: ",comparision)
            top_comparision["NE"].append(comparision)

            #reset p_values
            p_values = {k: 0 for k in p_values}

            print("NE done, starting SO")
            file_string="{}slowlocal{}_altr{}_{}_random_iteration{}_so{}.txt".format(graph_name, local, altr_value, graphname,iteration,str(True))
            objects_SO=read_binary(file_string)
            sum_priv_cost=0
            sum_bw_cost=0
            active_users=0
            inactive_users=0
            for i in objects_SO[6]:
                p_values[i.p_exponent]+=i.priv_cost
                if i.inactive==False or i.p_exponent==-1:
                    active_users+=1
                else:
                    p_values["none"]+=1
                    inactive_users+=1
                sum_priv_cost+=i.priv_cost
                sum_bw_cost+=- 1*(i.incoming+i.p*(number_of_edges-i.incoming))
            run_array["SO"].append(abs(sum_priv_cost+sum_bw_cost))
            data_SO.append({   "local":("Local" if local=="True" else "Global"),
                            "run_number":iteration,
                            "final_social":str(int(objects_SO[3][-1])),
                            "sum_priv_cost":str(int(sum_priv_cost)),
                            "sum_bw_cost":str(int(sum_bw_cost)),
                            "active_users":str(active_users),
                            "inactive_users":str(inactive_users)    })
            for key,values in p_values.items():
                             
                if objects_SO[0][key]!=0:
                    p_values[key]=values/objects_SO[0][key]
                
            p_values_list_SO[iteration] = p_values
            sum_of_values = sum(value for k, value in p_values.items() if k != -1)
            # Create a list of keys where the value is more than 0
            keys_with_value_more_than_zero = [key for key, value in p_values.items() if value < 0]

            # Count the number of keys in the list
            num_keys_with_value_more_than_zero = len(keys_with_value_more_than_zero)
            # print("num_keys_with_value_more_than_zero: ",num_keys_with_value_more_than_zero)
            # print("-1 strategy: ",p_values[-1])
            # print("sum of other strategies: ",sum_of_values)
            # print("avgerge of sum of other strategies: ",sum_of_values/(num_keys_with_value_more_than_zero - 1))
            comparision = p_values[-1]/(sum_of_values/(num_keys_with_value_more_than_zero - 1))
            print("-1 compared to average of others: ",comparision)
            top_comparision["SO"].append(comparision)
            names_list.append("Iteration\n{}".format(iteration))
        #print(p_values_list_NE)
        charts.boxchart_comparision([top_comparision["NE"],top_comparision["SO"]],["NE","SO"],
                                    "[EU][Random][0.1]Comparision of -1 strategy priv.loss\n to the average of other strategies between NE and SO",
                                    "Ratio of -1 strategy priv.loss\n to the average of other strategies")
        #charts.barchart_comparision(top_comparision,names_list,"[EU][Random][0.1]Comparision of -1 strategy priv.loss to the average of other strategies over different setups","Ratio of -1 strategy priv.loss to the average of other strategies")
        
        # charts.barchart_comparision(run_array,names_list)
        # charts.table_m8(data_NE,"{}_{}_{}".format(graph_name,altr_value,"NE"))
        # charts.table_m8(data_SO,"{}_{}_{}".format(graph_name,altr_value,"SO"))
    elif int(printmode)==11:
        read_runs(args.graph_name[0],args.altr_value,args.mode)
    elif int(printmode)==12:
        graph_comparision()
    elif int(printmode)==13:
        compare_datasets_across_runs(args.graph_name[0],args.graph_name[1])
    elif int(printmode)==14:
        sw_central_calculation(args.graph_name,float(args.altr_value))
    else:
        print("Invalid input")
    