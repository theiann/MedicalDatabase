This is a simple and demonstrative application for a Medical Database schema that I've created.
It's not meant to be practical, and if I was developing this in an actual work environment then I would 
definitely break up the methods into smaller chunks to make changing things easier, alongside other
security issues being fixed.

Use MySQL Workbench to run the provided "Project.sql" script. 
"SampleData.sql" is optional and is for demonstration purposes.

The python script connects to your local MySQL server using your password, which you provide.
To provide your MySQL password, create a new .txt file called "password.txt" and type your password
in there.

If you set everything up correctly, running the python script should greet you with the command menu
that looks something like this:
"Input your next command. (Type EXIT to exit) (Type HELP for a list of commands)"
