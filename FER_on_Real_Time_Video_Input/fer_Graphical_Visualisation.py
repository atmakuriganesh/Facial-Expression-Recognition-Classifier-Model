# Let us import the Libraries required.
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

# From Module named "fer_model", Let us import the FacialExpressionModel class.
from fer_model import FacialExpressionModel

# Creating an instance of the class with the parameters as model and its weights.
test_model = FacialExpressionModel("fer_model.json", "fer_model_weights.h5")
facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Let us define a Function that does the Analysis of Emotions
def Emotion_Analysis(img):

    # Read the Image through OpenCv's imread()
    img_p = cv2.imread("C:/Users/RITCDEV01/Documents/Internships/Technocolabs/Facial-Expression-Recognition-Classifier-Model/static/predict.jpg")

    # Convert the Image into Gray Scale
    gray_fr = cv2.cvtColor(img_p, cv2.COLOR_BGR2GRAY)

    # Detect the Faces in the given Image and store it in faces.
    faces = facec.detectMultiScale(gray_fr, 1.5, 3)

    for (x, y, w, h) in faces:

        # Taking the Face part in the Image
        fc = gray_fr[y:y+h, x:x+w]  

        # Let us resize the Image and store it as Region of Interest(roi) 
        roi = cv2.resize(fc, (48, 48))
        
        # Let us make the Prediction of Emotion present in the Image
        pred_e = test_model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
        
        # Let us define text and its Font style that is to be written on Image representing the prediction
        sym={"Happy":":)","Sad":":}","Surprise":"!!","Angry":"?","Disgust":"#","Neutral":".","Fear":"~"}
        text= str(pred_e) + sym[str(pred_e)] 
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Inserting the Text on Image
        cv2.putText(img_p,text, (x, y), font, 0.7, (180,105,255), 2)

        # Finding the Coordinates and Radius of Circle
        xc = (x + x+w)/2
        yc = (y + y+h)/2
        radius = w/2  # (h/2) can also be used

        # Drawing the Circle on the Image
        cv2.circle(img_p, (int(xc),int(yc)), int(radius), (0,255,0), 2)

        # Saving the Predicted Image
        cv2.imwrite("C:/Users/RITCDEV01/Documents/Internships/Technocolabs/Facial-Expression-Recognition-Classifier-Model/static/predpredict.jpg", img_p) 

        # List of Emotions
        EMOTIONS = ["Angry", "Disgust",
                        "Fear", "Happy",
                        "Neutral", "Sad",
                        "Surprise"]

        # Finding the Probability of each Emotion
        preds= test_model.return_probabs(roi[np.newaxis, :, :, np.newaxis])
        
        # Converting into list 
        data = preds.tolist()[0]
        
        # Initializing the Figure for Bar Graph 
        fig = plt.figure(figsize = (8, 5)) 
    
        # Creating the bar plot 
        plt.bar(EMOTIONS, data, color ='green',  
                width = 0.4) 
        
        # Labelling the axes and title
        plt.xlabel("Types of Emotions") 
        plt.ylabel("Probability") 
        plt.title("Face Emotion Recognition") 

        # Saving the Bar Plot
        plt.savefig( "C:/Users/RITCDEV01/Documents/Internships/Technocolabs/Facial-Expression-Recognition-Classifier-Model/static/bar_plotpredict.jpg")       

    # returns a list containing the names of Original, Predicted, Bar Plot Images
    return ( [img, "pred"+ img , "bar_plot" + img ] )
       