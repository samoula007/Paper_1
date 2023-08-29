import heapq
import math
import csv

def f(delta_i, alpha_i, gamma_i, p_i):
    """
    :param delta_i: float, cost of the offer
    :param alpha_i: float, churn out prob
    :param gamma_i: float, susceptibility towards offer acceptance
    :param p_i: float, monthly top-up amount
    :return: float, the expected profit of the offer for the customer
    """
    #compute beta_i
    beta_i = 1 - math.exp(-gamma_i * delta_i)
    #compute the expected profit
    return beta_i * (p_i - delta_i) + (1 - beta_i)*(1 - alpha_i) * p_i

# NOTE: Contrary to the authors' pseudocode, I will additionally input delta,supply,n to the data
def greedOffer( alpha, gamma, p, delta, supply, n):
    """
    :param alpha: list of floats, churn out prob for each subscriber
    :param gamma: list of floats, susceptibility towards offer acceptance for each subscriber
    :param p: list of floats, monthly top-up amount for each subscriber
    :param delta: list of floats, cost of the offer for each offer
    :param supply: list of ints, supply of each offer
    :param n: int, number of subscribers
    :return: list of tuples, the solution set A
    """

    #1
    #Initialize the set of subscribers S
    S = [i for i in range(n)]

    #2
    #Initialize the solution set A
    A = []

    #3
    #Construct the priority queues 1,...,k for each offer
    k = len(delta)
    Q = [ [] for i in range(k)] #The queue of queues Q_j
    for i in range(k):
        for j in range(n):
            priority = f(delta[i], alpha[j], gamma[j], p[j])
            heapq.heappush(Q[i], (priority, j))

    #4
    #Construct the lookup table T of size n x k
    #Each element of T references the position of a subscriber i in each queue j
    T = [ [0 for i in range(k)] for j in range(n)]
    for i in range(k):
        for j in range(n):
            T[j][i] = Q[i].index((f(delta[i], alpha[j], gamma[j], p[j]), j))
    
    #5
    #Construct the array L of size k
    L = [0 for i in range(k)]
    #Each element j of L is the head of each queue j in Q
    for i in range(k):
        L[i] = Q[i][0][1]
    
    #6
    #While the total number of offers is > 0, and the set of subscribers is not empty
    while sum(supply) > 0 and len(S) > 0:
        #initialize prios
        top_prio = float('-inf')
        curr_j = -1
        curr_i = -1
        # find the pair (i,j) with the highest priority
        # iterate through Q, and the queue with head of highest value is the one with highest prio 
        # the pair (i,j) is then given by the current j (representing offer) and the head of the queue (representing subscriber)
        for j in range(k):
            if len(Q[j]) == 0:
                continue
            largest = heapq.nlargest(1,Q[j])[0]
            if L[j] != -1 and largest[0] > top_prio:
                top_prio = largest[0]
                curr_j = j
                curr_i = largest[1]

        # Append it to A
        A.append((curr_i, curr_j))
        # Remove the customer i from S
        S.remove(curr_i)
        # Remove the customer i from all queues
        #the custommer number is the second element of the tuple in the queue
        for j in range(k):
            priority = f(delta[j], alpha[curr_i], gamma[curr_i], p[curr_i]) 
            if (priority, curr_i) in Q[j]:
                Q[j].remove((priority, curr_i))
            
        # Update the array L
        L[curr_j] = Q[curr_j][0][1]

        # Update the lookup table T
        for j in range(k):
            for i in range(n):
                priority = f(delta[j], alpha[i], gamma[i], p[i])
                if (priority, i) in Q[j]:
                    T[i][j] = Q[j].index((priority, i))

        # Update K and offer number
        supply[curr_j] -= 1
        # If there are no more offers of type j, remove Q_j from the set of queues.
        #this is also probably shit
        if supply[curr_j] == 0:
            Q[curr_j] = []
    #7
    #Return the solution set A
    return A
     

############################################################################################################
#Testing naive implementation

# Converts a given field of the csv to a list
def extract_field(filename, column_index):
    result = []
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)  # Read the header row
        for row in csv_reader:
            if len(row) > column_index:
                result.append(row[column_index])
    return result    

#extract fields as list of strings
price_s = extract_field('data/customers.csv', 0)
a_s = extract_field('data/customers.csv', 1)
g_s = extract_field('data/customers.csv', 2)
offers_s = extract_field('data/offers.csv', 0)
supply_s = extract_field('data/offers.csv', 1)

#convert the strings to numbers
p = [float(i) for i in price_s]
alpha = [float(i) for i in a_s]
gamma = [float(i) for i in g_s]
delta = [float(i) for i in offers_s]
supply = [int(i) for i in supply_s]
n = len(alpha)

#call the naive implementation
A = greedOffer(alpha, gamma, p, delta, supply, n)

print (A)