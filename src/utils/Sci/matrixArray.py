# -*- coding: utf-8 -*-

'''
Created on 18 Sep, 2014

PyMatrix implementation based on pure python oop charisma

Description:

@author: WANG LEI / YI, Research Associate @ NTU

@emial: L.WANG@ntu.edu.sg, Nanyang Technologcial University

@licence: licence
'''

from copy import *
from operator import *

# helper function for sign enhance
def enhance(func):
    def wrapper(*args, **key):
        if   args[1] == "sign":
            return args[0] 
        elif args[1] == {'transpose'}:
            return args[0].transpose()
        elif True:    
            obj = func(*args, **key)
            return obj
    return wrapper

_pre_ = []

# helper function to determine size while using selector like mat[:,2,1]     
def detector(*args, **key):
        
    key['shape_record'] = True  
    key['shape_detect'] = []

    # dealing
    if   isinstance(args[1],   int):
        key['shape_detect'].append( 1 )
    elif isinstance(args[1], slice):
        
        start, stop, step = args[1].indices(len(args[0]))
                                        
        l = range(start, stop, step)
        
        key['shape_detect'].append( len(l) )
        
    elif isinstance(args[1],  list):
        
        l = args[1]
        
        g = args[0].get_shape_array()
        
        i = 0
        
        for x in l:
            if   isinstance(x, int):
                key['shape_detect'].append( 1 )
            elif isinstance(x, slice):
                
                start, stop, step = x.indices( g[i] )
                
                lx = range(start, stop, step)
                
                key['shape_detect'].append( len(lx) )
                
            elif isinstance(x,  list):
                key['shape_detect'].append( len( x ))
            elif isinstance(x, tuple):
                key['shape_detect'].append( len( x ))
            
            # mimic the process, should not be called recursively    
            i += 1
            # ~~
                
    elif isinstance(args[1], tuple):
        
        l = args[1]
        
        g = args[0].get_shape_array()
        
        i = 0
        
        for x in l:
            if   isinstance(x, int):
                key['shape_detect'].append( 1 )
            elif isinstance(x, slice):
                
                start, stop, step = x.indices( g[i] )
                
                lx = range(start, stop, step)
                
                key['shape_detect'].append( len(lx) )
                                            
            elif isinstance(x,  list):
                key['shape_detect'].append( len( x ))
            elif isinstance(x, tuple):
                key['shape_detect'].append( len( x ))
                
            # mimic the process, should not be called recursively    
            i += 1
            # ~~
    
    # write back 
    try:
        args[2].shp=key['shape_detect'] 
    except Exception as e:
        pass  
              
    return key['shape_detect']

#===============================================================================
# operations between matrix
#===============================================================================
def Union(*Mats):
    '''
    Created on 10 Dec, 2014
    
    @author: wangyi, Researcher Associate @ EIRAN, Nanyang Technological University
    
    @email: L.WANG@ntu.edu.sg
    
    @copyright: 2014 www.yiak.co. All rights reserved.
    
    @license: license
    
    @param: 
    
    @decription:
    
    @param: Union
    '''

    def Union2Mat(Matl, Matr):
        
        if  isinstance(Matl, matrixArrayBase) and isinstance(Matr, matrixArrayBase):
            sizel = Matl.get_shape_array()
            sizer = Matr.get_shape_array()

            for i in range(0, max(sizel[0],sizer[0])):
                r = Matl[i]
                if   r != None:
                    # see documentation for difference between () and []
                    Matl(i).extend(Matr[i])
                    
                elif r == None:
                    # do assignment
                    Matl[i]=Matr[i]
    
    # create an empty matrix            
    mat = matrixArrayBase()
    
    # loop
    for obj in Mats:
        Union2Mat(mat, obj)
    
    return mat

def Intersection():
    pass

def rowTtf():
    pass

def colTtf():
    pass

