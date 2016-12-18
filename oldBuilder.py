import os
import shutil
import threading

class Builder:
    
    @staticmethod
    def _pyinstaller_build(source_name, source_folder, working_dir, project_name, build_target, includes_folder, build_options='', buttons_to_disable=None, cur_self=None):
        try:
            for button in buttons_to_disable:
                button.setDisabled(True)
            #Создаем временную папку по пути working_dir и компилируем в ней проект
            os.chdir(working_dir)
            shutil.copytree(source_folder, 'tmp2')
            os.chdir('tmp2')
            path = os.getcwd()
            os.system('pyinstaller ' + build_options + ' ' + source_name) #cmd \k + ...
            
            #Создаем папку с проетом project_name по пути build_target, помещаем в нее include files(из include_folder) 
            #и скомпилированный проект
            if not (source_name.split('.')[0] in os.listdir(os.path.join(path, 'dist'))): # Путь к папке со скомпилированным проектом зависит от
                exe_path = os.path.join(path, 'dist', source_name.split('.')[0] + '.exe') # модификаторов компиляции
                os.chdir(build_target)
                shutil.copytree(includes_folder, project_name)
                os.chdir(project_name)
                try:
                    os.remove(source_name) #Если по какой-то причине в папке с готовым проектом находится файл с исходным кодом
                except Exception:          #то его нужно оттуда удалить
                    pass
                shutil.copyfile(exe_path, project_name + '.exe')
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
    def pyinstaller_build(source_name, source_folder, working_dir, project_name, build_target, includes_folder, build_options='', buttons_to_disable=None, cur_self=None):
        #Запускаем метод в новом потоке чтобы не зависло главное окно с интерфейсом(на случай если такое имеется)
        t = threading.Thread(target=Builder._pyinstaller_build, args=(source_name, source_folder, working_dir, project_name, 
                                                                     build_target, includes_folder, build_options, buttons_to_disable, cur_self))
        t.start()
        
        
        
    @staticmethod
    def _cxfreeze_build(source_name, source_folder, working_dir, project_name, build_target, includes_folder, setup_file, buttons_to_disable=None, cur_self=None):
        try:
            for button in buttons_to_disable:
                button.setDisabled(True)
            #Создаем временную папку по пути working_dir и компилируем в ней проект
            os.chdir(working_dir)
            shutil.copytree(source_folder, 'tmp2')
            os.chdir('tmp2')
            shutil.copyfile(setup_file, 'setup.py')
            path = os.getcwd()
            os.system('python setup.py build')
            
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
            
            
    @staticmethod            
    def cxfreeze_build(source_name, source_folder, working_dir, project_name, build_target, includes_folder, setup_file, buttons_to_disable=None, cur_self=None):
        #Запускаем метод в новом потоке чтобы не зависло главное окно с интерфейсом(на случай если такое имеется)
        t2 = threading.Thread(target=Builder._cxfreeze_build, args=(source_name, source_folder, working_dir, project_name, 
                                                                     build_target, includes_folder, setup_file, buttons_to_disable, cur_self))
        t2.start()
            
