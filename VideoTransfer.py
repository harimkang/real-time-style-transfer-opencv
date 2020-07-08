import tensorflow as tf
import numpy as np
import cv2
import os
import sys
from style_transfer import StyleTransfer
from image_segmentation import ImageSegmentation


path=os.path.dirname(__file__)
loop=True

styles=["Gogh","Kandinsky","Monet","Picasso","Na","Mario"]
                 
for file in os.listdir(os.path.join(path,"samples")):

     filename=file.split(".")[0]
     extention=file.split(".")[1]

     cap=cv2.VideoCapture(os.path.join(path,"samples",file))

     frame_width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
     frame_height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
     frame_size=(frame_width,frame_height)

     fourcc=cv2.VideoWriter_fourcc(*'DIVX')
     out=cv2.VideoWriter(os.path.join(path,"results",filename+"_result."+extention),fourcc,24,frame_size)

     style_transfer=StyleTransfer(frame_width,frame_height)
     style_transfer.load()
     style_transfer.change_style(styles.index("Na"))
     image_segmentation=ImageSegmentation(frame_width,frame_height)

     print("\nencoding "+file+" |",end='')
     
     while True:
          print("=",end='')
          retval,frame=cap.read()
          
          if not retval:
               break

          style_image=style_transfer.predict(frame)
          seg_mask=image_segmentation.predict(frame)   
          seg_mask = cv2.cvtColor(seg_mask, cv2.COLOR_GRAY2RGB)

          result_image = np.where(seg_mask, style_image, frame)

          cv2.imshow("result",result_image)
          out.write(result_image)

          key=cv2.waitKey(30)
          if key==32:
               print("|")
               break
          
          if key==ord('q'):
               print("|") 
               loop=False
               break
          
     cap.release()
     out.release()
     cv2.destroyAllWindows()

     if loop==False:
          break


     
