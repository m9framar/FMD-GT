import numpy as np
import math
import networkx as nx
import multiprocessing as mp
import logging
import copy
import os
# logging.basicConfig(filename='BRD.log', filemode='a', format='%(asctime)s - %(name)s - %(threadName)s - %(thread)d - %(levelname)s - %(message)s'
#                     ,datefmt='%d-%b-%y %H:%M:%S',level=logging.DEBUG)
class User:
    selfish = 0
    altruist = 0
    cooperative=0
    #altruism_value_base=0.000

    def __init__(self, p, p_exponent ,incoming,breach_cost,cost=0,type=0\
                ,altruism_value=0.0,outgoing=0,id=0,
                neighbours=[]):
        if type==2 :
            self.altruism = altruism_value
            self.p_exponent = p_exponent
            self.inactive=False
            self.p = p           
            User.altruist += 1
        elif type==1:
            self.altruism = 0
            self.p = p
            self.p_exponent = p_exponent
            self.inactive=False
            User.cooperative+=1
        else:
            self.p=0
            self.altruism=0
            self.p_exponent = 0
            self.inactive=True      
            User.selfish += 1
        
         
        self.breach_loss = breach_cost
           
        self.incoming = incoming
        self.outgoing=outgoing
        self.cost = cost
        self.priv_cost=0
        self.id=id
        self.neighbours=neighbours
        
    def update_exponent(self,exponent):
        if(exponent<-10):
            self.p_exponent=-11
            self.p=0
            self.inactive=True
        elif exponent >-1:
            self.p_exponent=-1
            self.p=np.float64(math.pow(2, self.p_exponent))
            self.inactive=True
        else:
            self.p_exponent=exponent
            self.p=np.float64(math.pow(2, exponent))
            self.inactive=False
    def increase_exponent(self,count=1):     
            self.p_exponent+=count
            if self.p_exponent>=-1:
                self.p_exponent=-1
                self.inactive=True
            elif self.p_exponent<-1 and self.p_exponent>=-10:
                self.inactive=False
            self.p=np.float64(math.pow(2, self.p_exponent))
    def decrease_exponent(self,count=1):
        if count<0:
            logging.debug("invalid settings: %d",count)
            return
        self.p_exponent-=count
        if(self.p_exponent<-10):
            self.p=0
            self.p_exponent=-11
            self.inactive=True
        else:
            self.p=np.float64(math.pow(2, self.p_exponent))
    def update_cost(self,user_linkage,M,message_cost):
        self.priv_cost=-self.breach_loss * (1.0-(math.pow(1.0-user_linkage, self.incoming)))
        self.cost=  self.priv_cost\
                    - message_cost*(self.incoming+self.p*(M-self.incoming))\
                    
        
def refresh_costs(users,M,f,local_altruism):

    sum_cost=0.0
    others_privacy=0.0
    for i in users:  # refreshing linakges concerning privacy loss
        user_linkage = np.float64(1.0)
       
        for u in users: #calculating total exposure due to other users
            if i != u: 
                
                user_linkage *= (1.0-u.p)
                
        
            
        
        i.update_cost(user_linkage,M,f)
        others_privacy+=i.priv_cost
        sum_cost += i.cost
    for i in users:
        if i.altruism>0.0 and local_altruism==False:
            i.cost+=i.altruism*(others_privacy-i.priv_cost)
            sum_cost+=i.altruism*(others_privacy-i.priv_cost)
        elif i.altruism>0.0 and local_altruism==True:
            neighbours_cost=0.0
            for n in i.neighbours:
               neighbours_cost+=i.neighbours[n].priv_cost
            i.cost+=i.altruism*neighbours_cost
            sum_cost+=i.altruism*neighbours_cost
               
    return sum_cost
def dictionary_update(users,dictionary):
    for i in users:
        if i.p_exponent<=-1 and i.p_exponent>=-10:
            dictionary[i.p_exponent]+=1
        elif i.inactive==True:
            dictionary['none']+=1
        else:
            dictionary['none']+=1   
