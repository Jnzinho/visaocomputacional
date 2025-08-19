import cv2 as cv
 
camera = cv.VideoCapture(0)

ret, frame = camera.read()
if ret:
    frame_height, frame_width = frame.shape[:2]
else:
    frame_width, frame_height = 640, 480

fourcc = cv.VideoWriter_fourcc(*'mp4v')
output = cv.VideoWriter('output.mp4', fourcc, 30.0, (frame_width, frame_height))

if not camera.isOpened():
    print('Erro ao tentar abrir a camera')
    exit()

while True:
    ret, frame = camera.read()

    if not ret:
        print('Erro ao receber frame, acabou?')
        break

    output.write(frame)
    
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
    
camera.release()
output.release()
cv.destroyAllWindows()