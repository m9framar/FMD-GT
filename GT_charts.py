import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from operator import add

plt.rcParams['figure.figsize'] = [14, 14]
plt.rcParams['axes.titlesize']=30
plt.rcParams['axes.labelsize']=30
plt.rcParams['xtick.labelsize']=30
plt.rcParams['ytick.labelsize']=30
plt.rcParams['legend.fontsize']=30

def sw_and_dist(filename, p_values, p_values_start, iterations, social_welfare_array,title="default"):
    fig,ax=plt.subplots(2)
    
    fig.figsize=(18,19)
    
    fig.suptitle(title, fontsize=30,y=1.00)
    ax[0].set_title("Progression of brd with final value:{:.1f}".format(social_welfare_array[-1]))
    ax[0].plot(range(0,len(social_welfare_array)), social_welfare_array, marker="*")
    ax[0].set_xlabel("Number of iterations")
    ax[0].set_ylabel("Social cost",labelpad=1)
    ax[0].tick_params(axis='y', labelrotation=45)
    #ax[0].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax[0].ticklabel_format(style="sci",  axis="y",scilimits=(0,0),useMathText=True)
 
    X = p_values.keys()
    X_axis = np.arange(len(X))  
    bar1=ax[1].bar(X_axis - 0.2, p_values_start.values(), 0.4, label = 'Before')
    bar2=ax[1].bar(X_axis + 0.2, p_values.values(), 0.4, label = 'After')
    ax[1].bar_label(bar1,label_type='center',fontsize=20,padding=20)
    ax[1].bar_label(bar2,label_type='center',fontsize=20,padding=5)

    ax[1].set_xticks(X_axis, X)
    ax[1].set_xlabel("False positive rate exponents")
    ax[1].set_ylabel("Number of users")
    ax[1].set_title("Number of users with a given fp-rate")
    ax[1].legend()
  
    fig.tight_layout(pad=0.3)
    plt.savefig("results_swdist/{}_exponent_distribution.pdf".format(filename))
    plt.close()
def boxchart_comparision(data,xticks,title,ylabel,xlabel="Setup",filename="default"):
    fig,ax=plt.subplots()
    fig.suptitle(title, fontsize=50)
    # Call draw() to ensure the figure has been drawn
    fig.canvas.draw()
    
    # Get the title artist and calculate its height
    title_artist = fig._suptitle
    title_width = title_artist.get_window_extent().width / fig.dpi
    
    # Add the title height to the default height of the figure
    fig_width = fig.get_figheight() + title_width
    fig.set_size_inches(fig_width,14)
    boxplot=ax.boxplot(data,labels=xticks,patch_artist=True)
    ax.set_ylabel(ylabel,fontsize=45)
    ax.yaxis.grid(True)
    ax.set_ylim(0)
    ax.set_xlabel(xlabel,fontsize=40)
    ax.tick_params(axis='x', labelsize=45)
    ax.tick_params(axis='y', labelsize=45)
    #plt.show()
    fig.savefig("results/{}.pdf".format(filename))
def barchart_comparision(data, names,
                         title='Sum of privacy loss and bandwidth cost for every setup',
                         ylabel='Combined social cost',
                         filename="default",
                         xlabel="Setup"):
    x = np.arange(len(names))  # the label locations
    width = 0.25 # the width of the bars
    multiplier = 0


    fig, ax = plt.subplots()
    fig.figsize=(18,21)
    max_value = max(max(measurement) for measurement in data.values())
    for attribute, measurement in data.items():
        print(attribute, measurement)
        normalized_measurement = [m / max_value for m in measurement]
        offset = width * multiplier
        rects = ax.bar(x + offset, normalized_measurement, width, label=attribute)
        #ax.bar_label(rects, label_type=None, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title,pad=10)
    ax.set_xticks(x + width/2, names)
    ax.legend(loc='best', ncol=2)
    ax.set_ylim(0)
    ax.autoscale(axis='y')
    #ax.set_yscale('log')
    #ax.set_yticks([10**i for i in range(int(np.log10(ax.get_ylim()[0])), int(np.log10(ax.get_ylim()[1]))+1)])
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)

    #plt.show()
    plt.tight_layout(pad=0.3)
    fig.savefig("results/{}.pdf".format(filename))

