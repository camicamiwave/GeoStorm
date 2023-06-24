'''
Note: The output may be jumbled if ran on IDEs. Please run the script using Python Console.
'''
#IMPORTS
import time
import random as ran
import os
#Try to import external modules. If failed, install requirements automatically. If failed, tell user to install requirements.txt manually.
try:
    from pynput import keyboard
    from pynput.keyboard import Controller as conkb
    from pynput.mouse import Controller as conms
    import pygame
except:
    while True:
        answer = input("Do you want to install missing modules (Y/N)?\n\t>> ").strip()
        if answer.upper() in ['Y', 'YES']:
            try:
                os.system('cmd /c "pip install -r requirements.txt"')
                from pynput import keyboard
                from pynput.keyboard import Controller as conkb
                from pynput.mouse import Controller as conms
                import pygame
                break
            except:
                print("Please install the requirements.txt manually...")
                for i in range(3, -1, -1):
                    print(f"Closing in {i}...", end='\r')
                    time.sleep(1)
                exit()
        elif answer.upper() in ['N', 'NO']:
            print('This program cannot to run.')
            for i in range(3, -1, -1):
                print(f"Closing in {i}...", end='\r')
                time.sleep(1)
            exit()
        else: print('Invalid answer.')
#CLASS
class PossiblePaths:
    '''
    An object that calculates all possible routes the user can take.
    - Functions:
        -  RAPVars
        - PossiblePaths
        - NumPossiblePaths
    - __init__(map:list[str])
        - Parameter:
            - map:list[str]: numbered interpretation of the map.
    '''
    def __init__(self, map):
        self.places = 6
        self.neighbors = map
    def ReturnNeighbors(self, place:str):
        '''
        Returns the neighbor of the place.
        - Parameter:
            - place:str: initial place.
        '''
        for i in self.neighbors:
            if i.startswith(place):
                neigh = i.split(', ')[1:]
                neigh = list(map(int, neigh))
                return neigh
    def Results(self):
        '''
        Converts the numbered results into worded results.
        '''
        self.worded_route = []
        for i in range(len(self.returnmap)):
            i_list = self.returnmap[i].split(', ')
            route = ''
            for j in i_list:
                if j == '0': route += 'Forest, '
                elif j == '1': route += 'Park, '
                elif j == '2': route += 'Mall, '
                elif j == '3': route += 'Home, '
                elif j == '4': route += 'Mountains, '
                elif j == '5': route += 'Beach, '
                elif j == '6': route += 'School, '
            self.worded_route.append(route.strip(', '))
    def PossiblePaths(self):
        '''
        Get the worded route.
        '''
        return self.worded_route
    def NumPossiblePaths(self):
        '''
        Get the numbered route.
        '''
        return self.returnmap
    def ReturnAllPaths(self, user_current, user_destin, visited, path):
        '''
        ReturnAllPaths(user_current:int, user_destin:int, visited:list[bool], path:list[int])
        Returns all possible paths.
        - Parameters:
            - user_current:int: current position of user.
            - user_destin:int: target position of user.
            - visited:list[bool]: list of all visited nodes.
            - path:list[int]: list of all nodes gathered.
        '''
        visited[user_current]= True
        path.append(user_current)
        if user_current == user_destin:
            self.returnmap.append(', '.join(list(map(str, path))))
        else:
            current_neighbors = self.ReturnNeighbors(str(user_current))
            for i in current_neighbors:
                if not visited[i]:
                    self.ReturnAllPaths(i, user_destin, visited, path)
        path.pop()
        if len(path) == 0: self.Results()
        else: visited[user_current] = False

    def RAPVars(self, user_init, user_destin):
        '''
        RAPVars(self, user_init:int, user_destin:int) 
        Calculate for the possible paths to take.
        - Parameters:
            - user_init:int: initial position of user.
            - user_destin:int: target destination of user.
        '''
        visited =[False]*7
        path = []
        self.returnmap = []
        self.ReturnAllPaths(user_init, user_destin, visited, path)
class Sounds:
    '''
    An object to play sounds within the game.
    Functions:
        - playsound: Plays saved sounds from folder sound_util.
        - stopbgm: Stops currently playing background music.
    '''
    SOUND_FOLDER = 'sound_util'
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        #SFX
        self.titlesfx = pygame.mixer.Sound(os.path.join(self.SOUND_FOLDER, 'Jiosutoomu.mp3'))
        self.tsunamisfx = pygame.mixer.Sound(os.path.join(self.SOUND_FOLDER, 'tsunami-sfx.mp3'))
        self.clicksfx = pygame.mixer.Sound(os.path.join(self.SOUND_FOLDER, 'options.mp3'))
    def playsound(self, sound_name, mode) -> None:
        '''
        playsound(self, sound_name:str, mode:str) -> None
        
        Plays saved sounds from folder sound_util.
        - Parameters:
            - sound_name:str: name of the sound or music
            - mode:str: mode of music.
                - sfx: sound effects
                - bgm: background music
        '''
        if mode == 'sfx':
            try:
                pygame.mixer.Sound.play(eval(f"self.{sound_name+mode}"))
            except: print('DEBUG 404: SOUND NOT FOUND.')
        elif mode == 'bgm':
            try: pygame.mixer.music.stop()
            except: print('no sound to be stopped.')
            pygame.mixer.music.load(os.path.join(self.SOUND_FOLDER, f'{sound_name}.mp3'))
            pygame.mixer.music.play(-1)
    def stopall(self):
        '''
        stopall()
        Stops currently playing music.
        '''
        try: pygame.mixer.stop()
        except: pass
