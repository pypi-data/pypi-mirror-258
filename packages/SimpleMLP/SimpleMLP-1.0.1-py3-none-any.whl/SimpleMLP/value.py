
import numpy as np

# -----------------------------------------------------------------------------------------------------------

class Value():

  def __init__(self, data, parents = (), op='', label=''):

    self.label = label
    self.data = data
    self.parents = parents
    self.op = op
    self.grad = 0
    self._backward = lambda : None

# -----------------------------------------------------------------------------------------------------------

  def __repr__(self):
    return f"Value(data='{self.data}')"

# -----------------------------------------------------------------------------------------------------------

  def __add__(self, other):
    other = other if isinstance(other, Value) else Value(other, label=str(other))
    out =  Value(self.data + other.data, (self, other), '+')

    def _backward():
      self.grad += out.grad
      other.grad += out.grad
    out._backward = _backward

    return out



  def __radd__(self, other):
    return self + other
  def __sub__(self, other):
    return self + (-other)
  def __rsub__(self, other):
    return other + (-self)

# -----------------------------------------------------------------------------------------------------------

  def __mul__(self, other):
    other = other if isinstance(other, Value) else Value(other, label=str(other))
    out = Value(self.data * other.data, (self, other), '*')

    def _backward():
      self.grad += other.data * out.grad
      other.grad += self.data * out.grad
    out._backward = _backward

    return out


  def __rmul__(self, other):
    return self*other
  def __neg__(self):
    return self * -1

# -----------------------------------------------------------------------------------------------------------

  def __truediv__(self, other):
    return self * (other**-1)
  def __rtruediv__(self, other):
    return other * (self**-1)

# -----------------------------------------------------------------------------------------------------------


  def __pow__(self, other):
    assert isinstance(other, (float, int))

    out = Value(self.data**other, (self,), f"^{other}")

    def _backward():
      self.grad += other * (self.data**(other-1)) * out.grad
    out._backward = _backward

    return out


# -----------------------------------------------------------------------------------------------------------


  def tanh(self):

    x = self.data
    out =  Value(( (np.exp(2 * self.data) - 1) / (np.exp(2 * self.data) + 1) ), (self,), 'tanh')

    def _backward():
      self.grad += (1 - (out.data**2)) * out.grad
    out._backward = _backward

    return out


# -----------------------------------------------------------------------------------------------------------

  def exp(self):

    out = Value(np.exp(self.data), (self,), 'exp')

    def _backward():
      self.grad += out.data * out.grad
    out._backward = _backward

    return out


# -----------------------------------------------------------------------------------------------------------


  def backward(self):

      visited = set()
      topo = []
      def build_topo(start):
        if start not in visited:
          visited.add(start)
          for parent in start.parents:
            build_topo(parent)
          topo.append(start)

      self.grad= 1.0
      build_topo(self)

      for value in reversed(topo):
        value._backward()


# -----------------------------------------------------------------------------------------------------------


