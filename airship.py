import collections

RC = collections.namedtuple('rc',['r', 'c',])

class CellMatrix(object):
    def __init__(self):
        self.groups = list()
        self.cells = dict()
    def newCellGroup(self, needed_total, start, length):
        start = RC(*start)
        length = RC(*length)
        self.needed_total = needed_total
        new_group = Group(needed_total)
        for r in xrange(start.r,start.r+length.r):
            for c in xrange(start.c, start.c+length.c):
                if (r,c) not in self.cells:
                    self.cells[RC(r,c)] = Cell()
                new_group.add(self.cells[(r,c)])
        self.groups.append(new_group)
    def reduce(self):       
        keep_reducing = True
        while keep_reducing:
            keep_reducing = False #Only repeat if size of .allowed changes
            for cg in self.groups:
                print cg
                combos = hitTarget(cg.needed_total, cg.cells)
                print combos
                if len(combos): #It crashes unless this line is here.
                # The failure is on a 45 sum which is the same location where
                # it doesn't find the answer, yet it should!  Bug must be there.
                 for c in xrange(0,len(combos[0])):
                    used = [x[c] for x in combos]
                    starting_size = len(cg.cells[c].allowed)
                    cg.cells[c].allowed = [x for x in cg.cells[c].allowed if x in used]
                    if len(cg.cells[c].allowed) != starting_size:
                        keep_reducing = True
    def prettyPrint(self):
        #First find mix/max cell numbers, then just print them out
        rows = [cell.r for cell in self.cells]
        columns = [cell.c for cell in self.cells]
        for row in xrange(max(rows), min(rows)-1, -1):
            for column in xrange(min(columns), max(columns)+1):
                try:
                    print "%s"%self.cells[row, column],
                except:
                    print "         ",
            print ''
    def __repr__(self):
        ret = "%r\n%r"%(self.groups,self.cells)
        return ret
    
class Cell(object):
    min_value = 1
    max_value = 9
    def __init__(self):
        self.allowed = range(Cell.min_value, Cell.max_value+1)
        self._iter_index = 0
        return
    def __repr__(self):
        ret = ''
        for x in xrange(Cell.min_value,Cell.max_value+1):
            if x in self.allowed:
                ret += '%i'%x
            else:
                ret +='-'
        return ret
    def __len__(self):
        return len(self.allowed)
    def __getitem__(self, val):
        return self.allowed[val]
    def __iter__(self):
        return self
    def next(self):
        if self._iter_index < len(self.allowed):
            val = self.allowed[self._iter_index]
            self._iter_index += 1
            return val
        else:
            self._iter_index = 0
            raise StopIteration
        
class Group(object):
    def __init__(self, needed_total, start=None, length=None):
        self.needed_total = needed_total
        self.cells = list()
        self._iter_index = 0
        return
    def add(self, cell):
        self.cells.append(cell)
    def __repr__(self):
        return "needed_total=%s\ncells=%s\n" % \
            (self.needed_total,self.cells)
    def __iter__(self):
        return self
    def next(self):
        if self._iter_index < len(self.cells):
            val = self.cells[self._iter_index]
            self._iter_index += 1
            return val
        else:
            raise StopIteration    

# From http://stackoverflow.com/questions/4632322/finding-all-possible-combinations-of-numbers-to-reach-a-given-sum

def subset_sum_recursive(numbers,target,partial):
    s = sum(partial)

    #check if the partial sum is equals to target
    if s == target: 
        print "sum(%s)=%s"%(partial,target)
    if s >= target:
        return # if we reach the number why bother to continue

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i+1:]
        subset_sum_recursive(remaining,target,partial + [n]) 

def subset_sum(numbers,target):
    #we need an intermediate function to start the recursion.
    #the recursion start with an empty list as partial solution.
    subset_sum_recursive(numbers,target,list())



def hitTargetRecursive(target_sum, numbers, used, hits):
  
    for d in numbers[0]:
        if d not in used:
            used_copy = list(used)
            used_copy.append(d)
            if len(numbers)==1:
                if sum(used_copy)==target_sum:
                    hits.append(used_copy)
                continue
            hitTargetRecursive(target_sum, numbers[1:], used_copy, hits)


def hitTarget(target_sum, list_of_possible ):
    """ returns hits; a list of combinations that add to target_sum"""
    used = list()
    hits = list()
    hitTargetRecursive(target_sum=target_sum,
                             numbers=list_of_possible,
                             used=used,
                             hits=hits)
    return hits




