import numpy as np
import datetime 
def createGraph(cNodes):    
    structure = {}
    step = 1
    for i in range (cNodes):
        structure[str(i + step)] = [] 

    for i in range (cNodes):
        for j in range (i + 1,cNodes):
            w = np.random.randint(1, 6)

            structure[str(i + step)].append((str(j + step), w))
            structure[str(j + step)].append((str(i + step), w))
    
    return structure, step

def findWay(cNodes, struct, step, T = 1,Tmin = 1e-1000, alpha = 0.5):
    start = str(step)
    curr = start
    next_step = ''

    pb = [start]
    wb = 0

    for i in range (cNodes - 1):
        while True:
            next_step = str(np.random.randint(step, cNodes + 1))
            if next_step not in pb:
                break
        pb.append(next_step)
        
        for l in struct[curr]:
            if l[0] == next_step:
                wb += l[1]
        
        curr = next_step
    pb.append(start)
    for l in struct[curr]:
            if l[0] == start:
                wb += l[1]

    print(' -> '.join(pb))
    print('Вес:', wb)
    
    while T > Tmin:
        pi = [start]
        wi = 0

        for i in range (cNodes - 1):
            while True:
                next_step = str(np.random.randint(step, cNodes + 1))
                if next_step not in pi:
                    break
            pi.append(next_step)
            
            for l in struct[curr]:
                if l[0] == next_step:
                    wi += l[1]
            
            curr = next_step
        pi.append(start)
        for l in struct[curr]:
                if l[0] == start:
                    wi += l[1]

        if (wi - wb <= 0):
            wb = wi
            pb = pi
        else:
            if (np.exp(-(wi - wb) / T) > np.random.uniform(0, 1)):
                wb = wi
                pb = pi
        
        print(' -> '.join(pi))
        print('Вес:', wi)
        T *= alpha
    return pb, wb 


cNodes = 6
structure, step = createGraph(cNodes)
# print(structure)    
start = datetime.datetime.now()
path, weight = findWay(cNodes, structure, step)
end = datetime.datetime.now()
print(end - start)
print('\nКратчайший путь:')
print(' -> '.join(path))
print('Вес:', weight)