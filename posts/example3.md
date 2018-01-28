---
title: Example 3 -- Python Programming.
date: 2017.12.3
tags: python, programming
summary: a post about the python programming language
---

Python is a widely used high-level programming language for general-purpose programming, created by Guido van Rossum and first released in 1991. An interpreted language, Python has a design philosophy that emphasizes code readability (notably using whitespace indentation to delimit code blocks rather than curly brackets or keywords), and a syntax that allows programmers to express concepts in fewer lines of code than might be used in languages such as C++ or Java.[25][26] It provides constructs that enable clear programming on both small and large scales.[27]

Python features a dynamic type system and automatic memory management. It supports multiple programming paradigms, including object-oriented, imperative, functional and procedural, and has a large and comprehensive standard library.[28]

Python interpreters are available for many operating systems. CPython, the reference implementation of Python, is open source software[29] and has a community-based development model, as do nearly all of its variant implementations. CPython is managed by the non-profit Python Software Foundation.

```python
def derivative(f, dx):
    """Return a function that approximates the derivative of f
    using an interval of dx, which should be appropriately small.
    """
    def function(x):
        return (f(x + dx) - f(x)) / dx
    return function
```
