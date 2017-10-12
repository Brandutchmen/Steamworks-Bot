from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import wpilib
class DriveForward(StatefulAutonomous):
    
    DEFAULT = False
    MODE_NAME = 'Drop'
    
    def initialize(self):
        pass
    
    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.drive.arcadeDrive(0,0)
    @timed_state(duration=4, next_state='drop')
    def drive_forward(self):
        self.drive.arcadeDrive(0.5, 0)
    @timed_state(duration=0.5, next_state='reverse')
    def drop(self):
        self.gearDrop.set(wpilib.DoubleSolenoid.Value.kForward)
        self.drive.arcadeDrive(0, 0)
    @timed_state(duration=0.5, next_state='close')
    def reverse(self):
        self.drive.arcadeDrive(-0.5, 0)
    @timed_state(duration=0.5, next_state='stop')
    def close(self):
        self.gearDrop.set(wpilib.DoubleSolenoid.Value.kReverse)
        self.drive.arcadeDrive(0, 0)
    @state()
    def stop(self):
        self.drive.arcadeDrive(0,0,0)
