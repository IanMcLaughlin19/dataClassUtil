# Data Class Generator Project
This project is to try and make some utilties to autogenerate boilerplate Python classes from arbitrary json data.

### Motivation for this project
The reason I decided to do this was because that I found it very frustrating working with external API's and other data
sources, because I would often write code that works with external data sources such as AWS or CloudFlare API's, and 
my python code would look like a very hard to read series of dictionary references.  
In addition, the result of this was that the actual functions on the data structures from external API's wouldn't be
properly organized, since it always feel more natural to have the functions on data structures to be associated with the
structures themselves.

### What does this project do?
It takes in a python data structure in the form of a json file or python object and generates a python data class from it.

### Practical example 
I have been experimenting with the AlgoIndexer API from AlgoExplorer to gain some insights on the Algorand BlockChain