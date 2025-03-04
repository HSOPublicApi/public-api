# Python RESTful API example

## How to install Python3 and Pip3 if you don't already have them
1. Run the following brew command
```bash
brew install python@3.13
```
2. Add the following line to the end of your profile or bash_profile or .zshrc
```bash
export PATH="/usr/local/opt/python/libexec/bin:$PATH"
```
3. Now you can check that it's installed and the path is setup using the following command. You may need to restart the terminal.
```bash 
python3 --version
```

## Starting the application for the first time:
1. Replace $${\color{orange}clientId}$$ and $${\color{orange}clientSecret}$$ with your organizations values
  * The values you need to replace can be found near the top of main.py
  * $${\color{orange}THESE \space VALUES \space SHOULD \space BE \space KEPT \space SECRET!}$$
  * If you copy this code, these values should be moved to a protected file that is included in your .gitignore
2. Create venv
```bash
python3 -m venv venv
```
3. Activate venv 
```bash
source venv/bin/activate
```
4. Install libraries 
```bash
pip install -r requirements.txt
```
5. Start application
```bash
python3 main.py
```

## Starting the application again:
1. Activate venv 
```bash
source venv/bin/activate
```
2. Start application
```bash
python3 main.py
```
