from colorama import Fore, Style
import colorsys, time, os

def closest_color(rgb):
    color_dict = {
        Fore.BLACK: (0, 0, 0),
        Fore.RED: (255, 0, 0),
        Fore.GREEN: (0, 255, 0),
        Fore.YELLOW: (255, 255, 0),
        Fore.BLUE: (0, 0, 255),
        Fore.MAGENTA: (255, 0, 255),
        Fore.CYAN: (0, 255, 255),
        Fore.WHITE: (255, 255, 255),
    }

    color_percentages = {}
    for color in color_dict:
        difference_tuple = tuple(map(lambda i, j: i - j, rgb, color_dict[color]))
        distance = 0
        for value in difference_tuple:
            distance += abs(value)

        percentage = 1 - (distance / ((255 * 1) * 3))
        color_percentages[color] = percentage
        
    color_percentages = dict(sorted(color_percentages.items(), key=lambda item: item[1],reverse=True))
    actual_percentages = {}

    primary_weight = color_percentages[list(color_percentages.keys())[0]]
    actual_percentages[list(color_percentages.keys())[0]] = color_percentages[list(color_percentages.keys())[0]]

    for color in color_percentages:
        if primary_weight >= 1:
            break
        if (1 - primary_weight) * 5 > color_percentages[color]:
            break

        actual_percentages[color] = color_percentages[color]
    
    weight_sum = sum(list(actual_percentages.values()))

    for color in actual_percentages:
        actual_percentages[color] = actual_percentages[color] / weight_sum
    
    return actual_percentages


def colorize_text(text, rgb):
    closest_match = closest_color(rgb)
    
    return apply_prefixes(text, closest_match) + Style.RESET_ALL

def apply_prefixes(string, prefix_dict:dict):
    values = list(prefix_dict.values())
    keys = list(prefix_dict.keys())

    new = []
    
    # set all chars to the primary color initially
    for char in string:
        new.append({"text":char,"color":keys[0]})

    # find out which other colors to mix in
    for color, weight in prefix_dict.items():
        if color == keys[0]:
            continue # skip first since we already set colors to that

        if weight == 0:
            continue
            # avoid divison by 0

        frequency = int(len(string) / (len(string) * weight))

        for index, item in enumerate(new):
            if (index + 1) % frequency == 0:
                item["color"] = color
                # at every frequency:th item in array, set that to color


    raw = ""
    for part in new:
        raw += part["color"] + part["text"]

    return raw
    

def hue_shift(rgb, shift_value):
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + shift_value) % 1.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    r, g, b = [int(x * 255.0) for x in (r, g, b)]

    return r, g, b

def run_example():
    color = (199,255,0)
    while True:
        time.sleep(0.1)
        os.system("cls")
        text = '''                              ████████████                        
                        ████████████████████████                  
                    ████████████████████████████████              
                  ████████████████████████████████████            
                ████████████████████████████████████████          
              ████████████████████████████████████████████        
            ████████████████████████████████████████████████      
          ████████████████████████████████████████████████████    
          ████████████████████████████████████████████████████    
        ████████████████████████████████████████████████████████  
        ████████████████████████████████████████████████████████  
        ████████████████████████████████████████████████████████  
      ████████████████████████████████████████████████████████████
      ████████████████████████████████████████████████████████████
      ████████████████████████████████████████████████████████████
      ████████████████████████████████████████████████████████████
      ████████████████████████████████████████████████████████████
      ████████████████████████████████████████████████████████████
        ████████████████████████████████████████████████████████  
        ████████████████████████████████████████████████████████  
        ████████████████████████████████████████████████████████  
          ████████████████████████████████████████████████████    
          ████████████████████████████████████████████████████    
            ████████████████████████████████████████████████      
              ████████████████████████████████████████████        
                ████████████████████████████████████████          
                  ████████████████████████████████████            
                    ████████████████████████████████              
                        ████████████████████████                  
                              ████████████                        '''
        print(colorize_text(text,color), flush=False)
        color = hue_shift(color,0.01)

if __name__ == "__main__":
    run_example()