#===============================================================================
# matrix base for elementary matrix manipulation, whose element should be of any types
#===============================================================================
class matrixArrayBase(list):
    '''
    Created on 17 Nov, 2014
    
    @author: wang yi/Lei, Researcher Associate @ EIRAN, Nanyang Technological University
    
    @email: L.WANG@ntu.edu.sg
    
    @copyright: 2014 www.yiak.co. All rights reserved.
    
    @license: license
    
    @decription: N-Matrix container for objects of any type. It then could be 2 or demensions numeric matrix for computation
    
    @param:
    '''
    def __init__(self, *args, **hint):   
        self.row = 0
        self.col = 0
        self.shp = None
      
        # when debug, we provide to modes
        self.debug = False
        try:
            self.debug = hint['debug']
        except KeyError as e:
            pass
      
        # shape record
        self.shp = None
        try:
            self.shp   = hint['shape']
        except KeyError as e:
            pass
      
        numberOfargs = len(args)
        if   numberOfargs == 0:
            if   hint == {}:
                pass
            # no element specified
            elif hint != {}:
                # set up empty matrix
                # no, row, col or dimensions
                super(matrixArrayBase, self).__init__()
             
        elif numberOfargs == 1:
            if   isinstance(args[0], int):
                # create square null matrix
                # just for 2-D cases
                # what is about 3-D?
                super(matrixArrayBase, self).__init__()
                # To do: specify n * n null matrix
            elif isinstance(args[0], list):
                # copy or convert
                super(matrixArrayBase, self).__init__()
                # this works for matrix
                self.setUp( args[0] )    
                 
        elif numberOfargs == 2:
            if   isinstance(args[0], int) and isinstance(args[1], int):
                super(matrixArrayBase, self).__init__()    
                # To do: specify m * n null matrix
                self.nil(args[0], args[1])
                 
                 
            elif isinstance(args[0], int) and isinstance(args[1], list):
                super(matrixArrayBase, self).__init__()
                # To do: specify n * n null matrix
                self.nil(args[0], args[0])
                 
        elif numberOfargs  > 2:
            for i in range( 0, len(args) ):
                if not isinstance(args[i], int):
                    break
 
            if  i == 0 and isinstance(args[ 0 ], list):
                # To do: matrix cantenation
                super(matrixArrayBase, list).__init__()
                
                self = Union(*args) 
            
            # otherwise:
            self.shp = args[0:i]
                                  
            if  i != 0 and isinstance(args[ i ], list):
                # To do: specify, filling missing data by other iteratables
                super(matrixArrayBase, list).__init__()
                self.fillUp(args[i+1:])
        
        # when debug, please comment the following lines, otherwise comment out
        # analyze the size
        size = self.get_shape_array()[0:-1]
        if   len(size) == 2:
            self.row = size[0]
            self.col = size[1]
        elif len(size) == 1:
            if  self.shp:
                try:
                    if   self.shp[0] == 1 and self.shp[1] and self.shp[1] != 1:
                        self.row = 1
                        self.col = size[0]
                    elif self.shp[0] != 1 and self.shp[1] and self.shp[1] == 1:
                        self.row = size[0]
                        self.col = 1
                    elif self.shp[0] == 1 and self.shp[1] and self.shp[1] == 1:
                        self.row = 1
                        self.col = 1
                except Exception as e:
                    if  self.shp == None:
                        pass
                    else:
                        self.row = 1
                        self.col = size[0]
            else:
                self.row = size[0]
                self.col = 1
        elif len(size) == 0:
            self.row = 0
            self.col = 0
        
    # matrix STL iterators
    class matrixIterator(object):
        def __init__(self, matrixArrayBase):
            self.matrixArray = matrixArrayBase
            self.counter = self.__counter__()
            
        def __iter__(self):
            return self

        ## ! just for two dimensions for the moment
        def __counter__(self):
            # commment the following lines when debug, other wise comment out
            # when apply matrix 2 list this will be call
            size = self.matrixArray.get_shape_array()[0:-1]

            tier = len(size)
            iter = tier * [0]
            
            while True:
                yield iter
                
                def routine(iter, size, curr):
                    iter[curr] += 1         
                    if  iter[curr] >= size[curr]:
                        if   curr  == 0:
                            return    0
                        elif True:
                            iter[curr] = 0
                            return routine(iter, size, curr - 1)              
                    return 1
                     
                signal = routine(iter, size, tier - 1)
        
                if  signal == 0:
                    break
