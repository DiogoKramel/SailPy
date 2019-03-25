##### About this application:

**AppName.js** is a JavaScript library for conceptual ship design with an object-oriented paradigm. Vessel.js represents the vessel as an object, which is used to simulate different functionalities and behaviors.

The library is developed by Polytechnic School of the University of São Paulo in São Paulo. For documentation and other resources, visit our [wiki](https://github.com/shiplab/vesseljs/wiki).

## Contributing

When contributing, fork the repository and send pull requests with your commits. If your modifications are only to files related to examples and you have pull request authorization, you can approve them by yourself. If not, then wait for review and approval by the development team.

You are also welcome to create [issues](https://github.com/shiplab/vesseljs/issues) reporting bugs or suggesting improvements and features for development.

##### To run this app:

You can clone or download this repo:

```
git clone https://github.com/plotly/dash-vanguard-report.git
```

Then cd into the repo:

```
cd dash-vanguard-report
```

Now create and activate a virtualenv (noting the python runtime):  
On a mac:

```
virtualenv -p <python version> venv
source venv/bin/activate
```

On a Windows:

```
virtualenv -p <python version> venv
venv/Scripts/activate
```

Now that virtualenv is setup and active we can install the dependencies:

```
pip install -r requirements.txt
```

Once the dependencies have been installed, run the application:

```
python app.py
```

Then visit http://127.0.0.1:8050/introdction

More info: https://packaging.python.org/guides/installing-using-pip-and-virtualenv/

##### To understand this app:

[app.py] - add external CSS and JS scripts
[index.py] - creates the layout of each page
[layout.py] - contains the main elements (bottom bar, top bar, content...)
