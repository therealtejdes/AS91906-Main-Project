#defaults
import json
import pygame
import time

DEFAULTS = {"brightness": 100

            }
MIN_BRIGHTNESS=1
#constants
TEST_FILENAME="test.json"

class Settings():
    def __init__(self,filename,):
        self. _filename=filename
        self._settings= DEFAULTS
        #check for the file and load settings
    def write_settings(self):
        result= self.write_json(self._filename,self._settings)

    def read_settings(self,filename):
        result= self.read_json(filename)
        if result is not None:
            self._settings = result

    def write_json(self,filename,object):
        try: 
            output_file=open(filename, "w", encoding="utf-8")
            output_file.write(json.dumps(object))
            output_file.close()

        except:
            print("fail to open")
            #or output_file.write("")
    
    def read_json(self,filename):
        try:
            output_file=open(filename, "r", encoding="utf-8")
            json_text = output_file.read()
            the_object = json.loads(json_text)

            output_file.close()
            return the_object
        except:
            print("failibng to read")
            return None
        


    def get_brightness(self):
        return self._settings ["brightness"]
    def set_brightness(self,brightness):
        if brightness <MIN_BRIGHTNESS:
            print("invalid brightness")
            exit()

    from os.path import exists



    if __name__ =="__main__":
            print("testing not yet implement")
