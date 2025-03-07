import sys
import pyttsx


# main() function
def main():
    # use sys.argv if needed
    print
    'running speech-test.py...'
    engine = pyttsx.init()
    str = "I speak. Therefore. I am.  "
    if len(sys.argv) > 1:
        str = sys.argv[1]
    engine.say(str)
    engine.runAndWait()


# call main
if __name__ == '__main__':
    main()