# compare to the old version you might find it much more universal ^ ^                
# the following codes just used for 2-demension matrix container        
#             i = 0
#             j = 0
#             while True:
#                 yield [i,j]
#                 j = j + 1
#                 if  j >= size['col']:
#                     j = 0
#                     i = i + 1
#                     if  i >= size['row']:
#                         break 
     
        def __next__(self):
            try:
                index = next(self.counter)
                return self.matrixArray[index]
            except StopIteration as e:
                raise StopIteration()   
    
        def nextIndex(self):
            try:
                index = next(self.counter)
                return index
            except StopIteration as e:
                raise StopIteration()
            
    def name(self):
        return "matrixArrayBase:"
    #===========================================================================
    # n-d matrix size detector: when it is 2-d or 1-d, it reduces to {row, col} form
    #===========================================================================
    def size(self):
        shp = self.shape()
        if  isinstance(shp, dict):
            return "row:{row}, col:{col}".format( **shp )
        if  isinstance(shp, list):
            return "raw shape: {0}".format( str(shp) )

    def shape(self):
        # first get raw demen based on actual container size        
        shp = self.get_shape_array()[0:-1]
        
        # third step, visualize it
        if len(shp) == 0:
            self.row = 0
            self.col = 0
            return {'row':self.row, 'col':self.col}
        if len(shp) == 1:
            if  self.shp:
                try:
                    if   self.shp[0] == 1 and self.shp[1] != 1:
                        self.row = 1
                        self.col = shp[0]
                    elif self.shp[0] != 1 and self.shp[1] == 1:
                        self.row = shp[0]
                        self.col = 1
                    elif self.shp[0] == 1 and self.shp[1] == 1:
                        self.row = 1
                        self.col = 1
                        
                        return self.shp
                except Exception as e:
                    if  self.shp == None:
                        pass
                    else:
                        self.row = 1
                        self.col = shp[0]
            else:    
                self.row = shp[0]
                self.col = 1
            
            return {'row':self.row, 'col':self.col}
        if len(shp) == 2:
            self.row = shp[0]
            self.col = shp[1]
            return {'row':self.row, 'col':self.col}
        
        # return result
        return shp
    
    def __call__(self, key, value=None):
        if   value == None:
            return super(matrixArrayBase, self).__getitem__(key)
        elif value != None:
            super(matrixArrayBase, self).__setitem__(key, value)
            return self
        
    #===================================================================
    # basic matrix set element function:
    # it might changes the size after runtime modification, like 1-d vector becomes 2-d matrix
    #===================================================================
    def __setitem__(self, key, value):   
        # currently set method doesn't support selector     
        if   isinstance(key, int):
            while True:
                try:
                    # old method
                    self(key, value)#super(matrixArrayBase, self).__setitem__(key, value)
                    break  
                except Exception as inst:
                    if  self.debug == True:
                        print(key, inst, 'set')
                    self.append(None)
                
        elif isinstance(key, tuple) or isinstance(key, list):
            if   key.__len__() == 1:
                self[key[0]] = value
            elif key.__len__() == 2:  
                if  self.row == 1 and key[0] == 0:
                    self[key[1]] = value
                    return
                if  self.col == 1 and key[1] == 0:
                    self[key[0]] = value
                    return
                # get list
                while True:
                    try:
                        # old method
                        t = self(key[0])#super(matrixArrayBase, self).__getitem__(key[0])
                        break
                    except IndexError as e:
                        if  self.debug == True:
                            print(key[0], e, 'set')
                        self.append(None)
                
                # test codes
                if  not isinstance(t, matrixArrayBase) and not isinstance(t, list) and t != None:
                    t  = [t]
                    self(key[0], t)
                    
                if  t == None:# t == None
                    t  = []
                    self(key[0], t)#super(matrixArrayBase, self).__setitem__(key[0], t)
                
                while True:
                    try:
                        t[key[1]] = value
                        break
                    except Exception as inst:
                        if  self.debug == True:
                            print(key[1], inst, 'set')
                        t.append(None)
#               self[key[0]][key[1]] = value              
            elif len(key) >= 3:
                l = len(key) 
                # iteration part
                i = 1
                
                while True:
                    try:
                        # old method
                        t = self(key[0])#super(matrixArrayBase, self).__getitem__(key[0])
                        break
                    except IndexError as e:
                        if  self.debug == True:
                            print(key[0], e, 'set')
                        self.append(None)
                    
                if  t == None:# t == None
                    t  = []
                    self(key[0], t)#super(matrixArrayBase, self).__setitem__(key[0], t)
                
                while i < l - 1:
                    while True:
                        try:
                            s = t
                            t = s[key[i]]
                            break
                        except IndexError as e:
                            if  self.debug == True:
                                print(key[i], e, 'set')
                            s.append(None)
                    
                    if  t == None: # t == None
                        t = []
                        s[key[i]] = t
                    
                    i += 1
                # get list
                while True:
                    try:
                        t[key[l-1]] = value
                        # do not need to process error
                        break
                    except Exception as inst:
                        if  self.debug == True:
                            print(inst)
                        t.append(None)
