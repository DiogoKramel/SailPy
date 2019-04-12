# About SailPy

**SailPy** is a Python application for conceptual sailboat design with an object-oriented paradigm. **SailPy**  implements several routines in order to optimize the dimensions of the hull and all appendages of a sailboat. 

The application was developed by Diogo Kramel as result of his Master Thesis and is maintained by the Polytechnic School of the University of São Paulo in São Paulo.

## Key features

- Calculating and plotting the sections for racer and cruiser sailboats
- Set the limits of optimization for each dimensions
- Download all the sailboats dimensions created during the optimization proccess
- Assistance of dynamic representation to orient the user on chosing the best set of dimensions

## Contributing

When contributing, fork the repository and send pull requests with your commits. Wait for review and approval by the development team.

You are also welcome to create [issues](https://github.com/DiogoKramel/SailPy/issues) reporting bugs or suggesting improvements and features for further development.

## What do the files do?

A short summary of the files structure is provided below to encourage users to modify them to their own usage.

[app.py](app.py)

External sources.

[index.py](index.py)

The app itself. It organizes the layout and how each page is called when the user moves one tab next.

[assets/*](assets/)

This folder contains all images displayed in the app layout. It also contains the files to store relevant data between each step.

[callbacks/*](callbacks/)

Callbacks are all the functions that update the data to the scripts when the user changes an input property. 

[env/*](env/)

It stores all the libraries imported throughout the application. They are listed at [requirements.txt](requirements.txt) as well.

[functions/*](functions/)

In this folder you can find the scripts for calculating the resistance components, the Velocity Prediction Programme, the parametric hull, and the genetic algorithm.

[layouts/*](layouts/)

Contains the layouts for each page in the multi-page structure, connecting the callbacks and functions to the user interface.


## How to run the app locally

You can clone or download this repo:

```
git clone https://github.com/AppName
```

Then cd into the repo:

```
cd AppNamePath
```

Now create and activate a virtual environment. On a mac:

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

More info: https://packaging.python.org/guides/installing-using-pip-and-virtualenv/

## Licensing

SailPy is licensed under MIT.

***