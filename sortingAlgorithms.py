if __name__=='__main__':
    import sortingVisualizer
import random
from math import floor
from utils import *
from constants import *


def bubble_sort(cont):
    array = cont.blocks

    print("Bubble Sort Started!")
    
    for i in range(len(array)-1):
        for j in range(len(array)-1-i):
            cont.colordict[CHECKING_COLOR] = array[j:j+2]
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
            cont.setFreq(array[j])
            yield 1, 4

    print("Bubble Sort Completed! :)")


def bogo_sort(cont):
    array = cont.blocks
    
    def isSorted() -> bool:
        for i in range(len(array)-1):
            if array[i] > array[i+1]:
                return False
        return True
    
    print("Bogo Sort Started!")
    
    while not isSorted():
        a = random.randint(0, len(array)-1)
        b = random.choice([n for n in range(len(array)) if n != a])
        cont.colordict[CHECKING_COLOR] = [array[a], array[b]]
        cont.setFreq(array[a])
        yield 0, 0
        array[a], array[b] = array[b], array[a]
        yield 0, 2

    print("Bogo Sort Completed! :)")


def quick_sort(cont):
    cont.colordict["Yellow"] = lower_blocks = []
    cont.colordict["Red"] = higher_blocks = []

    def quick_sort_rec(array, low, high):
        if low < high:          # comparison
            lower_blocks.clear()
            higher_blocks.clear()

            pivot = array[high] # array access
            higher_blocks.append(pivot)
            index = low
            for _ in range(low, high):
                item = array.pop(index)         # array access
                if item > pivot:                # comparison
                    higher_blocks.append(item)
                    array.insert(high, item)    # array access
                    index -= 1
                else:
                    lower_blocks.append(item)
                    array.insert(low, item)     # array access
                index += 1
                cont.setFreq(item)
                yield 1, 2

            pivot_index = low + len(lower_blocks)

            yield from quick_sort_rec(array, low, pivot_index-1)
            yield from quick_sort_rec(array, pivot_index+1, high)
        yield 1, 1
                    
    print("Quick Sort Started!")
    
    array = cont.blocks
    yield from quick_sort_rec(array, 0, len(array)-1)

    print("Quick Sort Completed! :)")


def insertion_sort(cont):

    print("Insertion Sort Started!")
    array = cont.blocks

    for i in range(1, len(array)):
        for j in range(i-1, -1, -1):
            cont.colordict[CHECKING_COLOR] = [array[i], array[j]]

            if array[j] < array[i]:
                array.insert(j+1, array[i])
                array.pop(i+1)
                cont.colordict[CORRECT_COLOR] = [array[j+1]]
                cont.setFreq(array[j+1])
                break
            yield 1, 1
        else:
            array.insert(0, array[i])
            array.pop(i+1)
            cont.colordict[CORRECT_COLOR] = [array[0]]
        yield 0, 1

    print("Insertion Sort Completed! :)")


def imp_ins_sort(cont):
    print("ImProved Insertion Sort Started!")
    array:list = cont.blocks

    highest = array[0]
    for i in range(1, len(array)):
        item = array[i]
        cont.colordict[CHECKING_COLOR] = checked_blocks = []
        checked_blocks.append(item)

        if item > highest:
            highest = item
            yield 1, 1  # comparison, arrayaccess
            continue

        estimate = floor((item.size / highest.size) * i)

        if item > array[estimate]:
            span = range(estimate+1, i)
            compare = lambda el: item < el
            down_up = 0
        else:
            span = range(estimate, -1, -1)
            compare = lambda el: item > el
            down_up = 1

        checked_blocks.append(array[estimate])

        for e in span:
            checked_blocks.append(array[e])
            if compare(array[e]):
                array.insert(e + down_up, item)
                array.pop(i+1)
                break
            cont.setFreq(array[e])
            yield 1, 1      # 1 comparison, 1 array-access
        else:
            if down_up:
                array.insert(0, item)
                array.pop(i+1)
                yield 1,1

    print("ImProved Insertion Sort Completed! :)")


