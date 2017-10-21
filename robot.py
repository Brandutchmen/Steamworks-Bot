#!/usr/bin/env python3
# "Wall-E" Team 4480 Robot Code 2017
import wpilib

from wpilib import RobotDrive

import wpilib.buttons

from robotpy_ext.autonomous import AutonomousModeSelector

class MyRobot(wpilib.IterativeRobot):
    
    fLeftChannel  = 2
    rLeftChannel   = 1
    fRightChannel = 3
    rRightChannel  = 4
    joystickChannel   = 0
    
    def robotInit(self):
        if not wpilib.RobotBase.isSimulation():
            import ctre
            self.FLC = ctre.CANTalon(self.fLeftChannel)
            self.FRC = ctre.CANTalon(self.fRightChannel)
            self.RRC = ctre.CANTalon(self.rRightChannel)
            self.RLC = ctre.CANTalon(self.rLeftChannel)
        else:
            self.RRC = wpilib.Talon(self.rRightChannel)
            self.RLC = wpilib.Talon(self.rLeftChannel)
            self.FRC = wpilib.Talon(self.fRightChannel)
            self.FLC = wpilib.Talon(self.fLeftChannel)
        
        self.controller = wpilib.Joystick(self.joystickChannel)

        self.winch_motor1 = wpilib.Talon(7)
        self.winch_motor2 = wpilib.Talon(8)
        
        self.robotDrive = wpilib.RobotDrive(self.FLC, self.RLC, self.FRC, self.RRC)
        self.robotDrive.setInvertedMotor(RobotDrive.MotorType.kFrontLeft, True)
        self.robotDrive.setInvertedMotor(RobotDrive.MotorType.kRearLeft, True)

        #self.winch_forward = wpilib.buttons.JoystickButton(self.controller, 6)
        self.winch_backward = wpilib.buttons.JoystickButton(self.controller, 5)
        self.paddleGet = wpilib.buttons.JoystickButton(self.controller, 1)
        self.gearDrop = wpilib.buttons.JoystickButton(self.controller, 6) # Right Bumper
        #self.closeGear = wpilib.buttons.JoystickButton(self.controller, 4)
        self.xboxMec = wpilib.buttons.JoystickButton(self.controller, 8)
        self.xboxMec2 = wpilib.buttons.JoystickButton(self.controller, 7)
        self.paddle = wpilib.Solenoid(1)
        self.gear = wpilib.DoubleSolenoid(2,3)

        self.components = {
            'drive': self.robotDrive,
            'gearDrop': self.gear,
        }
        self.automodes = AutonomousModeSelector('autonomous', self.components)
        #wpilib.CameraServer.launch() #Goto 10.44.80.2:1181 to view the cameras without HTML page
   #     self.dm = 1
        
    def autonomousPeriodic(self):
        self.automodes.run()
    def teleopPeriodic(self):

        #if self.xboxMec.get():
         #   self.dm = 1
        #if self.xboxMec2.get():
          #  self.dm = 2
     #   if self.dm == 1:
        
      #  if self.dm == 2:
       #     self.robotDrive.mecanumDrive_Cartesian(self.controller.getY(), self.controller.getRawx(4), -1*self.controller.getRawX(), 0)
        
        if (self.winch_backward.get()):
            self.winch_motor1.set(-1*self.controller.getRawAxis(2))
            self.winch_motor2.set(-1*self.controller.getRawAxis(2))
        else:
            if self.controller.getRawAxis(2) > 0.1:
                self.winch_motor1.set(self.controller.getRawAxis(2))
                self.winch_motor2.set(self.controller.getRawAxis(2))
            else:
                self.winch_motor1.set(0)
                self.winch_motor2.set(0)
        
        if (self.paddleGet.get()):
            self.paddle.set(True)
        else:
            self.paddle.set(False)
        
        if (self.gearDrop.get()):
            self.gear.set(wpilib.DoubleSolenoid.Value.kForward)
            
        else:
            self.gear.set(wpilib.DoubleSolenoid.Value.kReverse)


        multi = 0.35 + (self.controller.getRawAxis(3) * 0.65)
        

        self.robotDrive.mecanumDrive_Cartesian(multi * self.controller.getY(),multi * self.controller.getX(), -1*self.controller.getRawAxis(4), 0)

if __name__ == '__main__':
    wpilib.run(MyRobot)