#FUNCTIONS
def ClearConsole()->None:
    '''
    ClearConsole()->None
    Clears the console for better display.
    '''
    mouse = conms()
    for _ in range(3):
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        mouse.scroll(0, 10)
def MainMenu(code)->None:
    '''
    MainMenu(code:int)->None
    Displays Main Menu and lets the user pick using up and down buttons.
    - Parameter:
        - code:int: mode of MainMenu display.
    '''
    def ScreenMenu():
        '''
        Displays the menu.
        '''
        global Menuchoice
        ClearConsole()
        print('''                                         \033[1;30;40m_________________  ______
                                        \033[1;30;40m( ;;  ;;;    ; ;;;  ;  );;; ; ;)
                                  \033[91m_  \033[1;30;40m(;;;;;;(;;;;);;;;;;) ;;; ;; ; ;)
                              \033[91m~__/ \__~ \033[1;30;40m((;;;);;)  ;; ; ;;)
                        \033[91m~__..--.......--..__~    \033[93m/    /
                  \033[91m~__..--___________________--..__~\033[93m  \\
                      \033[91m||     ジオストーム     ||    \033[93m/ /
                    \033[91m__||Jiosutoomu - GeoStorm||__   \033[93m/ \033[0m\033[0m
        ''')
        for i in displays[Menuchoice].split('\n'):
            print('                    '+i)
        print(ran.choices(['Tip: You can use up and down arrows to choose from the choices.', 'Tip: Press Enter to choose the highlighted choice.'])[0])
    def on_press(key):
        '''
        Reacts with the key listener and affects the ScreenMenu.
        '''
        global Menuchoice
        if key == keyboard.Key.up:
            sound.playsound('click', 'sfx')
            Menuchoice -= 1
            if Menuchoice == -1: Menuchoice = (3 if code == 1 else 4)
        elif key == keyboard.Key.down:
            sound.playsound('click', 'sfx')
            Menuchoice += 1
            if Menuchoice == (4 if code == 1 else 5): Menuchoice = 0
        elif key == keyboard.Key.enter:
            sound.playsound('click', 'sfx')
            Menuchoice = ["A", "B", "C", "D", "E"][Menuchoice]
            return False
        else: return
        ScreenMenu()
        time.sleep(.3)
    def display():
        '''
        Selects the appropriate menu depending on the code number.
        '''
        if code == 1:
            return [
            '        \033[1m\033[94m > Play Game\033[0m\033[0m\n        > About The Game\n        > Resources\n        > Exit',
            '        > Play Game\n        \033[1m\033[94m > About The Game\033[0m\033[0m\n        > Resources\n        > Exit',
            '        > Play Game\n        > About The Game\n        \033[1m\033[94m > Resources\033[0m\033[0m\n        > Exit',
            '        > Play Game\n        > About The Game\n        > Resources\n        \033[1m\033[93m > Exit\033[0m\033[0m'
            ]
        elif code == 2:
            return [
            '        \033[1m\033[94m > Play Again\033[0m\033[0m\n        > See All Safety Places \033[93m[New!]\033[0m\n        > About The Game\n        > Resources\n        > Exit',
            '        > Play Again\n        \033[1m\033[94m > See All Safety Places\033[0m \033[93m[New!]\033[0m\033[0m\n        > About The Game\n        > Resources\n        > Exit',
            '        > Play Again\n        > See All Safety Places \033[93m[New!]\033[0m\n        \033[1m\033[94m > About The Game\033[0m\033[0m\n        > Resources\n        > Exit',
            '        > Play Again\n        > See All Safety Places \033[93m[New!]\033[0m\n        > About The Game\n        \033[1m\033[94m > Resources\033[0m\033[0m\n        > Exit',
            '        > Play Again\n        > See All Safety Places \033[93m[New!]\033[0m\n        > About The Game\n        > Resources\n        \033[1m\033[93m > Exit\033[0m\033[0m'
            ]
        elif code == 3:
            return [
            '        \033[1m\033[94m > Play Again\033[0m\033[0m\n        > See All Safety Places\n        > About The Game\n        > Resources\n        > Exit',
            '        > Play Again\n        \033[1m\033[94m > See All Safety Places\033[0m\033[0m\n        > About The Game\n        > Resources\n        > Exit',
            '        > Play Again\n        > See All Safety Places\n        \033[1m\033[94m > About The Game\033[0m\033[0m\n        > Resources\n        > Exit',
            '        > Play Again\n        > See All Safety Places\n        > About The Game\n        \033[1m\033[94m > Resources\033[0m\033[0m\n        > Exit',
            '        > Play Again\n        > See All Safety Places\n        > About The Game\n        > Resources\n        \033[1m\033[93m > Exit\033[0m\033[0m'
            ]
    displays = display()
    ScreenMenu()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    input() #Counteract to a keyboard listener bug.
