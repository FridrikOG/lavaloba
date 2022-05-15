# How to run:

**REQUIREMENTS**: have python3, pip (or conda installed)

## Mac instructions:
```
pip install virtualenv 
```
(if you do not have it)
```
source venv/bin/activate
```
```
source venv/bin/activate
```

## Windows instructions:
```
pip install virtualenv
```
```
virtualenv venv
```
(run this next one within the main folder which contains the mr_lava_loba.py you wanna run)
```
.\venv\Scripts\activate
```
if you get a similar error to "[...] venv\Scripts\activate.ps1 cannot be loaded because running scripts is disabled on this system. For more information, see  about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170." 
then run: 
Set-ExecutionPolicy Unrestricted -Scope Process
and then run the previous command again!
```   
pip install -r requirements.txt
```
```
python3 OR python mr_lava_loba.py
```

----
To exit the environment simply run in the terminal: 
```
deactivate
```