
import numpy as np
import math
import random

from .value import Value

# -----------------------------------------------------------------------------------------------------------

class Module():

  def __init__(self, params):
    self.params = params

  def zero_grad(self):
    for p in self.params:
      p.grad = 0

  def params(self):
    return self.params

  def print_parameters(self):
    print(f'{len(self.params)} parameters : \n')
    for p in self.params:
      print(f'  --> {self.params.index(p)+1} : {p}')
    print('\n')

  def grads(self):
    print(f'{len(self.params)} parameters : \n')
    for p in self.params:
      print(f'  --> {p.grad}')
    return print('\n')

# -----------------------------------------------------------------------------------------------------------


class Neuron(Module):

  def __init__(self, Inputs, ActFunc):

    self.nin = Inputs

    self.weights = [Value(random.uniform(-1.0, 1.0)) for _ in range(self.nin)]
    self.bias = Value(0)
    self.actF = ActFunc

    super().__init__(self.weights + [self.bias])


  def __call__(self, input: list):

    act = sum( (w*i for w,i in zip(self.weights, input)), self.bias)
    return self.actF(act)



  def __repr__(self):
    print(f'Neuron : {self.nin} inputs | {self.params} parameters')


# -----------------------------------------------------------------------------------------------------------


class Layer(Module):



  def __init__(self, Inputs, Ouputs, ActFunc):

    self.nin = Inputs
    self.nout = Ouputs

    self.actF = ActFunc
    self.neurons = [Neuron(self.nin, self.actF) for _ in range(self.nout)]

    super().__init__([p for n in self.neurons for p in n.params])



  def __call__(self, input):
    return self.neurons[0](input) if len(self.neurons) == 1 else [n(input) for n in self.neurons]



  def __repr__(self):
    print(f'Layer : {len(self.neurons)} neurons | {self.params} parameters')



  def print_parameters(self, id):

    print(f'Layer {id} : ')
    super().print_parameters()


# -----------------------------------------------------------------------------------------------------------
    

class MLP(Module):


  def __init__(self, Inputs, Layers, ActFunc):

    self.nin = Inputs
    self.size = [self.nin] + Layers

    self.actF = ActFunc
    self.layers = [Layer(self.size[i], self.size[i+1], self.actF) for i in range(len(Layers))]

    super().__init__([p for l in self.layers for p in l.params])
    self.zero_grad()

  def __call__(self, input):

    for l in self.layers:
      input = l(input)

    return input

  def sample(self, inputs):

    return [self(i) for i in inputs]

  def print_parameters(self):

    print(f'MLP : {len(self.params)} total parameters \n')

    for i in range(len(self.layers)):
      self.layers[i].print_parameters(i+1)

    
# -----------------------------------------------------------------------------------------------------------
    
def basic_loss(preds, labels):
  return sum(((p-l)**2 for p,l in zip(preds, labels)))
def progress(current, total, size = 20, end=False,):
  p = (current/total) * size
  bar = '[' +( '😙' * round(p))  + (' -' * round(20-p)) + f'] {round((current/total) * 100, 2)} %'
  if end :print(bar)
  else: print(bar, end='\r')


# -----------------------------------------------------------------------------------------------------------

def train(Model, inputs, labels, loss = basic_loss, iter=1, LearnRate=0.1, LearnRateDecay = 1., print_results=False):
  
    print('\n ---> Training...')

    decay = 1.0001**(LearnRateDecay)

    for i in range(iter):

        Model.zero_grad()

        preds = Model.sample(inputs)
        l = loss(preds, labels)
        l.backward()

        LearnRate = LearnRate * (decay**-i)

        for p in Model.params:
            p.data += LearnRate * (-p.grad)

        if i % 10 == 0:
            progress(i, iter)
            if print_results:
                print(f"Iter : n {i+1} | loss : {l.data}")

    progress(iter, iter, end = True)
    print(f"Final loss achieved after {iter} iterations of traing: {l.data}\n ")