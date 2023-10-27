import os
import time
from PIL import Image
from io import BytesIO
import PySimpleGUI as sui
from matplotlib import pyplot as plt

import convertImage

raw_path = 'Data\\raw_images'
abs_path = ''
frames = []
resize = (789,592)

def ImageButton(title, key):
	return sui.Button(title, border_width=0, key=key)

optionsLayout = [[sui.Text("This is a settings menu")],
					[sui.Text("Movement Mode"), sui.Combo(['Fly', 'Model', 'Sun', 'Editing'], 'Fly', enable_events=True), sui.Button('Reset Camera', enable_events=True)],
					[sui.Text("Show Skybox"), sui.Checkbox('', True, s=(3,3), enable_events=True)],
					[sui.Text("Point Size"), sui.Slider((1,10), 3, 1, orientation='h', enable_events=True)],
					[sui.Text("Shader"), sui.Combo(['Standard', 'Unlit', 'Normals', 'Depth'], 'Standard', enable_events=True)],
					[sui.Text("Lighting ???")],
					[sui.Text(key='-UPDATE-')],
					[sui.Submit(), sui.Cancel()]]

mediaLayout = [[sui.Text('Media File Player')],
							 [sui.Graph(canvas_size=resize, 
							 						graph_bottom_left=(0,0),
													graph_top_right=resize, 
													background_color='black', key='-VIDEO-')],
							 [sui.Text('', size=(15,2), key='-OUTPUT-')],
							 [ImageButton('Restart', key='-RESTART-'), 
							  ImageButton('Pause', key='-PAUSE-'),
								ImageButton('Play', key='-PLAY-'),
								ImageButton('Exit', key='-EXIT-')]]

# Options window
def options(vis):
	window = sui.Window("More Options", optionsLayout, finalize=True)

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
		except Exception as e:
			print(e)

	window.close()

def array_to_data(array):
	im = Image.fromarray(array)
	with BytesIO() as output:
		im.save(output, format='PNG')
		data = output.getvalue()
	return data

# Video player window
def mediaPlayer(vis = None):
	window = sui.Window("Video Player", mediaLayout, finalize=True, element_justification='center');
	os.chdir(raw_path)
	frames = os.listdir()
	abs_path = os.getcwd()
	# os.chdir('..\..')

	# image = convertImage.grayscale(f'{os.getcwd()}\\16_11_32_266.raw', resize)
	# print(image)
	# window['-VIDEO-'].draw_image(data=array_to_data(image), location=(0,resize[1]))

	# ADD THREADING SO VIDEO CAN PLAY AND WINDOW CAN UPDATE WHILE ALSO WAITING FOR EVENTS

	while True:

		for file in frames:
			if file.endswith(".raw"):
				
				event, values = window.read()
				print("Event", event)

				image = convertImage.grayscale(f'{os.getcwd()}\{file}', resize)
				print(file)
				window['-VIDEO-'].draw_image(data=array_to_data(image), location=(0,resize[1]))
				time.sleep(0.17)

				try:
					if event == sui.WIN_CLOSED or event == 'Exit':
						break
					if event != sui.TIMEOUT_KEY:
						window['-OUTPUT-'].update(event)
					# if event == '-PLAY-':
					# 	video(window, frames, abs_path)
				except Exception as e:
					print(e)

	window.close()

# Grab video frames
def video(window, frames=[], abs_path=''):
	for file in frames:
		if file.endswith(".raw"):
			image = convertImage.grayscale(f'{abs_path}\{file}', resize)
			print(file)
			window['-VIDEO-'].draw_image(data=array_to_data(image), location=(0,resize[1]))
			time.sleep(0.17)

mediaPlayer()