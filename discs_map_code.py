from PIL import Image  
import pandas as pd

width = 13 
height = 26260

missing_color = (255, 255, 255, 255)
fix_color = (127, 127, 127, 255)

#helper functions
def sub_set_df(incoming_df, column_name_1, first_test, column_name_2, second_test):
	'''
	Subsets Pandas data using .loc() to isolate rows and then peform tests for two conditions: the string value of rows in two different columns.

	Inputs: Pandas dataframe, a column name to check, the condition for that column, a second column name to check, the condition for that column.
	Ouptuts: Pandas dataframe made up of targeted rows.
	'''
	outgoing_df = incoming_df.loc[(incoming_df[column_name_1] == first_test) & (incoming_df[column_name_2] == second_test)]
	return outgoing_df

def place_pixels(img_obj, data_list, index, color):
	'''
	Function used to place pixels at a specific location and with a specific color

	Inputs: PIL Image object, list of data points to be mapped to pixel rows, column index, pixel color in RGB
	Outputs: Indivdual pixels placed in a PIL image
	'''
	for item in data_list:
		img_obj.putpixel( (index, item), color )


def segment_image(img_obj, start, end, width, height, segments, label):
	'''
	Function segments a long PIL image by a user determined segment variable, which will be a constant used to
	peform floor division to divide the height of the image. The function iterates the same number of cycles as the 
	segment variable to ensure that all segments are derived.

	Inputs: PIL Image object, a start coordinate, and end coordinate, the width of the image, the height of the image, and segment number
	Ouptus: Cropped PIL Image sections, a png file written to disk and labeled with the segment number.
	'''
	
	#intialize x,y coordinates to begin at 0,0 left and 0,width right
	start_x= start
	start_y = end
	end_x = width

	#create segments by using floor division
	segments = segments
	seg_len = height//segments+1
	end_y = seg_len

	#iterate over image using segments as range
	for i in range(1,segments+1):
		#test to ensure that the segment does not exceed the height, which would cause an out of index error
		if end_y <= height:
			img_obj_cropped = img_obj.crop((start_x, start_y, end_x, end_y))
			img_obj_cropped.save(f'{label}_{i}.png')
			start_y = (i * seg_len)+1
			end_y += seg_len
		else:
			end_y = height
			img_obj_cropped = img_obj.crop((start_x, start_y, end_x, end_y))
			img_obj_cropped.save(f'{label}_{i}.png')

cc_path = 'desert_island_discs_cc.csv'
jd_path = 'desert_island_discs_jd.csv'


cc_path_df = pd.read_csv(cc_path, encoding='UTF-8')
jd_path_df = pd.read_csv(jd_path, encoding='UTF-8')


'''
Columns for discs sheet


0 - episode_ref 
1 -track_name (Jessika)
2 - trackNo 
3 - favourite (Carol)
4 - artist (Carol)
5 - disc (Carol)
6 - date 
7 - name (Carol)
8 - castaway_ref
9 - std_artist (Jessika)
10 - std_disc (Jessika)
11 - std_name (Jessika)
12 - disc_ref

'''

#subset data
track_name_missing_df = sub_set_df(jd_path_df, 'column_index', 'track_name', 'action', 'missing')
track_name_fix_df = sub_set_df(jd_path_df, 'column_index', 'track_name', 'action', 'fix')

favourite_missing_df = sub_set_df(cc_path_df, 'column_index', 'favourite', 'action', 'missing')
favourite_fix_df = sub_set_df(cc_path_df, 'column_index', 'favourite', 'action', 'fix')

artist_missing_df = sub_set_df(cc_path_df, 'column_index', 'artist', 'action', 'missing')
artist_fix_df = sub_set_df(cc_path_df, 'column_index', 'artist', 'action', 'fix')

disc_missing_df = sub_set_df(cc_path_df, 'column_index', 'disc', 'action', 'missing')
disc_fix_df = sub_set_df(cc_path_df, 'column_index', 'disc', 'action', 'fix')

name_missing_df = sub_set_df(cc_path_df, 'column_index', 'name', 'action', 'missing')
name_fix_df = sub_set_df(cc_path_df, 'column_index', 'name', 'action', 'fix')

std_artist_missing_df = sub_set_df(jd_path_df, 'column_index', 'std_artist', 'action', 'missing')
std_artist_fix_df = sub_set_df(jd_path_df, 'column_index', 'std_artist', 'action', 'fix')

std_disc_missing_df = sub_set_df(jd_path_df, 'column_index', 'std_disc', 'action', 'missing')
std_disc_fix_df = sub_set_df(jd_path_df, 'column_index', 'std_disc', 'action', 'fix')

std_name_missing_df = sub_set_df(jd_path_df, 'column_index', 'std_name', 'action', 'missing')
std_name_fix_df = sub_set_df(jd_path_df, 'column_index', 'std_name', 'action', 'fix')


#create y values
track_name_missing_y_vals = track_name_missing_df.row_index.values
track_name_fix_y_vals = track_name_fix_df.row_index.values

favourite_missing_y_vals = favourite_missing_df.row_index.values
favourite_fix_y_vals = favourite_fix_df.row_index.values

artist_missing_y_vals = artist_missing_df.row_index.values
artist_fix_y_vals = artist_fix_df.row_index.values

std_artist_missing_y_vals = std_artist_missing_df.row_index.values
std_artist_fix_y_vals = std_artist_fix_df.row_index.values

disc_missing_y_vals = disc_missing_df.row_index.values
disc_fix_y_vals = disc_fix_df.row_index.values

name_missing_y_vals = name_missing_df.row_index.values
name_fix_y_vals = name_fix_df.row_index.values

std_disc_missing_y_vals = std_disc_missing_df.row_index.values
std_disc_fix_y_vals = std_disc_fix_df.row_index.values

std_name_missing_y_vals = std_name_missing_df.row_index.values
std_name_fix_y_vals = std_name_fix_df.row_index.values

img  = Image.new( mode = "RGB", size = (width, height) )

place_pixels(img, track_name_missing_y_vals, 1, missing_color)

place_pixels(img, track_name_fix_y_vals, 1, fix_color)

place_pixels(img, favourite_missing_y_vals, 3, missing_color)

place_pixels(img, favourite_fix_y_vals, 3, fix_color)

place_pixels(img, artist_missing_y_vals, 4, missing_color)

place_pixels(img, artist_fix_y_vals, 4, fix_color)

place_pixels(img, disc_missing_y_vals, 5, missing_color)

place_pixels(img, disc_fix_y_vals, 5, fix_color)

place_pixels(img, name_missing_y_vals, 7, missing_color)

place_pixels(img, name_fix_y_vals, 7, fix_color)

place_pixels(img, std_artist_missing_y_vals, 9, missing_color)

place_pixels(img, std_artist_fix_y_vals, 9, fix_color)

place_pixels(img, std_disc_missing_y_vals, 10, missing_color)

place_pixels(img, std_disc_fix_y_vals, 10, fix_color)

place_pixels(img, std_name_missing_y_vals, 11, missing_color)

place_pixels(img, std_name_fix_y_vals, 11, fix_color)

#to color the columns for jd's project
# for i in range(height):
# 	img.putpixel( (6, i), (36, 214, 213, 50) )
# 	img.putpixel( (9, i), (36, 214, 213, 50) )
	
#to color rows for jd's project
# for j in range(width):
# 	img.putpixel( (j, 15), (36, 214, 213, 50) )


# segment_image(img, 0, 0, width, height, 40, 'Discs_data_map_part_')

img.show()






