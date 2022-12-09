import cplex
import itertools #import para fazer o permutation
import math
from math import sin, cos, sqrt, atan2, radians,e

c=list()
c1=list()
c2=list()
latitude = list()
longitude = list()
texto = open('testecoord.txt')  #testecoord -  burma14,  testecoord2- att48, testecoord3 - bayg29
for linha in texto:
    linha= linha.rstrip()
    aux_txt = linha.split(' ')
    c1.append(aux_txt[:])
    aux_txt.clear()
print(c1)
texto.close()


var1=int(len(c1))
var2=int(len(c1[0]))


for i in range(var1):
    latitude.append(float(c1[i][0]))
    longitude.append(float(c1[i][1]))

print('latitude')
print(latitude)
print('longitude')
print(longitude)


for a in range(var1):         #for para calcular a distância através da latitude e longitude
    for b in range(var1):
               
        lat1 = radians(latitude[a])
        lon1 = radians(longitude[a])
        lat2 = radians(latitude[b])
        lon2 = radians(longitude[b])
 
        dlon = lon2 - lon1
        dlat = lat2 - lat1
 
        operacao1 = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        operacao2 = 2 * atan2(sqrt(operacao1), sqrt(1 - operacao1))
 
        
        
        if a != b:
            c2.insert(b,6371.0 * operacao2)
            
        else:
            c2.insert(b,99999)
    c.append(c2[:])
    c2.clear()
    

    
i=var1
j=i

I=range(i)
J=range(j)    
IJ = [(a,b) for a in I for b in J]      #criação da lista com identificação dos pontos, ex.: IJ = [(0,0),(0,1),...(4,4)]

subrotas = []                           #lista subrotas vai receber todos os pontos para acompanhar se tem restrição para todas as subrotas

cpx=cplex.Cplex()



nx = ['x(' + str(i)+','+str(j)+')' for i in I for j in J]       #lista para nomear os index do dicionário, ex.: ['x(0,0)','x(0,1)',...'x(4,4)']


ix = {(a,b): idx for idx, (a,b) in enumerate(IJ)}       #dicionário para fazer a conversão, ex.: Chamar ix[(0,0)] = 0 | ix[(0,1)] = 1


cpx.variables.add(obj = [c[a][b] for b in range(j)\
                      for a in range(i)],
                    lb = [0.0]*i*j, ub=[cplex.infinity]*i*j,types = ['B']*i*j, names = nx)      #Função objetivo
    
vet_1=[]
[vet_1.append(1) for a in I]        #vetor de 1 para adicionar as restrições

[cpx.linear_constraints.add(lin_expr=[cplex.SparsePair(\
                                     [ix[(a,b)] for b in J],\
                                      [1.0 for b in J])],\
                                      senses = 'E',\
                                      rhs = [vet_1[a]]) for a in I ]    #restrição de i só poder ir para um j
    
[cpx.linear_constraints.add(lin_expr=[cplex.SparsePair(\
                                     [ix[(a,b)] for a in J],\
                                      [1.0 for a in J])],\
                                      senses = 'E',\
                                      rhs = [vet_1[b]]) for b in I ]    #restrição de i só poder receber um j


v=0                 #vértice
visitados = [v]     #vetor visitados vai armazernar os valores em uma rota para determinar se possui subrota
aux = [v]           #usado para manipular a lista visitados

[subrotas.append(a) for a in I]     #preencheu o vetor das subrotas para verificar se acabaram as subrotas
                                      
cpx.solve()
print('RESULTADO FUNÇÃO OBJETIVO')
print(cpx.solution.get_objective_value())

res = cpx.solution.get_values()     #lista com valores binários para identificar para onde cada ponto foi


while len(visitados) != i:          #repetir enquanto a rota não conseguir fechar sem acabar com as subrotas
    
    while len(subrotas) > 1:        #repetir enquanto não tiver criado restrição para as subrotas encontradas no último resultado do cplex
    
        print('subrotas')
        print(subrotas)
        
        while aux:                  #função de retornar uma lista de um ciclo a partir de um primeiro ponto
            
            a= aux.pop()
            
            for b in J:
                if res[ix[(a,b)]] == 1:
                    if b not in visitados:
                       # aux2.append(b) 
                        visitados.append(b)
                        print('visitados dentro do for')
                        print(visitados)
                        #aux2.clear()
                        aux.append(b)
                    else: 
                        aux.clear()
                 
        if len(visitados) != i:         #se a lista criada não possuir o mesmo número de pontos do sistema vai ser criado restrição 
                
            print('visitados')
            print(visitados)
            
            a= list(itertools.permutations(visitados,2))        #criar uma permutação a partir das surotas da lista visitados[]
            print('permutação')
            print(a)
            
            
            
            cpx.linear_constraints.add(lin_expr=[cplex.SparsePair(\
                                                  [ix[a[i]] for i in range(len(a))],\
                                                  [1.0 for i in range(len(a))])],\
                                                  senses = 'L',\
                                                  rhs = [len(visitados)-1])     #restrição criada a partir da permutação da subrota visitados[]
            
            [subrotas.remove(visitados[a]) for a in range(len(visitados))]      #remove da lista subrota os pontos que já foram criado restrições         
            
            print('subrotas')
            print(subrotas)
            
            if len(subrotas) >= 2:          #se tiver mais alguma subrota
                aux.append(subrotas[0])     #setando um valor para ele procurar subrota 
            
            visitados.clear()               #limpando o vetor para ele preencher com o novo ciclo
    
    cpx.solve()
    print('RESULTADO FUNÇÃO OBJETIVO')
    print(cpx.solution.get_objective_value())
    res = cpx.solution.get_values()
    
    
    v=0                 #linha 56
    visitados = [v]     #linha 57
    aux = [v]           #linha 58
    
    while aux:          #verificando se o novo ciclo com as restrições possui subrota
                    
        a= aux.pop()
        
        for b in J:
            if res[ix[(a,b)]] == 1:
                if b not in visitados:
                    visitados.append(b)
                    print('visitados dentro do for')
                    print(visitados)
                    aux.append(b)
                else: 
                    aux.clear()

    if len(visitados) != i:                 #caso ainda exista subrota, retando os valores para repetir o processo e adicionar mais subrotas
        [subrotas.append(a) for a in I]
        v=0
        visitados = [v]
        aux = [v]
        
cpx.write("modelo_matematico_tsp_versao_4.1.lp")
cpx.solve()
print('RESULTADO FUNÇÃO OBJETIVO')
print(cpx.solution.get_objective_value())
print(visitados)

