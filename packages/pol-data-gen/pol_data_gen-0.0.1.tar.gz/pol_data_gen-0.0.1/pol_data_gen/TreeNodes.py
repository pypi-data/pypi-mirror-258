from abc import ABC, abstractmethod

# ---------------- Abstract classes ----------------
class BranchNode(ABC):
    def __init__(self, left_node, right_node):
        self.left_node = left_node
        self.right_node = right_node

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def evaluate(self, environment):
        pass


class LeafNode(ABC):

    def __init__(self, value):
        self.value = value

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def evaluate(self, environment):
        pass

# ---------------- Branch nodes ----------------
class Power(BranchNode):

    def __str__(self):
        return f'{self.left_node}^{self.right_node}'

    def evaluate(self, environment):
        return self.left_node.evaluate(environment) ** self.right_node.evaluate(environment)


class Product(BranchNode):
    def __str__(self):
        return f'{self.left_node} * {self.right_node}'

    def evaluate(self, environment):
        return self.left_node.evaluate(environment) * self.right_node.evaluate(environment)


class Sum(BranchNode):

    def __str__(self):
        return f'({self.left_node} + {self.right_node})'

    def evaluate(self, environment):
        return self.left_node.evaluate(environment) + self.right_node.evaluate(environment)

# ---------------- Leaf Nodes ----------------
class Constant(LeafNode):

    def __str__(self):
        return f'({self.value})'

    def evaluate(self, environment):
        return self.value


class Variable(LeafNode):

    def __str__(self):
        return self.value

    def evaluate(self, environment):
        return environment.get(self.value)
