# Four Russians Algorithm

## Table of contents
* [Description](#description)
* [Setup](#setup)
* [Usage](#usage)

## Description
This project contains the implementation of **Four Russians Algorithm** for multiplication of boolean matrices.
The pseudocode is given below:
![pseudocode](https://louridas.github.io/rwa/assignments/four-russians/four_russians_algorithm.png)

The code wraps boolean matrices into the `BoolMatrix` abstraction, which can manipulate with raw 2d-lists. In particular, it supports logical-OR between matrices and rows, extracting blocks (row-wise and column-wise) from matrix, assigning and reading by index.

The Four Russians Algorithm itself is divided into 2 parts: decomposition into blocks (lines 2-4 and 19-20) and blocks multiplication (lines 5-18).

Block multiplication is done as follows:
1. Create matrix with all possible disjunctions (RS) from row-wise block matrix (B_i)
2. Create an empty block multiplication matrix (C_i)
3. Convert each row from column-wise block matrix (A_i) into the decimal number
4. Assign the row from RS by this decimal index to the corresponing row of C_i

In the block decomposition module we create row-wise and column-wise blocks and iteratively multiply them. After each block multiplication we apply logical-OR between result matrix in block multiplication result matrix.


Time complexity: <img src="https://render.githubusercontent.com/render/math?math=O(\frac{n^3}{log(n)})">

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
