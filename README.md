# Flexible and comprehensive software app for design of synthetic DNA sequences without unwanted patterns

## Pre-Requisite

Please execute the following command within your working environment:

```
pip3 install -r requirements.txt
```

## Execute Terminal Program

To execute the elimination tool from the Terminal, please use the following command:

```
python3 ./BioBliss.py -s <seq_file_path> -p <pattern_file_path> -c <codon_usage_table>
```

For example:

```
python3 ./BioBliss.py -s ./files/one_coding/s_file.txt -p ./files/one_coding/p_file.txt -c ./files/codon_usage_table/codon_usage.txt
```

## Execute GUI Program

To execute the elimination tool GUI, please use the following command:

```
python3 ./BioBliss.py -g
```
