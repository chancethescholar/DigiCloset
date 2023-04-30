import cv2
import math
import operator
from PIL import Image, ImageOps
from rembg import remove
import numpy as np
import mediapipe as mp
import os

def remove_background(image):
        # https://www.geeksforgeeks.org/how-to-remove-the-background-from-an-image-using-python/
        input = Image.open(image)
        input = ImageOps.exif_transpose(input)

        final_image = remove(input)

        final_image.save("no_background.png")
        input.close()

def image_to_binary(path):        
    remove_background(path)

    original_img = cv2.imread(path)
        
    # make sure images are all the same size to determine overlap later
    # will also make displaying clothing in UI easier
    original_img = cv2.resize(original_img, (700,700), interpolation = cv2.INTER_AREA)
        
    # convert image to grayscale
    gray_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    gray_img = cv2.resize(gray_img, (700,700), interpolation = cv2.INTER_AREA)

    # get a backup binary image
    _, backup_binary = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # invert binary image so that clothing is foreground (white) and background is black
    backup_binary = cv2.bitwise_not(backup_binary)



    no_bg = cv2.imread("no_background.png", cv2.IMREAD_COLOR)
        
    # make sure images are all the same size to determine overlap later
    # will also make displaying clothing in UI easier
    no_bg = cv2.resize(no_bg, (700,700), interpolation = cv2.INTER_AREA)

    # convert image to grayscale
    gray_img = cv2.imread("no_background.png", cv2.IMREAD_GRAYSCALE)
    gray_img = cv2.resize(gray_img, (700,700), interpolation = cv2.INTER_AREA)

    # get binary image
    _, binary = cv2.threshold(gray_img, 115, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # invert binary image so that clothing is foreground (white) and background is black
    #binary = cv2.bitwise_not(binary)

    #os.remove("no_background.png")

    cv2.imshow("binary", binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return original_img, no_bg, binary, backup_binary

def get_templates():
        templates = {}
        # get binary image for each of the template clothing items
        path = "Templates/TopTemplate.jpeg"
        top_img, _, top_binary, top_binary2 = image_to_binary(path)
        templates["top"] = {"image": top_img, "binary": top_binary, "binary2": top_binary2}

        path = "Templates/PantsTemplate.jpeg"
        pants_img, _, pants_binary, pants_binary2 = image_to_binary(path)
        templates["pants"] = {"image": pants_img, "binary": pants_binary, "binary2": pants_binary2}

        path = "Templates/ShoeTemplate.jpeg"
        shoe_img, _, shoe_binary, shoe_binary2 = image_to_binary(path)
        templates["shoe"] = {"image": shoe_img, "binary": shoe_binary, "binary2": shoe_binary2}

        path = "Templates/SweaterTemplate.jpeg"
        sweater_img, _, sweater_binary, sweater_binary2 = image_to_binary(path)
        templates["sweater"] = {"image": sweater_img, "binary": sweater_binary, "binary2": sweater_binary2}

        path = "Templates/DressTemplate.jpeg"
        dress_img, _, dress_binary, dress_binary2 = image_to_binary(path)
        templates["dress"] = {"image": dress_img, "binary": dress_binary, "binary2": dress_binary2}

        path = "Templates/SkirtTemplate.jpeg"
        skirt_img, _, skirt_binary, skirt_binary2 = image_to_binary(path)
        templates["skirt"] = {"image": skirt_img, "binary": skirt_binary, "binary2": skirt_binary2}

        path = "Templates/ShortsTemplate.jpeg"
        shorts_img, _, shorts_binary, shorts_binary2 = image_to_binary(path)
        templates["shorts"] = {"image": shorts_img, "binary": shorts_binary, "binary2": shorts_binary2}

        path = "Templates/JacketTemplate.jpeg"
        jacket_img, _, jacket_binary, jacket_binary2 = image_to_binary(path)
        templates["jacket"] = {"image": jacket_img, "binary": jacket_binary, "binary2": jacket_binary2}

        return templates

def get_overlap(clothing_binary, template_binary):
        #cv2.imshow("Clothing", clothing_binary)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        #cv2.imshow("Template", template_binary)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        overlap = 0
        # iterate through each pixel in the images
        for y in range(700):
            for x in range(700):
                # if both pixels are the same, then this is an overlap
                if clothing_binary[y][x] == template_binary[y][x]:
                    overlap += 1

        # get ratio of overlap to size of image
        # if ratio is over 0.7, then it is a match
        print(overlap / (700 * 700))

        ratio = overlap / (700 * 700)
        
        return ratio >= 0.68, ratio

    # https://gist.github.com/Dhruv454000/dce6491280e09ff8d920ed46fc625889
    # github gist for sharing code, helped with using contours to create convex hull
def get_convex_hull(threshold, binary2):
        #find contours
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #find contour of max area (clothing)
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
                
        #approx the contour a little
        epsilon = 0.0005 * cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
                
        #make convex hull around hand
        hull = cv2.convexHull(cnt)

        #find the defects in convex hull with respect to hand
        hull = cv2.convexHull(approx, returnPoints=False)

        try:
            defects = cv2.convexityDefects(approx, hull)

        except cv2.error as e:
            return get_convex_hull(binary2, binary2)

        # white clothing on darker background
        # in this case, the binary image will be inverted where the clothing will be 
        # thought to be the background and thus appear black
        # which causes no defects to be found in the image
        # so just invert the binary image so that the clothing is now white
        # and find the convex hull again using the inverted binary image
        if defects is None:
            threshold = cv2.bitwise_not(threshold)
            return get_convex_hull(threshold, threshold)
            
        return approx, defects, cnt, threshold

    # https://gist.github.com/Dhruv454000/dce6491280e09ff8d920ed46fc625889
    # github gist for sharing code, helped with finding defects in convex hull
    # was not knowledgeable on math behind this
def count_defects(img, thresh, defects, approx):      
        # l = no. of defects
        l = 0

        roi1 = img[:, :]
        roi2 = thresh[:, :]

        # code for finding no. of defects due to shape of clothing
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])                
                    
            # find length of all sides of triangle
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
                    
            #distance between point and convex hull
            d = (2*ar)/a

            # ignore points very close to convex hull(they generally come due to noise)
            if d > 30:
                l += 1
                cv2.circle(roi1, far, 3, [0,0,255], -1)
                cv2.circle(roi2, far, 3, [0,0,255], -1)
                    
            # draw lines around clothing
            cv2.line(roi1, start, end, [0,255,0], 2)
            cv2.line(roi2, start, end, [255,0,0], 2)

        cv2.imshow("defects", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return l

def get_defects(img, clothing_binary, clothing_binary2, count):
        approx, defects, clothing_contour, clothing_binary = get_convex_hull(clothing_binary, clothing_binary2)
        clothing_num_defects = count_defects(img, clothing_binary, defects, approx)

        #print(clothing_num_defects)
        if count == 0 and clothing_num_defects == 0:
            return get_defects(img, clothing_binary2, clothing_binary2, count+1)

        return clothing_num_defects, clothing_binary

def contour_match(clothing_num_defects, template_num_defects):
        print("defects", clothing_num_defects, template_num_defects)
        return clothing_num_defects == template_num_defects

def match_template(clothing_num_defects, clothing_binary, template_num_defects, template_binary):
        # match clothing item to top template
        # by finding overlap of binary images
        overlap, ratio = get_overlap(clothing_binary, template_binary)

        # and checking if number of contours match
        contour = contour_match(clothing_num_defects, template_num_defects)

        if (clothing_num_defects >= 6):
            return overlap, ratio
        
        return overlap and contour, ratio
    
def get_colors(img, binary):
        #cv2.imshow("binary", binary)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        clothing_colors = []

        colors = {
            #"red": (53.2, 80.1, 67.2),
            #"orange": (74.9, 23.9, 79),
            #"yellow": (84.4, 3.2, 85.4),
            #"green": (87.7, -86.2, 83.2),
            #"blue": (32.3, 79.2, -107.9),
            #"violet": (40.8, 83.1, -93.5),
            #"black": (0, 0, 0),
            #"white": (100, 0, 0)

            "red": (200, 0, 0),
            "orange": (255, 165, 0),
            "yellow": (255, 220, 100),
            "green": (1, 152, 99),
            "blue": (25,25,112),
            "light blue": (0, 0, 205),
            "purple": (128, 0, 128),
            "pink": (231, 84, 128),
            "black": (0, 0, 0),
            "burgundy": (128, 0, 32),
            "beige": (195, 176, 145),
            "brown": (101, 67, 33),
            "gray": (128, 128, 128),
            "white": (255, 255, 255)
        }

        #print(L[350][350], A[350][350], B[350][350])
        #print(img[350][350])

        #white_count = 0

        #for y in range(700):
           # for x in range(700):
              #  if int(binary[y][x] == 255):
               #     white_count += 1

        for color in colors:
            near = 0
            for y in range(700):
                for x in range(700):
                    if int(binary[y][x]) == 255:
                        distance =  math.sqrt((img[y][x][2] - colors[color][0]) ** 2 \
                                              + (img[y][x][1] - colors[color][1]) ** 2 \
                                                + (img[y][x][0] - colors[color][2]) ** 2)
                        #if color == "green":  
                        #    print(distance)
                        if distance <= 100:
                            near += 1

            print(color, near / ((700 * 700) / 2))
            if near / ((700 * 700) / 2) >= 0.4:
                clothing_colors.append(color)

        #print(white_count)
        return clothing_colors

def main():
        clothing_img, no_bg, clothing_binary, clothing_binary2 = image_to_binary("Clothing/BurgundyJacket.jpeg")
        #clothing_binary = binary.copy()

        # draw contours on copy of image, original image will be displayed in UI
        clothing_img_dup = clothing_img.copy()

        #clothing_img_dup = clothing_img.copy()

        templates = get_templates()

        clothing_num_defects, clothing_binary = get_defects(clothing_img_dup, clothing_binary, clothing_binary2, 0)

        shoe_num_defects, shoe_binary = get_defects(templates["shoe"]["image"], templates["shoe"]["binary"], templates["shoe"]["binary2"], 0)
        top_num_defects, top_binary = get_defects(templates["top"]["image"], templates["top"]["binary"], templates["top"]["binary2"], 0)
        sweater_num_defects, sweater_binary = get_defects(templates["sweater"]["image"], templates["sweater"]["binary"], templates["sweater"]["binary2"], 0)
        shorts_num_defects, shorts_binary = get_defects(templates["shorts"]["image"], templates["shorts"]["binary"], templates["shorts"]["binary2"], 0)
        pants_num_defects, pants_binary = get_defects(templates["pants"]["image"], templates["pants"]["binary"], templates["pants"]["binary2"], 0)
        skirt_num_defects, skirt_binary = get_defects(templates["skirt"]["image"], templates["skirt"]["binary"], templates["skirt"]["binary2"], 0)
        dress_num_defects, dress_binary = get_defects(templates["dress"]["image"], templates["dress"]["binary"], templates["dress"]["binary2"], 0)
        jacket_num_defects, jacket_binary = get_defects(templates["jacket"]["image"], templates["jacket"]["binary"], templates["jacket"]["binary2"], 0)

        all_overlap_ratios = {}
        shoe_is_match, shoe_ratio = match_template(clothing_num_defects, clothing_binary, shoe_num_defects, shoe_binary)
        all_overlap_ratios["Shoe"] = shoe_ratio

        top_is_match, top_ratio = match_template(clothing_num_defects, clothing_binary, top_num_defects, top_binary)
        all_overlap_ratios["Top"] = top_ratio

        sweater_is_match, sweater_ratio = match_template(clothing_num_defects, clothing_binary, sweater_num_defects, sweater_binary)
        all_overlap_ratios["Sweater"] = sweater_ratio

        shorts_is_match, shorts_ratio = match_template(clothing_num_defects, clothing_binary, shorts_num_defects, shorts_binary)
        all_overlap_ratios["Shorts"] = shorts_ratio

        pants_is_match, pants_ratio = match_template(clothing_num_defects, clothing_binary, pants_num_defects, pants_binary)
        all_overlap_ratios["Pants"] = pants_ratio

        skirt_is_match, skirt_ratio = match_template(clothing_num_defects, clothing_binary, skirt_num_defects, skirt_binary)
        all_overlap_ratios["Skirt"] = skirt_ratio

        dress_is_match, dress_ratio = match_template(clothing_num_defects, clothing_binary, dress_num_defects, dress_binary)
        all_overlap_ratios["Dress"] = dress_ratio

        jacket_is_match, jacket_ratio = match_template(clothing_num_defects, clothing_binary, jacket_num_defects, jacket_binary)
        all_overlap_ratios["Jacket"] = jacket_ratio

        match_overlap_ratios = {}

        if shoe_is_match:
            match_overlap_ratios["Shoe"] = shoe_ratio
        if top_is_match:
            match_overlap_ratios["Top"] = top_ratio
        if sweater_is_match:
            match_overlap_ratios["Sweater"] = sweater_ratio
        if jacket_is_match:
            match_overlap_ratios["Jacket"] = jacket_ratio
        if pants_is_match:
            match_overlap_ratios["Pants"] = pants_ratio
        if shorts_is_match:
            match_overlap_ratios["Shorts"] = shorts_ratio
        if skirt_is_match:
            match_overlap_ratios["Skirt"] = skirt_ratio
        if dress_is_match:
            match_overlap_ratios["Dress"] = dress_ratio

        if len(match_overlap_ratios) == 0:
            clothing_type = max(all_overlap_ratios.items(), key=operator.itemgetter(1))[0]

        else:
            clothing_type = max(match_overlap_ratios.items(), key=operator.itemgetter(1))[0]

        colors = get_colors(clothing_img, clothing_binary)

        print(clothing_type)
        print(colors)


if __name__ == "__main__":
    main()