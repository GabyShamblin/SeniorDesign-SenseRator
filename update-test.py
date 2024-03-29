import os
import time
import open3d as o3d
import PySimpleGUI as sui
import open3d.visualization.gui as gui

import convertCloud
import windows

absolute_path = os.getcwd()
pcd_path = 'Data\pcd_files'
ply_path = 'Data\ply_files'
raw_path = 'Data\\raw_images'

# point_cloud = o3d.io.read_point_cloud(f"{pcd_path}\pcd_out_000000.pcd")
# point_cloud_name = "Scene"

# ----- Open3D -----

def unpackPCD():
	# Unpack point clouds to seperate files
	try:
		convertCloud.pcap_to_pcd("Data\car_lidar_test.pcap", "Data\car_lidar_metadata.json", pcd_dir=f"{pcd_path}\.")
	except Exception as e:
		print(e)

def unpackPLY():
	# Unpack point clouds to seperate files
	try:
		convertCloud.pcap_to_ply("Data\car_lidar_test.pcap", "Data\car_lidar_metadata.json", ply_dir=f"{ply_path}\.")
	except Exception as e:
		print(e)

# Change file directory 
def setup_depth_streaming():
	print(os.getcwd())
	os.chdir(f'{absolute_path}\{pcd_path}')

# Empty point cloud
def setup_point_clouds():
	point_cloud = o3d.geometry.PointCloud()

# Initialize window and geometry
def setup_scene():
	vis.add_geometry(point_cloud_name, point_cloud)
	vis.reset_camera_to_default()
	# vis.setup_camera(60, [4,2,5], [0,0,-1.5], [0,1,0])

# Read next point cloud 
def update_point_clouds(file_path):
	point_cloud = o3d.io.read_point_cloud(file_path)
	return point_cloud

# Put new point cloud into the scene
def update_scene():
	vis.remove_geometry(point_cloud_name)
	vis.add_geometry(point_cloud_name, point_cloud)
	print(point_cloud_name, point_cloud)
	# vis.update_geometry(point_cloud_name, point_cloud)

def run_one_tick():
	app = o3d.visualization.gui.Application.instance
	tick_return = app.run_one_tick()
	if tick_return:
		vis.post_redraw()
	return tick_return

# ----- The Meat -----

# Create point cloud window
# vis = o3d.visualization.O3DVisualizer("Vis", 1000, 700)
vis = o3d.visualization.Visualizer()
vis.create_window("Vis", 1000, 700)

# vis.add_action("Custom Options", windows.options)
# vis.add_action("Video Player", windows.mediaPlayer)

point_cloud = o3d.geometry.PointCloud()
vis.add_geometry(point_cloud)

# Read each file and update frames
try:
	setup_depth_streaming()
	# setup_point_clouds()
	# setup_scene()

	for file in os.listdir():
		if file.endswith(".pcd"):
			vis.remove_geometry(point_cloud, False)
			point_cloud = update_point_clouds(f"{os.getcwd()}\{file}")
			print("Open file", file, point_cloud)
			vis.add_geometry(point_cloud)
			# vis.update_geometry(point_cloud)
			# update_scene()
			# run_one_tick()

			vis.poll_events()
			vis.update_renderer()
			time.sleep(0.05)

except Exception as e:
	print(e)

vis.close()
vis.destroy_window()

# Normal visualizer (no skybox or menu)
# main_vis = o3d.visualization.Visualizer()
# main_vis.create_window("main_vis", 700, 500)
# main_vis.add_geometry(hotel_cloud)
# main_vis.run()
# main_vis.destroy_window()