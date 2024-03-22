"""
config? yes, config.
"""
class AnsiCode:
    '''
    Ansi codes.
    '''
    class CSI:
        moveup          = "\033[%dA"
        movedown        = "\033[%dB"
        moveforward     = "\033[%dC"
        moveback        = "\033[%dD"

        movedownline    = "\033[%dE"
        moveupline      = "\033[%dF"

        clear           = "\033[%dJ"
    class Fore:
        '''
        Text colors
        '''
        RED                 = '\033[31m'
        BLUE                = '\033[34m'
        LB                  = '\033[94m'
        LBLK                = '\033[90m'
        WHITE               = '\033[37m'
        BLACK               = '\033[30m'
        LY                  = '\033[93m'
        RESET               = '\033[39m'

    class Style:
        '''
        Text Styles
        '''
        BRIGHT              = '\033[1m'
        DIM                 = '\033[2m'
        NORMAL              = '\033[22m'
        RESET_ALL           = '\033[0m'