# Example 1
if 1:
    s1 = CellMatrix()
    s1.newCellGroup(12, RC(0,1), RC(1,2))
    s1.newCellGroup(5, RC(0,1), RC(2,1))
    s1.newCellGroup(16, RC(0,2), RC(2,1))
    
    s1.reduce()
    print "Solution:"
    s1.prettyPrint()
    
    s2 = CellMatrix()
    s2.newCellGroup(9, RC(0,0), RC(1,3))
    s2.cells[0,0].allowed = [4,]
    s2.cells[0,2].allowed = [3,]
    s2.reduce()
    print "Solution:"
    s2.prettyPrint()
    
    s3 = CellMatrix()
    s3.newCellGroup(20, (1,1), (1,3))
    s3.newCellGroup(6, (0,2), (3,1))
    s3.reduce()
    print "Solution: (Note: Not possible to solve)"
    s3.prettyPrint()
    
    s4 = CellMatrix()
    s4.newCellGroup(3, (0,1), (1,2))
    s4.newCellGroup(4, (1,1), (1,2))
    s4.newCellGroup(4, (0,1), (2,1))
    s4.newCellGroup(6, (0,2), (3,1))
    s4.reduce()
    print "Solution: "
    s4.prettyPrint()

    s5 =  CellMatrix()
    # Rows
    s5.newCellGroup(8, (0,1), (1,2))
    s5.newCellGroup(11, (1,0), (1,3))
    s5.newCellGroup(17, (2,0), (1,2))
    s5.newCellGroup(18, (3,1), (1,3))
    s5.newCellGroup(4, (4,1), (1,2))
    s5.newCellGroup(9, (5,0), (1,2))
    s5.newCellGroup(14, (6,0), (1,2))
    s5.newCellGroup(19, (7,1), (1,4))
    s5.newCellGroup(5, (8,1), (1,2))
    s5.newCellGroup(3, (0,6), (1,2))
    s5.newCellGroup(17, (1,4), (1,4))
    s5.newCellGroup(17, (2,3), (1,3))    
    s5.newCellGroup(16, (2,7), (1,2))
    s5.newCellGroup(13, (3,7), (1,2))
    s5.newCellGroup(11, (4,6), (1,2))
    s5.newCellGroup(16, (5,5), (1,3))
    s5.newCellGroup(10, (6,3), (1,3))
    s5.newCellGroup(12, (6,7), (1,2))
    s5.newCellGroup(18, (7,6), (1,3))
    s5.newCellGroup(10, (8,6), (1,2))
    # Columns
    s5.newCellGroup(17, (1,0), (2,1))
    s5.newCellGroup(45, (0,1), (9,1))
    s5.newCellGroup(3, (0,2), (2,1))
    s5.newCellGroup(17, (5,0), (2,1))
    s5.newCellGroup(3, (7,2), (2,1))
    s5.newCellGroup(3, (3,2), (2,1))
    s5.newCellGroup(16, (2,3), (2,1))
    s5.newCellGroup(16, (6,3), (2,1))
    s5.newCellGroup(16, (1,4), (2,1))
    s5.newCellGroup(3, (6,4), (2,1))
    s5.newCellGroup(4, (1,5), (2,1))
    s5.newCellGroup(3, (5,5), (2,1))
    s5.newCellGroup(3, (0,6), (2,1))
    s5.newCellGroup(17, (4,6), (2,1))
    s5.newCellGroup(16, (7,6), (2,1))
    s5.newCellGroup(45, (0,7), (8,1))
    s5.newCellGroup(17, (2,8), (2,1))
    s5.newCellGroup(4, (6,8), (2,1))
    print "Full array"
    #s5.prettyPrint()
    #s5.reduce()
    #print("Solution to s5:")
    #s5.prettyPrint()    

    # On iphone puzzle 17
    s6 = CellMatrix()
    # Horizontal
    s6.newCellGroup(8, (9,4), (1,2))
    s6.newCellGroup(11, (9,7), (1,2))
    s6.newCellGroup(31, (8,2), (1,7))
    s6.newCellGroup(16, (7,2), (1,2))
    s6.newCellGroup(16, (7,6), (1,2))
    s6.newCellGroup(7, (6,3), (1,2))
    s6.newCellGroup(9, (6,6), (1,2))
    s6.newCellGroup(10, (5,4), (1,2))
    s6.newCellGroup(10, (5,7), (1,2))
    s6.newCellGroup(9, (4,5), (1,2))
    s6.newCellGroup(8, (4,8), (1,2))
    s6.newCellGroup(15, (3,5), (1,2))
    s6.newCellGroup(13, (3,8), (1,2))
    s6.newCellGroup(29, (2,4), (1,7))
    #columns
    s6.newCellGroup(9, (8,2), (2,1))
    s6.newCellGroup(21, (8,3), (3,1))
    s6.newCellGroup(4, (9,4), (2,1))
    s6.newCellGroup(6, (6,4), (2,1))
    s6.newCellGroup(15, (2,4), (2,1))
    s6.newCellGroup(12, (9,4), (2,1))
    s6.newCellGroup(21, (5,5), (5,1))
    s6.newCellGroup(17, (8,6), (3,1))
    s6.newCellGroup(15, (4,6), (3,1))
    s6.newCellGroup(24, (9,7), (5,1))
    s6.newCellGroup(13, (3,7), (2,1))
    s6.newCellGroup(11, (9,8), (2,1))
    s6.newCellGroup(26, (5,8), (5,1))
    s6.newCellGroup(12, (4,9), (3,1))
    s6.newCellGroup(5, (2,10), (1,1))
    print "Challenge problem 17"
    print "Full array"
    s6.prettyPrint()
    s6.reduce()
    print("Solution to s6:")
    s6.prettyPrint()    

       
