# kmtm
A simple CLI tool to convert kilometers to miles so that I don't have to look up the 
conversion each time I see someone post about cycling/running stats.

## Installation
```
pip install kmtkm
```
Okay, well not yet because I haven't looked into adding to pypi yet..

## Usage

Example:
```
kmtm 10 -k
```

For this example, 10 is the distance that you would like to convert, and `-k` represents the unit you would like the distance converted to.  In this situation, 10 miles will be converted to kilometers.

The NUMBER is a required argument and both `-k` and `-m` are options that can be used individuall or at the same time.


### kmtm --help
```
Options:
  -k, --kilos  Converts miles to kilometers
  -m, --miles  Converts kilometers to miles.
  --help       Show this message and exit.
  ```

