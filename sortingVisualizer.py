import pygame
from sortingAlgorithms import *
from pyo import *

# PYO stuff
server = Server()
server.boot()
server.start()
osc = Sine(400, 0.15) # Frequency, Amplitue

stop = False
skip = False

# Pygame init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
running = True

class Block:
    def __init__(self, size, i):
        self.size = size
        self.surf = pygame.Surface((BLOCK_WIDTH, size))
        self.rect = self.surf.get_rect(bottom = SCREEN_SIZE[1])
        self.i = i

    def draw(self, xcoord, color):
        self.surf.fill(color)
        self.rect.left = xcoord
        screen.blit(self.surf, self.rect)

    def __gt__(self, other):
        return self.size > other.size
    def __lt__(self, other):
        return self.size < other.size
    def __le__(self, other):
        return self.size <= other.size
    def __ge__(self, other):
        return self.size >= other.size
    def __eq__(self, other):
        return self.size == other.size

class Container:
    def __init__(self, alg) -> None:
        self.blocks = []
        self.block_count = int(SCREEN_SIZE[0] / (BLOCK_WIDTH+SPACING))
        self.seed = []
        self.colordict = {}
        self.sorting = True
        self.verifying = False
        self.generator = None
        self.comparisons = 0
        self.arraychecks = 0
        self.osc = osc
        self.alg = alg
        self.randomize()
        self.font = pygame.font.SysFont("arial", max(5, BLOCK_WIDTH-5))

    def setSort(self, sorting_algorithm):
        self.alg = sorting_algorithm

    def start(self):
        self.generator = self.alg(self)
        self.sorting = True
        self.osc.out()

    def randomize(self):
        self.seed.clear()
        self.blocks.clear()
        for i in range(self.block_count):
            random_number = random.randint(1, int(SCREEN_SIZE[1] * .8))
            self.blocks.append(Block(random_number, i))
            self.seed.append(random_number)
        self.start()

    def reset(self):
        self.blocks = [Block(n, i) for i, n in enumerate(self.seed)]
        self.colordict.clear()
        self.start()

    def update(self):
        if self.sorting:
            try:
                comps, lookups = next(self.generator)
                self.comparisons += comps
                self.arraychecks += lookups
            except StopIteration:
                self.sorting = False   
                self.verifying = True
                global WAIT
                WAIT = 4
                self.colordict.clear()
                self.generator = verify_sort(self)
            
        elif self.verifying:
            try:
                next(self.generator)
            except StopIteration:
                self.verifying = False
                self.osc.stop()
                self.colordict.clear()

        elif self.arraychecks != 0:
            print(f"comparisons: {self.comparisons}\narray checkups: {self.arraychecks}\n")
            self.comparisons = 0
            self.arraychecks = 0

    def setFreq(self, block):
        osc.setFreq(400+block.size//4)

    def display(self):
        for c, block in enumerate(self.blocks):
            x = c * (BLOCK_WIDTH + SPACING)
            color = BLOCK_COLOR

            if CHECKING_COLOR in self.colordict and block.i in [b.i for b in self.colordict[CHECKING_COLOR]]:
                color = CHECKING_COLOR
            else:
                for col, l in self.colordict.items():
                    if block.i in [b.i for b in l]:
                        color = col
            block.draw(x, color)

a = Container(heap_sort)
a.display()
pygame.display.update()
osc.out()

index = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_SPACE: 
                    if not a.verifying and not a.sorting:
                        print_sorting_algorithms()
                    elif stop: 
                        stop = False
                        a.osc.out()
                    else:
                        stop = True
                        a.osc.stop()
                case pygame.K_RIGHT:   skip = True
                case pygame.K_l:       WAIT += WAIT//10 + 1
                case pygame.K_j:       WAIT = max(1, WAIT - WAIT//10 - 1)
                case pygame.K_b:       a.setSort(bubble_sort);  print("Bubble Sort Selected")
                case pygame.K_p:       a.setSort(imp_ins_sort);   print("ImProved Insertion Sort Selected")
                case pygame.K_i:       a.setSort(insertion_sort); print("Insertion Sort Selected")
                case pygame.K_q:       a.setSort(quick_sort);   print("Quick Sort Selected")
                case pygame.K_m:       a.setSort(merge_sort);   print("Merge Sort Selected")
                case pygame.K_r:       a.setSort(radix_sort);   print("Radix Sort Selected")
                case pygame.K_g:       a.setSort(gnome_sort);   print("Gnome Sort Selected")
                case pygame.K_h:       a.setSort(heap_sort);   print("Heap Sort Selected")
                case pygame.K_o:       a.setSort(bogo_sort);    print("Bogo Sort Selected"); break
                case 13:
                    a.reset()
                    # stop = 
                case pygame.K_n:
                    a.randomize()
                    stop = True

    screen.fill(BACKGROUND_COLOR)

    if skip or (index%WAIT == 0 and not stop):
        a.update()
        skip = False
    a.display()

    pygame.display.update()
    index += 1

osc.stop()
server.stop()
pygame.quit()