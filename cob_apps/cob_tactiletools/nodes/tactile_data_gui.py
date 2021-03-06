#!/usr/bin/python
import roslib; roslib.load_manifest('cob_tactiletools')
import rospy
from cob_msgs.msg import TactileMatrix, TactileSensor
import pygtk
pygtk.require('2.0')
import gtk, gobject, cairo
import threading
import time

#Initializing the gtk's thread engine
gtk.gdk.threads_init()

class Screen(gtk.DrawingArea):

    # Draw in response to an expose-event
    __gsignals__ = { "expose-event": "override" }
    sizex = 3
    sizey = 1
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.tactile_array = (0,0,0)

    # Handle the expose-event by drawing
    def do_expose_event(self, event):
        # Create the cairo context
        cr = self.window.cairo_create()
        #print "Width: ", self.allocation.width
        #print "Height: ", self.allocation.height
        # Restrict Cairo to the exposed area; avoid extra work
        cr.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        cr.clip()
        self.draw(cr, self.allocation.width,self.allocation.height )

    def draw(self, cr, width, height):
        # Fill the background with gray
        color = 0.5
        xw = width/(self.sizex)
        yw = height/(self.sizey)
        print "SIZE+++++ ", len(self.tactile_array)
        for i in range(0,self.sizex):
            for j in range(0,self.sizey):
                #print (i+1)*(j+1)
                color = self.tactile_array[self.sizey*i+j]/1000
                if(color != 0.0):
                    print color
                cr.set_source_rgb(1, 1-color, 1)
                cr.rectangle((i)*xw, (j)*yw, xw, yw)
                cr.fill()

    def setMatrixSize(self, matrixx, matrixy):
        self.sizex = matrixx
        self.sizey = matrixy

    def updateTactileMatrix(self, array):
        print "Got something: ", array
        self.tactile_array = array
        self.queue_draw()


            
def roscb(data):
    global sc1
    global sc2
    global sc3
    global sc4
    global sc5
    global sc6
    global testv
    matrices = data.tactile_matrix
    gtk.threads_enter()
    for mat in matrices:
        if(mat.matrix_id == 0):
            sc1.setMatrixSize(mat.cells_x,mat.cells_y)
            sc1.updateTactileMatrix(mat.tactile_array)
        if(mat.matrix_id == 1):
            sc2.setMatrixSize(mat.cells_x,mat.cells_y)
            sc2.updateTactileMatrix(mat.tactile_array)
        if(mat.matrix_id == 2):
            sc3.setMatrixSize(mat.cells_x,mat.cells_y)
            sc3.updateTactileMatrix(mat.tactile_array)
        if(mat.matrix_id == 3):
            sc4.setMatrixSize(mat.cells_x,mat.cells_y)
            sc4.updateTactileMatrix(mat.tactile_array)
        if(mat.matrix_id == 4):
            sc5.setMatrixSize(mat.cells_x,mat.cells_y)
            sc5.updateTactileMatrix(mat.tactile_array)
        if(mat.matrix_id == 5):
            sc6.setMatrixSize(mat.cells_x,mat.cells_y)
            sc6.updateTactileMatrix(mat.tactile_array)
    gtk.threads_leave()


# GTK mumbo-jumbo to show the widget in a window and quit when it's closed
def main_quit(obh, obb):
    #Stopping the thread and the gtk's main loop
    gtk.main_quit()

try:
    window = gtk.Window()
    winwidth = 400
    winheight = 400
    window.set_size_request(winwidth,winheight)
    window.set_title("TactileSensorData")
    testv = 0
    sc1 = Screen()
    sc1.set_size_request((winwidth/3)-10, (winheight/2)-5)
    sc2 = Screen()
    sc2.set_size_request((winwidth/3)-10, (winheight/2)-5)
    sc3 = Screen()
    sc3.set_size_request((winwidth/3)-10, (winheight/2)-5)
    sc4 = Screen()
    sc4.set_size_request((winwidth/3)-10, (winheight/2)-5)
    sc5 = Screen()
    sc5.set_size_request((winwidth/3)-10, (winheight/2)-5)
    sc6 = Screen()
    sc6.set_size_request((winwidth/3)-10, (winheight/2)-5)
    hbox1=gtk.HBox(False ,10 )
    hbox1.pack_start(sc1,False, True, 0)
    hbox1.pack_start(sc2,False, True, 0)
    hbox1.pack_start(sc3,False, True, 0)
    hbox2=gtk.HBox(False,10)
    hbox2.pack_start(sc4,False, True, 0)
    hbox2.pack_start(sc5,False, True, 0)
    hbox2.pack_start(sc6,False, True, 0)
    vbox=gtk.VBox(True,0)
    vbox.pack_start(hbox1,False, False, 0)
    vbox.pack_start(hbox2,False, False, 0)
    window.add(vbox)
    window.show_all()
    window.connect("delete-event", main_quit)
    window.present()
    #ROS Subscribes
    rospy.init_node('TactileSensorView', anonymous=True)
    rospy.Subscriber("/sdh/tactile_data", TactileSensor, roscb)
    gtk.main()
except KeyboardInterrupt:
    main_quit("tut", "tut")
