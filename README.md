# 🐟 nemo — a tiny interpreted language 

nemo is a small, experimental programming language written in Python.  

---

## ✨ Features
- **Minimal syntax** — clean and easy to read.  
- **Dynamic typing** — no need for type declarations.  
- **Control flow** — `if / elif / else`, `loop`, and `stop`.   
- **Macros** — write code that writes code.  
- **JIT for loops** — repeat loops compile down to Python for extra speed.  

Example factorial in nemo:
```nemo
n = 5
fact = 1
i = 1

loop i <= n {
    fact *= i
    i += 1
}

yell("factorial of", n, "is", fact)
```

## 🧩 What is a Macro?
Think of them as tiny functions with no input or output — a way to group and reuse behavior.

---

### ✨ Example: Simple Macro
```nemo
macro greet {
    yell("hello there ")
    yell("welcome to nemo ")
}

yell("starting program")
greet
yell("program continues")
```

## 📝 Simple Example: Loops with Conditionals

```nemo
# Loop from 1 to 5
i = 1

# repeat can be used for fixed numebr of iterations
repeat 5 {

    # Check if number is even or odd
    if i % 2 == 0 {
        yell(i, "is even")
    } elif i % 2 != 0 {
        yell(i, "is odd")
    } else {
        yell(i, "is something else")
    }

    i += 1
}
```

## 🛠️ Requirements

To run nemo, you need:

- **Python 3.x** (Python 3.7 or higher recommended)  
- No additional dependencies or packages required 
