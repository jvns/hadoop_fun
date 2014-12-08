hadoop_fun
==========

Some Python code to help you have fun with Hadoop. Unmaintained.

Example code:

```python
import hdfs_fun
fun = hdfs_fun.HDFSFun()
blocks = fun.find_blocks('/wikipedia.csv')
fun.print_blocks(blocks)
```

will output something like:

```
     Bytes |   Block ID | # Locations |       Hostnames
 134217728 | 1073742025 |           1 |      hadoop-w-1
 134217728 | 1073742026 |           1 |      hadoop-w-1
 134217728 | 1073742027 |           1 |      hadoop-w-0
 134217728 | 1073742028 |           1 |      hadoop-w-1
 134217728 | 1073742029 |           1 |      hadoop-w-0
 134217728 | 1073742030 |           1 |      hadoop-w-1
 134217728 | 1073742031 |           1 |      hadoop-w-0
 134217728 | 1073742032 |           1 |      hadoop-w-1
 134217728 | 1073742033 |           1 |      hadoop-w-0
 134217728 | 1073742034 |           1 |      hadoop-w-1
 134217728 | 1073742035 |           1 |      hadoop-w-0
 134217728 | 1073742036 |           1 |      hadoop-w-0
```
