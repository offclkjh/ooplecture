class Temperature:
    # TODO: Class attribute
    unit = "Celsius"

    def __init__(self, value):
        # TODO: Instance attribute
        self.value = value

    # TODO: Instance method
    def display(self):
        print(f"value : {self.value}, unit : {self.unit}")
        return

    # TODO: Class method with relevant decorator
    def change_unit(cls, new_unit):
        if cls.unit == "Fahrenheit":
            cls.value = ((cls.value - 32) * 5) / 9
        elif cls.unit == "Kelvin":
            cls.value = cls.value - 273.15

        if new_unit == "Fahrenheit":
            cls.value = (cls.value * 1.8) + 32
        elif new_unit == "Kelvin":
                cls.value += 273.15
        cls.unit = new_unit

    # TODO: Static method with relevant decorator
    @staticmethod
    def to_fahrenheit(celsius):
        return (celsius * 1.8) + 32

Temperature = Temperature(100)
Temperature.display()
print(Temperature.to_fahrenheit(100))
Temperature.change_unit("Kelvin")
Temperature.display()
print("cuz user changed unit and automatically value")
