# Syndrome-Error-Decoding

**Update June 2022:** The simulation plot is not a very informative plot due to the time being multiplied by the error percentage. There is an issue of relative scales and also multiplication by zero. I do not recommend using this plot and I plan to make changes to make it more informative. 

I developed a class that is able to develop any (n, k) linear code including by generating a generator matrix, parity check matrix, 
and a syndrome decoding table. I used that class to develop an ASCII code class in order to correct errors in the ascii representation 
of alphabet letters. 

I developed a stochastic simulation in order to test the accuracy of different error correcting codes. This was done by  
writing a random text generator. Thanks to https://www.wordfrequency.info/ for supplying me with a 5000 word data set. I used the output
from the text generator to feed it into a function that parses the text and transforms it into a vector of binary representations of each character based on it's ASCII representation. I then used a function that randomly distorts bits in each character. From there I was able to apply the linear code to try and retrieve the original text. My simulation focused on measuring the time required for the operation and also the amount of errors that where corrected. 

Here are some results from the simulation:

This is the Simulation Plot:
![Simulation Plot](https://github.com/AmeanAsad/Syndrome-Error-Decoding/blob/master/Simulation_Results.png?raw=true)

This is the Error Percentage Table:

![Percentage Error Table](https://github.com/AmeanAsad/Syndrome-Error-Decoding/blob/master/SimulationTable.png?raw=true)
      


      
