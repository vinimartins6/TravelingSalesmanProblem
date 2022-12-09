# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 21:49:43 2021

@author: otavi
"""

import cplex
#while True: #é necessário rodar o modelo todo denovo ou esse while pode ficar mais embaixo, na parte de resolução do cplex?
i = 5
j = 5

I = range(i)
J = range(j)

IJ = [(a,b) for a in I for b in J]


cpx=cplex.Cplex()



nx = ['x(' + str(i)+','+str(j)+')' for i in I for j in J]




c= [[99999,10,15,12,20],\
    [10,99999,5,2,10],\
    [15,5,99999,7,8],\
    [12,2,7,99999,6],\
    [20,10,8,6,99999]]
    



ix = {(a,b): idx for idx, (a,b) in enumerate(IJ)}



cpx.variables.add(obj = [c[a][b] for b in range(j)\
                      for a in range(i)],
                    lb = [0.0]*i*j, ub=[cplex.infinity]*i*j,types = ['B']*i*j, names = nx)
    

vet_1 = [1,1,1,1,1]
vet_2 = [1,1,1,1,1]

[cpx.linear_constraints.add(lin_expr=[cplex.SparsePair(\
                                     [ix[(a,b)] for b in J],\
                                      [1.0 for b in J])],\
                                      senses = 'E',\
                                      rhs = [vet_1[a]]) for a in I ]
    
[cpx.linear_constraints.add(lin_expr=[cplex.SparsePair(\
                                     [ix[(a,b)] for a in J],\
                                      [1.0 for a in J])],\
                                      senses = 'E',\
                                      rhs = [vet_2[b]]) for b in I ]


    

                                      
cpx.write("teste.lp")

cpx.solve()
print(cpx.solution.get_objective_value())
res = cpx.solution.get_values()
v=0 #vértice
visitados = [v]
aux2= list()
aux = [v]        

while aux:
    
    a= aux.pop()
    
    for b in J:
        if res[ix[(a,b)]] == 1:
            if b not in visitados:
               # aux2.append(b) 
                visitados.append(b)
                #aux2.clear()
                aux.append(b)
            else: 
                aux.clear()
         
          
        
#from itertools import permutations
               
#a = permutations(visitados)
#print(a[1])

print(visitados)
import itertools
a= list(itertools.permutations(visitados,2))
print(a)



cpx.linear_constraints.add(lin_expr=[cplex.SparsePair(\
                                      [ix[a[i]] for i in range(len(a))],\
                                      [1.0 for i in range(len(a))])],\
                                      senses = 'L',\
                                      rhs = [len(visitados)-1]) 


cpx.write("teste.lp")


















#print(len(visitados))
#=(len(visitados))
#Variáveis =  (X(0,3) + X(0,1) + X(3,0) + X(3,1)+ X(1,0) + X(1,3) <= LEN(VISITADOS) -1 )
#                
#
# Se ele escolher algum ponto que já está em visitados, Sum (XIJ) irá para 3, 
# mas o Len visitados não aumenta devido ao segundo if (linha 81)
#if len(visitados) != len(I):
    #print('Tem Sub-rotas. Adicionar restrição')
    #[cpx.linear_constraints.add(lin_expr=[cplex.SparsePair(\
                                         #[ix[] for b in k2],\ 
                                         #[1.0 for b in k2])],\
                                         #senses = 'L',\
                                         #rhs = k-1) for a in K] 
    #cpx.solve()
    #print(cpx.solution.get_objective_value())
    #res =  cpx.solution.get_values()
    
        
#else:
    #break      
             
           


           

           
           
           
           
           
           
           
           
           
           
           
           
        