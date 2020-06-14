import png
from PIL import Image
######### Code to identify a pixel ########
img1_name = input("Enter image one name>>")
img2_name = input("Enter image two name>>")
img1 = Image.open(img1_name).convert("RGB")
w1,h1 = img1.size
print("image is ",h1,"by",w1)
img2 = Image.open(img2_name).convert("RGB")
w2,h2 = img2.size
print(img2.getpixel((50,50)))
# output will give us (255,255,255)

########### Convert each pixel from RGB to binary###################
def convert_to_binary(my_tuple):
	output = []
	for item in my_tuple:
		# keep the leading zeroes, 08b will format to 8bits
		output.append(format(item,'08b'))
	return output




############ Extracting the bits ############


def extract_front(pixel):
	output = [None,None,None]
	for i in range(3):
		output[i]=pixel[i][0:4]
	return output

# Checks
single_pixel = img2.getpixel((50,50))
pixel_binary = convert_to_binary(single_pixel)
print("single pixel",pixel_binary)
frontbits_image1 = extract_front(pixel_binary)
print('extracted',frontbits_image1)




############ Replacing last four bits for LSB steganography ############

def replace_bits(img1, img2):
	#initialize empty array 100x100
	#output_img = [[None]*100]*100
	# initialize a list of 300 pixel as png write takes in a one dimension list
	output_img = []
	# for each row
	for i in range(h1):
		row = []
		# for each pixel in column
		for j in range(w1):
			# get each pixel in binary form for both images
			# use (j,i) to get pixel, if not output will be rotated
			pixel_binary1 = convert_to_binary(img1.getpixel((j,i)))
			# to account for sizing difference
			try:
				pixel_binary2 = convert_to_binary(img2.getpixel((j,i)))
			except IndexError:
				pixel_binary2 = pixel_binary1
			# for each pixel there are 3 layers. so we need another for loop to replace the 3 RGB values
			# extract functions will give us a list
			frontbits_image1 = extract_front(pixel_binary1)
			frontbits_image2 = extract_front(pixel_binary2)
			# for each layer, combine. Convert bytes from string to bytes to int
			red_byte = frontbits_image1[0] + frontbits_image2[0]
			green_byte = frontbits_image1[1] + frontbits_image2[1]
			blue_byte = frontbits_image1[2] + frontbits_image2[2]
			#convert to int binary
			row.append(int(red_byte.encode('ascii'),2))
			row.append(int(green_byte.encode('ascii'),2))
			row.append(int(blue_byte.encode('ascii'),2))
			#print("O",convert_to_binary(img1.getpixel((i,j))))
			#print("E",frontbits_image1)
		# insert row touple
		output_img.append(row)
			
		
				
	return output_img

combined = replace_bits(img1,img2)
#print('Rows to write to png: ',len(combined),'Each row has:',len(combined[0]))

# png write takes in a flattened list isntead of a 2d list
# https://pypng.readthedocs.io/en/latest/ex.html
# [(r,g,b,r,g,b),(r,g,b,r,g,b)] a 2x2 input would look like this
with open('combined.png','wb') as f:
	w = png.Writer(w1,h1,greyscale=False)
	w.write(f,combined)


# for extraction
def extract_back(pixel):
	output = [None,None,None]
	for i in range(3):
		output[i]=pixel[i][4:8]
	return output

def extraction(img,h3,w3):
	output_img = []
	for i in range(h3):
		row = []
		# for each pixel in column
		for j in range(w3):
			# use (j,i) to get pixel, if not output will be rotated
			pixel = convert_to_binary(img.getpixel((j,i)))
			extracted_fourbits = extract_back(pixel)
			#print(extracted_fourbits)
			# We add 0000 to the back of the 4 bits
			red_byte = extracted_fourbits[0] + '0000'
			green_byte = extracted_fourbits[1] + '0000'
			blue_byte = extracted_fourbits[2] + '0000'
			row.append(int(red_byte.encode('ascii'),2))
			row.append(int(green_byte.encode('ascii'),2))
			row.append(int(blue_byte.encode('ascii'),2))
		# insert row touple
		output_img.append(row)
	
	return output_img
			
			

img3 = Image.open("combined.png").convert("RGB")
w3,h3 = img1.size
extracted_image = extraction(img3,h3,w3)

with open('extracted.png','wb') as f:
	w = png.Writer(w1,h1,greyscale=False)
	w.write(f,extracted_image)






