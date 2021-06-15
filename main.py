import os

def make_folders():
    folder_1 = ('\\downloads')
    folder_2 = ('\\text files')
    folder_path1 = str(os.path.dirname(os.path.realpath(__file__))) + folder_1
    folder_path2 = str(os.path.dirname(os.path.realpath(__file__))) + folder_2
    if not os.path.exists(folder_path1):
        os.makedirs(folder_path1)
    if not os.path.exists(folder_path2):
        os.makedirs(folder_path2)

def method():
    print('Welcome to FPR\n')
    print('How do you want your photo: ')
    print('1 - Download photos')
    print("2 - Collect photo's download link")
    print('0 - Exit')
    act = input('--> ')
    make_folders()
    if act == '1':
        import download
    elif act == '2':
        import text
    elif act == '0':
        exit_func()
    else:
        print('Input is incorrect. Try again. ')
        method()

def exit_func():
    print('exiting program...')
    exit()

method()