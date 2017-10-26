from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import wpilib
class DriveForward(StatefulAutonomous):
    
    DEFAULT = False
    MODE_NAME = 'Drop'
    
    def initialize(self):
        pass
    
    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.gearDrop.set(wpilib.DoubleSolenoid.Value.kReverse)
        self.drive.mecanumDrive_Cartesian(0,0,0,0) #Strafe Left, Forward Back, Strafe Right, Intensity)
    @timed_state(duration=4, next_state='drop')
    def drive_forward(self):
        if self.ultrasonic.getRangeInches()<9:
            self.next_state("Drop")
        else:
            self.drive.mecanumDrive_Cartesian(0,-1,0,.3)
        print (self.ultrasonic.getRangeInches())
    @timed_state(duration=0.5, next_state='reverse')
    def drop(self):
        self.gearDrop.set(wpilib.DoubleSolenoid.Value.kForward)
        self.drive.arcadeDrive(0, 0)
    @timed_state(duration=0.5, next_state='close')
    def reverse(self):
        self.drive.arcadeDrive(0, 0.5)
    @timed_state(duration=0.5, next_state='stop')
    def close(self):
        self.gearDrop.set(wpilib.DoubleSolenoid.Value.kReverse)
        self.drive.arcadeDrive(0, 0)
    @state()
    def stop(self):
        self.drive.arcadeDrive(0,0,0)
