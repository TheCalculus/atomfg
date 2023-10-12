classical, one-dimensional linear pde:
$ \dfrac{\partial^2 u(x,t)}{\partial x^2} = 
  \dfrac{1}{v^2} \dfrac{\partial^2 u(x,t)}{\partial t^2} $ 
<br>

solving using *separation of variables* <br>

$ u(x,t)=X(x)T(t) \\
  u(x,t)=\sum_i c_ iX_i(x)T_i(t), \forall c_i $
<br><br>

find values of $ c_i $ that satisfy boundary conditions <br>
substitute separated function into wave equation        <br><br>

$ \dfrac{\partial^2 X(x)T(t)}{\partial x^2} = 
  \dfrac{1}{v^2} \dfrac{\partial^2 X(x)T(t)}{\partial t^2} \\
  \dots \\ \space \\
  \dfrac{1}{X(x)} \dfrac{\partial^2 X(x)}{\partial x^2} = \dfrac{1}{v^2} \dfrac{1}{T(t)} \dfrac{\partial^2T(t)}{\partial t^2} \\ $
<br>

since the *lhs* depends only on $ x $ and *rhs* depends only on $ y $, 
the only way for the equation to hold is to have *lhs* = *rhs* = *some constant* $K$ <br>
https://www.public.asu.edu/~hhuang38/pde_slides_sepvar-heat.pdf                      <br>