def generate_users(I,User,altruism_threshold,privacy_loss_cost,p_exponent,altr_coef=0.0,selection_mode=0,bc_threshold=0.01):
    users=[]
    p_eu=np.float64(math.pow(2,p_exponent))
    users_dict={}
    if selection_mode==1:
        bc=nx.betweenness_centrality(I,normalized=True)
    for i in I:
        new_dict = {**dict.fromkeys(I.neighbors(i), True), **dict.fromkeys(I.predecessors(i), True)}
        if selection_mode==0:
            if I.in_degree(i)<=altruism_threshold[0] and I.out_degree(i)<=altruism_threshold[0]:
                user = User(0,0,I.in_degree(i),privacy_loss_cost,type=0,outgoing=I.out_degree(i),
                            id=i,neighbours=new_dict)  
            # elif I.in_degree(i)>altruism_threshold[0] and I.in_degree(i)<=altruism_threshold[1] and I.out_degree(i)<=altruism_threshold[1] :
            #     user = User(p_eu,p_exponent,I.in_degree(i),privacy_loss_cost,type=1,outgoing=I.out_degree(i))
                
                
            else:
                user = User(p_eu,p_exponent, I.in_degree(i),privacy_loss_cost,type=2,altruism_value=altr_coef,outgoing=I.out_degree(i),
                            id=i,neighbours=new_dict)
                #print(I.in_degree(i))
        if selection_mode==1:
            
            if bc[i]<=bc_threshold:
                    user = User(0,0,I.in_degree(i),privacy_loss_cost,type=0,outgoing=I.out_degree(i),
                            id=i,neighbours=new_dict)
            else:
                    user = User(p_eu,p_exponent, I.in_degree(i),privacy_loss_cost,type=2,altruism_value=altr_coef,outgoing=I.out_degree(i),
                            id=i,neighbours=new_dict)
        if selection_mode==2:
            random_number = np.random.randint(1, 11)
            p_value=np.float64(math.pow(2,-random_number))
            user = User(p_value,-random_number, I.in_degree(i),privacy_loss_cost,type=2,altruism_value=altr_coef,outgoing=I.out_degree(i),
                        id=i,neighbours=new_dict)
        if selection_mode==3:
            p_exponent=I.nodes[i]["fp-value"]
            p_eu=np.float64(math.pow(2,p_exponent))
            user = User(p_eu,p_exponent, I.in_degree(i),privacy_loss_cost,type=2,altruism_value=altr_coef,outgoing=I.out_degree(i),
                        id=i,neighbours=new_dict)
            user.update_exponent(p_exponent)

        users.append(user)
        users_dict[i]=user
    for i in users:
        
        for j in i.neighbours:
             
            i.neighbours[j]=users_dict[j]
            
    return users
def read_file(filename):


    I=nx.read_edgelist(filename,delimiter=',',
                        create_using=nx.MultiDiGraph(),
                        nodetype=int,
                        data=(("time",int),))
   
    return I
 #segedfuggveny a tobbprocesszoros megvalositashoz
def refresh_costs_mp_help(index,user_array,messages,message_cost,current_cost,queue,local_altruism):
    usercost=user_array[index].cost
    p=user_array[index].p_exponent
    epsilon = np.float64(math.pow(10,-5))
    usercost_epsilon=usercost*(1-epsilon)

    user_array[index].decrease_exponent()
    temp_cost=refresh_costs(user_array,messages,message_cost,local_altruism)
    
    usercost1=user_array[index].cost
    diff=usercost-usercost1
    diff2=0
    usercost2=current_cost
    if p <-1:
        user_array[index].increase_exponent(2)
        temp_cost2=refresh_costs(user_array,messages,message_cost,local_altruism)
        
        usercost2=user_array[index].cost
        diff2=usercost-usercost2
    #queue.put([usercost1,index,0,usercost_epsilon,usercost])
    if usercost1>=usercost_epsilon and (usercost1>usercost2 or p==-1):
        #queue.put([usercost1,index,0])
        queue.put([diff,index,0,usercost_epsilon,usercost1,current_cost,temp_cost])
    elif usercost2>usercost_epsilon and (usercost2>usercost1):
        #queue.put([usercost2,index,1])
        queue.put([diff2,index,1,usercost_epsilon,usercost1,current_cost,temp_cost2])  
