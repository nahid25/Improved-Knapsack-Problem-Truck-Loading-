import tkinter as tk
import math
import matplotlib.pyplot as plt
import time
import random

import Items
import Genome
import g

text_box1 = 0
text_box2 = 0
text_box3 = 0
text_box4 = 0
text_box5 = 0
text_boxR1 = 0
text_boxR2 = 0
text_boxR3 = 0
text_boxR4 = 0
text_boxR5 = 0
text_boxS1 = 0
text_boxS2 = 0
text_boxS3 = 0
check_box = 0
check_box_var = 0
greeting5 = 0
greetingT1 = 0
greetingT2 = 0
greetingT3 = 0
delayBox = 0

t0 = "";
t1 = "";
t2 = "";
t3 = "";
s0 = 0;
s1 = 0;
s2 = 0;
s3 = 0;

# critical items below
p: Genome.Population = None  # the entire population
items = 0  # an staic itemlist

# GUI Below
window = 0
windowX = 800
windowY = 600

globalRand = random.Random()  # use  globalRand.random


def initialise():
    global globalRand, text_boxR1, text_boxR2, text_boxR3, text_boxR4
    global p, items
    global t0, t1, t2, t3, s0, s1, s2, s3

    globalRand.seed(int(text_boxR1.get("1.0", tk.END)))
    g.POPULATION = int(text_boxR2.get("1.0", tk.END))
    g.MUTATIONPERCENT = float(text_boxR4.get("1.0", tk.END))
    g.maxGeneration = int(text_boxR3.get("1.0", tk.END));
    g.deduplicate = check_box_var.get()
    g.generation = 0
    g.mutations = 0
    g.baseline = float(text_boxR5.get("1.0", tk.END))
    items = Items.ItemList()
    items.setItems()
    p = Genome.Population(globalRand)
    g.best_genome = p.pop[0]
    g.best_fitness = p.pop[0].calcScore(items)
    g.first_generation_reach_best_fitness = 0
    showStats()
    showBest()


def showStats():
    global text_boxS1
    global p
    textA = "- Generation = " + str(g.generation)
    textB = "- Mutations  = " + str(g.mutations)
    textC = "- Best Score = " + str(round(g.best_fitness, 3))
    textD = "- First generation that reach best score = " + str(g.first_generation_reach_best_fitness)
    textE = "- Number of mutations on duplicated genes = " + str(p.deduplicated_cnt)
    text_boxS1.delete('1.0', tk.END)  # Delete from position 0 till end
    text_boxS1.insert(tk.END, textA + "\n" + textB + "\n" + textC + "\n" + textD + "\n" + textE)


def run1Generation(p):
    global globalRand
    g.generation = g.generation + 1
    p.selection(items, globalRand)
    p.mutate(globalRand)
    if g.deduplicate:
        p.deduplicate(globalRand)
    cur_generation_best_genome = p.pop[p.idOfBest(items)]
    if cur_generation_best_genome.calcScore(items) > g.best_fitness:
        g.best_genome = cur_generation_best_genome
        g.best_fitness = cur_generation_best_genome.calcScore(items)
        g.first_generation_reach_best_fitness = g.generation


def runAll():
    global p, delayBox, window, Checkbutton1
    while (g.generation < g.maxGeneration):
        run1Generation(p);
        showStats();
        showBest();
        window.update()
        if g.best_genome.calcScore(items) >= g.baseline:
            break
        delaySecs = float(delayBox.get("1.0", tk.END))
        if (delaySecs >= 0.01): time.sleep(delaySecs)
        # time.sleep(1)


def run1Gen():
    global p
    run1Generation(p);
    showStats();
    showBest();


def debug1():
    showBest()


def debug2():
    # Lists items to the console
    global items
    for i in range(0, g.NUM_OF_ITEMS):
        s = items.lst[i].name + " "
        s = s + items.lst[i].longName + " "
        s = s + str(items.lst[i].size) + " "
        s = s + items.lst[i].importance
        print(s)


