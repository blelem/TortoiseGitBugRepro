"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
import Alignment2D

import cv2
import os
from django.conf import settings
from django.conf.urls.static import static
import uuid
import numpy as np
from app.models import InputImages 

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def matchFeatures(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)


    img1 = cv2.imread(InputImages.objects.all()[1].image_1.path,cv2.CV_LOAD_IMAGE_COLOR)
    img2 = cv2.imread(InputImages.objects.all()[1].image_2.path,cv2.CV_LOAD_IMAGE_COLOR)
   
    (kp1Matches, kp2Matches) = Alignment2D.SetupTheStuff(img1,img2)
    Transform = Alignment2D.LinearLeastSquare(kp1Matches, kp2Matches) 
	#Transform = Alignment2D.Levenberg(kp1Matches, kp2Matches) 

    #Overlay the two images, showing the detected feature.
    rows,cols,colours = img1.shape
    Canvas1 = np.zeros((rows * 2, cols * 2, colours) , img1.dtype)
    Canvas2 = np.copy(Canvas1)

    finalRows, finalCols, colours = Canvas1.shape
    M = np.float32([[1,0,0],[0,1,0]])

    img3 = cv2.drawKeypoints(img1, kp1Matches,color=(0,0,255))
    cv2.warpAffine(img3, M,(finalCols, finalRows), Canvas1)

    img2 = cv2.drawKeypoints(img2, kp2Matches,color=(255,0,0))
    cv2.warpAffine(img2, Transform,(finalCols, finalRows), Canvas2, borderMode=cv2.BORDER_TRANSPARENT)

    alpha = 0.5
    beta = (1.0 - alpha)
    cv2.addWeighted(Canvas1, alpha, Canvas2, beta, 0.0, Canvas1)

    # Save the resulting image
    if not os.path.exists(settings.MEDIA_ROOT):
	    os.makedirs(settings.MEDIA_ROOT)

    filename = "%s.%s" % (uuid.uuid4(), 'jpg')
    ret = cv2.imwrite(os.path.join(settings.MEDIA_ROOT, filename), Canvas1)
    publicFilename = os.path.join(settings.MEDIA_URL, filename)

    return render(request,
        'app/featurematch.html',
        context_instance = RequestContext(request,
        {
            'mergedImageURL': publicFilename
        }))

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }))
