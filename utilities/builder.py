from utilities.message import Message
from utilities.buildlog import BuildLog
import os
import os.path
import shutil
import sys


class Builder:
    
    @staticmethod
    def pyinstaller_build(source_name, source_folder, working_dir, project_name, build_target, includes_folder, build_options, buttons_to_disable, cur_self):
        
        try:
            for button in buttons_to_disable:
                button.setDisabled(True)
            
            #Создаем временную папку по пути working_dir и компилируем в ней проект
            os.chdir(working_dir)
            shutil.rmtree('tmp2', ignore_errors=True)
            try:
                shutil.copytree(source_folder, 'tmp2')
            except Exception:
                shutil.rmtree('tmp2', ignore_errors=True)
                shutil.copytree(source_folder, 'tmp2')
            os.chdir('tmp2')
            path = os.getcwd()
            #os.system('pyinstaller ' + build_options + ' ' + source_name) #cmd \k + ...
            command = 'pyinstaller ' + build_options + ' ' + source_name
             
        except Exception:
            Message.errorMessage(cur_self, ' ', 'Unknown error ocurred.\nYou can try to restart application.', os.path.join(working_dir, 'Resources', 'empt.ico'))
            os.chdir(working_dir)
            shutil.rmtree('tmp2', ignore_errors=True)
            for button in buttons_to_disable:
                button.setDisabled(False)
            return
        
        
        #Исполняем команду компиляции, выводя логи в QTextEdit
        cur_self.log = BuildLog(command, Builder._installer_continue, working_dir, buttons_to_disable,
                       [source_name, source_folder, working_dir, project_name, build_target, includes_folder, build_options, buttons_to_disable, cur_self, path])
        
            
    #Продолжение работы pyinstaller_build        
    @staticmethod        
    def _installer_continue(source_name, source_folder, working_dir, project_name, build_target, includes_folder, build_options, buttons_to_disable, cur_self, path):
        try:
            #Создаем папку с проетом project_name по пути build_target, помещаем в нее include files(из include_folder) и скомпилированный проект 
            #Путь к папке со скомпилированным проектом зависит от модификаторов компиляции
            if not (os.path.isdir(os.path.join(os.path.dirname(os.path.join(path, 'dist')), source_name.split('.')[0]))):      
                exe_path = os.path.join(path, 'dist', source_name.split('.')[0] + ('.exe' if sys.platform == "win32" else '')) 
                os.chdir(build_target)
                shutil.copytree(includes_folder, project_name)
                os.chdir(project_name)
                try:
                    os.remove(source_name) #Если по какой-то причине в папке с готовым проектом находится файл с исходным кодом
                except Exception:          #то его нужно оттуда удалить
                    pass
                shutil.copy2(exe_path, project_name + ('.exe' if sys.platform == "win32" else ''))
                os.chdir(working_dir)
                shutil.rmtree('tmp2', ignore_errors=True) #Перед окончанием работы нужно удалить временную папку
                for button in buttons_to_disable:
                    button.setDisabled(False)
                    
                    
            else:
                build_folder = os.path.join(path, 'dist', source_name.split('.')[0])
                os.chdir(build_target)
                shutil.copytree(build_folder, project_name)
                os.chdir(project_name)
                for file in os.listdir(includes_folder):
                    if os.path.isdir(os.path.join(includes_folder, file)):
                        shutil.copytree(os.path.join(includes_folder, file), file)
                    else:
                        shutil.copyfile(os.path.join(includes_folder, file), file)
                try:
                    os.remove(source_name) #Если по какой-то причине в папке с готовым проектом находится файл с исходным кодом
                except Exception:          #то его нужно оттуда удалить
                    pass
                os.chdir(working_dir)
                shutil.rmtree('tmp2', ignore_errors=True) #Перед окончанием работы нужно удалить временную папку
                for button in buttons_to_disable:
                    button.setDisabled(False)
                    
                    
        except Exception:
            os.chdir(working_dir)
            shutil.rmtree('tmp2', ignore_errors=True) 
            for button in buttons_to_disable:
                button.setDisabled(False)
         
            
    @staticmethod
    def cxfreeze_build(source_name, source_folder, working_dir, project_name, build_target, includes_folder, setup_file, buttons_to_disable, cur_self):
        try:
            for button in buttons_to_disable:
                button.setDisabled(True)
            
            #Создаем временную папку по пути working_dir и компилируем в ней проект
            os.chdir(working_dir)
            shutil.rmtree('tmp2', ignore_errors=True)
            try:
                shutil.copytree(source_folder, 'tmp2')
            except Exception:
                shutil.rmtree('tmp2', ignore_errors=True)
                shutil.copytree(source_folder, 'tmp2')
            os.chdir('tmp2')
            shutil.copyfile(setup_file, 'setup.py')
            path = os.getcwd()
            command = str(sys.executable) + ' setup.py build'
        
        except Exception:
            Message.errorMessage(cur_self, ' ', 'Unknown error ocurred.\nYou can try to restart application.', os.path.join(working_dir, 'Resources', 'empt.ico'))
            os.chdir(working_dir)
            shutil.rmtree('tmp2', ignore_errors=True)
            for button in buttons_to_disable:
                button.setDisabled(False)
            return
        
        
        #Исполняем команду компиляции, выводя логи в QTextEdit
        cur_self.log = BuildLog(command, Builder._cxfreeze_continue, working_dir, buttons_to_disable,
                       [source_name, source_folder, working_dir, project_name, build_target, includes_folder, setup_file, buttons_to_disable, cur_self, path])
    
    
    #Продолжение работы cxfreeze_build 
    @staticmethod        
    def _cxfreeze_continue(source_name, source_folder, working_dir, project_name, build_target, includes_folder, setup_file, buttons_to_disable, cut_self, path):
        try:
            #Создаем папку с проетом project_name по пути build_target, помещаем в нее include files(из include_folder) 
            #и скомпилированный проект
            os.chdir(path)
            proj_path = os.path.join(path, 'build', os.listdir('build')[0])
            os.chdir(build_target)
            shutil.copytree(proj_path, project_name)
            os.chdir(project_name)
            
            for file in os.listdir(includes_folder):
                if file != os.path.basename(setup_file):
                    if os.path.isdir(os.path.join(includes_folder, file)):
                        shutil.copytree(os.path.join(includes_folder, file), file)
                    else:
                        shutil.copyfile(os.path.join(includes_folder, file), file)
                        
            try:
                os.remove(source_name) #Если по какой-то причине в папке с готовым проектом находится файл с исходным кодом
            except Exception:          #то его нужно оттуда удалить
                pass
            
            os.chdir(working_dir)
            shutil.rmtree('tmp2', ignore_errors=True) #Перед окончанием работы нужно удалить временную папку
            for button in buttons_to_disable:
                    button.setDisabled(False)
                    
        except Exception:
            os.chdir(working_dir)
            shutil.rmtree('tmp2', ignore_errors=True) 
            for button in buttons_to_disable:
                button.setDisabled(False)
            
            
    
            