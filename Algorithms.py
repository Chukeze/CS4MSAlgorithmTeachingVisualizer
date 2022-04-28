import math

import pygame
import random

pygame.init()


class DrawInformation:  # instantior
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    YELLOW = 45, 134, 123
    BACKGROUND_COLOR = WHITE
    SIDE_PADDING = 100
    TOP_PADDING = 100

    GRADIENTS = [
        (156, 156, 156), (160, 160, 160),
        (192, 192, 192)
    ]

    SMALL_FONT = pygame.font.SysFont('comicsans', 8)
    FONT = pygame.font.SysFont('comicsans', 25)
    LARGE_FONT = pygame.font.SysFont('comicsans', 50)

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height), )  # width and height passed as tuple
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.bar_width = round((self.width - self.SIDE_PADDING) / len(lst))  # total area / by number of blocks
        self.bar_height = math.floor(
            (self.height - self.TOP_PADDING) / (self.max_val - self.min_val))  # tells you range of height
        self.start_x = self.SIDE_PADDING // 2


'''Title unto screen'''
def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1,
                                  draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("1 - Reset | SPACE - Start Sorting | 2 - Ascending | 3 - Descending", 1,
                                     draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 35))

    sorting_and_algorithms = draw_info.SMALL_FONT.render("I - Insertion Sort | B - Bubble Sort | "
                                                         "S - Selection Sort |"
                                                         " M - Merge Sort "
                                                         "| H - Heap Sort |  "
                                                         "| * - A* PathFinder |"
                                                         " Q - Quick Sort |"
                                                         " G - Gnome Sort | V - Bogo Sort |"
                                                         " C - Chess Dijkstra Algorthm |"
                                                         " Z - Cocktail Shaker Sort ", 1,
                                                         draw_info.BLACK)
    draw_info.window.blit(sorting_and_algorithms, (draw_info.width / 2 - sorting_and_algorithms.get_width() / 2, 70))

    draw_list(draw_info)
    pygame.display.update()

'''Draws the list as rectangles'''
def draw_list(draw_info, color_positons={}, clear_background=False):
    lst = draw_info.lst

    if clear_background:
        clear_rect = (draw_info.SIDE_PADDING // 2, draw_info.TOP_PADDING,
                      draw_info.width - draw_info.SIDE_PADDING,
                      draw_info.height - draw_info.TOP_PADDING)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):  # enumerte ve u index and value in as it goes through list
        # calculate the x coordinate an y coordante of the top left corner of the rectangle
        # and calcucalte the color depdning on which rectanglel we draw
        x = draw_info.start_x + i * draw_info.bar_width
        # draws the taller rectange from the smaller by getting the y coordinate,
        # and draw base on getting the  overall height of the screen,
        # and subtract that form the wanted rectangle height.
        # also since val is gonna be range we need to account for that
        y = draw_info.height - (val - draw_info.min_val) * draw_info.bar_height

        color = draw_info.GRADIENTS[i % 3]  # every 3 element we reset color while changing gradient

        if i in color_positons:
            color = color_positons[i]
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height))
    if clear_background:
        pygame.display.update()

'''Generates a Random List of Numbers'''
def generate_starting_list(n, minimum, maximum):
    lst = []

    for _ in range(n):
        value = random.randint(minimum, maximum)
        lst.append(value)
    return lst

'''Finished'''
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]  # swap list without a temp array needed
                draw_list(draw_info, {j: draw_info.BLUE, j + 1: draw_info.RED}, True)
                yield True  # used yield here because when the function is called for each swap  instead of going
                # through entire algo it performs a swap and yield control to whatever called it until it needed again
                # yield pause and store state and then restarts
    return lst

'''Finished'''
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.YELLOW, i: draw_info.GREEN}, True)
            yield True
    return lst


