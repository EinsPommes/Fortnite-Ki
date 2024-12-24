import pyautogui
import keyboard
import mouse
import time

class FortniteControls:
    def __init__(self):
        # Konfiguration der Steuerung
        self.key_bindings = {
            'forward': 'w',
            'backward': 's',
            'left': 'a',
            'right': 'd',
            'jump': 'space',
            'build_wall': 'q',
            'build_ramp': 'f',
            'build_floor': 'c',
            'edit': 'g',
            'reload': 'r',
            'inventory': 'tab',
            'crouch': 'ctrl'
        }
        
        # Maussensitivität
        self.mouse_sensitivity = 1.0
        pyautogui.FAILSAFE = True
        
    def move(self, direction, duration=0.1):
        """Bewegung in eine bestimmte Richtung."""
        key = self.key_bindings.get(direction)
        if key:
            keyboard.press(key)
            time.sleep(duration)
            keyboard.release(key)
            
    def look_at(self, x, y):
        """Bewege die Maus zu einer bestimmten Position."""
        current_x, current_y = pyautogui.position()
        pyautogui.moveRel(
            (x - current_x) * self.mouse_sensitivity,
            (y - current_y) * self.mouse_sensitivity,
            duration=0.1
        )
        
    def shoot(self, duration=0.1):
        """Schieße für eine bestimmte Zeit."""
        mouse.press(button='left')
        time.sleep(duration)
        mouse.release(button='left')
        
    def build(self, structure_type):
        """Baue eine bestimmte Struktur."""
        key = self.key_bindings.get(f'build_{structure_type}')
        if key:
            keyboard.press(key)
            mouse.click(button='left')
            keyboard.release(key)
            
    def edit(self, edit_pattern):
        """Führe ein Gebäude-Edit aus."""
        # Editiermodus aktivieren
        keyboard.press(self.key_bindings['edit'])
        time.sleep(0.05)
        
        # Edit-Muster ausführen
        for point in edit_pattern:
            pyautogui.moveTo(point[0], point[1])
            mouse.press(button='left')
            time.sleep(0.05)
            mouse.release(button='left')
            
        # Edit bestätigen
        keyboard.press(self.key_bindings['edit'])
        keyboard.release(self.key_bindings['edit'])
        
    def switch_weapon(self, slot):
        """Wechsle zur Waffe in einem bestimmten Slot."""
        if 1 <= slot <= 5:
            keyboard.press(str(slot))
            keyboard.release(str(slot))
            
    def perform_action(self, action_vector):
        """Führe eine Aktion basierend auf dem KI-Aktionsvektor aus."""
        # Aktionsvektor: [vorwärts, rückwärts, links, rechts, springen, schießen, bauen, editieren]
        if action_vector[0]: self.move('forward')
        if action_vector[1]: self.move('backward')
        if action_vector[2]: self.move('left')
        if action_vector[3]: self.move('right')
        if action_vector[4]: keyboard.press(self.key_bindings['jump'])
        if action_vector[5]: self.shoot()
        if action_vector[6]: self.build('wall')  # Standard: Wand
        if action_vector[7]: self.edit([[960, 540]])  # Standard: Mittleres Edit