def addToTruck(item, truckNum):
    global t0, t1, t2, t3, s0, s1, s2, s3
    global items
    # // truck 0 = stuff thats left out
    if (truckNum == 0):
        t0 = t0 + items.lst[item].name + " (" + str(items.lst[item].size) + ":";
        t0 = t0 + str(items.lst[item].importance) + ")\r\n";
        s0 = s0 + items.lst[item].size;

    if (truckNum == 1):
        t1 = t1 + items.lst[item].name + " (" + str(items.lst[item].size) + ":";
        t1 = t1 + str(items.lst[item].importance) + ")\r\n";
        s1 = s1 + items.lst[item].size;

    if (truckNum == 2):
        t2 = t2 + items.lst[item].name + " (" + str(items.lst[item].size) + ":";
        t2 = t2 + str(items.lst[item].importance) + ")\r\n";
        s2 = s2 + items.lst[item].size;

    if (truckNum == 3):
        t3 = t3 + items.lst[item].name + " (" + str(items.lst[item].size) + ":";
        t3 = t3 + str(items.lst[item].importance) + ")\r\n";
        s3 = s3 + items.lst[item].size;


def showBest():
    global p, NUM_OF_ITEMS, text_box1, text_box2, text_box3, greetingT1, greetingT2, greetingT3
    global t0, t1, t2, t3, s0, s1, s2, s3
    t0 = "";
    t1 = "";
    t2 = "";
    t3 = "";
    s0 = 0;
    s1 = 0;
    s2 = 0;
    s3 = 0;


    for item_idx in range(g.NUM_OF_ITEMS):
        addToTruck(item_idx, g.best_genome.genes[item_idx])

    t0 = t0 + "Sum = " + str(s0);
    t1 = t1 + "Sum = " + str(s1);
    t2 = t2 + "Sum = " + str(s2);
    t3 = t3 + "Sum = " + str(s3);

    txt = "Score = " + str(round(g.best_genome.score, 3))
    greeting5.configure(text=txt);

    # text_box1  t1;
    text_box1.delete('1.0', tk.END)  # Delete from position 0 till end
    text_box1.insert(tk.END, t1)

    text_box2.delete('1.0', tk.END)
    text_box2.insert(tk.END, t2)

    text_box3.delete('1.0', tk.END)
    text_box3.insert(tk.END, t3)

    text_box4.delete('1.0', tk.END)
    text_box4.insert(tk.END, t0)

    # textBox8.Text = t0;

    ss1 = "Truck 1 (" + str(g.TRUCK_CAPACITY) + ")";
    ss2 = "Truck 2 (" + str(g.TRUCK_CAPACITY) + ")";
    ss3 = "Truck 3 (" + str(g.TRUCK_CAPACITY) + ")";

    greetingT1.configure(text=ss1)
    greetingT2.configure(text=ss2)
    greetingT3.configure(text=ss3)


