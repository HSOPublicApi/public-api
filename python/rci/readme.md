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
1. Create config.py from the example (if it doesn't exist) and replace the following values:
  * $${\color{orange}environment}$$ - Set to "test" for sandbox or "prod" for production
  * $${\color{orange}organizationId}$$ - Replace with your organization ID
  * $${\color{orange}patientId}$$ - Replace with your patient ID
  * $${\color{orange}clientId}$$ - Replace with your client ID
  * $${\color{orange}clientSecret}$$ - Replace with your client secret
  * $${\color{orange}THESE \space VALUES \space SHOULD \space BE \space KEPT \space SECRET!}$$
  * The config.py file is already included in .gitignore to prevent committing sensitive information
3. Create venv
```bash
python3 -m venv venv
```
4. Activate venv 
```bash
source venv/bin/activate
```
5. Install libraries 
```bash
pip install -r requirements.txt
```
6. Start application
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