def refresh_cost_mp_help_social(index,user_array,messages,message_cost,current_cost,queue,local_altruism):
   
    p=user_array[index].p_exponent
    original_cost=user_array[index].cost

    user_array[index].decrease_exponent()
    temp_cost=refresh_costs(user_array,messages,message_cost,local_altruism)
    diff=current_cost-temp_cost
    changed_cost=user_array[index].cost
    

    diff2=0
    
    if p <-1:
        user_array[index].increase_exponent(2)
        temp_cost2=refresh_costs(user_array,messages,message_cost,local_altruism)
        diff2=current_cost-temp_cost2
        changed_cost2=user_array[index].cost
        
    if diff<=diff2 and diff<0:
        queue.put([diff,index,0,original_cost,changed_cost,current_cost,temp_cost])
    elif diff2<diff and diff2<0:
        queue.put([diff2,index,1,original_cost,changed_cost2,current_cost,temp_cost2])
# minden agentet megszámolni és kiszámolni a személyes costjukat a rendszer által ajánlott fp érték mellett
# megkeresni a következő legvalószínűbb deviátort
# átírni az fp értékét
# nyomon követni a rendszer állapotát
# repeat addig amíg nem már senkinek sem éri meg váltani 
def brd(eu_users, edge_number, f,p_values,slow,local_altruism,calculate_social_optimum=False):
    
 
    #kezdeti ertek megallapitasa
    
    
    sum_eu_start=refresh_costs(eu_users,edge_number,f,local_altruism)
    
    sum_cost_new = sum_eu_start
    sum_cost_old = sum_eu_start*2
    biggest_cost_array=[]
    social_welfare_array=[]
    social_welfare_array.append(sum_eu_start)
    biggest_difference_array=[]
