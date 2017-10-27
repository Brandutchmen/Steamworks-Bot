from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import wpilib
class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Gear Front'

    def initialize(self):
        kP = 0.01
        kI = 0.0001

        turnController = wpilib.PIDController(kP, kI, 0, 0, self.navx, output=self)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-.5, .5)
        turnController.setContinuous(True)
        self.turnController = turnController
        self.rotation = 0

    def pidWrite(self, output):

        self.rotation = output

    @timed_state(duration=0.5, next_state='toPeg', first=True)
    def drive_wait(self):
        self.turnController.setSetpoint(self.navx.getYaw())
        self.turnController.enable()
        self.gearDrop.set(False)
        self.drive.mecanumDrive_Cartesian(0,0,self.rotation, 0) #Strafe Left/Right, Forward Back, rotate, gyro angle


    @timed_state(duration=4, next_state="OpenJaws")
    def toPeg(self):
        self.gearDrop.set(False)
        if self.ultrasonic.getRangeInches()<9:
            self.next_state("OpenJaws")
        else:
            self.drive.mecanumDrive_Cartesian(0,-.23, self.rotation, 0)
        print (self.ultrasonic.getRangeInches())

    @timed_state(duration=.6, next_state="openUp")
    def OpenJaws(self):
        self.gearDrop.set(True)
        self.drive.mecanumDrive_Cartesian(0,0, self.rotation, 0)


    @timed_state(duration=1, next_state="pushGear")
    def openUp(self):
        self.gearDrop.set(True)
        self.drive.mecanumDrive_Cartesian(0,0, self.rotation, 0)


    @timed_state(duration=1, next_state="backAfterPush")
    def pushGear(self):
        self.gearDrop.set(False)
        self.drive.mecanumDrive_Cartesian(0,-.23, self.rotation, 0)

    @timed_state(duration=1, next_state="stop")
    def backAfterPush(self):
        self.gearDrop.set(False)
        self.drive.mecanumDrive_Cartesian(0,.3, self.rotation, 0)

    @state()
    def stop(self):
        self.drive.mecanumDrive_Cartesian(0,0, self.rotation, 0)
        self.turnController.disable()
