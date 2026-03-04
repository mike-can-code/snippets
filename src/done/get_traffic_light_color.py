def get_traffic_light_color(perc: Union[float, int, str]) -> str:
    color = ( 'Green'  if perc >=85  else
              'Yellow' if perc >=70  else
              'Red'    if perc >=50  else
              'Black'  if perc < 50  else
             )
    return color
