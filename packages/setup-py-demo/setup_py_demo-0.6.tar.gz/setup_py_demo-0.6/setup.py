from setuptools import setup,find_packages


with open("README.md","r") as f:
    description = f.read()

setup(
	name="setup_py_demo",
	version='0.6',
	packages=find_packages(),
	install_requires=[
	],
	entry_points={
     "console_scripts":[
         "setup_py_demo = setup_py_demo:hello",
         ],
     },
 long_description = description,
 long_description_content_type = "text/markdown"
 )

