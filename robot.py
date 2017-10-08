#!/usr/bin/env python3

import wpilib
from wpilib import RobotDrive
import wpilib.buttons
from robotpy_ext.autonomous import AutonomousModeSelector



class MyRobot(wpilib.IterativeRobot):
    
    frontLeftChannel  = 2
    rearLeftChannel   = 1
    frontRightChannel = 3
    rearRightChannel  = 4
    
    
    
    joystickChannel   = 0
    
    
    def robotInit(self):
        if not wpilib.RobotBase.isSimulation():
            import ctre
            
            self.FLC = ctre.CANTalon(self.frontLeftChannel)
            self.FRC = ctre.CANTalon(self.frontRightChannel)
            self.RRC = ctre.CANTalon(self.rearRightChannel)
            self.RLC = ctre.CANTalon(self.rearLeftChannel)
        
        else:
            self.RRC = wpilib.Talon(self.rearRightChannel)
            self.RLC = wpilib.Talon(self.rearLeftChannel)
            self.FRC = wpilib.Talon(self.frontRightChannel)
            self.FLC = wpilib.Talon(self.frontLeftChannel)
        
        self.controller = wpilib.Joystick(self.joystickChannel)
        self.winch_motor1 = wpilib.Talon(7)
        self.winch_motor2 = wpilib.Talon(8)
        
        self.robotDrive = wpilib.RobotDrive(self.FLC, self.RLC, self.FRC, self.RRC)
                                            
        wpilib.CameraServer.launch()
        
        #Goto 10.44.80.2:1181
        #to view the cameras without HTML page
            
        self.robotDrive.setInvertedMotor(RobotDrive.MotorType.kFrontLeft, True)
                                            
        self.robotDrive.setInvertedMotor(RobotDrive.MotorType.kRearLeft, True)
                                            
                        
        self.winch_forward = wpilib.buttons.JoystickButton(self.controller, 5)
        self.winch_backward = wpilib.buttons.JoystickButton(self.controller, 6)
                                            
        self.flip = wpilib.buttons.JoystickButton(self.controller, 1)
        self.open_double = wpilib.buttons.JoystickButton(self.controller, 3)
        self.close_double = wpilib.buttons.JoystickButton(self.controller, 4)
                                            
        self.single_solenoid = wpilib.Solenoid(1)
        self.double_solenoid = wpilib.DoubleSolenoid(2,3)
        
        self.dm = 2

        self.xboxMec = wpilib.buttons.JoystickButton(self.controller, 8)
        self.xboxTank = wpilib.buttons.JoystickButton(self.controller, 7)



        self.components = {
            'drive': self.robotDrive,
            'gearDrop': self.double_solenoid,
        }

        self.automodes = AutonomousModeSelector('autonomous', self.components)

    def autonomousPeriodic(self):
        self.automodes.run()


    def teleopPeriodic(self):


        if self.xboxMec.get():
            self.dm = 1
        if self.xboxTank.get():
            self.dm = 2
        if self.dm == 1:
            self.robotDrive.mecanumDrive_Cartesian(self.controller.getX(), self.controller.getY(), self.controller.getRawAxis(4), 0)
        if self.dm == 2:
            self.robotDrive.tankDrive(self.controller.getY(), self.controller.getRawAxis(5), True)


        if (self.winch_forward.get()):
            self.winch_motor1.set(1)
            self.winch_motor2.set(1)
        elif (self.winch_backward.get()):
            self.winch_motor1.set(-1)
            self.winch_motor2.set(-1)
        else:
            self.winch_motor1.set(0)
            self.winch_motor2.set(0)
        
        if (self.flip.get()):
            self.single_solenoid.set(True)
        else:
            self.single_solenoid.set(False)
        
        if (self.open_double.get()):
            self.double_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
            
        elif (self.close_double.get()):
            self.double_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)


if __name__ == '__main__':
    wpilib.run(MyRobot)