def AboutGame()->None:
    '''
    AboutGame()->None
    Displays the abouts of this game.
    '''
    ClearConsole()
    sound.playsound('about', 'bgm')
    print('█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█')
    print('█\033[1m'+'About the game:'.center(98)+'\033[0m█')
    print("""█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
█       The sky was tar-black and the large clouds were moving towards the city... A sign of bad   █
█   omen;  A  catastrophe  will  soon  happen.  You  are stuck in a random site where a calamity   █
█   will hit.                                                                                      █""")
    print('█\033[96m'+"Where should you go?".center(98)+'\033[0m█')
    print('█\033[96m'+"    Quickened your pace, find the safest place!".center(98)+'\033[0m█')
    print("""█       GeoStorm; a text-based program made using python language under console interface is  an   █
█   educational game that aims to assess the awareness of the player related  to  calamities. It   █
█   involves seven locations corresponding to different calamities and each has  its  respective   █
█   scenarios.                                                                                     █
█                                                                                                  █
█       The  game  starts  with  you,  the  player,  on  a random location where the calamity is   █
█   happening.  You  need  to  decide where is the safest target destination for you to go. Each   █
█   location has a corresponding point, being the most secured place, and the opposite  for  the   █
█   less secured site. Once you chose a certain location, the  points will be displayed  and the   █
█   next calamity scenario will follow soon after.                                                 █
█                                                                                                  █
█       The safest place hunting cycle will continue until the last calamity  is  finished. Once   █
█   done, the points will be accumulated and displayed on the console with acknowledgement based   █
█   on your score.                                                                                 █
█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
    """)
    print('Press Esc to exit...')
    def on_press(k):
        if k == keyboard.Key.esc:
            sound.playsound('click', 'sfx')
            return False
    with keyboard.Listener(on_press=on_press) as listener: listener.join()
    ClearConsole()
def Resources()->None:
    '''
    Resources()->None
    Displays all the resources used in making this game.
    '''
    ClearConsole()
    sound.playsound('resources', 'bgm')
    print("""
█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
█   \033[1mLinks:\033[0m                                                                                         █
█   Hurricanes/Storms:                                                                             █
█       \033[94mhttps://www.travelers.com/resources/weather/hurricanes/hurricane-survival-guide\033[0m            █
█   Tsunami:                                                                                       █
█       \033[94mhttps://www.ready.gov/tsunamis\033[0m                                                             █
█   Earthquake:                                                                                    █
█       \033[94mhttps://ehs.stanford.edu/manual/emergency-response-guidelines/earthquake\033[0m                   █
█       \033[94mhttps://www.cdc.gov/disasters/earthquakes/during.html\033[0m                                      █
█   Volcanic Eruption:                                                                             █
█       \033[94mhttps://www.redcross.org/get-help/how-to-prepare-for-emergencies/types-of-emergencies/\033[0m     █
█                   \033[94mvolcano.html\033[0m                                                                   █
█       \033[94mhttps://www.redcross.org/get-help/how-to-prepare-for-emergencies/types-of-emergencies/\033[0m     █
█                   \033[94mvolcano.html\033[0m                                                                   █
█   Wildfires:                                                                                     █
█       \033[94mhttps://www.cdc.gov/disasters/wildfires/duringfire.html\033[0m                                    █
█       \033[94mhttp://www.parks.ca.gov/?page_id=30661\033[0m                                                     █
█   Heatwave:                                                                                      █
█       \033[94mhttps://www.redcross.org/get-help/how-to-prepare-for-emergencies/types-of-emergencies/\033[0m     █
█                   \033[94mheat-wave-safety.html\033[0m                                                          █ 
█   Tornado:                                                                                       █
█       \033[94mhttps://www.getprepared.gc.ca/cnt/hzd/trnds-drng-en.aspx\033[0m                                   █
█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

""")
    print('Press Esc to exit...')
    def on_press(k):
        if k == keyboard.Key.esc:
            sound.playsound('click', 'sfx')
            return False
    with keyboard.Listener(on_press=on_press) as listener: listener.join()
    ClearConsole()
def RandomBuild(arr)->list:
    '''
    RandomBuild(arr:list[str])->list[str]
    Randomizes distances between connected buildings.
    - Parameter:
        - arr:list[str]: building connections ['main, *neighbors', 'main, *neibors', ... ]
    '''
    ne0, ne1, ne2, ne3, ne4, ne5, ne6 = ['0'], ['1'], ['2'], ['3'], ['4'], ['5'], ['6']
    for i in arr:
        arrlist = i.split(', ')
        main = arrlist[0]
        neighbors = arrlist[1:]
        for j in neighbors:
            distance = ran.randint(10, 100)
            for k in eval(f"ne{j}"):
                if main == k.partition(":")[0]:
                    distance = k.partition(":")[-1]
            eval(f"ne{main}.append('{j}:{distance}')")
    return [', '.join(ne0), ', '.join(ne1), ', '.join(ne2), ', '.join(ne3), ', '.join(ne4),
            ', '.join(ne5), ', '.join(ne6)]
