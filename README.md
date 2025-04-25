I am reading files using UTF-8 to support manually created text files. 
The > operator on windows normally writes in UTF-16, so when using the world generator I pass this parameter:
 python .\make_vacuum_world.py 5 7 0.15 3 | Out-File -Encoding ascii random-5x7.txt
This way I can use the world generator as well as notepad files to make different worlds.
