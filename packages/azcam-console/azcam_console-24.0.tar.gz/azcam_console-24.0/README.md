# AzCam Console

*azcam-console* is a console application for the *azcam* acquisition and analysis package. It usually runs in an IPython window and is used to both acquire and analyze data in a python scripting environment.

## Documentation

See https://azcam.readthedocs.io/.

## Installation

`pip install azcam-console`

Or download the latest version from from github: https://github.com/mplesser/azcam-console.git.

You may need to install `python3-tk` on Linux systems [`sudo apt-get install python3-tk`].

## Configuration and startup 

An example code snippet to start an *azcamconsole* process is:

```
ipython -m azcam_itl.console --profile azcamconsole -i -- -system DESI
```

and then in the IPython window:

```python
instrument.set_wavelength(450)
wavelength = instrument.get_wavelength()
print(f"Current wavelength is {wavelength}")
exposure.expose(2., 'flat', "a 450 nm flat field image")
```
