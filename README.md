# General
- Attempt to implement the following paper: https://arxiv.org/pdf/2308.12606.pdf
- I am not affiliated with the authors of the paper, nor do I claim any rights to the paper. I am simply implementing the paper for my own learning purposes.

# Describing the problem
- $p_i$: The price of the subscription the customer currently has.
- $\alpha_i$: The probability we lose the customer (churn out).
- $\gamma_i$: The susceptibility the customer has towards accepting an offer.
- $x_i$: A list of vectors $\in \{0,1\}$ such that $x_i = [x_1,x_2,...,x_k]$, and exactly one element of $x_i$ has value 1.
- $\delta_i$: A list of positive real-valued denominations representing offers available such that $\delta_i = [\delta_1,\delta_2,...,\delta_k]$.
    - Each offer $\delta_{i,j}$ has a limited supply $n_j$.
    - The budget allocated to an offer is $w_j = \delta_{i,j} n_j$.
    - The total number of offers $K = \sum_{j\geq0}n_j$.
    - The total budget $W= \sum_{j\geq0}w_j$.
    - Note that the size of $\delta_i$ varies depending on the customer, as there may be offers not available anymore due to supply limitations. Of course, the same can be said on the size of $x_i$ as a corollary.
- $\delta_i \cdot x_i$: The dot product of $x_i$ and $\delta_i$. It is essentially assigning an offer to the customer from the set of offers, as exactly only one element $\in x_i$ holds value 1.
- $\beta_i$: The probability a customer accepts the offer.
    - $\beta_i = 1 - e^{-\gamma_i(\delta_i \cdot x_i)}$
- $f(\delta_i\cdot x_i, \alpha_i,\gamma_i,p_i)$: Simplified to $f(\Omega_i)$, is the expected value of a customer.
    - The total expected optimized value is given by $\sum_{i\geq0}f(\Omega_i)$, and our goal is to optimize this value.

# Algorithm
- Greedily maximize f($\Omega$).

# Uncertainties 
The following points are only related to my understanding of the paper, and can be ignored during the implementation.
- Maybe we can represent $\gamma_i$ with a poisson distribution.
- Not sure how to model $\alpha_i$ given customer data.