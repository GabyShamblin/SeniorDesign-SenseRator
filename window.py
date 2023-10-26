import os
import time
import open3d as o3d
import open3d.visualization.gui as gui
import PySimpleGUI as sui
import convertCloud
import convertImage
# import vlc

print("Animated point cloud test")

app = o3d.visualization.gui.Application.instance
app.initialize()

path = r".\Data\pcd_files"

# Unpack point clouds to seperate files
# try:
# 	convertCloud.pcap_to_pcd("Data\car_lidar_test.pcap", "Data\car_lidar_metadata.json", pcd_dir=f"{path}\.")
# except Exception as e:
# 	print(e)

# point_cloud = o3d.io.read_point_cloud(f"{path}\pcd_out_000000.pcd")
point_cloud = o3d.geometry.PointCloud()
point_cloud_name = "Scene"
# hotel_cloud = o3d.io.read_point_cloud("Hotel.ply")
# player = vlc.MediaPlayer()

# ----- SimpleUI -----

def ImageButton(title, key):
	return sui.Button(title, border_width=0, key=key)

# For SimpleUI
layout = [[sui.Text("This is a settings menu")],
					[sui.Text("Movement Mode"), sui.Combo(['Fly', 'Model', 'Sun', 'Editing'], 'Fly', enable_events=True), sui.Button('Reset Camera', enable_events=True)],
					[sui.Text("Show Skybox"), sui.Checkbox('', True, s=(3,3), enable_events=True)],
					[sui.Text("Point Size"), sui.Slider((1,10), 3, 1, orientation='h', enable_events=True)],
					[sui.Text("Shader"), sui.Combo(['Standard', 'Unlit', 'Normals', 'Depth'], 'Standard', enable_events=True)],
					[sui.Text("Lighting ???")],
					[sui.Text(key='-UPDATE-')],
					[sui.Submit(), sui.Cancel()]]

mediaLayout = [[sui.Text('Media File Player')],
							 [sui.Text('', size=(15,2), key='-OUTPUT-')],
							 [ImageButton('restart', key='-RESTART-'), 
							  ImageButton('pause', key='-PAUSE-'),
								ImageButton('next', key='-NEXT-'),
								ImageButton('exit', key='-EXIT-')]]

# Show test options window
def simpleui(vis):
	window = sui.Window("More Options", layout)

	while True:
		event, values = window.read()
		print(event, values)
		try:
			if event == sui.WIN_CLOSED or event == 'Cancel':
				break
			elif event == 'Submit':
				window['-UPDATE-'].update('Saved')
			elif event == 'Reset Camera':
				vis.reset_camera_to_default()
				window['-UPDATE-'].update('Reset camera')
			elif event == 0:
				if values[0] == 'Fly': vis.mouse_mode = gui.SceneWidget.Controls.FLY
				elif values[0] == 'Model': vis.mouse_mode = gui.SceneWidget.Controls.ROTATE_MODEL
				elif values[0] == 'Sun': vis.mouse_mode = gui.SceneWidget.Controls.ROTATE_SUN
				elif values[0] == 'Editing': vis.mouse_mode = gui.SceneWidget.Controls.PICK_POINTS
				else: vis.mouse_mode = gui.SceneWidget.Controls.FLY
				window['-UPDATE-'].update('Updated mouse_mode')
			elif event == 1:
				vis.show_skybox(values[1])
				window['-UPDATE-'].update('Updated show_skybox()')
			elif event == 2:
				vis.point_size = int(values[2])
				window['-UPDATE-'].update('Updated point_size')
			elif event == 3:
				if values[3] == 'Standard': vis.scene_shader = vis.STANDARD
				elif values[3] == 'Unlit': vis.scene_shader = vis.UNLIT
				elif values[3] == 'Normals': vis.scene_shader = vis.NORMALS
				elif values[3] == 'Depth': vis.scene_shader = vis.DEPTH
				else: vis.scene_shader = vis.STANDARD
				window['-UPDATE-'].update('Updated scene_shader')
		except:
			print('Something went wrong')

	window.close()

# Video player window
def mediaPlayer(vis):
	window = sui.Window("Video Player", mediaLayout);

	while True:
		event, values = window.read()
		try:
			if event == sui.WIN_CLOSED or event == 'Exit':
				break
			if event != sui.TIMEOUT_KEY:
				window['-OUTPUT-'].update(event)
		except:
			print("Something went wrong")

	window.close()

# ----- Open3D -----

def setup_depth_streaming():
	# Change file directory 
	os.chdir(path)

def setup_point_clouds():
	point_cloud = o3d.geometry.PointCloud()

def setup_scene():
	vis.add_geometry(point_cloud_name, point_cloud)
	vis.reset_camera_to_default()
	# vis.setup_camera(60, [4,2,5], [0,0,-1.5], [0,1,0])

def update_point_clouds(file_path):
	point_cloud = o3d.io.read_point_cloud(file_path)

def update_scene():
	vis.remove_geometry(point_cloud_name)
	vis.add_geometry(point_cloud_name, point_cloud)

def run_one_tick():
	app = o3d.visualization.gui.Application.instance
	tick_return = app.run_one_tick()
	if tick_return:
		vis.post_redraw()
	return tick_return

# Create point cloud window
vis = o3d.visualization.O3DVisualizer("O3DVis", 1000, 700)
vis.add_action("Custom Options", simpleui)
vis.add_action("Video Player", mediaPlayer)

# Show window
app.add_window(vis)

# Read each file and update frames
try:
	setup_depth_streaming()
	setup_point_clouds()
	setup_scene()

	for file in os.listdir():
		if file.endswith(".pcd"):
			# FILE WONT OPEN ??? -------------------------------------------------------
			update_point_clouds(f"{os.getcwd()}\{file}")
			update_scene()
			run_one_tick()
			print("Open file", file, point_cloud)
			time.sleep(1)
except Exception as e:
	print(e)

# app.run()

# --- Events --- 
# 0: mouse_mode = out
# 1: vis.show_skybox(out)
# 2: point_size = out
# 3: scene_shader = out
# Reset Camera: vis.reset_camera_to_default()

# --- Automated actions ---
# Add/clear 3d label
# Add/get/remove/update geometry
# Animation stuff

# --- User actions ---
# Export current image
# Mouse mode (movement)
# Show skybox
# Point size
# Scene shader
# Lighting?
# Selecting (if time)

# For video: https://www.pysimplegui.org/en/latest/Demos/#demo_media_playerpy
# For lidar: http://www.open3d.org/docs/latest/python_api/open3d.visualization.O3DVisualizer.htmls

# Normal visualizer (no skybox or menu)
# main_vis = o3d.visualization.Visualizer()
# main_vis.create_window("main_vis", 700, 500)
# main_vis.add_geometry(hotel_cloud)
# main_vis.run()
# main_vis.destroy_window()