def mapDisplay(player_pos, player_des)->None:
    '''
    mapDisplay(player_pos:str, player_des:str)->None
    Displays the whole map of ジオストーム.
    - Parameters:
        - player_pos:str: Player position; displayed as their respective color
        - player_des:str: Player destination; displayed as light_magenta color
    '''
    global connections
    d05  = "\033[0m"+f"{connections[0]}m".center(5)  #0 - 05 - Forest:Beach
    d06  = "\033[0m"+f"{connections[1]}m".center(5)  #1 - 06 - Forest: School
    d10  = "\033[0m"+f"{connections[2]}m".center(5)  #1 - 10 - Park:Forest
    d12  = "\033[0m"+f"{connections[3]}m".center(5)  #2 - 12 - Park:Mall
    d13  = "\033[0m"+f"{connections[4]}m".center(5)  #3 - 13 - Park:Home
    di16 = "\033[0m"+f"{connections[5]}m".center(6)  #4 - 16 - Park:School
    d23  = "\033[0m"+f"{connections[6]}m".center(5)  #5 - 23 - Mall:Home
    d24  = "\033[0m"+f"{connections[7]}m".center(5)  #6 - 24 - Mall:Mountains
    d45  = "\033[0m"+f"{connections[8]}m".center(5)  #7 - 45 - Mountains:Beach
    d46  = "\033[0m"+f"{connections[9]}m".center(5)  #8 - 46 - Mountains:School
    d56  = "\033[0m"+f"{connections[10]}m".center(5) #9 - 56 - Beach:School
    home = '\033[1;33;40m' if player_pos == 'Home' else '\033[97m' if player_des == 'Home' else '\033[2m\033[90m'
    mall = '\033[1;35;40m' if player_pos == 'Mall' else '\033[97m' if player_des == 'Mall' else '\033[2m\033[90m'
    mountains = '\033[1;31;40m' if player_pos == 'Mountains' else '\033[97m' if player_des == 'Mountains' else '\033[2m\033[90m'
    beach = '\033[1;36;40m' if player_pos == 'Beach' else '\033[97m' if player_des == 'Beach' else '\033[2m\033[90m'
    park = '\033[1;34;40m' if player_pos == 'Park' else '\033[97m' if player_des == 'Park' else '\033[2m\033[90m'
    school = '\033[1;32;40m' if player_pos == 'School' else '\033[97m' if player_des == 'School' else '\033[2m\033[90m'
    forest = '\033[1;30;40m' if player_pos == 'Forest' else '\033[97m' if player_des == 'Forest' else '\033[2m\033[90m'
    print(f'\033[1;37;40m█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█')
    print(f'\033[1;37;40m█                                             ジオストーム                                         █')
    print(f'\033[1;37;40m█                                       (Jiosutoomu - GeoStorm)                                    █')
    print(f'\033[1;37;40m█                                                                                                  █')
    print(f'\033[1;37;40m█  {home}█▀▀▀▀▀▀█      {mall} █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█     {mountains}  █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█       {beach}█▀▀▀█  \033[1;37;40m█')
    print(f'\033[1;37;40m█  {home}█      █      {mall} █                        █ {d24}{mountains} █                                █ {d45}{beach} █   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█  {home}█      █ {d23}{mall} █                        █ \033[1;37;40m→→→→→{mountains} █            MOUNTAINS           █ \033[1;37;40m→→→→→ {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█  {home}█ HOME █ \033[1;37;40m←←-→→{mall} █          MALL          █      {mountains} █                                █       {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█  {home}█      █      {mall} █                        █      {mountains} █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█       {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█  {home}█      █      {mall} █                        █                      \033[1;37;40m      ↑                   {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█  {home}█▄▄▄▄▄▄█      {mall} █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█                         \033[1;37;40m   ↓{d46}              {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█     ↑                \033[1;37;40m  ↑                        {school}  █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█       {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█  \033[1;37;40m   ↑{d13}           \033[1;37;40m  ↓{d12}                   {school}  █                               █       {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█  \033[1;37;40m   ↑{park}          █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█                {school}  █▄                              █       {beach}█ B █  \033[1;37;40m█')
    print(f'\033[1;37;40m█  \033[1;37;40m   ↑{park} █▀▀▀▀▀▀▀▀▀               ▀▀▀▀▀▀▀▀▀█       {school}   █▄▄▄▄▄▄▄                       █       {beach}█ E █  \033[1;37;40m█')
    print(f'\033[1;37;40m█  {park}█▀▀▀▀▀                                 ▀▀▀▀▀█  {di16}{school}    █                       █ {d56} {beach}█ A █  \033[1;37;40m█')
    print(f'\033[1;37;40m█  {park}█                    PARK                   █ \033[1;37;40m←←←←←→→→→→ {school}█         SCHOOL        █ \033[1;37;40m←←-→→ {beach}█ C █  \033[1;37;40m█')
    print(f'\033[1;37;40m█  {park}█▄▄▄▄▄                                 ▄▄▄▄▄█  {school}          █                       █       {beach}█ H █  \033[1;37;40m█')
    print(f'\033[1;37;40m█  {park}     █▄▄▄▄▄▄▄▄▄               ▄▄▄▄▄▄▄▄▄█       {school}   █▀▀▀▀▀▀▀                       █       {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█  {park}              █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█                {school}  █▀                              █       {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█                   \033[1;37;40m     ↓                        {school}  █                               █       {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█                   \033[1;37;40m     ↓ {d10}                  {school}  █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█       {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█ {forest} █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█                           \033[1;37;40m↑                   {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█ {forest} █                                        █                           \033[1;37;40m↑{d06}              {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█ {forest} █                  FOREST                ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█ {d05} {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█ {forest} █                                                                                █\033[1;37;40m →→→→→ {beach}█   █  \033[1;37;40m█')
    print(f'\033[1;37;40m█ {forest} █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█       {beach}█▄▄▄█  \033[1;37;40m█')
    print(f'\033[1;37;40m█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█')
