from pyfiglet import Figlet
import sys, random

figlet = Figlet()
if len(sys.argv) == 1 or (len(sys.argv) == 3 and sys.argv[1] in ("-f", "--font") and sys.argv[2] in figlet.getFonts()):
    figlet.setFont(font=(random.choice(figlet.getFonts()) if (len(sys.argv) == 1) else sys.argv[2]))
    print("Output:\n" + figlet.renderText(input("Input: ")))
else:
    print("Invalid usage")
    sys.exit(1)
