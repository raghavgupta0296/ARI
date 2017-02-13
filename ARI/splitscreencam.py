import cv2
import pygame
import numpy
from imutils.video import WebcamVideoStream
from PIL import Image

pygame.init()
disp = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
resx,resy = disp.get_size()
print (resx,resy)
bg = pygame.Surface(disp.get_size())
# bg = bg.convert()
bg.fill((0,0,0))

fps = pygame.time.Clock()
pygame.font.init()
fps_text = pygame.font.SysFont("Comic Sans MS",19)

running = True
switchEyes = True

space_pressed = False
space_released = False

cam = WebcamVideoStream(1)
cam2 = WebcamVideoStream(2)
cam.start()
cam2.start()

while running: #cam.isOpened and cam2.isOpened and running:
    frame = cam.read()
    frame2 = cam2.read()

    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame2=cv2.cvtColor(frame2,cv2.COLOR_BGR2RGB)

    frame = numpy.fliplr(frame)
    frame2 = numpy.fliplr(frame2)

    camx,camy = frame.shape[:-1]
    camx2,camy2 = frame2.shape[:-1]

    imRect1 = pygame.Rect(((1*resx/4-camx/2),(resy/2-camy/2)),(camx,camy))  # ((x1,y1),(w,h)
    im1 = pygame.surfarray.make_surface(frame)

    imRect2 = pygame.Rect(((3*resx/4-camx2/2),(resy/2-camy2/2)),(camx2,camy2))
    im2 = pygame.surfarray.make_surface(frame2)

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
            cam.stop()
            cam2.stop()
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_ESCAPE:
                running = False
                cam.stop()
                cam2.stop()
            if events.key == pygame.K_SPACE:
                space_pressed = True
        if events.type == pygame.KEYUP:
            if events.key == pygame.K_SPACE:
                space_released = True

    if space_pressed and space_released:
        switchEyes = not switchEyes
        space_pressed = False
        space_released = False

    if switchEyes == True:
        bg.blit(im1, imRect2)
        bg.blit(im2, imRect1)
        disp.blit(bg, (0, 0))
        fps_surface = fps_text.render("FPS:"+str(fps.get_fps()), False,(255, 255, 255))
        disp.blit(fps_surface, (5, 2))
        #pygame.display.flip()
        pygame.display.update([imRect1,imRect2,pygame.Rect((0,0),(200,40))])

    elif switchEyes == False:
        bg.blit(im1, imRect1)
        bg.blit(im2, imRect2)
        disp.blit(bg, (0, 0))
        fps_surface = fps_text.render("FPS:"+str(fps.get_fps()), False,(255, 255, 255))
        disp.blit(fps_surface, (5, 2))
        #pygame.display.flip()
        pygame.display.update([imRect1,imRect2,pygame.Rect((0,0),(200,40))])
    fps.tick()

cam.stop()
cam2.stop()