def Scenarios(place)->None:
    '''
    Displays the appropriate  scenario depending on the randomized place
    that the user got.
    - Parameters:
        - place:str: Contains the user's current destination.
    '''
    if place == 'Forest':
        print('''
                                           \033[1mForest: Wildfire\033[0m
        It  was  a  beautiful  sunny day. You and your buddies were camping in the woods. It  was
    amazing  and exciting until you  noticed something was wrong.\033[91m  You witness  a  gigantic plume
    of dark smoke coming from nowhere. Blazing pyrotechnic flame can be seen near the campsite  a
    few  seconds  later. The  furious  scorching fire  flows  through the trees like ocean waves,
    igniting them.
        \033[1mYou must flee to a safe location, or you will all be reduced to ashes.\033[0m\033[0m''')
    elif place == 'Park':
        print('''
                                          \033[1mPark: Heatwave\033[0m 
        \033[3mBeing adult is really tough as what they say,
        too many neccessities and  bills to buy and pay.
        You were looking for a job in the city all day
        yet still didn't get hired and now you're walking astray.
        
        You've decide to go to the park and rest...
        since you are stressed...
        in this job hunting.

        Your  sweats drips like spring,
        all of a sudden your phone ring
        \033[91mand saw an MDDRM warning,
        that an extreme wave of heat is coming.\033[0m\033[0m
''')
    elif place == 'Mall':
        print('''
                                           \033[1mMall: Earthquake\033[0m
        \033[3mMassive crowds were cheering and clapping,
        it was day of the largest mall in the country is opening.
        Once the ribbon was cut,
        the big automatic glass door opens up.
        There comes in sight all the staffs in falling in line,
        behind them lies a breathtaking interior design.\033[0m

        \033[1mFast forward...\033[0m
        The  opening  event  ended  well  and  now  all  the  crowds  is  on  their way  to shop.
    \033[91mUnexpectedly,  the  ground  tremble  violently  as  if  the  whole  building  becomes  alive.
    The  air  fills  with  the  building's  inhuman noises: rumbles and groans, the screeching of
    metals. The sound of loud wails can be heard all over the place.\033[0m
        In just a small amount of time the bright and  luxurious  mall  got  deformed way  beyond
    imagination.
        \033[91m\033[1mIn face of this massive destruction, how will you handle the situation?\033[0m\033[0m''')
    elif place == 'Home':
        print('''
                                      \033[1mHome: Storm\033[0m
        The  sky  was  tar-black  and the large clouds were moving towards the city.\033[91m A  storm  is
    approaching;  you're  stuck  at  your home. Torrential rainfall  started pouring down and you
    need  to take shelter to  a safe location. The roads got submerge by rushing floods making it
    worst to travel around. 
        \033[1mWhere would you go? What should you do?\033[0m\033[0m
''')
    elif place == 'Mountains':
        print('''
                                     \033[1mMountains: Volcanic eruption\033[0m
        It  was  your  day-off  at  work.  As  a local geo-biologist and mountain enthusiast, you
    decided to relax by hiking in the highlands where a volcano that has  been  dormant  for ages
    resides. The hike was uneventful, and you arrived safely at the campsite. 

        The  night approaches  and it's still serene; you're admiring the star-studded night sky.
    \033[91mWhile gazing at the firmament,  you  observe  something glowing near the volcano's crater, as
    well as a faint smoke billowing at its center. It was then succeeded by ground tremor. As the
    volcano is said to be inactive, no one expect for it to erupt.

        \033[1mYou're goal is to  inform  the  natives  and  authorities  about  it.  And plan  for  the
    evacuation to a secured place.\033[0m\033[0m
''')
    elif place == 'Beach':
        print('''
                                            \033[1mBeach: Tsunami\033[0m
    \033[3mThe night was dark as ever as you sat alone on the shore,
    thinking why your life has been so unsure. 
    Looking at the firmament even tho its cloudy,
    no moon nor stars which made the mood somehow gloomy. \033[0m

        \033[91mIt was the right mood to senti, but then there came a loud ocean roar followed by unusual
    receding seawater. 

    \033[1mA clear sign of a great calamity; a tsunami.
    Don't panic, stay rational\033[0m\033[0m
''')
    elif place == 'School':
        print('''
                                           \033[1mSchool: Tornado\033[0m
    \033[3m"What a tough job being a teacher,
    you're still in the school even the weather is extreme checking student's paper".\033[0m
    
        These are your thoughts while you're sitting in  the office  facing  the computer. Black
    storm clouds gather in the sky accompanied by lightning ang thunder. Which makes you feel of
    wanting to go home. After a  while, you've finally finished your work and start to pack your
    things up. While outside, a funnel suddenly appears, as though descending from a cloud. Then
    it hits the ground and roars  forward with a  sound  that's so  loud. The  tornado  tears up
    everything in its path. Howling wind can be heard as if Barbatos burst its wrath.

                You only have few minutes to evacuate. Move fast before its too late.            
''')
def DisplayChoices(current)->None:
    '''
    DisplayChoices(current:str)->None
    
    Displays the choices and lets the player choose their destination.
    - Parameter:
        - current:str: user's initial position.
    '''
    def choices():
        '''
        Collects all choices.
        '''
        choice = []
        letters = ['A', 'B', 'C', 'D', 'E', 'F']
        if current != 'Forest': choice.append('Forest')
        if current != 'Park': choice.append('Park')
        if current != 'Mall': choice.append('Mall')
        if current != 'Home': choice.append('Home')
        if current != 'Mountains': choice.append('Mountains')
        if current != 'Beach': choice.append('Beach')
        if current != 'School': choice.append('School')
        for i in range(len(choice)):
            choice[i] = f'[{letters[i]}] - {choice[i]}'
        return choice
    def screendisplay(first = False, mode = 1, text = None):
        '''
        screendisplay(first:bool = False, mode:int = 1, text:str = None)
        Displays Choices.
        - Parameter:
            - first:bool: If first time executing.
            - mode:int:
                - mode 1 - choosing
                - mode 2 - choice verification
            - text:str: displays text if mode 2.
        '''
        if not first:
            ClearConsole()
        if mode != 2:
            mapDisplay(user_init, choice[user_destin][6:])
            Scenarios(user_init)
            for i in range(6):
                if i == user_destin:
                    print(f'         \033[4m> {choice[i]}\033[0m')
                else: print(f'        > {choice[i]}')
            print(ran.choice(['Tip: You can use up and down arrows and letters a to f to choose from the choices.', 'Tip: Press Enter to choose the underlined choice.', "Tip: The points you'll get depends heavily on how safe your destination is."]))
        else:
            ClearConsole()
            print(text)
        if not first:
            user_destin_real = Place_Number(choice[user_destin][6:])
            paths = PossiblePaths(arrangement)
            paths.RAPVars(Place_Number(user_init), user_destin_real)
            possible_paths = paths.PossiblePaths()
            numbered_possible_paths = paths.NumPossiblePaths()
            route_distances = RouteDistances(numbered_possible_paths, *[i.split(', ')[1:] for i in arrang_with_dist])
            recom_dist, recom_route = RouteRecomm(route_distances, possible_paths)
            recom_time = TimeNeeded(recom_dist)
            print("▓████████████████████████████████████████▓ROUTE INFORMATION▓████████████████████████████████████████▓")
            print(f'The path from {user_init} to {Place_Number(user_destin_real)} has the following possible routes with their distances:')
            print('\n'.join([f'\nPath #{h}: {i.replace(", ", " -> ")}\nDistance: {j} meters' for h, i, j in zip(range(1, len(possible_paths)+1), possible_paths, route_distances)]))
            print('\nThe recommended route and its distance is:')
            print(f'{recom_route.replace(", ", " -> ")}: {recom_dist} meters.')
            print('\nThe minimum time it would take to go there is:')
            print(f'{recom_time} with the speed of 0.1 meter per second.')
            print("▓███████████████████████████████████████████████████████████████████████████████████████████████████▓")
    def on_press(key):
        '''
        Reacts with the key listener and affects the ScreenMenu.
        '''
        global user_destin
        nonlocal chosen
        if chosen: return makesure(key)
        if key == keyboard.Key.up:
            sound.playsound('click', 'sfx')
            user_destin -= 1
            if user_destin == -1: user_destin = 5
        elif key == keyboard.Key.down:
            sound.playsound('click', 'sfx')
            user_destin += 1
            if user_destin == 6: user_destin = 0
        elif key == keyboard.Key.enter:
            sound.playsound('click', 'sfx')
            chosen = True
            screendisplay()
            screendisplay(mode = 2, text = "Are you sure of your answer?".center(100)+"\n                                           Yes        \033[4mNo\033[0m")
            return
        else:
            try:
                if   key.char in ['a', 'A']: user_destin = 0
                elif key.char in ['b', 'B']: user_destin = 1
                elif key.char in ['c', 'C']: user_destin = 2
                elif key.char in ['d', 'D']: user_destin = 3
                elif key.char in ['e', 'E']: user_destin = 4
                elif key.char in ['f', 'F']: user_destin = 5
                else: return
            except: return
        screendisplay()
        time.sleep(.3)
    def makesure(key):
        '''
        makesure(key)
        Makes sure of user's destination.
        '''
        global user_destin
        nonlocal chosen, sure
        if key == keyboard.Key.left:
            sound.playsound('click', 'sfx')
            sure = True
            screendisplay(mode = 2, text = "Are you sure of your answer?".center(100)+"\n                                           \033[4mYes\033[0m        No")
        elif key == keyboard.Key.right:
            sound.playsound('click', 'sfx')
            sure = False
            screendisplay(mode = 2, text = "Are you sure of your answer?".center(100)+"\n                                           Yes        \033[4mNo\033[0m")
        elif key == keyboard.Key.enter:
            sound.playsound('click', 'sfx')
            if sure:
                user_destin = choice[user_destin][6:]
                return False
            else:
                chosen = False
                screendisplay()

    print("Please select where to evacuate:")
    choice = choices()
    chosen = False
    sure = False
    screendisplay(True)
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
def RouteRecomm(distances, routes) -> list:
    '''
    RouteRecomm(distances:list[int], routes:list[str]) -> list[int|str]

    Returns recommended route and its distance from the list.
    - Parameter:
        - distances:list[int]: list of distances.
        - routes:list[str]: list of routes.
    '''
    recommended = min(distances)
    ind = distances.index(recommended)
    recomm_route = routes[ind]
    return recommended, recomm_route 
