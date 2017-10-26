#!/usr/bin/env python3
'''
"Wall-E" Team 4480 Robot Code for the FRC 2017 Competition "Steamworks"
Written by Brandon Young and Kennedy Allen for Team 4480 UCBotics
'''
import wpilib
from wpilib import RobotDrive
import wpilib.buttons
from robotpy_ext.autonomous import AutonomousModeSelector
from robotpy_ext.common_drivers import units, navx
from networktables import NetworkTable
import networktables

class MyRobot(wpilib.IterativeRobot):


    rLeftChannel = 1
    fLeftChannel = 2
    fRightChannel = 3
    rRightChannel = 4
    joystickChannel = 0
    
    
    def robotInit(self):
       

        if not wpilib.RobotBase.isSimulation():#This makes simulator show motor outputs for debugging
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


        wpilib.CameraServer.launch() #Goto 10.44.80.2:1181 to view the cameras without HTML page


        self.robotDrive = wpilib.RobotDrive(self.FLC, self.RLC, self.FRC, self.RRC)#Sets motors for robotDrive commands
        self.robotDrive.setInvertedMotor(RobotDrive.MotorType.kFrontLeft, True)
        self.robotDrive.setInvertedMotor(RobotDrive.MotorType.kRearLeft, True)


        #Controller Input Variables
        self.controller = wpilib.Joystick(self.joystickChannel)
        self.winch_backward = wpilib.buttons.JoystickButton(self.controller, 5)
        self.paddleGet = wpilib.buttons.JoystickButton(self.controller, 1)
        self.gearDrop = wpilib.buttons.JoystickButton(self.controller, 6) # Right Bumper
        self.xboxMec = wpilib.buttons.JoystickButton(self.controller, 8)
        self.xboxMec2 = wpilib.buttons.JoystickButton(self.controller, 7)
        
        
        #CRio Output Variables
        self.winch_motor1 = wpilib.Talon(7)
        self.winch_motor2 = wpilib.Talon(8)
        self.paddle = wpilib.Solenoid(1)
        self.gear = wpilib.DoubleSolenoid(2,3)
        self.ultrasonic = wpilib.Ultrasonic(5, 4) #trigger to echo
        self.ultrasonic.setAutomaticMode(True)
        
        
        #Auto mode variables
        self.components = {
            'drive': self.robotDrive,
            'gearDrop': self.gear,
            'ultrasonic': self.ultrasonic
        }
        self.automodes = AutonomousModeSelector('autonomous', self.components)


    def autonomousPeriodic(self):
        self.automodes.run()
    
    
    def teleopPeriodic(self):
        
        
        ###  Climing code
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
    
    
        ### Paddle/flipper assist code
        if (self.paddleGet.get()):
            self.paddle.set(True)
        else:
            self.paddle.set(False)


        ### Gear dropping code
        if (self.gearDrop.get()):
            self.gear.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.gear.set(wpilib.DoubleSolenoid.Value.kReverse)


        #RobotDrive Code
        self.robotDrive.mecanumDrive_Cartesian(self.controller.getY(),self.controller.getX(), -1*self.controller.getRawAxis(4), 0)


if __name__ == '__main__':
    wpilib.run(MyRobot)


# NOTES SECTION:
# This note section is to declutter the real code. Put each component that is being quarentined into it's respective def designations.
'''
    
    def autonomousPeriodic(self):
        #self.navx.reset()


    def robotInit(self):
        #self.winch_forward = wpilib.buttons.JoystickButton(self.controller, 6)
        #self.closeGear = wpilib.buttons.JoystickButton(self.controller, 4)
        #self.navx = navx.AHRS.create_spi()
        #self.dm = 1
        

    def updater(self):
        #   self.robotStats.putBoolean('GEAR', self.switch.get())
        #self.robotStats.putNumber('F1', self.ultrasonic.getRangeInches())
        #   self.robotStats.putNumber('PSI', self.psiSensor.getVoltage())
        pass
        
        
    def teleopPeriodic(self):
    ###This is the switching drive modes logic code#####
        #if self.xboxMec.get():
        #   self.dm = 1
        #if self.xboxMec2.get():
        #  self.dm = 2
        #   if self.dm == 1:
        
        #  if self.dm == 2:
        #     self.robotDrive.mecanumDrive_Cartesian(self.controller.getY(), self.controller.getRawx(4), -1*self.controller.getRawX(), 0)
        
        
        
        multi = 0.35 + (self.controller.getRawAxis(3) * 0.65)
        
        
        self.robotDrive.mecanumDrive_Cartesian(multi * self.controller.getY(),multi * self.controller.getX(), -1*self.controller.getRawAxis(4), 0)


    def disabledPeriodic(self):
        self.updater()
    
    



'''
