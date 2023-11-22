from GUI import GUI
from HAL import HAL

victims_x_position = 30
victims_y_position = -40
victims_region_threshold = 1

boat_x_position = 0
boat_y_position = 0

angle = 0.6

n_victims = 6
finish = False

drone_position = HAL.get_position()
print("Ready")

HAL.takeoff(3)

def in_survivors_zone():
    return victims_x_position - victims_region_threshold < drone_position[0] \
      and drone_position[0] < victims_x_position + victims_region_threshold \
      and victims_y_position - victims_region_threshold < drone_position[1] \
      and drone_position[1] < victims_y_position + victims_region_threshold
    
    

def drone_above_the_boat():
  return False


while True:
    GUI.showImage(HAL.get_frontal_image())
    GUI.showLeftImage(HAL.get_ventral_image())
    drone_position = HAL.get_position()

    if not finish:
        if n_victims == 0:
            print("Returning to boat position")
            HAL.set_cmd_pos(boat_x_position, boat_y_position, 3, angle)
            
        if n_victims == 0 and drone_above_the_boat():
            print("Landing")
            HAL.land()
            finish = True
            
        elif not in_survivors_zone():
            # Go to survivors zone
            print("Looking for survivors position")
            HAL.set_cmd_pos(victims_x_position, victims_y_position, 3, angle)
        else:
            # Search_survivors
            print("In position")
            
        # print("Drone position: {}".format(drone_position))