def Place_Number(place):
    '''
    Place_Number(place:str|int)->str|int

    Converts place to index or vice versa.
    - Parameters:
        - place:str|int: place or index.
    '''
    try:
        place.isalpha() #checks if place is string (Goes to except if not)
        return ["Forest", "Park", "Mall", "Home", "Mountains", "Beach", "School"].index(place)
    except: return ["Forest", "Park", "Mall", "Home", "Mountains", "Beach", "School"][place]
def RouteDistances(routes, Ne0, Ne1, Ne2, Ne3, Ne4, Ne5, Ne6)->list:
    '''
    RouteDistances(routes:list[str], Ne0, Ne1, ..., Ne6:list[str])->list

    Computes the distances of each routes.
    - Parameters:
        - routes:list[str]: list of routes the user will take.
        - Ne0, Ne1, ..., Ne6:list[str]: contains the list of all 7 connected sites.
    '''
    distances = []
    for route in routes:
        routelist = route.split(', ')
        distance = 0
        for i in range(len(routelist)-1):
            for j in eval(f'Ne{routelist[i]}'):
                if j.partition(':')[0] == routelist[i+1]:
                    distance += int(j.partition(':')[-1])
                    break
        distances.append(distance)
    return distances
def TimeNeeded(distance)->str:
    '''
    TimeNeeded(distance:int)->str

    Calculates the time needed to reach a destination in hours and a speed of 0.1m/min.
    returns a 2-decimal-point time.
    - Parameter:
        - distance:int: distance to convert into time
    '''
    time = distance/0.1
    time = time/60
    return '%.2f hours'%time