# epsilon-PNE megkeresése best response dynamics implementálásával
    epsilon = np.float64(math.pow(10,-5))
    iterations = 0
    manager=mp.Manager()
    queue=manager.Queue()
    #altruist_users=[]
    done=False
    # for user in eu_users:
    #     if user.altruism>0.0:
    #         altruist_users.append(user)
    while(done==False and iterations <10000):
        done=True
        if iterations%100==0:
            logging.debug("current iteration is: %d",iterations)
            logging.info("current social welfare %f",sum_cost_new)
        if calculate_social_optimum==True:
            sum_cost_old = sum_cost_new  
        biggest_cost=0.0
        biggest_index=0
        biggest_difference=0
        #változtatás iránya, ha igaz, akkor csökkenteni kell, ha hamis akkor növelni kell
        #a user p_exponens értékét
        direction_decrease_down=True
        #lett-e ertelmes elorelepes, false ra allitodik ha igen
        

        #KORREKT IMPLEMENTÁCIÓ
        #Legnagyobb cost decrease alapjan vegigmenni
        if slow==True:
            array_index=0
                      
            with mp.Pool(os.cpu_count())as pool:
                for i in eu_users:
                    
                    if i.inactive==False:

                        #logging.debug("particular user cost %f,and p_value %d",\
                         #   eu_users[array_index].cost,eu_users[array_index].p_exponent)
                        
                        if calculate_social_optimum==False:
                            pool.apply_async(refresh_costs_mp_help,
                            [array_index,eu_users.copy(),edge_number,f,sum_cost_new,queue,local_altruism])
                        elif calculate_social_optimum==True:
                            pool.apply_async(refresh_cost_mp_help_social,
                            [array_index,eu_users.copy(),edge_number,f,sum_cost_new,queue,local_altruism])
                        

                    array_index+=1
                pool.close()
                pool.join()
                
                #logging.debug("The pool is closed")
            #logging.debug("Reading from queue with size %d",queue.qsize())
            biggest_difference=0 #garantáltan kisebbek mint nulla
            
            #logging.info("current social welfare %f",sum_cost_new)
            if(queue.empty()==False): done=False
            while(queue.empty()==False):
                eredmeny=queue.get()
                #logging.debug("%f %d %d %f %f", eredmeny[0],eredmeny[1],eredmeny[2],eredmeny[3],eredmeny[4])
                # logging.debug("difference %f index:%d up or down: %d", eredmeny[0],eredmeny[1],eredmeny[2])
                # logging.debug("usercost-epsilon %f, changed_cost %f",eredmeny[3],eredmeny[4])
                # logging.debug("current cost %f, new cost %f",eredmeny[5],eredmeny[6])
                if eredmeny[0]<biggest_difference:
                    biggest_difference=eredmeny[0]
                    biggest_index=eredmeny[1]
                    # logging.debug("Biggest difference is %f",biggest_difference)
                    biggest_cost=eu_users[biggest_index].cost
                    #0 a csokkentes, 1 a noveles
                    direction_decrease_down=True if eredmeny[2]==0 else False
            # logging.debug("Reading from queue done. Difference: %f , its index %d ,its cost: %f",biggest_difference,biggest_index,biggest_cost)
            #logging.debug("Increase or decrease: %d",direction_decrease_down)

  
        #HEURISZTIKA
        #Legnagyobb cost alapjan vegigmenni
        else:
            for i in eu_users:
                #ha mindenki inactivera van allitva akkor nem fog belepni!
                if(i.cost < biggest_cost and i.inactive==False):
                    done=False
                    
                    biggest_cost = i.cost
                    biggest_index = eu_users.index(i)
            biggest_index=biggest_index
    # p érték csökkentése 1-el
    #nyomon követés a dictionaryben: lefutas check eloszor, hogy ne menjen a dictionary ertek 0 ala
        
        if done==False:  
                
                p_values[eu_users[biggest_index].p_exponent]-=1
                if direction_decrease_down==True:
                    # logging.debug("changing user at index %d",biggest_index)                           
                    eu_users[biggest_index].decrease_exponent()
                                       
                else:
                    # logging.debug("changing user at index %d",biggest_index)  
                    eu_users[biggest_index].increase_exponent() 
    
        #uj ertek elmentese!
       
        sum_cost_new=refresh_costs(eu_users,edge_number,f,local_altruism)
        if slow==False:
            if sum_cost_new>sum_cost_old:
                biggest_difference=sum_cost_old-sum_cost_new
       #ha az uj ertek rosszabb, akkor visszacsináljuk a változtatásokat, majd kilépünk
        # if sum_cost_new<=sum_cost_old:
           
        #     if done==False:
        #         if direction_decrease_down==True:
        #             eu_users[biggest_index].increase_exponent()
        #         else: 
        #             eu_users[biggest_index].decrease_exponent()
        #         p_values[eu_users[biggest_index].p_exponent]+=1           
        #     logging.info("inital social welfare: %f  --  final social welfare: %f",sum_eu_start,sum_cost_old)
        #     return p_values,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,eu_users
        
        #ha az uj ertek jobb akkor rogzitjuk az eredmenyeket
        if done==False:
           
            if  eu_users[biggest_index].p_exponent < -10:
                
                p_values['none']+=1 
               
                
            else:
                
                 p_values[eu_users[biggest_index].p_exponent]+=1
                


        
            biggest_cost_array.append(biggest_cost)
            social_welfare_array.append(sum_cost_new)
            #logging.info("iteration: %d  --  social welfare: %f  --  biggest cost: %f  --  biggest difference: %f -- its index %d",iterations,sum_cost_new,biggest_cost,biggest_difference,biggest_index)
            biggest_difference_array.append(biggest_difference)
            if calculate_social_optimum==True:   
                if sum_cost_old*(1.0-epsilon) >= sum_cost_new:
                    logging.debug("sum_cost old: %f  --  sum_cost_new: %f",sum_cost_old*(1.0-epsilon),sum_cost_new)
                    logging.info("epsilon threshold reached")
                    logging.info("inital social welfare: %f  --  final social welfare: %f",sum_eu_start,sum_cost_new)
                    return p_values,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,eu_users
       
            iterations+=1

    #ha mar csak minimalis javulas erheto el, vagy tullepzuk a megengedett lepesszamot
    logging.info("inital social welfare: %f  --  final social welfare: %f",sum_eu_start,sum_cost_new)
    return  p_values,iterations,social_welfare_array,biggest_cost_array,biggest_difference_array,eu_users
