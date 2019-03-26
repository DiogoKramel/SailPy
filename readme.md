##### About this application:

**App Name** is a Python application for conceptual sailboat design with an object-oriented paradigm. App Name implements several routines in order to optimize the dimensions of the hull and all appendages of a sailboat. 

The application was developed by Diogo Kramel and is maintained by the Polytechnic School of the University of São Paulo in São Paulo. For documentation and other resources, visit our [wiki](https://github.com/AppName/wiki).

## Contributing

When contributing, fork the repository and send pull requests with your commits. If your modifications are only to files related to examples and you have pull request authorization, you can approve them by yourself. If not, wait for review and approval by the development team.

You are also welcome to create [issues](https://github.com/AppName/issues) reporting bugs or suggesting improvements and features for further development.

##### To run this app locally:

You can clone or download this repo:

```
git clone https://github.com/AppName
```

Then cd into the repo:

```
cd AppNamePath
```

Now create and activate a virtual environment:  
On a mac:

```
virtualenv -p <python version> venv
source eenv/bin/activate
```

On a Windows:

```
virtualenv -p <python version> env
eenv/Scripts/activate
```

Now that virtualenv is setup and active we can install the dependencies:

```
pip install -r requirements.txt
```

Once the dependencies have been installed, run the application:

```
python app.py
```

Then visit http://127.0.0.1:8050/introduction

More info: https://packaging.python.org/guides/installing-using-pip-and-virtualenv/

##### To understand this app:

[app.py] - add external CSS and JS scripts
[index.py] - creates the layout of each page with static components nad dynamic content
 ---[assets] - static content: images, CSS, files
 ---[callbacks] - callbacks and plots design
 ---[data] - data storage 
 ---[functions] - scripts for NSGAII, resistance calculation and VPP
 ---[layouts] - folder with each page design
 
