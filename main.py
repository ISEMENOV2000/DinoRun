# Arkanoid.py
# Author: Kateryna Kharkivska (G21062212)
# Email: kkharkivska@uclan.ac.uk
# Description: The Arkanoid.py program demonstrates

from tkinter import *


TITLE = 'Arkanoid Game'
WIDTH = 800
HEIGHT = 600

BALL_RADIUS = 10

DEFAULT_SPEED = 5
DEFAULT_BALL_RADIUS = 10
DELAY = 20

BRICK_COLORS = ['PeachPuff3', 'dark slate gray', 'rosy brown', 'light goldenrod yellow',
                'turquoise3']  # a brick colors for eache of the five rows
bricks = []  # a list to keep the drawn bricks

score_value = 0  # Initialises the value for the score
score_in_text = score_value


balls = []
drawn_rectangles = []  # a list to keep the craft
drawn_circles = []  # a list to keep the drawn circles
MAX_SIZE = 1
MAX_SIZE_B = 5  # a maximum number of drawn circles that can be kept on the screen
rect_w = 90

# Creates the window
win = Tk()
win.title(TITLE)
win.geometry(str(WIDTH) + "x" + str(HEIGHT))

# Creates and packs the canvas
canvas = Canvas(win, width=WIDTH, height=HEIGHT)
canvas.pack()

text_score = canvas.create_text(43, HEIGHT - 15, text=('Score: ' + str(score_in_text)), font=('Italic', 15),
                                fill='white')
text_level = canvas.create_text(WIDTH / 2, HEIGHT - 400, text='LEVEL 1', font=('Italic', 14), fill='white')
canvas.config(bg='black')  # a custom background

print('If you want to exit the Game, please enter: x')
print('To move the  craft hover mouse left and right')

