# -*- coding: utf-8 -*-
import     threading
import     sched, time

class Timeout(threading.Thread):
    """ se encarga de lanzar un funcion en un determinado tiempo """
 
    def __init__(self, timeout, function):
        threading.Thread.__init__(self)
        self.__scheduler = sched.scheduler(time.clock, self.check_cancel)
        self.__end = False
	self.current_event = self.__scheduler.enter(timeout, 1, function, ())

    def run(self):
        """ inicializa la hebra y lanza el planificador """
	print "llamado el run"
        self.__end = False
        self.__scheduler.run()

    def cancel(self):
        self.__end = True

    def check_cancel(self, t):
        """ funcion que espera t segundos comprobando durante esos t 
	segundos si hemos cancelado la espera """
        if self.__end:
		self.__scheduler.cancel(self.current_event)

    def is_running(self):
    	return not self.__end

def pintar():
    print "Estoy pintando"

if (__name__ == '__main__'):
    t = Timeout(0.75, pintar)   
    t.start()
    #time.sleep(1)
    t.cancel()