#               self[key[:l-1]][key[l-1]] = value
#               print(self)

        elif True:
            raise TypeError("index must be int or slice")
        
    #==========================================================================
    # elementray get element function
    #==========================================================================
    def __getitem__(self, key):
        
        if   isinstance(key, int):
            try:
                result = self(key)#super(matrixArrayBase, self).__getitem__(key)#how can we get sub matrixArray, i.e. mat is result : True
            except IndexError as e:
                if  self.debug == True:
                    print(key, e, 'get')
                return None
            if  isinstance(result, list):
                return matrixArrayBase(result)# this method is bad
            elif True:
                return result
        elif isinstance(key, slice):
            
            start, stop, step = key.indices(len(self))
            
            results = []
            
            for i in range(start, stop, step):
                results.append(self(i)) 
                       
            return matrixArrayBase(results)# this method is bad      
            
        elif isinstance(key, tuple) or isinstance(key, list) :
            # add codes here
            
            if   key.__len__() == 0:
                # return self
                return self
            elif key.__len__() == 1:
                # a special case
                return self[key[0]] # call user defined
            elif key.__len__()  > 1:
                try:
                    if   isinstance(key[0], int):
                        # recursively calling
                        return self[key[0]][key[1:]]
                    elif isinstance(key[0], tuple ) or isinstance(key[0], list):
                        # I would like to change it in the future to support logic vecotrs like matlab, honestly speaking this is the very cool characteristics in matlab
                        return self[key[0]][key[1:]]
                    elif isinstance(key[0], slice):
                        # additional procession
                        results = self[key[0]]
                        # in the future, I will change it to canecation matrix
                        l = len(results)
                        
                        tmarray = []
                        
                        for i in range(0, l):
                            tmarray.append(results[i][key[1:]])
                            
                        results = tmarray
                                      
                        return matrixArrayBase(results)# this method is bad 
                    
                except Exception as inst:
                    if  self.debug == True:
                        print(inst)
                    # if column vector                          
                    if  self.row == len(self):#self.col == 1:
                        flag = 1
                        for item in key[1:]:
                            if item != 0:
                                flag = 0
                                return None#raise( TypeError("wrong index") )
                        if  flag == 1:
                            return self[key[0]]
                        
                    # if row vector
                    if  self.col == len(self):#self.row == 1:
                        flag = 1
                        for item in key[:key.__len__()-1 ]:
                            if item != 0:
                                flag = 0
                                return None#raise( TypeError("wrong index") )
                        if flag == 1:
                            return self[key[key.__len__()-1]]
                    
                    # universial purpose
                    if  str(inst) == 'list index out of range':
                        return None
                    
            elif True:
                raise TypeError("index must be int or slice")
        
        
    def __setattr__(self, name, value):
        if   isinstance(name, tuple):
            pass
        elif True:
            self.__dict__[name] = value   
    
    def __iter__(self):
        return self.matrixIterator(self)
    #===========================================================================
    # n-d array size detector
    #===========================================================================
    def get_shape_array(self):
        queue = []
        dems = []
        axis= 0
        
        # updating current axis
        dems.append( self.__len__() )
        # updating axis 
        axis += 1
        
        # start processing
        queue.append( (self, axis) )
        # compute next demensions      
        def routines(obj, dems, axis, queue):
            while queue.__len__() > 0:
                obj, axis = queue.pop(0)
                # temporary storage
                tm = []
                
                if   isinstance(obj, matrixArrayBase):
                    if   obj.__len__() == 0:
                        tm.append(0)
                    elif obj.__len__() >= 1:
                        # broadth first searching
                        for i in range(0, len(obj) ):
                            if  isinstance(obj(i), list):
                                tm.append( obj(i).__len__() )
                                # broadth first
                                queue.append( (obj(i), axis + 1) )
                            elif True:
                                tm.append( 1 )
                         
                        # updating current axis - Mat lenth
                        # axis control the looping layer        
                        try:
                            if  dems[axis] < max( tm ):
                                dems[axis] = max( tm )
                        except:
                            dems.append( max( tm ) )
                
                elif isinstance(obj, list):
                    if   obj.__len__() == 0:
                        tm.append(0)
                    elif obj.__len__() >= 1:
                        # broadth first searching
                        for i in range(0, len(obj) ):
                            if  isinstance(obj[i], list):
                                tm.append( obj[i].__len__() )
                                # broadth first
                                queue.append( (obj[i], axis + 1) )
                            elif True:
                                tm.append( 1 )
                         
                        # updating current axis - Mat lenth
                        # axis control the looping layer        
                        try:
                            if  dems[axis] < max( tm ):
                                dems[axis] = max( tm )
                        except:
                            dems.append( max( tm ) )           
                elif True:
                    pass             
                      
        routines(self, dems, axis, queue)  
        
        return dems    
    #===========================================================================
    # elementary setup funciton from a iterable
    #===========================================================================
    def setUp(self, l=None):
        # clearn up
        self.clear()
        # set up container values
        if  str(type(l)) == "<class 'list'>":
            self.extend(l)
        else:
            iti = l.__iter__()
            itv = l.__iter__()
            while True:
                try:
                    index = iti.nextIndex()
                    value = itv.__next__()
                    # use redefined method
                    self[index] = value
                except StopIteration as e:
                    break
        # modify shape accordingly
    #===============================================================================
    # basic matrix filling function, m = matrixArray(list1, list2, list3 ...)
    #===============================================================================
    def fillUp(self, *iterators):
        obj = self
        
        for itx in iterators:
            itl = obj.__iter__()
            itr = itx.__iter__()
            while True:
                try:
                    p = itl.nextIndex()
                    q = itr.__next__()
                    # use redefined method
                    obj[p] = q                  
                except StopIteration as e:
                    break 
        
        return self
    
    # this help funciton is exclusively for 2-demension case. I consider it seriously. 
    def nil(self, r, c, value=None):
        super(matrixArrayBase, self).clear() 
        # set size 
        self.shp = [r,c]        
