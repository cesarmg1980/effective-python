class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


class VoltageResistor(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

r2 = VoltageResistor(1e3)
print(f'Before: {r2.current:.2f} amps')
r2.voltage = 10
print(f'After: {r2.current:.2f} amps')


class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <=0:
            raise ValueError(f'ohms must be > 0; got {ohms}')
        self._ohms = ohms

r3 = BoundedResistance(1e3)
try:
    r3.ohms = 0
except ValueError as ex:
    print(f"Error: {ex.args[0]}")

try:
    BoundedResistance(-1)
except ValueError as ex:
    print(
        f"Also an error is thown when an invalid value is passed to the constructor: {ex.args[0]}"
    )


class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Ohms is immutable")
        self._ohms = ohms

r4 = FixedResistance(1e23)
try:
    r4.ohms = 2e3
except AttributeError as ex:
    print(f"Error: {ex.args[0]}")
