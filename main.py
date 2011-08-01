from coordination import wire, runtime
import msvspyproj

if __name__ == '__main__':
    msvspyproj.magick()
    from test.texteditor import main
    main.main()