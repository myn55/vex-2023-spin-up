#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 40.5, 232.5, MM, 1)
controller_1 = Controller(PRIMARY)
Flywheel = Motor(Ports.PORT6, GearSetting.RATIO_6_1, True)
Intake = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
Roller = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)



# define variables used for controlling motors based on controller inputs
controller_1_right_shoulder_control_motors_stopped = True
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, controller_1_right_shoulder_control_motors_stopped, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis1
            # right = axis3 - axis1
            drivetrain_left_side_speed = controller_1.axis3.position() + controller_1.axis1.position()
            drivetrain_right_side_speed = controller_1.axis3.position() - controller_1.axis1.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
            # check the buttonR1/buttonR2 status
            # to control Flywheel
            if controller_1.buttonR1.pressing():
                Flywheel.spin(FORWARD)
                controller_1_right_shoulder_control_motors_stopped = False
            elif controller_1.buttonR2.pressing():
                Flywheel.spin(REVERSE)
                controller_1_right_shoulder_control_motors_stopped = False
            elif not controller_1_right_shoulder_control_motors_stopped:
                Flywheel.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_1_right_shoulder_control_motors_stopped = True
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)
#endregion VEXcode Generated Robot Configuration
# Muhammad Nabil
# Thu Jan 5 2023
# TODO autonomous

from vex import *
import urandom

# Brain should be defined by default
brain=Brain()
brain_color = Color.BLUE
brain_text_color = Color.WHITE

# Robot configuration code
left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 40.5, 232.5, MM, 1)
controller_1 = Controller(PRIMARY)
Flywheel = Motor(Ports.PORT6, GearSetting.RATIO_36_1, True)
Intake = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
Roller = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)

# wait for rotation sensor to fully initialize
wait(30, MSEC)

# define variables used for controlling motors based on controller inputs
controller_1_right_shoulder_control_motors_stopped = True
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# Robot states
flywheel_active = False
intake_active = False

# Helper functions
def print_with_color(text, _color, new_line=True):
    brain.screen.set_pen_color(_color)
    brain.screen.print(text)
    brain.screen.set_pen_color(brain_text_color)
    if new_line:
        brain.screen.next_row()

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, controller_1_right_shoulder_control_motors_stopped, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis1
            # right = axis3 - axis1
            drivetrain_left_side_speed = controller_1.axis3.position() + controller_1.axis1.position()
            drivetrain_right_side_speed = controller_1.axis3.position() - controller_1.axis1.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
            # check the buttonR1/buttonR2 status
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)
#endregion VEXcode Generated Robot Configuration

def manualControl():
    # drip
    brain.screen.set_fill_color(brain_color)
    brain.screen.draw_rectangle(0, 0, 500, 500)
    brain.screen.set_pen_color(brain_text_color)
    brain.screen.print("                  2022-2023")
    brain.screen.next_row()
    brain.screen.print("  ___  ____  __ _  ____  ____   __   __    ____ ")
    brain.screen.next_row()
    brain.screen.print(" / __)(  __)(  ( \\(  __)(  _ \\ / _\\ (  )  / ___)")
    brain.screen.next_row()
    brain.screen.print("( (_ \\ ) _) /    / ) _)  )   //    \\/ (_/\\\\___ \\")
    brain.screen.next_row()
    brain.screen.print("\\___/(____)\\_)__)(____)(__\\_)\\_/\\_/\\____/(____/")
    brain.screen.next_row()
    brain.screen.print("                 Team 37458")
    brain.screen.next_row()
    brain.screen.print("       Supervised by ")
    print_with_color("Muhammad Nabil", Color.YELLOW)
    brain.screen.print("       Built by ")
    print_with_color("Muhammad Nabil", Color.YELLOW)
    brain.screen.print("       Programmed by ")
    print_with_color("Muhammad Nabil", Color.YELLOW)
    #controller_1.rumble("..-")

def handle_flywheel():
    global flywheel_active
    if flywheel_active:
        Flywheel.spin(FORWARD, 10, VOLT)
        flywheel_active = True
    else:
        Flywheel.stop()
        flywheel_active = False

def handle_intake():
    global intake_active
    if intake_active:
        Intake.spin(FORWARD, 8, VOLT)
        intake_active = True
    else:
        Intake.stop()
        intake_active = False

# system event handlers
controller_1.buttonUp.pressed(handle_flywheel)
controller_1.buttonDown.pressed(handle_intake)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

manualControl()
