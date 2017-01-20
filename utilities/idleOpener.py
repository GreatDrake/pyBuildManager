from utilities.message import Message
import sys
import os.path 
import subprocess
import time


#Используется для открытия idle на разных системах
class IdleOpener:
    sleepTime = 0.15
    
    @staticmethod
    def openInIdle(current_self, fullsource):
        python = os.path.dirname(sys.executable)
        idle = os.path.join(python, "Lib", "idlelib") #Директория с idle
        
        if os.path.isdir(idle):
            if 'idle.bat' in os.listdir(idle):
                idle = os.path.join(idle, 'idle.bat')
                
                try: 
                    command = idle + (' "%s"' % fullsource)
                    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Что-то типа:  ...\\idle.bat ...\\(source).py
                    time.sleep(IdleOpener.sleepTime) #Ждем sleepTime и проверяем, смог ли запуститься процесс
                    if result.poll(): #result.poll() - процесс не работает
                        Message.errorMessage(current_self, "Fail", "Failed to open IDLE") 
                except Exception:
                    pass
                
            elif 'idle.py' in os.listdir(idle):
                idle = os.path.join(idle, 'idle.py')
                
                try:
                    command = idle + (' "%s"' % fullsource)
                    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Что-то типа:  ...\\idle.py ...\\(source).py
                    time.sleep(IdleOpener.sleepTime)
                    if result.poll():
                        Message.errorMessage(current_self, "Fail", "Failed to open IDLE") 
                except Exception:
                    pass
            else:
                try:
                    command = 'idle3' + (' "%s"' % fullsource)
                    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
                    time.sleep(IdleOpener.sleepTime)
                    if result.poll():
                        try:
                            command = 'idle' + (' "%s"' % fullsource)
                            result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
                            time.sleep(IdleOpener.sleepTime)
                            if result.poll():
                                Message.errorMessage(current_self, "Fail", "Failed to open IDLE") 
                        except Exception:
                            pass
                except Exception:
                    pass
        else:
            try:
                command = 'idle3' + (' "%s"' % fullsource)
                result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
                time.sleep(IdleOpener.sleepTime)
                if result.poll():
                    try:
                        command = 'idle' + (' "%s"' % fullsource)
                        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
                        time.sleep(IdleOpener.sleepTime)
                        if result.poll():
                            Message.errorMessage(current_self, "Fail", "Failed to open IDLE")
                    except Exception:
                        pass
            except Exception:
                pass
            
            