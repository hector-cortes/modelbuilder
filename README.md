# Basic Usage
```python
from modelbuilder import Model, Attribute

class Pet(Model):
    tag = Attribute(obj_name="tag", obj_type=Tag)
    name = Attribute(obj_name="name", obj_type=str)
    
class Tag(Model):
    id = Attribute(obj_name="id", obj_type=int)
```
# Purpose
Small project to learn more about Python metaclasses

# Useful Resources
* Videos 
  * David Beazley - Python 3 Metaprogramming
    * https://www.youtube.com/watch?v=sPiWg5jSoZI
  * James Powell - Advanced Metaphors in Coding with Python
    * https://www.youtube.com/watch?v=R2ipPgrWypI
* Blogs
  * Eli Bendersky - Python metaclasses by example
    * https://nbviewer.jupyter.org/github/akittas/presentations/blob/master/pythess/meta_alltheway/meta_alltheway.ipynb
  * Ionel Maries - Understanding Python metaclasses
    * https://blog.ionelmc.ro/2015/02/09/understanding-python-metaclasses/
  * It's metaclasses all the way down
    * https://nbviewer.jupyter.org/github/akittas/presentations/blob/master/pythess/meta_alltheway/meta_alltheway.ipynb