def merge_sort(cont):
    array:list = cont.blocks

    def merge_sort_rec(low, high): # HIGH IS INCLUSIVE
        diff = high - low
        if diff == 1:
            if array[low] > array[high]:
                array[low], array[high] = array[high], array[low]
                cont.setFreq(array[low])
                yield 1, 2
            
        elif diff > 1:
            right = low + (high - low) // 2 + 1
            left = low

            yield from merge_sort_rec(low, right - 1)
            yield from merge_sort_rec(right, high)

            while left < right and right <= high:
                cont.colordict[CHECKING_COLOR] = [array[left], array[right]]
                if array[left] > array[right]:
                    array.insert(left, array[right])
                    array.pop(right+1)
                    right += 1
                cont.setFreq(array[left])
                left += 1
                yield 3, 2
            
    yield from merge_sort_rec(0, len(array)-1)
    print("Merge Sort Completed! :)")


def radix_sort(cont):
    print("Radix Sort Started!")
    array:list = cont.blocks
    index = 1

    colornames = ["#" + c*6 for c in "BA98765432"]
    for col in colornames:
        cont.colordict[col] = []
    
    while True:
        numberLists = [[] for _ in range(10)]
        for block in array:
            digit = block.size // index % 10
            numberLists[digit].append(block)
            for col in colornames:
                if block.i in [b.i for b in cont.colordict[col]]:
                    cont.colordict[col].remove(block)
                    break
            cont.colordict[colornames[digit]].append(block)
            
            cont.setFreq(block)
            yield 0, 1
        
        if len(array) in [len(l) for l in numberLists]:
            break

        array.clear()
        for l in numberLists:
            array.extend(l)

        yield 0, 0
        index *= 10
    print("Radix Sort Completed! :)")


def gnome_sort(cont):
    print("Gnome Sort Started!")
    array:list = cont.blocks

    pos = 0
    while pos < len(array):
        if pos == 0 or array[pos] >= array[pos-1]:
            cont.setFreq(array[pos])
            pos += 1
        else:
            array[pos], array[pos-1] = array[pos-1], array[pos]
            cont.setFreq(array[pos])
            pos -= 1
        cont.colordict[CHECKING_COLOR] = [array[pos-1]]
        yield 0,0

    print("Gnome Sort Completed! :)")


def heap_sort(cont):
    print("Heap Sort Started!")
    array:list = cont.blocks
    colors = generate_subtree_colors(len(array))
    for col in colors:
        cont.colordict[col] = []
    
    def heapify(array, n, i): # heapify down
        cont.setFreq(array[i])
        leftChild = 2*i + 1 
        rightChild = 2*i + 2
        if rightChild >= n: rightChild = leftChild

        largestChild = rightChild if array[leftChild] < array[rightChild] else leftChild

        # Swap if bigger
        if array[largestChild] > array[i]:
            array[i], array[largestChild] = array[largestChild], array[i]
            if largestChild <= n//2 - 1:
                yield from heapify(array, n, largestChild)
                yield 0,0

    # Create max heap
    count = len(array)
    for i in range(count//2-1, -1, -1):
        yield from heapify(array, count, i)

    # Sort get max 1 by 1
    while count > 2:
        for col in colors:
            cont.colordict[col].clear()
        for i in range(count):
            cont.colordict[colors[get_subtree_level(i)]].append(array[i])

        array[0], array[count-1] = array[count-1], array[0]
        count -= 1
        list(heapify(array, count, 0))
        yield 0,0
        
    array[0], array[count-1] = array[count-1], array[0]

    print("Heap Sort Completed! :)")


def verify_sort(cont):
    array = cont.blocks
    cont.colordict[CORRECT_COLOR] = correct = []
    cont.colordict[WRONG_COLOR] = wrong = []

    for i in range(len(array)-1):
        if len(wrong) != 0:
            wrong.append(array[i])
        elif array[i] <= array[i+1]:
            correct.append(array[i])
            cont.setFreq(array[i])
        else:
            wrong.append(array[i])
        yield 0,0

