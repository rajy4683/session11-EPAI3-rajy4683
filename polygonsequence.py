from polygonlib import ConvexPolygon
from functools import lru_cache
import math
import numbers
import decimal

class PolygonSequences():
    '''
    Polygon Iterable class that generates all polygons for a given circumradius and upto the max edges specified by n_sides.
    E.g: If input radius = 4 and n_sides = 10, polygons starting from sides = 3,4,...10 of size 4 will be generated
    Returns Iterable of ConvexPolygon class.
    '''
    def check_number_type(self, x):
        if isinstance(x, bool):
            return False
        if isinstance(x, complex):
            return False
        return isinstance(x, numbers.Number)
    
    def __init__(self, n_sides, circumradius):
        """
        n_sides and circumradius are expected to be numbers
        """
        if (self.check_number_type(n_sides) == False or
            self.check_number_type(circumradius) == False):
            raise TypeError
                
        if n_sides < 3:
            raise ValueError(f'Minimum number of sides should be 3. Input n_sides={n_sides} ')
            
        self.max_poly_edges = n_sides
        self.circumradius = circumradius
        self._offset_to_polysides =  { idx:PolygonSequences._polygonator(i, self.circumradius) for idx,i in enumerate(range(3, self.max_poly_edges+1, 1)) }
        self.max_efficient_poly = self.get_max_efficiency_poly()
    
    def get_max_efficiency_poly(self):
        '''
        Returns the max efficient polygon. We can make a simple hack to use the one with largest number of edges.
        '''
        max_pol_ratio = self._offset_to_polysides[0].get_area/self._offset_to_polysides[0].get_perimeter
        max_pol_offset = 0
        for k,v in self._offset_to_polysides.items():
            curr_ratio = v.get_area/v.get_perimeter
            if curr_ratio > max_pol_ratio:
                max_pol_offset = k
                max_pol_ratio = curr_ratio
        return self._offset_to_polysides[max_pol_offset]
    def __repr__(self):
        '''
        Repr for Polygon sequence
        '''
        return f"Instance of PolygonSequences class. Max Edges:{self.max_poly_edges} Radius:{self.circumradius} Len: {len(self._offset_to_polysides)}"
    def __len__(self):
        '''
        Total length of the sequence. This will be equal to the max value provided during sequence creation.
        '''
        return len(self._offset_to_polysides)    
    def __getitem__(self, s):
        '''
        Allows for proper iteration of the sequence.
        '''
        if isinstance(s, int):
            if s < 0:
                s = self.__len__() + s
            if s < 0 or s >=self.__len__():
                raise IndexError(f"Invalid Index.")
            else:
#                 return PolygonSequences._polygonator(self.offset_to_polysides[s], self.circumradius)
                return self._offset_to_polysides[s]
        else:
#             print(type(s))
            start, stop, step = s.indices(self.__len__())
#             return [PolygonSequences._polygonator(self.offset_to_polysides[i], self.circumradius) for i in range(start, stop, step)]
            return [self._offset_to_polysides[i] for i in range(start, stop, step)]
            
    def __iter__(self):
#         print("Calling Polygon Sequence __iter__")
        return self.PolygonSqIterator(self) 
    
    @staticmethod 
    @lru_cache(2**10) 
    def _polygonator(n_sides, circumradius):                
        if n_sides < 3:
            raise ValueError(f'Minimum number of sides for a polygon is 3')
        
        return ConvexPolygon(n_sides, circumradius)
    
    class PolygonSqIterator:
        '''
        The iterator class over Polygon sequence that converts it into an iterable.
        Implements __next__ and __iter__ functions.
        '''
        def __init__(self, polygon_sq_obj):
#             print("Calling PolygonSqIterator __init__")
            self.polygon_sq_obj = polygon_sq_obj
            self._index = 0
            
        def __iter__(self):
            '''
            Basic __iter__ method that returns an instance of the iterator
            '''
#             print("Calling PolygonSqIterator instance __iter__")
            return self
        
        
        def __next__(self):
            '''
            Implementation of __next__ function. Throws StopIteration when length is bypassed.
            '''
#             print("Calling PolygonSqIterator __next__")
            if self._index >= len(self.polygon_sq_obj):
                raise StopIteration
            else:
                item = self.polygon_sq_obj._offset_to_polysides[self._index]
                self._index += 1
                return item
    