# Create a Controller class to connect the GUI and the model
from functools import partial


class LoginCtrl:
    """PyCalc Controller class."""
    def __init__(self, view):
        """Controller initializer."""
        self.view = view
        # Connect signals and slots
        self.connectSignals()

    def buildExpression(self, sub_exp):
        """Build expression."""
        expression = self.view.displayText() + sub_exp
        self.view.setDisplayText(expression)

    def connectSignals(self):
        """Connect signals and slots."""
        for btnText, btn in self.view.buttons.items():
            if btnText not in {'x'}:
                btn.clicked.connect(partial(self.buildExpression, btnText))

        self.view.buttons['x'].clicked.connect(self.view.clearDisplay)