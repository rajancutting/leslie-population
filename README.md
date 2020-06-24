## Overview

Overpopulation is becoming a growing concern. However from 2010 to 2018, the population in the United States has only modestly increased a total of 6%, with an annual growth rate of less than one percent. There are even some states with decreasing populations.
<p align="center"> 
  <img src="https://github.com/rajancutting/leslie-population/blob/master/United%20States.png">
 </p>
 
Instead of overpopulation, Americans should be concerned with the changing age distribution of the population. With advances in technology and medical breakthroughs, people are living longer and are also choosing to have less children. These factors will have different longterm impacts on each state. In 2010 in Vermont people 54 and older made up 30.13% of the total population, but eight years later in 2018 they were 35.03% of the population. 
In comparison people under the age of 18 were 19.27% of the population in 2010 and 17.36% by 2018. There are fewer young people in Vermont, and that has already led to schools closing. 
<p align="center">
   <img src="https://github.com/rajancutting/leslie-population/blob/master/visuals/quintile/Vermont_quintile.png">
 </p>

Understanding age distribution in a state’s population is critical to analyze its future economic prospects and societal life. The purpose of this project is to take a closer look at age distribution in the United States. 
Then using the Leslie Model, this project forecasts future population growth with varying birth rates. 

## Background
The Leslie model (more commonly known as the Leslie matrix) is one of the more well know population models. 
It was the appropriate model for this project because it incorporates age distribution. However it does have some drawbacks that I hope to address in future work. 
The Leslie model assumes populations are closed to migration, which is obviously crucial to understand population change. 
The Leslie matrix is a square matrix with the same number of rows and columns as the population vector has elements. 
The entries in the first row are the fertility rate of the population with each entry at position (i,1) corresponding to the fertility rate of the ith age class. 
After the first row, there is only one nonzero entry in each row. The nonzero entry in each row at (i,j) is the survival rate for the individuals in the ith age class. 
At each time step, the population vector is multiplied by the Leslie matrix to generate the population vector for the subsequent time step.

Another limitation to the Leslie model is that it normally only includes a single sex population, usually females. 
This project incorporates both sexes. To account for this limitation, I have two separate matrices. 
The first matrix is the first row of the traditional Leslie matrix and has fertility rates that are user inputs. 
The population vector is only the female population. 

The second matrix has the survival rates and the population vectors includes the total population of males and females. 
The first calculation gives the new births and the second is the total population that survives to the next year.
The sum of the two is the new total population. 

## Dataset
The population data from 2010 to 2018 is broken down by age and is reported by the census bureau. 
The death data used to calculate the survival rates is 2007 data from the CDC. The fertility rates are user inputs. 
One of the goals of this project is to measure how varying birth rates change the outlook for future population trends, so that is partly why I chose to have birth rates be user inputs.

## Results
The model assumed that only women between the ages of 13 and 48 can give birth. Then the fertility was broken down into age clusters with corresponding fertility rates. 

<table style="width:100%">
  <tr>
    <th> Ages 13-18 </th>
    <th> Ages 19-24 </th>
    <th> Ages 25-30 </th>
    <th> Ages 31-36 </th>
    <th> Ages 37-42 </th>
    <th> Ages 43-48 </th>
 </tr>
 <tr>
   <td> 0.05% </td>
   <td> 6.0% </td>
   <td> 9.0% </td>
   <td> 8.0% </td>
   <td> 7.0% </td>
   <td> 0.075% </td>
 </tr>
 </table>

With these birth rates, states will continue the same population trend. The model predicts that the states that had decreasing populations in 2018 will continue to see a downard trend in births and an increasing share of older people. Some of the results are shown below.

<p align="center">
  <img src="https://github.com/rajancutting/leslie-population/blob/master/visuals/future_trend_head.png">
</p>

## Future Work
There are a few things that I want to continue adding to this project. 

Migration — I want to fact in total migration to my model. 
In some states there is a clear trend of a peak in college-aged young people and then a drop off in older ages.  
It is clear that many students are attending college in these states and then leaving after graduation. I want to account for a total migration 
factor by looking at the excess decrease in population age classes that are not attributed to deaths.
<p align="center">
  <img src="https://github.com/rajancutting/leslie-population/blob/master/visuals/state_graph/Vermont.png">
</p>

Possible births - Right now the model accounts for a one-dimensional outlook on fertility. The user is prompted to input the percentage
of women in a specific age category that are going to have children, but in reality it is more complicated than that. 
Younger women are increasingly postponing having children in order to pursue careers. I would like to analyze workforce data and see 
if I can factor in the impact working has on births. How many children a woman already has will also impact her decision to have another one.
The current model tries to capture all of these varying factors in a set percentage, but that is not accurate and I want to build more
specificity in my future model.


Changing Course — I want to establish a baseline for a balanced population spread. 
That involves establishing what an ideal state looks like and how many births per year are needed to sustain that growth.
Then I would like to provide analysis on a changing course strategy. For a state like Vermont that might mean figuring out how
many young people need to move into the state to support their aging population. 
