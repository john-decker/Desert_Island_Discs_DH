from PIL import Image  
import pandas as pd

#Sublime users, be sure to activate the conda environment in the command palette

width = 15 
height = 3218

missing_color = (255, 255, 255, 255)
fix_color = (127, 127, 127, 255)


#helper functions

#subset the data
def sub_set_df(incoming_df, column_name_1, first_test, column_name_2, second_test):
	'''
	Subsets Pandas data using .loc() to isolate rows and then peform tests for two conditions: the string value of rows in two different columns.

	Inputs: Pandas dataframe, a column name to check, the condition for that column, a second column name to check, the condition for that column.
	Ouptuts: Pandas dataframe made up of targeted rows.
	'''
	outgoing_df = incoming_df.loc[(incoming_df[column_name_1] == first_test) & (incoming_df[column_name_2] == second_test)]
	return outgoing_df

#place pixels in the image
def place_pixels(img_obj, data_list, index, color):
	'''
	Function used to place pixels at a specific location and with a specific color

	Inputs: PIL Image object, list of data points to be mapped to pixel rows, column index, pixel color in RGB
	Outputs: Indivdual pixels placed in a PIL image
	'''
	for item in data_list:
		img_obj.putpixel( (index, item), color )


#cut complete image into segments for processing and printing
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

#calculate various width and height measures for data
def calculate_size(pixel_width, pixel_height):
	'''
	function that takes in pixel measurements and returns mm, cm, in, and ft measurements
	pixel to cm value from http://www.endmemo.com/sconvert/millimeterpixel.php#:~:text=%C2%BB%20Millimeter%20Conversions%3A&text=mm%E2%86%94Pixel%201%20mm%20%3D%203.779528%20Pixel
	mm to cm, inch, and foot values from https://www.unitconverters.net/

	Input: number of pixels for width of image, number of pixels for height of image
	Output: a list of tuples containing the converted width and height as well as a string for the specific measurement type (e.g. 'mm')
	'''
	measurements = []

	#create helper function to convert from pixels to mm
	def pixel_to_mm(num_pixels):
		mm_conversion = num_pixels * 0.264583
		return mm_conversion

	#create helper function to convert from mm to cm
	def mm_to_cm(mm_measurement):
		cm_conversion = mm_measurement * 0.1
		return cm_conversion

	#create helper function to convert from mm to inches
	def mm_to_inch(mm_measurement):
		inch_conversion = mm_measurement * 0.0393700787
		return inch_conversion

	#create helper function to convert from mm to feet
	def inch_to_foot(inch_measurement):
		foot_conversion = inch_measurement * 0.0833333333
		return foot_conversion

	width_mm = pixel_to_mm(pixel_width)
	height_mm = pixel_to_mm(pixel_height)
	measurements.append((width_mm, height_mm, 'mm'))

	width_cm = mm_to_cm(width_mm)
	height_cm = mm_to_cm(height_mm)
	measurements.append((width_cm, height_cm, 'cm'))

	width_inch = mm_to_inch(width_mm)
	height_inch = mm_to_inch(height_mm)
	measurements.append((width_inch, height_inch, 'in'))

	width_foot = inch_to_foot(width_inch)
	height_foot = inch_to_foot(height_inch)
	measurements.append((width_foot, height_foot, 'ft'))

	return measurements

#calculate scaled measurements for width and height of data
'''
A function that scales converted pixel measurements 

Input: list of measurements and a scaling factor
Output: a printed string message with scaled conversions
'''
def get_scaled_size(measurement_list, scale_factor):
	print(f'Scaled Width| Scaled Height')
	print('-' * 30)
	for item in measurement_list:
		print(f'{round((item[0]*scale_factor),2)} {item[2]} | {round((item[1]*scale_factor),2)} {item[2]})')

#color columns for key
def column_key(image_obj, column_list, color_tuple, length_range):
	for column in column_list:
		for i in range(length_range):
			image_obj.putpixel( (column, i), (color_tuple) )


# convert initial pixel measurements to mm, cm, in, and ft
base_measure = calculate_size(width, height)

#print the output
#the output can be used to create other examples of width or height (i.e. a string or ribbon instead of the printed image)
get_scaled_size(base_measure, 15)

#comparing desert island extent with that of a much larger data set
print('\nComaprison Data\nhttps://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh')
comparison_measure = calculate_size(45, 648000)
get_scaled_size(comparison_measure, 15)

#imort data
lm_path = 'desert_island_discs_lm.csv'
ak_path = 'desert_island_discs_ak.csv'


lm_paths_df = pd.read_csv(lm_path, encoding='UTF-8')
ak_paths_df = pd.read_csv(ak_path, encoding='UTF-8')

'''
0 - episode_ref
1 - date
2 - castaway_ref

column index conversions for ak
3 - name
4 - std_name
5 - gender
6 - profession

column index conversions for lm
7 - country_of_citizenship
8 - place_of_birth
10 - date_of_birth
11 - favTrack
12 - luxury
13 - book

14 - wiki_link
15 - link
'''



#subset data
name_missing_df = sub_set_df(ak_paths_df, 'column_index', 'name', 'action', 'missing')
name_fix_df = sub_set_df(ak_paths_df, 'column_index', 'name', 'action', 'fix')

std_name_missing_df = sub_set_df(ak_paths_df, 'column_index', 'std_name', 'action', 'missing')
std_name_fix_df = sub_set_df(ak_paths_df, 'column_index', 'std_name', 'action', 'fix')

