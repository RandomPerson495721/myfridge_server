# Run instructions
## To run the program, first create a virtual environment and activate it:
```bash
 python -m venv .venv
 source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```
## Then install dependencies
```bash
 pip install -r requirements.txt
```

## You'll need a firebase Admin SDK key
### You can get it from the Firebase console:
### https://console.firebase.google.com/project/_/settings/serviceaccounts/adminsdk
### You'll need to create a new project and download the JSON key file.
- Save the key file somewhere secure, I used ~/.config/myfridge/\<KEY\>.json
- Set the environment variable 'FIREBASE_ADMIN_SDK_KEY_PATH' to the real path of the key (Pycharm allows this in the run configuration)

## To run the program, use the following command from within the main directory:
```bash
 python app.py
```
### The program will listen on port 5000

### To point the app to the server, change the URL on line 22 of build.gradle.kts in the app module to http://10.0.2.2:5000 
### (This is assuming it's running on the emulator)

### You'll also need to download the google-services.json file and replace the one currently in the app/src directory with the one from your project

