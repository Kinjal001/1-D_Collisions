class Empty(Exception):
    '''Error raised while attempting to access an element from an empty container'''
    pass

'''implementing heap class to store list of (t,i,x)'''
class Heap():

    #various class methods
    def _parent(self,j):
        return (j-1)//2

    def _left(self,j):
        return 2*j+1

    def _right(self,j):
        return 2*j+2

    def _has_leftchild(self,j):
        return self._left(j)<len(self._data)

    def _has_rightchild(self,j):
        return self._right(j)<len(self._data)

    def _swap(self,i,j):
        self._data[i],self._data[j]=self._data[j],self._data[i]

    def _swapindex(self,i,j):
        self._index[self._data[i][1]],self._index[self._data[j][1]]= self._index[self._data[j][1]],self._index[self._data[i][1]]

    def _upheap(self,j):
        parent=self._parent(j)
        if j>0 and self._data[j]<self._data[parent]:        #checking heap condition
            self._swap(j,parent)
            self._swapindex(j,parent)                       #swaping indexes to track all the indexes of i th collision after we swap 
            self._upheap(parent)

    def _downheap(self,j):
        parent=self._parent(j)
        if self._has_leftchild(j):
            left=self._left(j)
            small_child=left
            if self._has_rightchild(j):
                right=self._right(j)                        
                if self._data[right]<self._data[left]:
                    small_child=right                               #selecting smallest child 
            if self._data[small_child]<self._data[j]:
                self._swap(j,small_child)                           #swapping wrt heap condition and also swapping indexes
                self._swapindex(j,small_child)
                self._downheap(small_child)

    #fast buildheap, time complexity=O(n)
    def __init__(self,lis):
        l=len(lis) 
        self._data = [] 
        #list to store index for i th collision at i th index
        self._index = [i for i in range(l)]             
        for i in range(l):
            self._data.append(lis[i])                
        if(len(self._data)>1):
            self._heapify()
    
    def _heapify(self):
        #it takes list input and create its heap 
        start = self._parent(len(self._data) -1) 
        for j in range(start, -1, -1): 
            self._downheap(j)

    def top(self):
        return self._data[0]

    def __len__(self):
        return len(self._data)

    def add(self,value):
        self._data.append(value)
        self._upheap(len(self._data)-1)

    def update(self,j,newval):                 #updates and sort heap
        tinitial = self._data[j][0]  
        self._data[j] = newval 
        tfinal = self._data[j][0]        
        if(tfinal<tinitial):                #condition to sort heap after updating
            self._upheap(j)
        else:
            self._downheap(j)

    def is_empty(self):
        return len(self._data)==0

    def min(self):
        if self.is_empty():
            raise Empty('The priority queue is empty.')
        item=self._data[0]                  #minimum element is at the root of heap
        return (item)

    def remove_min(self):
        if self.is_empty():
            raise Empty('The priority queue is empty.')
        self._swap(0,len(self._data)-1)     #swap last and first
        item =self._data.pop()              #remove last and sort heap
        self._downheap(0)
        return (item)

def col_time(i,x,v,T):
        oof=10**100                         #infinite time for no collision between particles
        if v[i]>v[i+1]:                     #condition for collision to occur
            t=(x[i+1]-x[i])/(v[i]-v[i+1])
        else:
            t=oof 
        return t

def listCollisions(M,x,v,m,T):
    
    tixlis=[]   #store initial values for collisions
    output=[]   #list that stores output
    l=len(M)    #length of input lists
    nofcol=0    #total number of collisions
    tmin=0      #total time after each collision considering lowest time from heap
    tlast=[0]*l #last time when the value for i th particle was changed
    oof=10**100 #infinite time for no collision between particles

    for i in range(l-1):
        t=col_time(i,x,v,T)
        tixlis.append([t,i,x[i]])       #list to form heap

    tixheap=Heap(tixlis)            #heap formation

    if tixheap._data[0][0]==oof or l==0 or l==1 or (l==2 and v[0]<=v[1]):       #base cases
        return output

    while nofcol<m and tmin<=T:         
        tmin=tixheap._data[0][0]            #most preffered collision happening in least time
        data=tixheap._data                  #list of heap data
        if tmin<T:                          
            i=data[0][1]                    #index assigning for collision
            treq=tmin-tlast[i]              #time required must exclude the last time when position was changed from total time 
            #calculating and updating values of x,v for i and i+1 particles 
            u1,u2=v[i],v[i+1]
            x[i]=x[i]+v[i]*treq
            x[i+1]=x[i]
            v1=((M[i]-M[i+1])/(M[i]+M[i+1]))*u1 + 2*(M[i+1]/(M[i]+M[i+1]))*u2
            v2=((2*M[i])/(M[i]+M[i+1]))*u1 - ((M[i]-M[i+1])/(M[i]+M[i+1]))*u2
            v[i],v[i+1]=v1,v2
                        
            data[0][2]=x[i]                    
            colele=data[0].copy()               #collsion list
            tcol,xcol=round(colele[0],4),round(colele[2],4)     #round off
            output.append((tcol,colele[1],xcol))
            tlast[i],tlast[i+1]=tmin,tmin       #updating last collision time for i and i+1
            data[0][0]=oof                      #it is provided 3 particles cannot collide altogether so setting time to a large value until next collision
            tixheap._downheap(0)                #heapifying again to get values for next collisions later
            data=tixheap._data                  #updating data

            if i>0:                                                 #0th particle don't have previous element
                x[i-1]=x[i-1]+(tmin-tlast[i-1])*v[i-1]              #updating values for i-1 th particle as position of i th particle hence the time for collision for i-1 and i th particles changed
                iprev=tixheap._index[i-1]                           #location of previous particle in the heap
                tixprev=data[iprev].copy()
                tlast[i-1]=tmin
                if v[i-1]>v[i]:                                     #checking and assigning for collision condition
                    tixprev[0]= (x[i]-x[i-1])/(v[i-1]-v[i]) + tmin
                else:
                    tixprev[0]=oof   

                nofcol=nofcol+1                                     #updating number of collisions
                tixprev[2]=x[i-1]
                if i!= l-2: 
                    nofcol=nofcol-1         #preventing counting of i th collision twice
                tixheap.update(iprev,tixprev)                       #updating heap for previous particle in the heap

            if i<l-2:                                               #i+2 th particle is not defined for i=l-1 and i=l-2 th particles
                inext=tixheap._index[i+1]                           #location of next particle in the heap
                tlast[i+1]=tmin                
                x[i+2]=x[i+2]+(tmin-tlast[i+2])*v[i+2]              #if i+1 th particle has collision, updating for i+1,i+2
                tlast[i+1]=tmin
                tlast[i+2]=tmin
                tixnex=data[inext].copy()
                if v[i+1]>v[i+2]:                                   #checking and assigning for collision condition
                    tixnex[0]= (x[i+1]-x[i+2])/(v[i+2]-v[i+1]) + tmin
                else:
                    tixnex[0]=oof
                nofcol=nofcol+1                                     #updating number of collisions
                tixnex[2]=x[i+1]
                tixheap.update(inext,tixnex)                        #updating heap for next particle in the heap

    return output


#print(listCollisions([1.0, 5.0], [1.0, 2.0], [3.0, 5.0], 100, 100.0))
#print(listCollisions([1.0, 1.0, 1.0, 1.0], [-2.0, -1.0, 1.0, 2.0], [0.0, -1.0, 1.0, 0.0], 5,5.0))
#print(listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 6, 10.0))
#print(listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 100, 1.5))













