# Import the heap functions from python library
from heapq import heappush, heappop, heapify
import math
import csv

# A class for Max Heap
# Need to negate the values in order to get a Max
# Slightly modified implementation from: https://www.geeksforgeeks.org/binary-heap/
class MaxHeap:
	# Constructor to initialize a heap
	def __init__(self):
		self.heap = []

	def parent(self, i):
		return (i-1)/2
	
	# Inserts a new key 'k'
	def insertKey(self, k,j):
		heappush(self.heap, (-k,j))		

	# Decrease value of key at index 'i' to new_val
	# It is assumed that new_val is smaller than heap[i]
	def decreaseKey(self, i, new_val):
		self.heap[i] = new_val
		while(i != 0 and self.heap[self.parent(i)] > self.heap[i]):
			# Swap heap[i] with heap[parent(i)]
			self.heap[i] , self.heap[self.parent(i)] = (
			self.heap[self.parent(i)], self.heap[i])
			
	# Method to remove max element from max heap
	def extractRoot(self):
		return heappop(self.heap)

	# This function deletes key at index i. It first reduces
	# value to minus infinite and then calls extractMax()
	def deleteKey(self, i):
		self.decreaseKey(i, float("-inf"))
		self.extractRoot()

	# Get the minimum element from the heap
	def getRoot(self):
		return self.heap[0]

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

def greedOffer( alpha, gamma, p, delta, supply):
    """
    :param alpha: list of floats, churn out prob for each subscriber
    :param gamma: list of floats, susceptibility towards offer acceptance for each subscriber
    :param p: list of floats, monthly top-up amount for each subscriber
    :param delta: list of floats, cost of the offer for each offer
    :param supply: list of ints, supply of each offer
    :return: list of tuples, the solution set A
    """
    n = len(alpha)
    #1
    #Initialize the set of subscribers S
    S = [i for i in range(n)]

    #2
    #Initialize the solution set A
    A = []

    #3
    #Construct the list Q of maxHeaps 1,...,k for each offer
    k = len(delta)
    Q = [ [] for i in range(k)] #The queue of queues Q_j
    for i in range(k):
        heap = MaxHeap()
        for j in range(n):
            priority = f(delta[i], alpha[j], gamma[j], p[j])
            heap.insertKey(priority,j)
		# max = - Q[i].getRoot()[0] --> peek the root positive value
        # customer = Q[i].getRoot()[1] --> peek the customer number
        # max = -heap.extractRoot()[0] --> pop the root positive value
        Q[i] = heap

    #4
    #Construct the lookup table T of size n x k
    #Each element of T references the position of a subscriber i in each queue j
    T = [ [0 for i in range(k)] for j in range(n)]
    #Loop through the queues
    #whenever we see customer i for queue j, we update T[i][j] to the position of i in Q[j]
    for j in range(k):
        for i in range(n):
            customer = Q[j].getRoot()[1]
            T[j][customer] = i
    print(T)
    
    
"""
    #5
    #Construct the array L of size k
    L = [0 for i in range(k)]
    #Each element j of L is the head of each queue j in Q
    
    
    #6
    #While the total number of offers is > 0, and the set of subscribers is not empty
    while sum(supply) > 0 and len(S) > 0:
        
        # Append it to A
        
        # Remove the customer i from S
        
        # Remove the customer i from all queues
        #the custommer number is the second element of the tuple in the queue
        
        # Update the array L
        

        # Update the lookup table T
        

        # Update K and offer number
        
        # If there are no more offers of type j, remove Q_j from the set of queues.
        #this is also probably shit
        
    #7
    #Return the solution set A
    return A
"""
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

#call the naive implementation
A = greedOffer(alpha, gamma, p, delta, supply)
print("############################################################################################################")
print (A)