#       self.head = [None] * self.row
        if   r > 1:
            row = [value] * c
            
            for r in range(0, r):
#               self.head[r] = deepcopy(row)
                super(matrixArrayBase, self).append(deepcopy(row))
        elif r == 1:
            for i in range(0, c):
                self.append(value) 
    
    # further extension form nil funciton            
    def Zeors(self, r, c=None):
        if  c == None:
            self.nil(r, 0)
        else:
            self.nil(r, c, 0) 

        
class matrixArray(matrixArrayBase):
    '''
    Created on 15 Nov, 2014
    
    @author: wangyi, Researcher Associate @ EIRAN, Nanyang Technological University
    
    @email: L.WANG@ntu.edu.sg
    
    @copyright: 2014 www.yiak.co. All rights reserved.
    
    @license: license
    
    @decription:
    
    @param: 
    '''
    
    def __init__(self, *args, **hint):
        '''
        Constructor
        '''
        super(matrixArray, self).__init__(*args,  **hint)
   
    def __getitem__(self, key):
       
        smat = super(matrixArray, self).__getitem__(key)  
        
        shpM = detector(self,key, smat) 
        
        if  shpM == [4, 1, 1]:
            pass
        
        if  isinstance(smat, matrixArrayBase):
            return matrixArray(smat, shape=shpM)
        else:
            return smat
