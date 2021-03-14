# Four Russians Algorithm

## Table of contents
* [Description](#description)
* [Setup](#setup)
* [Usage](#usage)

## Description
This project contains the implementation of **Four Russians Algorithm** for multiplication of boolean matrices.
The pseudocode is given below:
![pseudocode](https://louridas.github.io/rwa/assignments/four-russians/four_russians_algorithm.png)

Time complexity: <img src="https://render.githubusercontent.com/render/math?math=O(\frac{n^3}{log(n)}) = -1">

Explanation of the algorithm: [Real World Algorithms](https://louridas.github.io/rwa/assignments/four-russians/)  
The details of the algorithm: [Springer](https://link.springer.com/content/pdf/10.1007%2F978-0-387-88757-9_9.pdf).

## Setup
The algorithm is implemented using `python 3.8.5`.  
Tested using `pytest`.  
Console interface is provided by `click`.

> :warning: Numpy is used only for testing. All matrices manipulation is done using custom wrapper `BoolMatrix`


To set up the environment run:
```
pip install -r requirements.txt
```

## Usage

### Run

To run the algorithm you should create a `json`-file with `left` and `right` matrices' data as following:
```json
{
    "left": [[true, false], [false, true]],
    "right": [[true, true], [false, false]]
}
```

#### Simple
The following command will log into the console the result of computation:
```
python3 main.py <matrices' data json-file>
```

#### Save the output
To save the output in json file run:
```
python3 main.py <matrices' data json-file> --result_write_path <output json-file>
```

### Test
To run the tests make sure that `pytest` is installed.
Simply run the following command to test the whole `four_russians` library, including both `BoolMatrix` and algorithm implementation:
```
pytest
```

Numpy is used for the reference computation.
