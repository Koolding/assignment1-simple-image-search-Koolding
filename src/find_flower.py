# flowers.zip is unzipped beforehand from terminal using "unzip flowers.zip"
import os
import pandas as pd
import cv2

def load_img(filename = str): # loading a test image 
    folder = os.path.join("..", "data", "flowers") # defining filepath for all images
    filepath = os.path.join(folder, filename) # defining specific filepath
    test_image = cv2.imread(filepath) # loading the image file
    return test_image, folder

def processing(test_image): # creating histogram of test image values
    hist1 = cv2.calcHist([test_image], [0,1,2], None, [8,8,8], [0,256, 0,256, 0,256]) # creating histogram with small bins
    hist1 = cv2.normalize(hist1, hist1, 0, 1.0, cv2.NORM_MINMAX) # normalizing the histogram
    return hist1

def find_flower(hist1, folder): # finding similar pictures
    results = [] # creating empty results object
    images = os.listdir(folder) # treating the folder as a list

    for image in images: # for every image file in the folder, do the following:
        if image.endswith(".jpg"): # ensuring only the images are processed
            picture = cv2.imread(os.path.join(folder, image)) # loading the image for each loop
            hist2 = cv2.calcHist([picture], [0,1,2], None, [8,8,8], [0,256, 0,256, 0,256]) # creating hist with small bins
            hist2 = cv2.normalize(hist2, hist2, 0, 1.0, cv2.NORM_MINMAX) # normalizing hist
            distance = round(cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR), 2) # comparing hist1 and hist2
            if distance != 0.0: # if hist2 is not identical to hist1, do the following:
                result = (image, distance) # make a tupe result of result and name
                results.append(result) # and append to the results list
    
    results.sort(key = lambda x: x[1]) # sorting the results, ascending, by contents of second column
    df = pd.DataFrame(results[:5]) # make dataframe from 5 closest images
    df.columns = ["Filename", "Distance"] # naming dataframe columns
    return df # return dataframe with first five elements

def save_results(df): # saving the results 
    outpath = os.path.join("..","out","image_search_" + filename[6:10] + ".csv") # defining .cvs outpath
    df.to_csv(outpath) # saving dataframe as .cvs
    return None 

def main():
    test_img, img_dir = load_img("image_0011.jpg") # loading a test image and defining the image directory
    histogram = processing(test_img) # creating histogram of test image values
    dataframe = find_flower(histogram, img_dir) # creating dataframe of the 5 images with most similar histograms
    save_results(dataframe) # saving the results in the out folder
    return None

if __name__ == "__main__":
    main()