gender_missing_df = sub_set_df(ak_paths_df, 'column_index', 'gender', 'action', 'missing')
gender_fix_df = sub_set_df(ak_paths_df, 'column_index', 'gender', 'action', 'fix')

profession_missing_df = sub_set_df(ak_paths_df, 'column_index', 'profession', 'action', 'missing')
profession_fix_df = sub_set_df(ak_paths_df, 'column_index', 'profession', 'action', 'fix')

country_of_citizenship_missing_df = sub_set_df(lm_paths_df, 'column_index', 'country_of_citizenship', 'action', 'missing')
country_of_citizenship_fix_df = sub_set_df(lm_paths_df, 'column_index', 'country_of_citizenship', 'action', 'fix')

place_of_birth_missing_df = sub_set_df(lm_paths_df, 'column_index', 'place_of_birth', 'action', 'missing')
place_of_birth_fix_df = sub_set_df(lm_paths_df, 'column_index', 'place_of_birth', 'action', 'fix')

date_of_birth_missing_df = sub_set_df(lm_paths_df, 'column_index', 'date_of_birth', 'action', 'missing')
date_of_birth_fix_df = sub_set_df(lm_paths_df, 'column_index', 'date_of_birth', 'action', 'fix')

favTrack_missing_df = sub_set_df(lm_paths_df, 'column_index', 'favTrack', 'action', 'missing')
favTrack_fix_df = sub_set_df(lm_paths_df, 'column_index', 'favTrack', 'action', 'fix')

luxury_missing_df = sub_set_df(lm_paths_df, 'column_index', 'luxury', 'action', 'missing')
luxury_fix_df = sub_set_df(lm_paths_df, 'column_index', 'luxury', 'action', 'fix')

book_missing_df = sub_set_df(lm_paths_df, 'column_index', 'book', 'action', 'missing')
book_fix_df = sub_set_df(lm_paths_df, 'column_index', 'book', 'action', 'fix')


# #create y values 
name_missing_y_vals = name_missing_df.row_index.values
name_fix_y_vals = name_fix_df.row_index.values

std_name_missing_y_vals = std_name_missing_df.row_index.values
std_name_fix_y_vals = std_name_fix_df.row_index.values

gender_missing_y_vals = std_name_missing_df.row_index.values
gender_fix_y_vals = std_name_fix_df.row_index.values

profession_missing_y_vals = std_name_missing_df.row_index.values
profession_fix_y_vals = std_name_fix_df.row_index.values

country_of_citizenship_missing_y_vals = country_of_citizenship_missing_df.row_index.values
country_of_citizenship_fix_y_vals = country_of_citizenship_fix_df.row_index.values

place_of_birth_missing_y_vals = place_of_birth_missing_df.row_index.values
place_of_birth_fix_y_vals = place_of_birth_fix_df.row_index.values

date_of_birth_missing_y_vals = date_of_birth_missing_df.row_index.values
date_of_birth_fix_y_vals = date_of_birth_fix_df.row_index.values

favTrack_missing_y_vals = favTrack_missing_df.row_index.values
favTrack_fix_y_vals = favTrack_fix_df.row_index.values

luxury_missing_y_vals = luxury_missing_df.row_index.values
luxury_fix_y_vals = luxury_fix_df.row_index.values

book_missing_y_vals = book_missing_df.row_index.values
book_fix_y_vals = book_fix_df.row_index.values


#Castaways Data

#for Weights Sheet
# fix_color = (22, 166, 37, 50)

img  = Image.new( mode = "RGB", size = (width, height) )

place_pixels(img, name_missing_y_vals, 3, missing_color)

place_pixels(img, name_fix_y_vals, 3, fix_color)

place_pixels(img, std_name_missing_y_vals, 4, missing_color)

place_pixels(img, std_name_fix_y_vals, 4, fix_color)

place_pixels(img, gender_missing_y_vals, 5, missing_color)

place_pixels(img, gender_fix_y_vals, 5, fix_color)

place_pixels(img, profession_missing_y_vals, 6, missing_color)

place_pixels(img, profession_fix_y_vals, 6, fix_color)

place_pixels(img, country_of_citizenship_missing_y_vals, 7, missing_color)

place_pixels(img, country_of_citizenship_fix_y_vals, 7, fix_color)

place_pixels(img, place_of_birth_missing_y_vals, 9, missing_color)

place_pixels(img, place_of_birth_fix_y_vals, 9, fix_color)

place_pixels(img, date_of_birth_missing_y_vals, 10, missing_color)

place_pixels(img, date_of_birth_fix_y_vals, 10, fix_color)

place_pixels(img, favTrack_missing_y_vals, 11, missing_color)

place_pixels(img, favTrack_fix_y_vals, 11, fix_color)

place_pixels(img, luxury_missing_y_vals, 12, missing_color)

place_pixels(img, luxury_fix_y_vals, 12, fix_color)

place_pixels(img, book_missing_y_vals, 13, missing_color)

place_pixels(img, book_fix_y_vals, 13, fix_color)



# music_project_columns = [1,3,10]
# music_project_color = (56, 175, 245, 50)

# column_key(img, music_project_columns, music_project_color, height)


# segment_image(img, 0, 0, width, height, 9, 'Castaways_data_map_colored_part_')

# img = img.crop((0,0, 15,500))


# img.save('Castaways_data_map.png')
# img = img.resize((170,32190), resample=3)
# img.save('Castaways_data_map_larger.png')

img.show()