#===============================================================================
# 2 - D Matrix Array Representation: 
#===============================================================================
    def __str__(self):
        size = self.get_shape_array()[0:-1]
        if   len(size) == 2:
            self.row = size[0]
            self.col = size[1]
        elif len(size) == 1:
            if  self.shp:
                try:
                    if   self.shp[0] == 1 and self.shp[1] != 1:
                        self.row = 1
                        self.col = size[0]
                    elif self.shp[0] != 1 and self.shp[1] == 1:
                        self.row = size[0]
                        self.col = 1
                    elif self.shp[0] == 1 and self.shp[1] == 1:
                        self.row = 1
                        self.col = 1
                except Exception as e:
                    if  self.shp == None:
                        pass
                    else:
                        self.row = 1
                        self.col = size[0]
            else:
                self.row = size[0]
                self.col = 1
        elif len(size) == 0:
            self.row = 0
            self.col = 0
           
        if   len(size)  > 2:
            return self.name() + '\n' + super(matrixArray, self).__str__()
           
        if   self.shp and len(self.shp) > 2 and self.shp[2] > 1:
            return self.name() + '\n' + super(matrixArray, self).__str__()  
           
        str = self.name() + '\n' 
        str = str + "["
        str = str + '{:1s}'.format(' ')
           
        # column vector
        if  self.col == 1:
            for i in range(0, self.row):
                try:
                    str = str + '{:<.2f} '.format(self[i])# '{:<.2f} '
                except TypeError  as e:
                    str = str + '{:s}'.format('null ')
                except ValueError as e:
                    str = str + '{:<} '.format(self[i])
                   
                if  i + 1 < self.row:
                    str = str + "\n  "
                      
        # row vector
        elif self.row == 1:
            for j in range(0, self.col - 1):
                try:
                    str = str + '{:<10.2f}'.format(self[j])# '{:<10.2f}'
                except TypeError as e:
                    str = str + '{:<10s}'.format('null')
                except ValueError as e:
                    str = str + '{:<10}'.format(self[j])
                      
            try:
                str = str + '{:<.2f}'.format(self[self.col - 1]) # '{:<.2f}'
            except TypeError as e:
                str = str + '{:s}'.format('null')
            except ValueError as e:
                str = str + '{:<}'.format(self[self.col - 1])
                  
            str = str + '{:1s}'.format(' ')
        # matrix
        elif True:        
            for i in range(0, self.row):
                for j in range(0, self.col):
                       
                    if   j + 1 < self.col:
                        try:
                            str = str + '{:<10.2f}'.format(self[i,j])# '{:<10.2f}' #.format(super(matrixArray, self).__getitem__(i).__getitem__(j))
                        except TypeError  as e:
                            if  e.__str__() == 'non-empty format string passed to object.__format__':
                                str = str + '{:10s}'.format('null')
                        except ValueError as e:
                            str = str + '{:<10}'.format(self[i,j])
                                  
                    elif True:
                        try:
                            str = str + '{:<.2f}'.format(self[i,j])# '{:<.2}' #.format(super(matrixArray, self).__getitem__(i).__getitem__(j))
                            str = str + ' '
                        except TypeError  as e:
                            if  e.__str__() == 'non-empty format string passed to object.__format__':
                                str = str + '{:s}'.format('null') 
                                str = str + ' ' 
                        except ValueError as e: 
                            str = str + '{:<}'.format(self[i,j])# '{:<.2}' #.format(super(matrixArray, self).__getitem__(i).__getitem__(j))
                            str = str + ' '                                
                       
                if i + 1 < self.row:
                    str = str + '\n'
                    str = str + '{:1s}'.format('  ')
                       
        str = str + "]"
        return str
    
    def name(self):
        return "matrixArray:"

## for operation
#===============================================================================
# 2-D matrix basic computation
#===============================================================================
    def equal_size(self, object):
        sizel = self.shape()
        sizer = object.shape()
        
        if sizel['row'] != sizer['row']:
            raise( TypeError('matrix size unmatched') )
        if sizel['col'] != sizer['col']:
            raise( TypeError('matrix size unmatched') )

    def __neg__(self):
        return self.map(neg)

    @enhance
    def __add__(self, object):
        self.equal_size(object)
        return self.map(add, object)
    
    @enhance
    def __sub__(self, object):
        self.equal_size(object)
        return self.map(sub, object)
    
    @enhance
    def __mul__(self, object):
        self.tolerate(object)
        return self.dot(object)
    
    @enhance
    def __gt__(self,  object):
        pass

## just for 2-D matrix 
## for linear algebra
#===============================================================================
# 2-D matirx linear algebra
#===============================================================================
    def transpose(self):
        mat = matrixArray(self.col, self.row) 
        
        for i in range(mat.row):
            for j in range(mat.col):
                mat[i,j] = self[j,i]
                
        return mat
    
    # test wether two matrix can tolerate each other
    def tolerate(self, object):
        sizel = self.shape()
        sizer = object.shape()
        
        if  sizel['col'] == sizer['row']:
            return
        raise( TypeError("matrix does not tolerate to the object!") )
    
    def dot(self, object):
        self.tolerate(object)
        
        if  self.row == 1 and object.col == 1:
            sum = 0.0
            for k in range(self.col):
                sum += self[0,k] * object[k,0]
            
            return sum
        
        mat = matrixArray(self.row, object.col)
        
        for i in range(mat.row):
            for j in range(mat.col):
                sum = 0.0
                for k in range(self.col):
                    sum += self[i,k] * object[k,j]
                mat[i,j] = sum
                
        return mat
      
    def svdDec(self):
        pass
    
    def __div__(self, obj):
        pass
            
## just for 2-D matirx            
## for computation
##    
    def map(self, Func, *iterables):
        mapobject = map(Func, self, *iterables)
        
        return matrixArray([m for m in mapobject])
    
    @staticmethod
    def main():
        pass

# MATRIXDILIMITERPATTER = "\[ (\n  )* \]"
# MATRIXOBJECTPATTER    = "(format(number)*number)*"

x = 'sign'
_x_ = x

T = 'transpose'
_T_ = T