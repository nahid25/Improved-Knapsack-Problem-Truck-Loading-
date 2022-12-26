import math
import time
import random
import g


class Item(object):
    name = "";  # // max of say 10 chars
    longName = "";  # // any length if blank defaults to short name
    size = 9999;  # // 1 - 100 how it fits
    importance = " ";  # Importance C=Critical  V=Very Important I=Important N=Not Important

    def __init__(self, nameQ, longNameQ, sizeQ, importanceQ):
        self.name = nameQ
        self.longName = longNameQ
        self.size = sizeQ
        self.importance = importanceQ


class ItemList(object):
    lst = [];  # the actual list of items

    def __init__(self):
        self.lst = [None] * g.NUM_OF_ITEMS

    def setItems(self):
        self.lst[0] = Item("Bandages", "", 6,
                           "C");  # Importance C=Critical  V=Very Important I=Important N=Not Important
        self.lst[1] = Item("BandagesXL", "", 6, "C");
        self.lst[2] = Item("Bandage", "Full Body 'mummy' Cast", 3, "I");
        self.lst[3] = Item("Oxygen", "Oxygen Cylinders", 12, "C");
        self.lst[4] = Item("Hospital I", "Tent Hospital part 1", 12, "I");
        self.lst[5] = Item("Hospital II", "Tent Hospital part 2", 17, "I");
        self.lst[6] = Item("Generator", "Electricity Generator", 6, "V");
        self.lst[7] = Item("Petrol44a", "44 Gal Drum of Petrol", 9, "N");
        self.lst[8] = Item("Petrol44b", "44 Gal Drum of Petrol", 9, "N");
        self.lst[9] = Item("Petrol20", "20L Gerrycans of fuel", 4, "N");
        self.lst[10] = Item("Condoms", "", 1, "N");
        self.lst[11] = Item("Mercurochrome", "Disinfectant for wounds", 3, "C");
        self.lst[12] = Item("Chocolate", "Large box donated by Cadbury", 5, "N");
        self.lst[13] = Item("Radio", "Large multifreq radio+gen", 11, "C");
        self.lst[14] = Item("HeliSpare", "Helicopter Rotor", 8, "I");
        self.lst[15] = Item("Box", "Grey box marked 'Top Secret'", 11, "C");
        self.lst[16] = Item("Spuds", "Crate of Potates", 4, "I");
        self.lst[17] = Item("Ping", "Machine That goes Ping", 9, "V");
        self.lst[18] = Item("Difox201", "DF201 For mine rescue", 8, "V");
        self.lst[19] = Item("Trash", "Trash Disposal system", 1, "N");
        self.lst[20] = Item("Batteries", "Mobile Phone batteries", 6,
                            "I");  # Importance C=Critical  V=Very Important I=Important N=Not Important
        self.lst[21] = Item("GDP", "Government policy manual", 10, "I");
        self.lst[22] = Item("Guzzoline e10", "E10 good to reduce carbon", 7, "N");
        self.lst[23] = Item("RB", "Rubber Bags and lime", 8, "I");
        self.lst[24] = Item("SaltP", "Salt Pork", 4, "N");
        self.lst[25] = Item("Water1", "Water 150L", 9, "I");
        self.lst[26] = Item("Peaches", "Tins Of Peaches", 4, "N");
        self.lst[27] = Item("UGS", "UGS - Type 20", 11, "V");
        self.lst[28] = Item("MS", "Coffins", 9, "I");
        self.lst[29] = Item("Doctor", "Doctors Kit", 13, "V");
        self.lst[30] = Item("Albanese", "Anthony Albanese For a PR shoot", 8, "N");
        self.lst[31] = Item("Triage", "Hospital triage unit", 3, "N");
        self.lst[32] = Item("WPlant", "Water Purification Plant", 7, "V");
        self.lst[33] = Item("Water2", "Water 300L", 12, "C");
        self.lst[34] = Item("Nintendo", "Stop them getting bored", 1, "N");
