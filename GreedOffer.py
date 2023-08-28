import heapq
import math

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

# NOTE: Contrary to the author's pseudocode, I will additionally input delta,supply,n to the data
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
            priority = -f(delta[i], alpha[j], gamma[j], p[j]) # negate the prio for maxprio
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
        for i in S:
            for j in range(k):
                if supply[j] > 0:  # There are available offers of type j
                    priority = -f(delta[j], alpha[i], gamma[i], p[i])
                    if priority > top_prio:
                        top_prio = priority
                        curr_j = j
                        curr_i = i
        if curr_j == -1:  # No more offers available
            break
        # Append it to A
        A.append((curr_i, curr_j))
        # Remove the customer i from S
        S.remove(curr_i)
        # Remove the customer i from all queues
        for j in range(k):
            if curr_i in Q[j]:
                Q[j].remove(curr_i)
        # Update the array L
        L[curr_j] = Q[curr_j][0][1]
        # Update the lookup table T
        for j in range(k):
            T[curr_i][j] = Q[j].index((f(delta[j], alpha[curr_i], gamma[curr_i], p[curr_i]), curr_i))
        # Update K and offer number
        supply[curr_j] -= 1
        # If there are no more offers of type j, remove Q_j from the set of queues.
        if supply[curr_j] == 0:
            Q[curr_j] = []
    #7
    #Return the solution set A
    return A

#TODO: Test the code        
# Need to create the csv to list converter in order to test the code

    
        