def biggest_costs(iterations,array,name):
    fig,ax=plt.subplots()
    ax.set_title("Progression of selected users cost in system over time")
    ax.plot(range(0,iterations), array, marker="*")
    ax.set_xlabel("Number of iterations")
    ax.set_ylabel("Biggest cost")
    plt.savefig("results/{}_bcosts.pdf".format(name))
def biggest_cost_reduction(iterations,array,name):
    fig,ax=plt.subplots()
    ax.set_title("Progression of the amount of possible cost reduction in system")
    ax.plot(range(0,iterations), array, marker="*")
    ax.set_xlabel("Number of iterations")
    ax.set_ylabel("Biggest achievable cost reduction")
    plt.savefig("results/{}_bcost_reduction_progress.pdf".format(name))
def random_run_comparison(iterations,array_local_altr,array_global_altr,name):
    fig,ax=plt.subplots()
    ax.set_title("Random runs:{}".format(name))
    ax.plot(range(0,iterations+1), array_local_altr, marker="*",label="Local altruism")
    ax.plot(range(0,iterations+1), array_global_altr, marker="*",label="Global altruism")
    ax.set_xlabel("Run number")
    ax.set_ylabel("Social cost")
    ax.legend()
    plt.savefig("results/{}_local_vs_global.pdf".format(name))
def central_distr(p_values,name):
    fig,ax=plt.subplots()
    #ax.set_title("Social welfare options in a centrally controlled system")
    ax.set_xlabel("False-positive rate exponent strategy", fontweight='bold')
    ax.set_ylabel("Social cost",fontweight='bold')
    markers=["*","o"]
    for dataset_name, p_values in p_values.items():
        X = p_values.keys()
        #print(X)
        X_axis = np.arange(len(X))
        #print(X_axis)  
        
        
        #print(list(p_values.values()))
        ax.plot(list(p_values.values()), marker=markers.pop(),label=dataset_name,markersize=25, linewidth=3)

        ax.set_xticks(X_axis, X,fontsize=30)
    ax.legend(loc='lower left')
    fig.savefig("results/{}_sw_central.png".format(name),dpi=300,bbox_inches='tight')
def table_graph(data,name):
    fig,ax=plt.subplots()
    fig.tight_layout()
    ax.set_title(
	    name,
	    loc='left',
	    fontsize=18,
	    weight='bold'
        )
    rows=8
    cols=2
    ax.set_ylim(-1, rows + 1)
    ax.set_xlim(0, cols + .5)
    ax.plot([0, cols + 1], [rows-0.5, rows-0.5], lw='.5', c='black')
    for row in range(rows):
	# extract the row data from the list

        d = data[row]

        # the y (row) coordinate is based on the row index (loop)

        # the x (column) coordinate is defined based on the order I want to display the data in

        ax.text(x=.5, y=row, s=d['local'], va='center', ha='left')
        

        ax.text(x=2, y=row, s=d['selection_mode'], va='center', ha='right')
    ax.text(.5, 7.75, 'Original\ngraph', weight='bold', ha='left')
    ax.text(2, 7.75, 'Halved\ngraph', weight='bold', ha='right')
    ax.axis('off')
    plt.show()
