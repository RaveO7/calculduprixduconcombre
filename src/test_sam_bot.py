from sambot.window import Window
import sambot.controls

foreground= Window.get_foreground()
screenshot= foreground.screenshot()
screenshot.show()