# The Ball class was adapted from the Collisions.py under Week 3, step 0306
class Ball:

    def __init__(self, ball_x, ball_y, speed_x, speed_y, ball_r, color_ball):  # this function sets the values
        self.x = ball_x
        self.y = ball_y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = ball_r
        self.color = color_ball
        self.score = 0
        self.level_counter = 0



    def move(self):  # this function moves the ball inside the window
        # first update the X...
        global p
        self.x = self.x + self.speed_x
        # ...then make sure that if it bounces, the horizontal speed is reversed
        if self.x >= WIDTH - self.radius:
            self.speed_x = -abs(self.speed_x)
        if self.x <= self.radius:
            self.speed_x = abs(self.speed_x)
        # next update the Y...
        self.y = self.y + self.speed_y
        # ...and make sure that if it bounces, the vertical speed is reversed
        # if self.y >= HEIGHT - self.radius:
        #     self.speed_y = -abs(self.speed_y)
        if self.y <= self.radius:
            self.speed_y = abs(self.speed_y)
        #Check for vertical position collision
        if self.y + self.radius >= p.y_rec - p.height_rectangle / 2:
            #check if the ball collides with the craft in the x dimension
            if self.x + self.radius >= p.x_rec - p.width_rectangle / 2 and self.x - self.radius <= p.x_rec + p.width_rectangle / 2:
                #Reverse the speed of the ball (there is a collision)
                self.speed_y = -abs(self.speed_y)


    def draw(self):  # this function draws a circle and a small tail for it
        # this part of the code was adapted from the ManyCircles.py under Week 2, step 0206
        circle_id = canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, fill= self.color, outline='black')
        drawn_circles.append(circle_id)
        if len(drawn_circles) > MAX_SIZE_B:
            id_of_circle_to_be_deleted = drawn_circles.pop(0)
            canvas.delete(id_of_circle_to_be_deleted)

    def brick_hit(self):  # this function deletes the bricks when the ball has contact with one of them
        for h in bricks:
            x_h1, y_h1, x_h2, y_h2 = canvas.coords(h)
            if x_h1 <= self.x <= x_h2 and y_h1 <= self.y - self.radius <= y_h2 and self.speed_y <= 1:  # checks if the ball contacted the bottom side of the brick
                self.speed_y = abs(self.speed_y)  # speed y is changed
                canvas.delete(h)  # deletes one brick from the window
                bricks.pop(bricks.index(h))  # removes the brick from Bricks
                self.score += 10  # increases the value of the score by 10
            elif x_h1 <= self.x <= x_h2 and y_h1 <= self.y + self.radius <= y_h2 and self.speed_y >= 1:  # checks if the ball contacted the top side of the brick
                self.speed_y = abs(self.speed_y)  # speed y is changed
                canvas.delete(h)  # deletes one brick from the window
                bricks.pop(bricks.index(h))  # removes the brick from Bricks
                self.score += 10  # increases the value of the score by 10
            elif x_h1 <= self.x - self.radius <= x_h2 and y_h1 <= self.y <= y_h2 and self.speed_x <= 1:
                self.speed_x = abs(self.speed_x)  # changes only the horizontal speed
                canvas.delete(h)  # deletes one brick from the window
                bricks.pop(bricks.index(h))  # removes the brick from Bricks
                self.score += 10
            elif x_h1 <= self.x + self.radius <= x_h2 and y_h1 <= self.y <= y_h2 and self.speed_x >= 1:
                self.speed_x = abs(self.speed_x)  # changes only the horizontal speed
                canvas.delete(h)  # deletes one brick from the window
                bricks.pop(bricks.index(h))  # removes the brick from Bricks
                self.score += 10


    def levels(self):
        if self.score == 10 and self.level_counter == 0:
            self.level_counter = 1
            bri.draw_rectangle()
            self.speed_x += 12

            if self.level_counter == 1:
                canvas.delete(text_level)
                canvas.create_text(WIDTH / 2, HEIGHT - 400, text='LEVEL 2', font=('Italic', 14), fill='white')
                self.x = WIDTH / 2
                self.y = HEIGHT / 2
                width = 2

        if self.score == 2000 and self.level_counter == 1:
            canvas.delete(text_level)
            canvas.create_text(WIDTH / 2, HEIGHT - 400, text='LEVEL 3', font=('Italic', 14), fill='white')
            self.x = WIDTH / 2
            self.y = HEIGHT / 2
            self.speed_y += 6
            bri.draw_rectangle()




    def game_over(self):  # this function stops the game and prints the statement if the ball touches the bottom of the window
        if self.y == HEIGHT:
            self.speed_y = 0
            self.speed_x = 0
            canvas.create_text(WIDTH / 2, 275, text='Game Over!', font=('Italic', 20), fill='pale violet red')
            print('Game Over!')
        if self.score == 3000:
            self.x = WIDTH / 2
            self.y = HEIGHT / 2
            self.speed_x = 0
            self.speed_y = 0
            canvas.create_text(WIDTH / 2, 275, text='You Won!', font=('Italic', 20), fill='pale violet red')
            print('You Won!')



class Brick:

    def __init__(self, x_brick, y_brick, color_brick):  # this function sets the values
        self.x_brick = x_brick
        self.y_brick = y_brick
        self.color_brick = color_brick

    def draw_rectangle(self):  # his function draws and sets the colors for the bricks
        for i in range(0,1):
            for j in range(0, 20):
                self.color_brick = BRICK_COLORS[i]
                x_brick = j * 39.5
                y_brick = i * 24
                x_b1 = x_brick + 5
                y_b1 = y_brick + 5
                x_b2 = x_brick + self.x_brick
                y_b2 = y_brick + self.y_brick
                bricks.append(canvas.create_rectangle(x_b1, y_b1, x_b2, y_b2, fill=self.color_brick,
                                                      outline='white'))  # draws the rectangle in a bricks list


