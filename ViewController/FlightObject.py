
class FlightObject:

    @property
    def current_PositionX(self):
        return self.position_X[self.currentStep]

    @property
    def current_PositionY(self):
        return self.position_Y[self.currentStep]

    @property
    def current_VelocityX(self):
        return self.velocity_X[self.currentStep]

    @property
    def current_VelocityY(self):
        return self.velocity_Y[self.currentStep]

    @property
    def prediction_X(self):
        return self.position_X[self.currentStep:self.currentCalculationStep]

    @property
    def prediction_Y(self):
        return self.position_Y[self.currentStep:self.currentCalculationStep]
