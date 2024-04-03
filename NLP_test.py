"""
The script is used for multiple destination test.
"""

import EIdrive.scenario_testing.utils.sim_api as sim_api
from EIdrive.scenario_testing.utils.keyboard_listener import KeyListener
from EIdrive.scenario_testing.utils.spectator_api import SpectatorController
import sys
import os
import random


player_ids = []


def run_scenario(scenario_params):
    try:
        y_combo = [26.6, 30.0, 33.6, 37.1]
        x_combo = [-280.0, -286.0]
        record_data = True

        if os.path.exists("NLP dataset.txt") and record_data:
            open("NLP dataset.txt", "w").close()

        # Create game world
        gameworld = sim_api.GameWorld(scenario_params, map_name='town04')

        for i in range(847, 1200):
            random.seed(i)
            random_y = random.choice(y_combo)
            print(random_y)
            scenario_params.scenario.vehicle_list[0].spawn_position[1] = random_y  # ego
            scenario_params.scenario.vehicle_list[1].spawn_position[1] = random_y
            scenario_params.scenario.vehicle_list[2].spawn_position[0] = random.uniform(-280.0, -276.0)
            scenario_params.scenario.vehicle_list[2].spawn_position[1] = random.choice(y_combo)
            scenario_params.scenario.vehicle_list[3].spawn_position[0] = random.uniform(-260.0, -256.0)
            scenario_params.scenario.vehicle_list[3].spawn_position[1] = random.choice(y_combo)

            vehicle_list = gameworld.create_vehicle_agent()

            spectator = gameworld.world.get_spectator()

            # Keyboard listener
            t = 0
            kl = KeyListener()
            kl.start()

            spec_controller = SpectatorController(spectator)

            vehicle_list[1].stop_mode = True
            vehicle_list[2].stop_mode = True
            vehicle_list[3].stop_mode = True

            if record_data:
                with open("NLP dataset.txt", "a") as file:  # Open the file for writing
                    # Assuming you have obstacle information
                    file.write(f"{i}\n")
                    obstacle_location = vehicle_list[1].vehicle.get_transform().location
                    coord = f"({obstacle_location.x:.1f}, {obstacle_location.y:.1f})"
                    obstacle_width = vehicle_list[1].vehicle.bounding_box.extent.y * 2
                    obstacle_length = vehicle_list[1].vehicle.bounding_box.extent.x * 2
                    file.write(
                        f"Obstacle:\ncar_1 at {coord}, with width of {obstacle_width:.1f} and length of {obstacle_length:.1f}.\n")
                    obstacle_location = vehicle_list[2].vehicle.get_transform().location
                    coord = f"({obstacle_location.x:.1f}, {obstacle_location.y:.1f})"
                    obstacle_width = vehicle_list[2].vehicle.bounding_box.extent.y * 2
                    obstacle_length = vehicle_list[2].vehicle.bounding_box.extent.x * 2
                    file.write(
                        f"car_2 at {coord}, with width of {obstacle_width:.1f} and length of {obstacle_length:.1f}.\n")
                    obstacle_location = vehicle_list[3].vehicle.get_transform().location
                    coord = f"({obstacle_location.x:.1f}, {obstacle_location.y:.1f})"
                    obstacle_width = vehicle_list[3].vehicle.bounding_box.extent.y * 2
                    obstacle_length = vehicle_list[3].vehicle.bounding_box.extent.x * 2
                    file.write(
                        f"car_3 at {coord}, with width of {obstacle_width:.1f} and length of {obstacle_length:.1f}.\n\n")
                    file.write("ego vehicle trajectory:\n")

            while True:
                # Pause and exit
                if kl.keys['esc']:
                    exit(0)
                if kl.keys['p']:
                    continue

                gameworld.tick()

                for vehicle_agent in vehicle_list:
                    vehicle_agent.update_info()
                    sim_api.gamemap_visualize(vehicle_agent)
                    control = sim_api.calculate_control(vehicle_agent)
                    vehicle_agent.vehicle.apply_control(control)

                spec_controller.bird_view_following(vehicle_list[0].vehicle.get_transform())

                if t % 30 == 0 and record_data:
                    with open("NLP dataset.txt", "a") as file:
                        ego_location = vehicle_list[0].vehicle.get_transform().location  # Replace with actual location retrieval logic
                        coord = f"({ego_location.x:.1f}, {ego_location.y:.1f})"
                        file.write(f"{coord}, ")

                t = t + 1

                if (vehicle_list[0].vehicle.get_transform().location.x > -250.0 or t > 400):    # Ending condition
                    if record_data:
                        with open("NLP dataset.txt", "a") as file:
                            file.write(f"\n\n")
                    for vehicle in vehicle_list:
                        vehicle.destroy()
                    print("Destroy all vehicles")
                    break

    finally:
        if gameworld is not None:
            gameworld.close()
        print("Destroyed gameworld")