def main():
    global window, text_boxR1, text_boxR2, text_boxR3, text_boxR4, text_boxS1, greeting5, text_boxS2, text_boxS3
    global text_box1, text_box2, text_box3, text_box4, greetingT1, greetingT2, greetingT3, delayBox, Checkbutton1
    global check_box, check_box_var, text_boxR5, text_box5

    window = tk.Tk()

    geom = str(windowX) + "x" + str(windowY)
    window.geometry(geom)  # "800x600"
    window.title("GA 2021")

    TOP_CTRL = 10
    tyy = 25

    # main control buttons  
    startGAb = tk.Button(window, text="Initialise", bg="cyan", fg="black", relief="raised", command=initialise)
    startGAb.place(x=5, y=TOP_CTRL + tyy * 0, width=100, height=20)
    stopGAb = tk.Button(window, text="Run All", bg="cyan", fg="black", relief="raised", command=runAll)
    stopGAb.place(x=5, y=TOP_CTRL + tyy * 1, width=100, height=20)
    pauseGAb = tk.Button(window, text="Run 1 gen", bg="cyan", fg="black", relief="raised", command=run1Gen)
    pauseGAb.place(x=5, y=TOP_CTRL + tyy * 2, width=100, height=20)
    continueGAb = tk.Button(window, text="Debug1", bg="cyan", fg="black", relief="raised", command=debug1)
    continueGAb.place(x=5, y=TOP_CTRL + tyy * 3, width=100, height=20)
    continueGAb = tk.Button(window, text="Debug2", bg="cyan", fg="black", relief="raised", command=debug2)
    continueGAb.place(x=5, y=TOP_CTRL + tyy * 4, width=100, height=20)

    # contents of trucks
    text_box1 = tk.Text(window, height=14, width=30)
    text_box1.place(x=5, y=350)
    text_box2 = tk.Text(window, height=14, width=30)
    text_box2.place(x=260, y=350)
    text_box3 = tk.Text(window, height=14, width=30)
    text_box3.place(x=260 * 2, y=350)

    # leftovers 
    text_box4 = tk.Text(window, height=18, width=30)
    text_box4.place(x=260 * 2, y=5)

    # Contents of trucks
    greetingT1 = tk.Label(window, text="Truck 1", bg="cyan", fg="black")
    greetingT1.place(x=5, y=350 - 25, width=90, height=20)
    greetingT2 = tk.Label(window, text="Truck 2", bg="cyan", fg="black")
    greetingT2.place(x=260, y=350 - 25, width=90, height=20)
    greetingT3 = tk.Label(window, text="Truck 3", bg="cyan", fg="black")
    greetingT3.place(x=260 * 2, y=350 - 25, width=90, height=20)

    baseY2 = 150
    # labels for Random seed, population, generations, Mutation percent
    greeting1 = tk.Label(window, text="Random Seed", bg="cyan", fg="black")
    greeting1.place(x=5, y=baseY2, width=100, height=20)
    greeting2 = tk.Label(window, text="Population", bg="cyan", fg="black")
    greeting2.place(x=5, y=baseY2 + 1 * 25, width=100, height=20)
    greeting3 = tk.Label(window, text="Generations", bg="cyan", fg="black")
    greeting3.place(x=5, y=baseY2 + 2 * 25, width=100, height=20)
    greeting4 = tk.Label(window, text="Mutation Percent", bg="cyan", fg="black")
    greeting4.place(x=5, y=baseY2 + 3 * 25, width=100, height=20)
    greeting6 = tk.Label(window, text="Baseline", bg="cyan", fg="black")
    greeting6.place(x=5, y=baseY2 + 4 * 25, width=100, height=20)
    greeting7 = tk.Label(window, text="Mutate duplicated \ngenes", bg="cyan", fg="black")
    greeting7.place(x=5, y=baseY2 + 5 * 25, width=100, height=40)

    # Input boxes for Random seed, population, generations, Mutation percent
    text_boxR1 = tk.Text(window, height=1, width=10)  # Random Seed
    text_boxR1.place(x=110, y=baseY2)
    text_boxR1.insert(tk.END, "101")  # tk.END
    text_boxR2 = tk.Text(window, height=1, width=10)  # Population
    text_boxR2.place(x=110, y=baseY2 + 1 * 25)
    text_boxR2.insert(tk.END, str(g.POPULATION))
    text_boxR3 = tk.Text(window, height=1, width=10)  # Generations
    text_boxR3.place(x=110, y=baseY2 + 2 * 25)
    text_boxR3.insert(tk.END, str(g.maxGeneration))
    text_boxR4 = tk.Text(window, height=1, width=10)  # Mutation Percent
    text_boxR4.place(x=110, y=baseY2 + 3 * 25)
    text_boxR4.insert(tk.END, str(g.MUTATIONPERCENT))
    text_boxR5 = tk.Text(window, height=1, width=10)  # Mutation Percent
    text_boxR5.place(x=110, y=baseY2 + 4 * 25)
    text_boxR5.insert(tk.END, str(-g.marker))
    check_box_var = tk.BooleanVar(value=g.mutate_duplicated_genes)
    check_box = tk.Checkbutton(window, var=check_box_var, onvalue=True, offvalue=False)
    check_box.place(x=110, y=baseY2 + 5 * 25)

    # generation and mutation count 
    text_boxS1 = tk.Text(window, height=8, width=30)  # stats
    text_boxS1.place(x=210, y=baseY2)
    text_boxS1.insert(tk.END, "..\n..")

    # Best Score and individual number
    greeting5 = tk.Label(window, text="...", bg="cyan", fg="black")
    greeting5.place(x=210, y=baseY2 + 5 * 25 - 10, width=140, height=20)

    # Ms delay
    greeting4 = tk.Label(window, text="Delay in seconds", bg="cyan", fg="black")
    greeting4.place(x=210, y=baseY2 + 6 * 25 - 10, width=100, height=20)

    delayBox = tk.Text(window, height=1, width=10)
    delayBox.place(x=315, y=baseY2 + 6 * 25 - 10, width=90, height=20)
    delayBox.insert(tk.END, "0.00")

    # text_box.delete('1.0',tk.END)       # Delete from position 0 till end

    window.mainloop()


if __name__ == "__main__":
    main()
