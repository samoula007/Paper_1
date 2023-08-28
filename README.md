# General
- Attempting to implement the following paper: https://arxiv.org/pdf/2308.12606.pdf
- I am not affiliated with the authors of the paper, nor do I claim any rights to the paper. I am simply implementing the paper for my own learning purposes.
---
# Describing the variables
- $p_i$: The price of the subscription the customer currently has.
- $\alpha_i$: The probability we lose the customer (churn out).
- $\gamma_i$: The susceptibility the customer has towards accepting an offer.
- $x_i$: A list of vectors $\in \{0,1\}$ such that $x_i = [x_1,x_2,...,x_k]$, and exactly one element of $x_i$ has value 1.
- $\delta_i$: A list of positive real-valued denominations representing offers available such that $\delta_i = [\delta_1,\delta_2,...,\delta_k]$.
    - Each offer $\delta_{i,j}$ has a limited supply $n_j$.
    - The budget allocated to an offer is $w_j = \delta_{i,j} n_j$.
    - The total number of offers $K = \sum_{j\geq0}n_j$.
    - The total budget $W= \sum_{j\geq0}w_j$.
    - Note that $\delta$ is actually a constant set, as it does not change.
- $\delta_i \cdot x_i$: The dot product of $x_i$ and $\delta_i$. It is essentially assigning an offer to the customer from the set of offers, as exactly only one element $\in x_i$ holds value 1.
- $\beta_i$: The probability a customer accepts the offer.
    - $\beta_i = 1 - e^{-\gamma_i(\delta_i \cdot x_i)}$
- $f(\delta_i\cdot x_i, \alpha_i,\gamma_i,p_i)$: Simplified to $f(\Omega_i)$, is the expected value of a customer.
    - $f(\Omega_i) = \beta_i(p_i-\delta_i\cdot x_i) + (1-\beta_i)(1-\alpha_i)p_i$
    - The total expected optimized value is given by $\sum_{i\geq0}f(\Omega_i)$, and our goal is to optimize this value.
    - Note that $\beta_i$ is not input to the function, as it can be computed from the other arguments.
---
# Structures
- Construct $k$ max priority queues $Q_j$
    - Each offer $j$ has a corresponding max priority queue $Q_j$ that contains the values $f(\Omega_i)$ of each customer
    - We have k such queues, namely $Q_1,Q_2,...,Q_k$.
    - Each queue is implemented using a binary heap (complete binary tree stored in an array).
    - The max value of the queue $Q_j$ is at the root of the heap.
- Construct an array L
    - It has size k.
    - It references the head of each $Q_j$.
    - To find the max value fast.
- Construct a lookup table T
    - It has size $n\times k$.
    - Each element references the place of a subscriber $i$ in each $Q_j$.
    - To delete an element from k priority queues efficiently.
# Algorithm
- Input
    - GreedOffer$(\alpha[1,...,n], \gamma[1,...,n], p[1,...,n])$
        - $e_{\alpha} \in \alpha$: float
        - $e_{\gamma} \in \gamma$: float
        - $e_{p} \in p$: float
    - Offers $\delta[1,...,k]$ with limited supply $n[1,...,k]$.
        - $e_{\delta} \in \delta$: float
        - $e_{n} \in n$: int
        - Constant set, so not input to the function.
- Output
    - A list of $(i,j)$ pairs, where $i$ is the customer, and $j$ is the offer.
        - $(i,j)$: (int, int)
1. Initialize the set of subscribers $S$
    - $S = [1,2,...,n]$
2. Initialize the answer set $A$
    - $A = []$
3. Construct the priority queues
    - $Q_1, Q_2,...,Q_k$
4. Construct the lookup table $T$
5. Construct the array $L$
6. While $K>0$ and $S\neq\emptyset$, where $K$ is the total number of offers
    - Find the pair $(i,j)$ such that $f(\Omega_i)$ is the max value in $Q_j$.
    - Append it to $A$.
    - Remove the customer $i$ from $S$.
    - Remove the customer $i$ from all queues.
    - Update the array $L$.
    - Update the lookup table $T$.
    - Update $K$.
    - Update the total number of offers for offer type $j$.
    - If there are no more offers of type $j$, remove $Q_j$ from the set of queues.
7. Return $A$

# Time Complexity, Space Complexity, Solution Optimality
- Refer to the corresponding sections of the paper.
---
# Uncertainties 
*The following points are only related to my understanding of the paper, and can be ignored during the implementation.*
- Maybe we can represent $\gamma_i$ with a poisson distribution.
- Not sure how to model $\alpha_i$ given customer data.
- Note that I implement the paper without modification of the original authors' intention (hopefully). However, in my opinion, if we want to speed up the algorithm, one thing we could do is to apply the secretary problem to the algorithm (in the case of $\delta_i\cdot x_i$). The solution will be suboptimal in roughly $1 - {1\over e}$ cases, which is quite signifiant, but at the cost of running faster, especially in the case where the number of customers and offers is very large.
    - I might just implement both algorithms and compare the performance?
- Maybe try to find opportunities where such an algorithm can be tried in a different context, where the data is more available than in the case for which the problem has been designed.
- Data input from CSV file most likely. How delta is input is still unclear, but might just be in an independant CSV file, which is the most likely case.
- Should I include toy data to test the algorithm? Probably.