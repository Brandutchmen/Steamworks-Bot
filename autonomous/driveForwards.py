from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state

class DriveForward(StatefulAutonomous):

    DEFAULT = True
    MODE_NAME = 'Drive Forward'
    
    def initialize(self):
        pass
    
    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        """
            Waits .5 seconds. Not necessary, But sometimes sensors are not ready right away
            """
        self.drive.mecanumDrive_Cartesian(0, 0, 0, 0)

    @timed_state(duration=1.5, next_state='stop')
    def drive_forward(self):
        """
            Drives forward for 4 seconds
            """
        self.drive.mecanumDrive_Cartesian(-.5, 0, 0, 0)
    
    @state()
    def stop(self):
        """
            Stop until auto ends
            """
        self.drive.mecanumDrive_Cartesian(0, 0, 0, 0)
