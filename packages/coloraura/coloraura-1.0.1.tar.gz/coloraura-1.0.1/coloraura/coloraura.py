class Styler:
    def __init__(self):
        self.colors = {
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m',
            'reset': '\033[0m',
            'bright_black': '\033[90m',
            'bright_red': '\033[91m',
            'bright_green': '\033[92m',
            'bright_yellow': '\033[93m',
            'bright_blue': '\033[94m',
            'bright_magenta': '\033[95m',
            'bright_cyan': '\033[96m',
            'bright_white': '\033[97m'
        }
        self.reset = False

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_ansi(self, rgb_color):
        r, g, b = rgb_color
        return f'\033[38;2;{r};{g};{b}m'

    def format_color(self, text, color):
        return f"{self.colors.get(color, '')}{text}{self.colors['reset']}"

    def apply_gradient(self, text, start_color, end_color):
        start_rgb = self.hex_to_rgb(start_color)
        end_rgb = self.hex_to_rgb(end_color)
        gradient = [self.rgb_to_ansi((
            int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / len(text)),
            int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / len(text)),
            int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / len(text))
        )) for i in range(len(text))]
        return ''.join(f"{gradient[i]}{char}" for i, char in enumerate(text)) + self.colors['reset']

    def apply_style(self, text, style):
        styles = {
            'strikethrough': '\033[9m',
            'bold': '\033[1m',
            'italic': '\033[3m',
            'reset': '\033[0m'
        }
        return f"{styles.get(style, '')}{text}{styles['reset'] if self.reset else ''}"

    def style(self, text, color=None, gradient=None, style=None):
        if gradient:
            start_color, end_color = gradient
            text = self.apply_gradient(text, start_color, end_color)
        if color:
            text = self.format_color(text, color)
        if style:
            text = self.apply_style(text, style)
        return text

# Define the instances
gradient = Styler()
color = Styler()
style = Styler()

# Set reset to True by default
color.reset = True
gradient.reset = True
style.reset = True
