from setuptools import setup,find_packages

setup(
	name="setup_py_demo",
	version='0.3',
	packages=find_packages(),
	install_requires=[
	],
	entry_points={
     "console_scripts":[
         "setup_py_demo = setup_py_demo:hello",
         ],
     },
 )


