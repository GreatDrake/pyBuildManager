import sys
import os.path 
import subprocess
from message import Message

#Используется для открытия idle на разных системах
class IdleOpener:
    
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
                    _, error = result.communicate()
                    if error:
                        Message.errorMessage(current_self, "Fail", "Failed to open IDLE") 
                except Exception:
                    pass
                
            elif 'idle.py' in os.listdir(idle):
                idle = os.path.join(idle, 'idle.py')
                
                try:
                    command = idle + (' "%s"' % fullsource)
                    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Что-то типа:  ...\\idle.py ...\\(source).py
                    _, error = result.communicate()
                    if error:
                        Message.errorMessage(current_self, "Fail", "Failed to open IDLE") 
                except Exception:
                    pass
            else:
                try:
                    command = 'idle3' + (' "%s"' % fullsource)
                    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
                    _, error = result.communicate()
                    if error:
                        try:
                            command = 'idle' + (' "%s"' % fullsource)
                            result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
                            _, error = result.communicate()
                            if error:
                                Message.errorMessage(current_self, "Fail", "Failed to open IDLE") 
                        except Exception:
                            pass
                except Exception:
                    pass
        else:
            try:
                command = 'idle3' + (' "%s"' % fullsource)
                result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
                _, error = result.communicate()
                if error:
                    try:
                        command = 'idle' + (' "%s"' % fullsource)
                        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
                        _, error = result.communicate()
                        if error:
                            Message.errorMessage(current_self, "Fail", "Failed to open IDLE")
                    except Exception:
                        pass
            except Exception:
                pass
            
            