1.Which of the following Python data structures is most similar to the value returned in this line of Python:
x = urllib.request.urlopen('http://data.pr4e.org/romeo.txt')
==>file handle

2.In this Python code, which line actually reads the data?
import socket

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(('data.pr4e.org', 80))
cmd = 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\n\n'.encode()
mysock.send(cmd)

while True:
    data = mysock.recv(512)
    if (len(data) < 1):
        break
    print(data.decode())
mysock.close()

==>mysock.recv()

3.Which of the following regular expressions would extract the URL from this line of HTML:
<p>Please click <a href="http://www.dr-chuck.com">here</a></p>
==> href="(.+)"

4.In this Python code, which line is most like the open() call to read a file:
import socket

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(('data.pr4e.org', 80))
cmd = 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\n\n'.encode()
mysock.send(cmd)

while True:
    data = mysock.recv(512)
    if (len(data) < 1):
        break
    print(data.decode())
mysock.close()

==>mysock.connect()

5.Which HTTP header tells the browser the kind of document that is being returned?
==>Content-Type:

6.What should you check before scraping a web site?
==> That the web site allows scraping

7.What is the purpose of the BeautifulSoup Python library?
==>It repairs and parses HTML to make it easier for a program to understand

8.What ends up in the "x" variable in the following code:
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
x = soup('a')
==> A list of all the anchor tags (<a..) in the HTML from the URL

9.What is the most common Unicode encoding when moving data between systems?
==> UTF-8

10.What is the decimal (Base-10) numeric value for the upper case letter "G" in the ASCII character set?
==> 71

11.What word does the following sequence of numbers represent in ASCII:
108, 105, 110, 101
==> line

12.How are strings stored internally in Python 3?
==>Unicode

13.Question 13
When reading data across the network (i.e. from a URL) in Python 3, what method must be used to convert it to the internal format used by strings?
==> decode()

14. What is the ASCII character that is associated with the decimal value 42?
==> *