def PointRank(user_init, user_destin)->int:
    '''
    PointRank(user_init:str, user_destin:str)->int

    Returns the corresponding points of their destination.
    - Parameter:
        - user_init:str: initial position of user.
        - user_destin:str: destination of user.
    '''
    if user_init == 'Forest':
        if user_destin == 'Home': return 10
        elif user_destin == 'Beach': return 10
        elif user_destin == 'Mall': return 8
        elif user_destin == 'School': return 6
        elif user_destin == 'Mountains': return 2
        elif user_destin == 'Park': return 2
    elif user_init == 'Park':
        if user_destin == 'Mall': return 10
        elif user_destin == 'Home': return 8
        elif user_destin == 'School': return 6
        elif user_destin == 'Forest': return 6
        elif user_destin == 'Mountains': return 4
        elif user_destin == 'Beach': return 2
    elif user_init == 'Mall':
        if user_destin == 'School': return 10
        elif user_destin == 'Home': return 8
        elif user_destin == 'Park': return 6
        elif user_destin == 'Mountains': return 4
        elif user_destin == 'Beach': return 2
        elif user_destin == 'Forest': return 0
    elif user_init == 'Home': 
        if user_destin == 'School': return 10
        elif user_destin == 'Mall': return 8
        elif user_destin == 'Mountains': return 4
        elif user_destin == 'Beach': return 2
        elif user_destin == 'Park': return 2
        elif user_destin == 'Forest': return 0
    elif user_init == 'Mountains':
        if user_destin == 'Home': return 10
        elif user_destin == 'School': return 8
        elif user_destin == 'Mall': return 6
        elif user_destin == 'Forest': return 4
        elif user_destin == 'Beach': return 2
        elif user_destin == 'Park': return 2
    elif user_init == 'Beach': 
        if user_destin == 'Mountains': return 10
        elif user_destin == 'Mall': return 8
        elif user_destin == 'Home': return 6
        elif user_destin == 'School': return 6
        elif user_destin == 'Forest': return 4
        elif user_destin == 'Park': return 2
    elif user_init == 'School':
        if user_destin == 'Home': return 10
        elif user_destin == 'Mall': return 8
        elif user_destin == 'Park': return 2
        elif user_destin == 'Mountains': return 2
        elif user_destin == 'Forest': return 2
        elif user_destin == 'Beach': return 2
def AssessmentResult(points)->None:
    '''
    AssessmentResult(points:int)->None

    Assesses the result of the game according to points.
    - Parameters:
        - points:int: points to assess.
    '''
    sound.playsound('about', 'bgm')
    if 0 <= points <= 14:
        print(f"You got a total of \033[91m{points}\033[0m.\nI recommend you do your research on preparedness in case of emergency. We left links on the main menu.")
    elif 15 <= points <= 28:
        print(f"You got a total of \033[95m{points}\033[0m.\nBe serious, polite and careful to your decisions. Don't try to panic and don't jump ship.")
    elif 29 <= points <= 42:
        print(f"You got a total of \033[93m{points}\033[0m.\nGood you're doing great! Learn more!")
    elif 43 <= points <= 56:
        print(f"You got a total of \033[94m{points}\033[0m.\nVery good! You're choosing and planning ability are insane! Keep it up!")
    elif 57<= points <= 70:
        print(f"You got a total of \033[92m{points}\033[0m.\nExcellent! You're very aware on calamity safety!")
    
    print('Press Spacebar to continue...')
    def on_press(k):
        if k == keyboard.Key.space: return False
    with keyboard.Listener(on_press=on_press) as listener: listener.join()
def Answers()->None:
    '''
    Answers()->None

    Displays all the ranked answers to this game.
    '''
    ClearConsole()
    sound.playsound('answers', 'bgm')
    print("""
█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
█   Best Places for each scenarios:                                                                █
█       Forestfires or wildfires:                                                                  █
█           - It is best to stay indoors and lock up all possible entrances for smoke.             █
█           - It is also great to go somewhere that there are strong  winds  that  can             █
█             blow away smokes.                                                                    █
█       Heatwave:                                                                                  █
█           - It is best to  stay  cool.  Go to  places  where there are either proper             █
█             ventilation or airconditioning.                                                      █
█       Earthquake:                                                                                █
█           - After the earthquake, it is best to go to an large open space and there              █
█           are no buildings nearby that can possibly collapse onto you.                           █
█       Storm:                                                                                     █
█           - It is best to stay at home during storms. But whenever the storm is too              █
█             dangerous to even stay in your home,  go  to  an  announced  evacuation              █
█             center.                                                                              █
█       Volcanic Eruption:                                                                         █
█           - It is best to move somewhere away from the  volcano.  But  if  you  are              █
█             seeking immediate  shelter  and  there are currently volcanic ashes and              █
█             debris, it is best to stay indoors  and  close  all  possible entrances              █
█             for volcanic spews.                                                                  █
█       Tsunami:                                                                                   █
█           - During a tsunami, it is best to go miles away from the seashore.                     █
█           - If the previous is not an option, then go to a  place 100  feet  higher              █
█             than sea level.                                                                      █
█       Tornado:                                                                                   █
█           - It is always best to be on the lowest floor in a solid building.                     █
█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
█       Disclaimer:                                                                                █
█           - In some calamities mentioned, e.g., tornado, it is best  to  stay where              █
█             you are. This game is meant to demonstrate the concept of a map and the              █
█             retrieval  of  all  possible  routes  to a destination. Thus, this game              █
█             required  you  to  switch  to  another place, other than the one you are             █
█             currently in, where you think is safe.                                               █
█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
""")
    print('Press Esc to exit...')
    def on_press(k):
        if k == keyboard.Key.esc:
            sound.playsound('click', 'sfx')
            return False
    with keyboard.Listener(on_press=on_press) as listener: listener.join()
    ClearConsole()
