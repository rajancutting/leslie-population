"""
Rajan Cutting
Created 5/14

Purpose is to calculate future population growth via Leslie Matrices. Taking
the existing population and calculated survivlal rates from known death rates,
user inputs assumed birth rates. One of the major limitations to leslie models is
that they assume a closed population. In reality migration is a huge factor in projecting
population growth that this model does not currently include.
"""

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import rcParams
import statistics

df = pd.read_csv('population.csv')

D = pd.read_csv('death_rates.csv') #2007 death rates
P = pd.read_csv('population.csv') #Population from 2010 to 2018


#The corresponding future-pop-estimate csv used the following inputs
#[0.005,.06,.09,.08,.07,.0075]



class State:
    def __init__(self,name):
        self.name = name
    def population(self,year,sex): # For specific states
        state_pop = df[df.NAME== self.name]
        all_sex = state_pop[state_pop.SEX == sex]
        pop_year = all_sex['POPEST{}_CIV'.format(year)].to_list()
        total_pop = pop_year[-1]
        pop_year.pop() #to get rid of the last entry population total
        over_oldest = pop_year[-1] # These are all the people  85+
        pop_year.pop()

        oldest = pop_year[-1] # These are the people who are 84
        even_gap = int(over_oldest)//int(oldest)
        remainder = round((int(over_oldest)/int(oldest) - even_gap)*int(oldest))
        all_ages = all_sex['AGE'].to_list()
        all_ages.pop() # Get's rid of 999
        all_ages.pop() # get's rid of 85+
        add_age = all_ages[-1]

        for i in range(1,even_gap+1):
            new_age = add_age + i
            all_ages.append(new_age)
            pop_year.append(oldest)
        if remainder > 0:
            pop_year.append(remainder)
            add_age = all_ages[-1]
            all_ages.append(add_age+1)

        return {'ages':all_ages,'population':pop_year,'total':total_pop}

    def get_results(self,year,sex): #Makes a list with death rates
        """
        Function returns a list with each entry corresponding to the death rate for each age.
        The first element is the mortality rate for people less than 1. Second element is
        death rate for 1 year olds. And so on. This function is needed to make death rates data
        have the same dimension as population data. Population data is given by age, whereas death
        data is broken into age clusters.


        Args:
            year --> string of the year e.g. '2018'
            sex --> 0 is all, 1 is men, 2 is women

        """

        death_stats = D[D.Area == self.name].values.tolist()
        pop_stats = self.population(year,sex)['ages']

        proper_list = []

        first_group = float(death_stats[0][2])
        second_group = float(death_stats[0][3])
        third_group = float(death_stats[0][4])
        fourth_group = float(death_stats[0][5])
        fifth_group = float(death_stats[0][6])
        sixth_group = float(death_stats[0][7])
        seventh_group = float(death_stats[0][8])
        eigth_group = float(death_stats[0][9])
        ninth_group = float(death_stats[0][10])
        tenth_group = float(death_stats[0][11])
        eleven_group = float(death_stats[0][12])


        first_list = [first_group] * len(pop_stats[0:1])
        second_list = [second_group] * len(pop_stats[1:5])
        third_list = [third_group] * len(pop_stats[5:15])
        fourth_list = [fourth_group] * len(pop_stats[15:25])
        fifth_list = [fifth_group] * len(pop_stats[25:35])
        sixth_list = [sixth_group] * len(pop_stats[35:45])
        seventh_list = [seventh_group] * len(pop_stats[45:55])
        eigth_list = [eigth_group] * len(pop_stats[55:65])
        ninth_list = [ninth_group] * len(pop_stats[65:75])
        tenth_list = [tenth_group] * len(pop_stats[75:85])
        eleven_list = [eleven_group] * len(pop_stats[85:])

        proper_list.extend(first_list)
        proper_list.extend(second_list)
        proper_list.extend(third_list)
        proper_list.extend(fourth_list)
        proper_list.extend(fifth_list)
        proper_list.extend(sixth_list)
        proper_list.extend(seventh_list)
        proper_list.extend(eigth_list)
        proper_list.extend(ninth_list)
        proper_list.extend(tenth_list)
        proper_list.extend(eleven_list)

        return proper_list

    def survival_rate(self,year,sex):
        """
        This function calculats the survival rate for each age group.
        Args:
            year --> string of the year e.g. '2018'
            sex --> 0 is all, 1 is men, 2 is women
        """
        pop = self.population(year,sex)['population']
        death_rate = self.get_results(year,sex)

        surv = []
        for i in range(0,len(death_rate)):
            amount = pop[i]
            death = death_rate[i]

            #death rates are given in people per 100,000
            all_death = (amount/100000) * death
            calc_rate = (amount-all_death)/amount

            surv.append(calc_rate)
        return surv

    def existing(self,year,sex,forecast):
        """
        This function calculates the future shifted populations. For example if today
        there are x amount of 10 year olds, this function will tell you how many 15 year
        olds there will be in 5 years assuming the forecast is 5.

        Args:
            year --> string of the year e.g. '2018'
            sex --> 0 is all, 1 is men, 2 is women
            forecast --> integer
        """

        pop = self.population(year,sex)['population']

        surv = self.survival_rate(year,sex)
        max_age = len(surv) - forecast

        existing_humans = []
        for i in range(0,max_age):
            existing_humans.append(round(pop[i]*np.product(surv[i:i+forecast])))

        total = sum(existing_humans)

        return {'existing_list':existing_humans,'existing_count':total}

    def new_births(self,year,sex,forecast):
        """
        Using inputted birth rates this function calculates new births. Consistent with
        Leslie matrices, only women are passed into the sex argument.

        Args:
            year --> string of the year e.g. '2018'
            sex --> 0 is all, 1 is men, 2 is women
            forecast --> integer

        """
        print("NO spaces or percent sign. Input 5% as .05")
        r1 = float(input('What perfect of women aged 13-18 get pregnant?: '))
        r2 = float(input('What perfect of women aged 19-24 have children?: '))
        r3 = float(input('What perfect of women aged 25-30 have children?: '))
        r4 = float(input('What perfect of women aged 31-36 have children?: '))
        r5 = float(input('What perfect of women aged 37-42 have children?: '))
        r6 = float(input('What perfect of women aged 43-48 have children?: '))
        BR = [r1,r2,r3,r4,r5,r6]

        pop = self.population(year,sex)['population']

        new_babies = 0
        for age in range(forecast):
            if age == 0:

                first = sum(pop[13:19]) *BR[0]
                second = sum(pop[19:25]) * BR[1]
                third = sum(pop[25:31]) * BR[2]
                fourth = sum(pop[31:37]) * BR[3]
                fifth = sum(pop[37:43]) * BR[4]
                sixth = sum(pop[43:49]) * BR[5]

                new_babies += round(first + second + third + fourth + fifth + sixth)

            else:

                data = self.existing(year,2,age+1)['existing_list']
                first = sum(data[13-age:19-age]) *BR[0]
                second = sum(data[19-age:25-age]) * BR[1]
                third = sum(data[25-age:31-age]) * BR[2]
                fourth = sum(data[31-age:37-age]) * BR[3]
                fifth = sum(data[37-age:43-age]) * BR[4]
                sixth = sum(data[43-age:49-age]) * BR[5]

                new_babies += round(first + second + third + fourth + fifth + sixth)

        return new_babies

    def new_pop(self,exist,births):
        return(exist+births)
    def future(self):
        """
        This function returns a list of population estimates. The first entry is the state name
        then the second is the 2018 information. Everything after that is estimated.
        """
        all_states = set(P['NAME'].to_list())

        # The row that will be added to the DF

        current_pop = self.population("2018",0)['total']
        one = self.new_pop(self.existing("2018",0,1)['existing_count'] , self.new_births("2018",2,1))
        two = self.new_pop(self.existing("2018",0,2)['existing_count'] , self.new_births("2018",2,2))
        three = self.new_pop(self.existing("2018",0,3)['existing_count'] , self.new_births("2018",2,3))
        four = self.new_pop(self.existing("2018",0,4)['existing_count'] , self.new_births("2018",2,4))
        five = self.new_pop(self.existing("2018",0,5)['existing_count'] , self.new_births("2018",2,5))
        six = self.new_pop(self.existing("2018",0,6)['existing_count'] , self.new_births("2018",2,6))
        seven = self.new_pop(self.existing("2018",0,7)['existing_count'] , self.new_births("2018",2,7))
        eight = self.new_pop(self.existing("2018",0,8)['existing_count'] , self.new_births("2018",2,8))
        nine = self.new_pop(self.existing("2018",0,9)['existing_count'] , self.new_births("2018",2,9))
        ten = self.new_pop(self.existing("2018",0,10)['existing_count'] , self.new_births("2018",2,10))

        data = [self.name,current_pop,one,two,three,four,five,six,seven,eight,nine,ten]
        return data

    def make_plots(self,year1,year2,sex):
        info1 = self.population(year1,sex)
        pop_year1 = info1['population']
        age_year1 = info1['ages']
        pop_year1 = [y*.001 for y in pop_year1]

        info2 = self.population(year2,sex)
        pop_year2 = info2['population']
        age_year2 = info2['ages']

        pop_year2 = [y*.001 for y in pop_year2]

        if len(pop_year1) > len(pop_year2):
            diff = len(pop_year1) - len(pop_year2)
            for i in range(diff):
                pop_year2.append(0)
                last = pop_age2[-1]
                pop_age2.append(last+i+1)
        if len(pop_year2) > len(pop_year1):
            diff = len(pop_year2) - len(pop_year1)
            for i in range(diff):
                pop_year1.append(0)

        plt.plot(age_year2,pop_year1,label = "{} population".format(year1))
        plt.plot(age_year2,pop_year2,label = "{} population".format(year2))

        plt.title("{} {} population vs. {} population".format(self.name,year1,year2))
        plt.ylabel("Population in thousands")
        plt.legend()
        plt.minorticks_on()
        plt.grid(which="minor",linestyle=":",linewidth="0.5")
        #plt.grid(which='major', linestyle='-', linewidth='0.5', color='red')
        #plt.yaxis.set_ticks(np.arrange(start,end,50))
        #ax.xaxis.set_ticks(np.arange(start, end, 0.712123))
        plt.savefig('visuals/state_graph/{}.png'.format(self.name))
        #plt.show()

    def growth_rate(self,year1,year2):
        pop1 = self.population(year1,0)['total']
        pop2 = self.population(year2,0)['total']

        start = pop1
        end = pop2
        time = int(year2) -int(year1)
        rate = (np.log(end)-np.log(start))/time

        #print("growth rate " + str(rate))

        return rate

    def avg_age(self,year,sex):
        info = self.population(year,sex)
        pop = info['population']
        ages = info['ages']

        avg_list = pop[:]
        total = info['total']
        for i in range(1,len(avg_list)):
            avg_list[i] = avg_list[i] * ages[i]
        sum_list = sum(avg_list)
        len_list = len(avg_list)
        avg = round(sum_list/total)
        #print("the average age:",avg)
        return avg

    def median_age(self,year,sex):

        info = self.population(year,sex)

        pop = info['population']
        ages = info['ages']

        construct_age = []
        for i in range(0,len(ages)):
            add_age = [ages[i]]*pop[i]
            construct_age.extend(add_age)
        median = statistics.median(construct_age)
        #print("The median age:",median)
        return median

    def quintile(self,year,sex):

        info = self.population(year,sex)
        pop = info['population']
        total_pop =info['total']
        first_group = sum(pop[0:17])/total_pop * 100
        second_group = sum(pop[18:35])/total_pop * 100
        third_group = sum(pop[36:53])/total_pop * 100
        fourth_group = sum(pop[54:71])/total_pop * 100
        fifth_group = sum(pop[72:])/total_pop * 100
        obj = [round(first_group,2), round(second_group,2), round(third_group,2), round(fourth_group,2),round(fifth_group,2)]
        #print ("quintile:",obj)
        return obj

    def plot_quintiles(self,year1,year2,sex):

        y0 = self.quintile(year1,sex)
        y1 = self.quintile(year2,sex)

        max0 = max(y0)
        max1 = max(y1)
        true_max = max(max0,max1)
        labels = ['0-17','18-35','36-53','54-71','72+']
        x = np.arange(len(labels))
        width = 0.35

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, y0, width, label=year1)
        rects2 = ax.bar(x + width/2, y1, width, label=year2)

        ax.set_ylabel('Share of Population %')
        ax.set_title('{} Population Distribution'.format(self.name))
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        plt.ylim(top=true_max+6)

        stuff = [rects1,rects2]
        for rect in stuff:
            for rec in rect:
                height = rec.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rec.get_x() + rec.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        #graph = plt.plot(x,y0)
        plt.savefig('visuals/quintile/{}_quintile'.format(self.name))
        #plt.show()

def create_df():
    all_states = set(P['NAME'].to_list())

    df = pd.DataFrame(columns=['States','2018_pop','2019_pop','2020_pop','2021_pop','2022_pop','2023_pop','2024_pop','2025_pop','2026_pop','2027_pop','2028_pop'])

    for state in all_states:
        print(state)
        state_obj = State(state)
        df.loc[len(df)] = state_obj.future()
    df.to_csv('future-pop-estimate.csv')

#vt = State('Vermont')
#quintile = vt.plot_quintiles('2010','2018',0)


def make_quin():
    all_states = set(P['NAME'].to_list())

    for state in all_states:
        print(state)
        state_obj = State(state)
        state_obj.make_plots('2010','2018',0)
make_quin()
