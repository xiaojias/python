# Course Notes
## Programming
- comment
- print


## Concepts
testin frameworks: pytest, se, splinter

# Python Data Types
- Numeric: Integer, Complex Number, Float

- Dictionary

- Boolean

- Set

- Sqquence Type: String, List, Tuple

## Identity
id()

Can be considered to be the address in the memory where the object is stored. An object's identity never changes once it has been created.

'is' operator compares the identity of two objects. id() functions returns an integer representing its identity.

## Type
type()


## Type conversion
int()
str()

tuple('random')
```
('r', 'a', 'n', 'd', 'o', 'm')
```

list('random')
```
['r', 'a', 'n', 'd', 'o', 'm']
```

set('random')
```
{'d', 'o', 'm', 'a', 'n', 'r'}
```

## Fucntions for sequence data

### String

```
>>> test = 'random'
>>> test[0]
'r'
>>> test.index('d')
3

>>> test[1:3]
'an'
```
- Slicing
st = 'myname'
st[1:3]

upper(), lower(), split(), 

### List
- List elements can be accessed by index
```
>>> a = [1, 2, 3, 4, 5, 6]
>>> a[2:5]
[3, 4, 5]
>>> a[1:6:2]
[2, 4, 6]

>>> a[::-1]
[6, 5, 4, 3, 2, 1]
```

- Concatenation and replication
```
>>> a += [7, 8, 9]
>>> a
[1, 2, 3, 4, 5, 6, 7, 8, 9]

>>> a = [0] + a
>>> a
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

>>> a
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> a * 2
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


```

- Modify list Values
```
>>> a
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> a[0:3] = [101, 102, 103]
>>> a
[101, 102, 103, 3, 4, 5, 6, 7, 8, 9]

>>> a
[101, 102, 103, 3, 4, 5, 6, 7, 8, 9]
>>> a[0:3] = [100] *3
>>> a
[100, 100, 100, 3, 4, 5, 6, 7, 8, 9]

```

- Methods
a = [1, 2, 3]

a.append(5)
extend()

```
>>> a.extend([5, 6, 7])
>>> a
[1, 2, 3, 4, 5, 6, 7]
```

remove()
```
>>> a
[1, 2, 3, 4, 5, 6, 7]
>>> a.remove(5)
>>> a
[1, 2, 3, 4, 6, 7]
```

pop()
```
>>> a
[1, 2, 3, 4, 6, 7]
>>> a.pop()
7
>>> a
[1, 2, 3, 4, 6]

>>> a
[1, 2, 3, 6]
>>> a.pop(0)
1
>>> a
[2, 3, 6]
```

## Tuple
Tuple are another ordered collection of objects like list, except for 2 properties where they differ:
1. Typles are immutible;
2. Tuples are defined using parentthesis instead of square brackets.

- Tuple packing and unpacking
(a, b, c, d) = (1, 2, 3, 4)
```
>>> (a, b, c, d) = (1, 2, 3, 4)
>>> a
1
>>> c
3
```

Tuple is faster then List;

## Dictionary
- Definition

```
>>> d = {'banana': 'yellow', 'apple': 'red'}
>>> type(d)
<class 'dict'>
>>> d
{'banana': 'yellow', 'apple': 'red'}

>>> e = dict([('banana', 'yellow'), ('apple', 'red')])
>>> type(e)
<class 'dict'>
>>> e
{'banana': 'yellow', 'apple': 'red'}


```

- **Keys should be unique**
- **Dictionary keys must be of immutable data type, Duplicate keys not allowed. No such restrictions on values**

```
>>> e = dict([('banana', 'yellow'), ('apple', 'red'), ('apple', 'blue')])
>>> e
{'banana': 'yellow', 'apple': 'blue'}
>>> e.keys()
dict_keys(['banana', 'apple'])

>>> e['apple']
'blue'
>>>

```

### Dictionary Operations and functions
- Using Keys
d.items(),    ---> List of all key & Values
d.keys(),    ---> List of all keys
d.values()      ---> List of all values

d.get('apple'), 

d.popitem()  --> pop up the last item


# Python Type Hirerachy

## special Operator
is, not is, in, not in

```
a = 1001
b = 1000 + 1
a == b

#True

a is b
# False

```

## Math Module in Python


# Importance of Identation in Python

# Conditional Expressions ( Python's Ternary Operator)

age = 26
x = 'adult' if age > 18 else 'child'
x

# Pass Statement
```
age = 20
if age > 18:
    pass
else:
    print("This person is an young.")
```

## While Loop in Python
```
age = 20
if age > 18:
    pass
else:
    print("This person is an young.")
```

## Break and Continue Statements
```
break

continue
```