def table_m6(data,name):
    # first, we'll create a new figure and axis object

    fig, ax = plt.subplots(figsize=(10,6))
    fig.tight_layout()

    # set the number of rows and cols for our table

    rows = 16
    cols = 9

    # create a coordinate system based on the number of rows/columns

    # adding a bit of padding on bottom (-1), top (1), right (0.5)

    ax.set_ylim(-1, rows + 1)
    ax.set_xlim(0, cols + .5)
    ax.plot([0, cols + 1], [rows-0.5, rows-0.5], lw='.5', c='black')
    for row in range(rows):
	# extract the row data from the list

        d = data[row]

        # the y (row) coordinate is based on the row index (loop)

        # the x (column) coordinate is defined based on the order I want to display the data in

        ax.text(x=.5, y=row, s=d['local'], va='center', ha='left')
        

        ax.text(x=2, y=row, s=d['selection_mode'], va='center', ha='right')
        

        ax.text(x=3, y=row, s=d['start_p'], va='center', ha='right')
        

        ax.text(x=4, y=row, s=d['threshold_set'], va='center', ha='right')
       

        ax.text(x=5, y=row, s=d['final_social'], va='center', ha='right', weight='bold')

        ax.text(x=6, y=row, s=d['sum_priv_cost'], va='center', ha='right')

        ax.text(x=7, y=row, s=d['sum_bw_cost'], va='center', ha='right')
        ax.text(x=8, y=row, s=d['active_users'], va='center', ha='right')
        ax.text(x=9, y=row, s=d['inactive_users'], va='center', ha='right')
    ax.text(.5, 15.75, 'Altruism\ntype', weight='bold', ha='left')
    ax.text(2, 15.75, 'Threshold\ntype', weight='bold', ha='right')
    ax.text(3, 15.75, 'Start\np', weight='bold', ha='right')
    ax.text(4, 15.75, 'Threshold\nexistence', weight='bold', ha='right')
    ax.text(5, 15.75, 'Calculated\nSW', weight='bold', ha='right')
    ax.text(6, 15.75, 'Summed\npriv. loss', weight='bold', ha='right')
    ax.text(7, 15.75, 'Summed\nbw. cost', weight='bold', ha='right')
    ax.text(8, 15.75, 'Active\nusers', weight='bold', ha='right')
    ax.text(9, 15.75, 'Inactive\nusers', weight='bold', ha='right')
    ax.set_title(
	    name,
	    loc='left',
	    fontsize=18,
	    weight='bold'
        )
    for row in range(rows):
        ax.plot(
            [0, cols + 1],
            [row -.5, row - .5],
            ls=':',
            lw='.5',
            c='grey'
        )
    ax.axis('off')
    plt.show()

def table_m7(data,name):
    fig, ax = plt.subplots(figsize=(8,6))

    # set the number of rows and cols for our table

    rows = 8
    cols = 7
    ax.set_ylim(-1, rows + 1)
    ax.set_xlim(0, cols + .5)
    ax.plot([0, cols + 1], [rows-0.5, rows-0.5], lw='.5', c='black')

    for row in range(rows):
	# extract the row data from the list

        d = data[row]

        # the y (row) coordinate is based on the row index (loop)

        # the x (column) coordinate is defined based on the order I want to display the data in

        ax.text(x=.5, y=row, s=d['local'], va='center', ha='left')
        

        ax.text(x=2, y=row, s=d['ordering'], va='center', ha='right')
        
        ax.text(x=3, y=row, s=d['final_social'], va='center', ha='right', weight='bold')

        ax.text(x=4, y=row, s=d['sum_priv_cost'], va='center', ha='right')

        ax.text(x=5, y=row, s=d['sum_bw_cost'], va='center', ha='right')
        ax.text(x=6, y=row, s=d['active_users'], va='center', ha='right')
        ax.text(x=7, y=row, s=d['inactive_users'], va='center', ha='right')
    ax.text(.5, 7.75, 'Altruism\ntype', weight='bold', ha='left')
    ax.text(2, 7.75, 'Ordering', weight='bold', ha='right')
    ax.text(3, 7.75, 'Calculated\nSW', weight='bold', ha='right')
    ax.text(4, 7.75, 'Summed\npriv. loss', weight='bold', ha='right')
    ax.text(5, 7.75, 'Summed\nbw. cost', weight='bold', ha='right')
    ax.text(6, 7.75, 'Active\nusers', weight='bold', ha='right')
    ax.text(7, 7.75, 'Inactive\nusers', weight='bold', ha='right')
    ax.set_title(
	    name,
	    loc='left',
	    fontsize=18,
	    weight='bold'
        )
    ax.axis('off')
    plt.show()
    fig.savefig("{}_table_m7.png".format(name),dpi=300,bbox_inches='tight')
