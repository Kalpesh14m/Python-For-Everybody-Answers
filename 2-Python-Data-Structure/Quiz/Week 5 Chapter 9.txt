1.How are Python dictionaries different from Python lists?
==> Python lists are indexed using integers and dictionaries can use strings as indexes

2.What is a term commonly used to describe the Python dictionary feature in other programming languages?
==> Associative arrays

3.What would the following Python code print out? 
stuff = dict(); 
print(stuff['candy'])
==> The program would fail with a traceback

4.What would the following Python code print out? stuff = dict(); print stuff.get('candy',-1)
==> -1

5.(T/F)When you add items to a dictionary they remain in the order in which you added them.
==> False

6.What is a common use of Python dictionaries in a program?
==> Building a histogram counting the occurrences of various strings in a file

7.Which of the following lines of Python is equivalent to the following sequence of statements assuming that counts is a dictionary? 
if key in counts: 
	counts[key] = counts[key] + 1 
else: 
	counts[key] = 1
==> counts[key] = counts.get(key,0) + 1

8.In the following Python, what does the for loop iterate through? 
x = dict() ... 
for y in x : ...
==> It loops through the keys in the dictionary

9.Which method in a dictionary object gives you a list of the values in the dictionary?
==> values()

10.What is the purpose of the second parameter of the get() method for Python dictionaries?
==> To provide a default value if the key is not found