def social_welfare_central(User_model,graph,privacy_loss_cost,threshold,message_cost=1,local_altruism=False):
    starter_p=-1
    p_values={-1:0,-2:0,-3:0,-4:0,-5:0,-6:0,-7:0,-8:0,-9:0,-10:0,'none':0}
    
    users=generate_users(graph,User_model,threshold,privacy_loss_cost,starter_p)
    while starter_p>-11:
        social_cost=refresh_costs(users,graph.number_of_edges(),message_cost,local_altruism)
        #social_cost2=refresh_costs(users,graph.number_of_edges(),message_cost,social_cost)
        p_values[starter_p]=social_cost
        starter_p-=1
        for i in users:
            i.decrease_exponent()
    for i in users:
        i.decrease_exponent()
        social_cost=refresh_costs(users,graph.number_of_edges(),message_cost,local_altruism)
        p_values['none']=social_cost
    return p_values   
def graph_thinner(G,number_of_graphs=2):

    # Get a list of nodes ordered by degree
    nodes_by_degree = sorted(G.nodes(), key=G.degree, reverse=True)

    #print("Number of nodes:", len(nodes_by_degree))
    #print("Number of edges:", G.number_of_edges())
    # Create a new MultiDiGraph containing every second node
    H = nx.MultiDiGraph()
    for i, node in enumerate(nodes_by_degree):
        if i % 2 == 0:
            H.add_node(node)
    #print("Number of nodes in H:", len(H))
    for u, v, key in G.edges(keys=True):
        if u in H and v in H:
            H.add_edge(u, v)
    #print("Number of edges in H:", H.number_of_edges())
    if number_of_graphs==1:
        return H
    # Compute betweenness centrality for each node
    bc = nx.betweenness_centrality(G)

    # Order nodes by betweenness centrality in descending order
    nodes_by_bc = sorted(bc, key=bc.get, reverse=True)
    #print("ordered nodes by bc:",nodes_by_bc)
    BC_graph = nx.MultiDiGraph()
    for i, node in enumerate(nodes_by_bc):
       
        if i % 2 == 0:
            BC_graph.add_node(node)
    
    #print("Number of nodes in H:", len(H))
    for u, v, key in G.edges(keys=True):
        if u in BC_graph and v in BC_graph:
            BC_graph.add_edge(u, v)

    return H,BC_graph
def exp_dist(exponent,sorted_list,num_groups=11):
   
    group_index = 0
    remaining_nodes = len(sorted_list)
    groups=[]
    # Distribute nodes into groups based on exponential distribution
    for i in range(num_groups):
        group_size = min(exponent ** i, remaining_nodes)
        group = sorted_list[group_index:group_index + group_size]
        
        group_index += group_size
        remaining_nodes -= group_size
        if remaining_nodes <= 0:
            break
        groups.append(group)
    return groups

def halver(results,lst,num_categories=11):
    if len(lst) <=1: 
        results.append(lst)
        return results
    elif num_categories==0: 
        results.append(lst)
        return results
        
        
    else:
        midpoint = math.ceil(len(lst)/2)
        first_half = lst[:midpoint]
        results.append(first_half)
        second_half = lst[midpoint:]
        
        return halver(results,second_half,num_categories-1)   

def lin_dist(sorted_list,num_groups=11):
    total_nodes = len(sorted_list)
    group_size = math.ceil(total_nodes / num_groups)

    # # Distribute nodes into groups
    groups = [sorted_list[i:i + group_size] for i in range(0, total_nodes, group_size)]
    return groups