def table_m8(data,name):
    fig,ax=plt.subplots(figsize=(8,6))
    rows=10
    cols=7
    ax.set_ylim(-1, rows + 1)
    ax.set_xlim(0, cols + .5)
    ax.plot([0, cols + 1], [rows-0.5, rows-0.5], lw='.5', c='black')
    for row in range(rows):
        d=data[row]
        ax.text(x=.5, y=row, s=d['local'], va='center', ha='left')
        ax.text(x=2, y=row, s=d['run_number'], va='center', ha='right')
        ax.text(x=3, y=row, s=d['final_social'], va='center', ha='right', weight='bold')
        ax.text(x=4, y=row, s=d['sum_priv_cost'], va='center', ha='right')
        ax.text(x=5, y=row, s=d['sum_bw_cost'], va='center', ha='right')
        ax.text(x=6, y=row, s=d['active_users'], va='center', ha='right')
        ax.text(x=7, y=row, s=d['inactive_users'], va='center', ha='right')
    ax.text(.5, 9.75, 'Altruism\ntype', weight='bold', ha='left')
    ax.text(2, 9.75, 'Run\nnumber', weight='bold', ha='right')
    ax.text(3, 9.75, 'Calculated\nSW', weight='bold', ha='right')
    ax.text(4, 9.75, 'Summed\npriv. loss', weight='bold', ha='right')
    ax.text(5, 9.75, 'Summed\nbw. cost', weight='bold', ha='right')
    ax.text(6, 9.75, 'Active\nusers', weight='bold', ha='right')
    ax.text(7, 9.75, 'Inactive\nusers', weight='bold', ha='right')
    ax.set_title(
        name,
        loc='left',
        fontsize=18,
        weight='bold'
        )
    ax.axis('off')
    plt.show()
def equlibra_chart(poa_array,pos_array,name):
    fig,ax=plt.subplots()
    ax.set_title("Progression of PoA/PoS with changing altruism coefficient")
    ax.plot(range(0,len(poa_array)),poa_array, marker="+",color='r')
    ax.plot(range(0,len(pos_array)),pos_array, marker="*",color='g')
    ax.set_xlabel("Altruism coefficent")
    ax.set_ylabel("PoA/PoS")
    X=np.arange(0.0,1.01,0.1).round(1).tolist()
    X_axis=np.arange(len(X))
    ax.set_xticks(X_axis,X)
    fig.savefig("results/{}_equlibria_chart.pdf".format(name))
def dist_indegree(users,pvalues,cutoff1,cutoff2,filename):
    fig,ax=plt.subplots()
    X = pvalues.keys()
    X_axis = np.arange(len(X))
    dict1= dict.fromkeys(pvalues, 0)
    dict2= dict.fromkeys(pvalues, 0)
    dict3= dict.fromkeys(pvalues, 0)
    for i in users:
        if i.incoming<=int(cutoff1):
            if i.p_exponent<-10 or i.p_exponent>-1:
                dict1['none']+=1
            else:
                dict1[i.p_exponent]+=1
        elif i.incoming>int(cutoff1) and i.incoming<=int(cutoff2):
            if i.p_exponent<-10 or i.p_exponent>-1:
                dict2['none']+=1
            else:
                dict2[i.p_exponent]+=1
        else:
            if i.p_exponent<-10 or i.p_exponent>-1:
                dict3['none']+=1
            else:
                dict3[i.p_exponent]+=1
    #print(dict1.values())
    
    #print(dict2.values())

    #print(dict3.values())
    res_list = list(map(add, list(dict1.values()), list(dict2.values())))
  

    also=ax.bar(X_axis,dict1.values(),0.4,label="Below:{}".format(cutoff1))
    kozepso=ax.bar(X_axis,dict2.values(),0.4,bottom=list(dict1.values()) ,label="Between:{} and {}".format(cutoff1,cutoff2))
    felso=ax.bar(X_axis,dict3.values(),0.4,bottom=res_list,label="Above:{}".format(cutoff2))
    ax.bar_label(also,label_type='center',fontsize=20)
    ax.bar_label(kozepso,label_type='center',fontsize=20)
    ax.bar_label(felso,label_type='edge',fontsize=20)
    ax.set_xticks(X_axis, X)
    ax.set_xlabel("False positive rate exponents")
    ax.set_ylabel("Number of users")
    ax.set_title("Number of users with a given fp-rate grouped by incoming messages")
    ax.legend()
    fig.savefig("results/{}_dist_indegree.pdf".format(filename))