def BGMPlayer(place)->None:
    '''
    BGMPlayer(place:str)->None

    Plays the appropriate background music for each places.
    - Parameter:
        - place:str: a string value that contains where the current
                 position of the player is and what background
                 music to play.
    '''
    if place == 'Forest': sound.playsound('forestfire', 'bgm')
    elif place == 'Park': sound.playsound('heatwave', 'bgm')
    elif place == 'Mall': sound.playsound('earthquake', 'bgm')
    elif place == 'Home': sound.playsound('storm', 'bgm')
    elif place == 'Mountains': sound.playsound('volcano', 'bgm')
    elif place == 'Beach':
        sound.playsound('tsunami-bg', 'bgm')
        sound.playsound('tsunami', 'sfx')
    elif place == 'School': sound.playsound('tornado', 'bgm')
#Setup Window
kb = conkb()
kb.tap(keyboard.Key.f11)
newmenu = True
sound = Sounds()
ClearConsole()
sound.playsound('title', 'sfx')
sound.playsound('menu', 'bgm')
#Main Menu
while True:
    ClearConsole()
    sound.playsound('menu', 'bgm')
    kb.tap('a') #activate console screen (bug)
    Menuchoice = 0
    MainMenu(1)
    if Menuchoice == "A": break
    elif Menuchoice == "B": AboutGame()
    elif Menuchoice == "C": Resources()
    elif Menuchoice == "D":
        kb.tap(keyboard.Key.f11)
        sound.playsound('click', 'sfx')
        exit()
#MAIN CODE
arrangement = ["0, 5, 6", "1, 0, 2, 3, 6", "2, 1, 3, 4", "3, 2", "4, 5, 6", "5, 6", "6, 1, 4, 5"]
uniqueroads = ["05", "06", "10", "12", "13", "16", "23", "24", "45", "46", "56"]
while True:
    ClearConsole()
    #Display overview of game
    sound.playsound('waitingscreen', 'bgm')
    print("""
█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
█                                           -~OVERVIEW~-                                           █                         
█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
█       The  game starts  with  you,  the  player,  on  a  random location where the calamity is   █
█   happening. You  need  to  decide  where is the safest target destination for you to go. Each   █
█   location has  a  corresponding point, being the most secured place, and the opposite for the   █
█   less secured  site.  Once you chose a certain location, the points will be displayed and the   █
█   next calamity scenario will follow soon after.                                                 █
█                                                                                                  █
█       The  safest  place hunting cycle will continue until the last calamity is finished. Once   █
█   done, the points will be accumulated and displayed on the console with acknowledgement based   █
█   on your score.                                                                                 █
█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
""")
    loading = ['| ', '/ ', '-- ', '\\ ', '| ']
    for i in range(5, 0, -1):
        for j in range(5):
            print(f'Proceeding in {i} {loading[j]}', end = '\r')
            time.sleep(.2)
    
    #Initialize variables:
    #   Buildings - contains all string value of buildings.
    #   rand_user_init - contains an exact copy of buildings. Used for randomizing player position and keeps tracks of what buildings are already played.
    #   total_points - accumulates the points that the user gets throughout the game.
    buildings = ["Forest", "Park", "Mall", "Home", "Mountains", "Beach", "School"]
    rand_user_init = buildings.copy()
    total_points = 0
    
    #Start of game cycle
    for _ in range(7):
        ClearConsole()
        arrang_with_dist = RandomBuild(arrangement)
        user_init = ran.choice(rand_user_init)
        rand_user_init.remove(user_init)
        BGMPlayer(user_init)
        connections = []
        for i in arrang_with_dist:
            i = i.split(', ')
            for j in i[1:]:
                if i[0]+j.partition(':')[0] in uniqueroads:
                    connections.append(j.partition(':')[-1])
        user_destin = 0
        DisplayChoices(user_init)
        sound.stopall()
        sound.playsound('nextround', 'bgm')
        round_points = PointRank(user_init, user_destin)
        total_points += round_points
        ClearConsole() #per second -> per minute
        print(f'                               You got: {round_points} points!\n                               Your current point is: {total_points}.')
        for i in range(3,0,-1):
            print(f'Proceeding in {i}...', end="\r")
            time.sleep(1)
    ClearConsole()
    AssessmentResult(total_points)
    while True:
        ClearConsole()
        sound.playsound('menu', 'bgm')
        Menuchoice = 0
        MainMenu(2 if newmenu else 3)
        if Menuchoice == "A": break
        elif Menuchoice == "B":
            newmenu = False
            Answers()
        elif Menuchoice == "C": AboutGame()
        elif Menuchoice == "D": Resources()
        elif Menuchoice == "E": 
            kb.tap(keyboard.Key.f11)
            sound.playsound('click', 'sfx')
            exit()