def binaryinsertionsort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending
            if not ascending_sort and not descending_sort:
                break
            low = 0
            high = i
            while low < high:
                mid = math.floor((low + high) / 2)
                if i <= lst[mid]:
                    high = mid
                else:
                    low = mid + 1
            draw_list(draw_info, {i - 1: draw_info.YELLOW, i: draw_info.GREEN}, True)
            yield True
    return lst


def callquicksort(draw_info,ascending=True):
    lst = draw_info.lst
    beg = lst[0]
    n = len(lst) - 1
    end = lst[n]

    return quicksorting(draw_info, first= beg, last= end)


def quicksorting(draw_info, first, last, ascending=True):
    dataset = draw_info.lst
    for i in range(1, len(dataset)):
        current = dataset[i]
        while True:
            ascending_sort = i > 0 and dataset[i - 1] > current and ascending
            descending_sort = i > 0 and dataset[i - 1] < current and not ascending
            if not ascending_sort and not descending_sort:
                break
            if first < last:
                pivotIndex = partition(dataset, first, last)
                quicksorting(dataset, first, pivotIndex - 1)
                quicksorting(dataset, pivotIndex + 1, last)
                draw_list(draw_info, {i - 1: draw_info.YELLOW, i: draw_info.GREEN}, True)
                yield True
    return dataset


def partition(datavalues, first, last):
    pivotvalue = datavalues[first]
    lower = first + 1
    upper = last

    done = False
    while not done:
        while lower <= upper and datavalues[lower] <= pivotvalue:
            lower += 1
        # TODO: advance the upper index
        while datavalues[upper] >= pivotvalue and upper >= lower:
            upper -= 1
        # TODO: if the 2 index cross we have found the split point
        if upper < lower:
            done = True
        else:
            temporary = datavalues[lower]
            datavalues[lower] = datavalues[upper]
            datavalues[upper] = temporary
    # when split point is found exchange the pivot values
    temporary = datavalues[first]
    datavalues[first] = datavalues[upper]
    datavalues[upper] = temporary
    # return the split point index
    return upper

#ToDo
def mergesort(draw_info, ascending=True):
    lst = draw_info.lst

    def merge():
        pass

    if len(lst) > 1:
        mid = len(lst) // 2
        left = lst[:mid]
        right = lst[mid:]


def selectionsort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        minimum = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i - 1] > minimum and ascending
            descending_sort = i > 0 and lst[i - 1] < minimum and not ascending
            if not ascending_sort and not descending_sort:
                break

            for j in range(len(lst) - 1 - i):
                pointer = lst[j]
                num2 = lst[j + 1]

                if (pointer < minimum and ascending):
                    minimum = pointer
                    lst[j], num2 = num2, lst[j]
                # if (minimum != i):
                # lst[i] =

                draw_list(draw_info, {i - 1: draw_info.YELLOW, i: draw_info.GREEN}, True)
                yield True
    return lst

#todo:
def reaction_diffusion_algorithm():
    pass


def main():
    run = True
    clock = pygame.time.Clock()
    n = 10
    min_val = 0
    max_val = 100
    defaultlist = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1500, 800, defaultlist)
    sorting = False
    ascending = False

    algorithm = bubble_sort
    algorithm_name = "Bubble Sort"
    algorithm_generator = None
    while run:
        clock.tick(50)
        if sorting:
            try:
                next(algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, algorithm_name, ascending)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_1:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                algorithm_generator = algorithm(draw_info, ascending)

            elif event.key == pygame.K_2 and not sorting:
                ascending = True
            elif event.key == pygame.K_3 and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                algorithm = insertion_sort
                algorithm_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                algorithm = bubble_sort
                algorithm_name = "Bubble Sort"
            elif event.key == pygame.K_n and not sorting:
                algorithm = binaryinsertionsort
                algorithm_name = "Binary Insertion Sort"
            elif event.key == pygame.K_s and not sorting:
                algorithm = selectionsort
                algorithm_name = "Selection Sort"
            elif event.key == pygame.K_q and not sorting:
                algorithm = callquicksort
                algorithm_name = "Quick Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