def scatterplots_NE(graph_name,altr_value,NE_runs,filename,socialopt=False):
        ne_runs_local_x = []
        ne_runs_local_y1 = []
        ne_runs_local_y2 = []
        ne_runs_local_y3 = []

        for run in NE_runs[0]:
            ne_runs_local_x.append(run[3])
            ne_runs_local_y1.append(run[4])
            ne_runs_local_y2.append(run[5])
            ne_runs_local_y3.append(run[6])
            
        fig, ax = plt.subplots(ncols=3)
        fig.suptitle("[{}][{}]Local {} runs correlation".format(graph_name,altr_value,("NE" if socialopt==False else "SO")),fontsize=30)
        fig.set_constrained_layout(True)
        ax[0].scatter(ne_runs_local_x, ne_runs_local_y1, s=150)
        ax[0].set_xlabel("Achieved SW")
        ax[0].xaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0))
        ax[0].set_ylabel("Iterations compared to best SW")
        yticks = ax[0].get_yticks()
        ax[0].set_yticklabels([f"{int(ytick)}%" for ytick in yticks])
        #ax[0].set_title("Correlation between achieved SW and iterations compared to best SW")

        ax[1].scatter(ne_runs_local_x, ne_runs_local_y2, s=150)
        ax[1].set_xlabel("Achieved SW")
        ax[1].xaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0))
        ax[1].set_ylabel("Sum of normalized bc of users\n with -1 strategy")
        #ax[1].set_title("Correlation between achieved SW and\n sum of normalized bc of users with -1 strategy")

        ax[2].scatter(ne_runs_local_x, ne_runs_local_y3, s=150)
        ax[2].set_xlabel("Achieved SW")
        ax[2].set_ylabel("Number of top 10 bc users with -1 strategy")
        ax[2].xaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0))
        #ax[2].set_title("Correlation between achieved SW and\n number of top 10 bc users with -1 strategy")

        
        fig.savefig("results/{}_{}_runs_local.pdf".format(filename,("NE" if socialopt==False else "SO")))

        ne_runs_global_x = []
        ne_runs_global_y1 = []
        ne_runs_global_y2 = []
        ne_runs_global_y3 = []

        for run in NE_runs[1]:
            ne_runs_global_x.append(run[3])
            ne_runs_global_y1.append(run[4])
            ne_runs_global_y2.append(run[5])
            ne_runs_global_y3.append(run[6])

        fig, ax = plt.subplots(ncols=3)
        
        fig.set_constrained_layout(True)
        fig.suptitle("[{}][{}]Global {} runs correlation".format(graph_name,altr_value,("NE" if socialopt==False else "SO")),fontsize=30)
        ax[0].scatter(ne_runs_global_x, ne_runs_global_y1, s=150)
        ax[0].set_xlabel("Achieved SW")
        ax[0].xaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0))
        ax[0].set_ylabel("Iterations compared to best SW")
        yticks = ax[0].get_yticks()
        ax[0].set_yticklabels([f"{int(ytick)}%" for ytick in yticks])
        #ax[0].set_title("Correlation between achieved SW and iterations compared to best SW")

        ax[1].scatter(ne_runs_global_x, ne_runs_global_y2, s=150)
        ax[1].set_xlabel("Achieved SW")
        ax[1].xaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0))
        ax[1].set_ylabel("Sum of normalized bc of users\n with -1 strategy")
        #ax[1].set_title("Correlation between achieved SW and\n sum of normalized bc of users with -1 strategy")


        ax[2].scatter(ne_runs_global_x, ne_runs_global_y3, s=150)
        ax[2].set_xlabel("Achieved SW")
        ax[2].xaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0))
        ax[2].set_ylabel("Number of top 10 bc users with -1 strategy")
        #ax[2].set_title("Correlation between achieved SW and\n number of top 10 bc users with -1 strategy")


        
        fig.savefig("results/{}_{}_runs_global.pdf".format(filename,("NE" if socialopt==False else "SO")))
def table_all(rundata,rowlabels,collabels,tabletitle,filename):
    fig, ax = plt.subplots()
    
    ax.axis('off')
    ax.axis('tight')
    table=ax.table(cellText=rundata, 
             colLabels=collabels,
             rowLabels=rowlabels,
             loc='center',
             fontsize=50,
             cellLoc='center') # add fontsize parameter
    table.auto_set_font_size(False)
    table.auto_set_column_width([i for i in range(len(collabels))])
    fig.suptitle(tabletitle,fontsize=30,)
    fig.set_tight_layout(True)
    fig.savefig("results/{}_table.png".format(filename),bbox_inches='tight',dpi=300)
