# har2rf-req
A tool to convert har files into robot framework files using requests library, it will try it's best to correlate request body values from previous requests, if not successful it create a variable for the value.

This tool is still experimental and has not been well tested, there may be bugs and it may not handle all situations as expected.

## Usage

```
python har2rf-req <path to har files>
```
or
```
python har2rf-req <path to har file>/<harfile>
```
