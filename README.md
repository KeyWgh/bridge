#Transfer a string form of BBO play to a txt form.

Author: Ganghua Wang.

Email: keywgh@gmail.com

Version: 0.1

Copyright 2018. All Rights Reserved.



### Using instruction for windows:

- log in http://www.bridgebase.com


- My BBO —— Results

- ![1517327953](pictures/1517327953.png)

- Choose the play you want to transfer.

- ![1517328105](pictures/1517328105.png)

- Export the play —— link of Handviewer

- ![1517328245(1)](pictures/1517328245(1).png)

- show —— open in new window

- copy the url of new window to the file you want to use as input, default the input.txt in the same file with the transfer.py.

- Open command line

- cd to the file where transfer.py is

- ```
  >>> python transfer.py --input xxx.txt --filename xxx.txt
  ```

  where --input and --filename is optional, default is input.txt and output.txt.

  Also you can use -fn for short.

  ​

Welcome to report any bug!

