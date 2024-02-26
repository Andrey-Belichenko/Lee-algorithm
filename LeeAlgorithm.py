from PIL import Image, ImageDraw, ImageFont

"""
                            Intput map 
        0 - free place | 1 - start point | x - wall | b - exit
"""
Place_1=[[0,  0,0,0,'x',  0,0,0,  0,  0,  0,  0,0,  0,0,0],
         [0,  0,0,0,'x',  0,0,0,  0,  0,  0,  0,0,'b',0,0],
         [0,  0,0,0,'x',  0,0,0,  0,  0,  0,  0,0,  0,0,0],
         [0,  1,0,0,'x',  0,0,0,  0,  0,  0,'x',0,  0,0,0],
         [0,  0,0,0,'x',  0,0,0,  0,'x','x','x',0,  0,0,0],
         [0,  0,0,0,'x',  0,0,0,  0,'x','x','x',0,  0,0,0],
         [0,  0,0,0,'x',  0,0,0,'x','x','x','x',0,  0,0,0],
         [0,  0,0,0,'x',  0,0,0,'x','x','x','x',0,  0,0,0],
         [0,  0,0,0,'x',  0,0,0,  0,'x','x','x',0,  0,0,0],
         [0,  0,0,0,'x',  0,0,0,  0,  0,'x','x',0,  0,0,0],
         [0,  0,0,0,  0,'x',0,0,  0,  0,'x','x',0,  0,0,0], 
         [0,  0,0,0,  0,'x',0,0,  0,  0,'x','x',0,  0,0,0],
         [0,  0,0,0,  0,  0,0,0,  0,  0,'x','x',0,  0,0,0],
         [0,  0,0,0,  0,  0,0,0,  0,  0,  0,'x',0,  0,0,0],
         [0,  0,0,0,  0,  0,0,0,  0,  0,  0,'x',0,  0,0,0],
         [0,  0,0,0,  0,  0,0,0,  0,  0,  0,  0,0,  0,0,0]]

# Creating background 
PL = Image.new('RGB', (1600, 1600), (255,255,255))
re_PL = ImageDraw.Draw(PL)
front = ImageFont.truetype("arial.ttf", 50)


def ShowPlace(Place):
    """
    Space marking function
    input: map (Two-dimensional list)
    """
    n = 0
    for i in Place:
        n += 1
        m = 0
        for j in i:
            m += 1
            if j == 'x':
                re_PL.rectangle((m*100-100, n*100-100, m*100, n*100), fill='black', outline=(255, 255, 255))
            elif j == 1 or j == 'b':
                re_PL.rectangle((m*100-100, n*100-100, m*100, n*100), fill='yellow', outline=(0, 0, 0))
                re_PL.text((m*100-80, n*100-80), str(j), fill='black', font=front)
            else:
                re_PL.rectangle((m*100-100, n*100-100, m*100, n*100), fill='white',outline=(0, 0, 0))
                re_PL.text((m*100-80, n*100-80), str(j), fill='black', font=front)


def start_point(Place):
    """
    Start point finding on map
    input: map (Two-dimensional list)
    return: start point cords 
    """
    n = 0
    for i in Place:
        n += 1
        m = 0
        for j in i:
            m += 1
            if j == 1:
                point_s = (Place.index(i),i.index(j))
    return point_s
 

def point_min(s_i, s_j):
    """
    Finding minimal point around current 
    """
    cord_dict = {Place_1[s_i-1][s_j]:[s_i-1,s_j],    
                 Place_1[s_i][s_j+1]:[s_i,s_j+1],
                 Place_1[s_i+1][s_j]:[s_i+1,s_j],
                 Place_1[s_i][s_j-1]:[s_i,s_j-1]}
    if 'x' in cord_dict.keys():
        del cord_dict['x']
    if 'b' in cord_dict.keys():
        del cord_dict['b']
    m = min(cord_dict.keys())
    for k in cord_dict.keys():
        if k == m:
            start_cords = cord_dict[k]
            start_point_i = start_cords[0]
            start_point_j = start_cords[1]
            return ([start_point_i, start_point_j, m])


def trail_painting(way):
    """
    Function for colorizing way-points 
    input: way = [(first_way_i_cord, first_way_j_cord, value_at_cords), .... ,(last_way_i_cord, last_way_j_cord, value_at_cords)]
    """
    for cords in way:           # cords = (way_i_cord, way_j_cord, value_at_cords)
        x = cords[1] + 1
        y = cords[0] + 1
        re_PL.rectangle((x*100-100, y*100-100, x*100, y*100), fill='red', outline=(0, 0, 0))
        re_PL.text((x*100-80, y*100-80), str(cords[2]), fill='black', font=front)


# way tracing 

max_way_length = 50             # Wave length
start_point_cords = start_point(Place_1)  # Start point (b)
width = len(Place_1[0])         
height = len(Place_1)           

p_s = 1             
# placing way points from start (1) to finish ('b')            
for k in range(max_way_length):
    for i in range(height):     
        for j in range(width):  
            if Place_1[i][j] == p_s:
                if j < 15 and Place_1[i][j+1] == 0:
                    Place_1[i][j+1] = p_s + 1
                if j > 0 and Place_1[i][j-1] == 0:
                    Place_1[i][j-1] = p_s + 1 
                if i < 15 and Place_1[i+1][j] == 0:
                    Place_1[i+1][j] = p_s + 1
                if i > 0 and Place_1[i-1][j] == 0:
                    Place_1[i-1][j] = p_s + 1
    p_s = p_s + 1

# find finish
p_e = 'b'                       # End point (b)
for i in range(height):
    for j in range(width):
        if Place_1[i][j] == p_e:
            s_i = i
            s_j = j


# Counting best 'first step' from 'b'
start_point_i, start_point_j, step_value = point_min(s_i, s_j)
way = []                        # cords list    way = [(first_way_i_cord, first_way_j_cord, value_at_cords), .... ,(last_way_i_cord, last_way_j_cord, value_at_cords)]


way.append((start_point_i, start_point_j, step_value)) 

for k in range(max_way_length):
    # using poin_min for find best next step 
    start_point_i, start_point_j, step_value = point_min(start_point_i, start_point_j)

    if (start_point_i, start_point_j) == start_point_cords:
        break
    else:
        way.append((start_point_i, start_point_j, step_value))



ShowPlace(Place_1)              
trail_painting(way)             
PL.show()                       # screen output