class Score:  # this class counts and draws the score

    def __init__(self):  # this function sets a value for the class
        self.score = 0

    def score_count(self):  # this function counts the score and after draws it
        self.score = b.score
        canvas.itemconfig(text_score, text=('Score: ' + str(self.score)), font=('Italic', 13), fill='white')


    def level(self):  # this function reprints levels
        self.score = b.score
        if b.score == 10:  # checks if score is equal to 1000
            canvas.delete(text_level)  # deletes first level
            canvas.itemconfig(text_level, text='LEVEL 2', font=('Italic', 14), fill='white')  # configuring second level
        if b.score == 2000:  # checks if score is equal to 2000
            canvas.delete(text_level)  # deletes second level
            canvas.itemconfig(text_level, text='LEVEL 3', font=('Italic', 14), fill='white')  # configuring third level
        """
        if b.score == 3000:  # checks if score is equal to 3000
            canvas.delete(text_level)  # deletes third level
            canvas.itemconfig(text_level, text='You Won!', font=('Italic', 14), fill='white')  
        """

class Craft:
    def __init__(self, width_rectangle, height_rectangle, x_rec, y_rec,
                 color_pad):  # this function sets values for the class
        self.width_rectangle = width_rectangle
        self.height_rectangle = height_rectangle
        self.x_rec = x_rec
        self.y_rec = y_rec
        self.color_pad = color_pad
        self.canvas_object_p = canvas.create_rectangle(self.x_rec - width_rectangle / 2,
                                                       self.y_rec - height_rectangle / 2,
                                                       self.x_rec + width_rectangle / 2,
                                                       self.y_rec + height_rectangle / 2, fill=color_pad,
                                                       outline='black')

    def p_move(self, event):  # this function moves the craft left and right
        global p
        mouse_x = event.x
        self.x_rec = event.x
        canvas.delete(self.canvas_object_p)
        if mouse_x > self.width_rectangle / 1.8 and mouse_x <= WIDTH - self.width_rectangle / 1.8:
            pad_id = canvas.create_rectangle(mouse_x - self.width_rectangle / 2, self.y_rec - self.height_rectangle / 2,
                                             mouse_x + self.width_rectangle / 2, self.y_rec + self.height_rectangle / 2,
                                             fill=self.color_pad, outline='white')
            drawn_rectangles.append(pad_id)
            if len(drawn_rectangles) > MAX_SIZE:
                id_of_rectangle_to_be_deleted = drawn_rectangles.pop(0)
                canvas.delete(id_of_rectangle_to_be_deleted)

    def p_draw(self):  # this function draws rectangle in the center of the window
        canvas.coords(self.canvas_object_p, self.x_rec - self.width_rectangle / 2,
                      self.y_rec - self.height_rectangle / 2, self.x_rec + self.width_rectangle / 2,
                      self.y_rec + self.height_rectangle / 2)



b = Ball(ball_x=WIDTH / 2, ball_y=HEIGHT / 2, speed_x=5, speed_y=5, ball_r=BALL_RADIUS,
         color_ball='red')  # sents values to the Ball class
balls.append(b)
s = Score()  # sents values to the Score class
p = Craft(width_rectangle=90, height_rectangle=10, x_rec=WIDTH / 2, y_rec=HEIGHT - 10,
          color_pad='DarkSeaGreen1')  # sents values to the Craft class

bri = Brick(39.5, 24, BRICK_COLORS)  # sents values to the Brick class


def p_movement(event):  #this function calls all the required functions in the craft class
    p.p_move(event)
    p.p_draw()


def animation():  # this function calls all the required functions in the ball,score classes
    global balls
    for b_n in balls:
        b_n.brick_hit()
        b_n.move()
        b_n.draw()
        b_n.game_over()
        b_n.levels()
    s.level()
    s.score_count()
    canvas.after(DELAY, animation)


# This piece of code was adapted from the MoreKeyboardInput.py under Week 2, step 0202
def key_press(event):  # unction that if x is pressed then the program terminates.
    if event.char == 'x':
        quit()


animation()
bri.draw_rectangle()

win.bind('<Motion>', p_movement)
win.bind('<KeyPress>', key_press)
win.mainloop()  # listens for events, such as key presses and mouse clicks
