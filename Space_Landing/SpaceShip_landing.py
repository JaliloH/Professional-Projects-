import turtle
import math
import random
turtle.bgcolor("gray") 


class SpaceCraft(turtle.Turtle):
    '''
    Purpose: This class creates all of the nesscary operations for our spacecraft in the game. It calls to the left, right, and forward controls for our ship. 
    Instance variables: There are many instance variables in this class. self.fuel calls the fuel of the ship, self.x is the x position of the ship, self.y is y position of the ship, self.vx is the velocity of the ship in the x direction, and self.vy is the veolicty of the ship in the y direction.
    Methods: __init__ creates all of the instance variables for the class, move is what the gravity that moves the ship, left is the method that moves the ship to the left, right is what moves the ship right, and thurst is what moves the ship forward.
    '''

    def __init__(self, x, y, vx, vy):
        turtle.Turtle.__init__(self)
        self.fuel = 50
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.penup()
        self.left(90)
        self.speed(0)
        self.setpos(x,y)
    def move(self):
        self.vy -= 0.0486
        x = self.xcor() + self.vx
        y = self.ycor() + self.vy
        self.setpos(x,y)
    def Left(self):
        if self.fuel > 0:
            self.fuel -= 1
            self.left(15)
            print("Current Fuel: ", self.fuel)
            #turtle.write(self.fuel)
        else:
            print("Out of fuel")
    def Right(self):
        if self.fuel > 0:
            self.fuel -= 1
            self.right(15)
            print("Current Fuel: ", self.fuel)
        else:
            print("Out of fuel")

    def thrust(self):
        
        if self.fuel > 0:
            self.fuel = self.fuel - 1
            ship_angle = math.radians(self.heading())
            self.vx += math.cos(ship_angle)
            self.vy += math.sin(ship_angle)
            print("Current Fuel: ", self.fuel)
        else:
            print('Out of Fuel')

class Obstacle(turtle.Turtle):
    '''
    Purpose: This is what creates the obstacles for the class. 
    Instance variables: self.xpos is the x position of the obstacle, self.ypos is the y position of the obstacle, self.xvel is the x velocity of the obstacle, self.yvel is the y velocity of the obstacle. 
    Methods: __init__ creates all the instance variables for the class, and the obs_move is what moves the obstacles created by the class. 
    '''

    def __init__(self, xpos, ypos, yvel, xvel):
        turtle.Turtle.__init__(self)
        self.xpos = xpos
        self.ypos = ypos
        self.yvel = yvel
        self.xvel = xvel
        self.penup()
        self.speed(0)
        self.setpos(xpos, ypos)
        self.color("Blue")
        self.shape("circle")
        self.turtlesize(2)
    # def obstacle_show(self):
    #     xpos = self.xcor() + self.xvel
    #     ypos = self.ycor() + self.yvel
    #     self.setpos(xpos,ypos)
    def obs_move(self):
        xpos = self.xcor() + self.xvel
        ypos = self.ycor() + self.yvel
        self.setpos(xpos,ypos)
        if self.xcor() < 10 or self.xcor() > 990:
            self.xvel *= -1
        else:
            self.yvel *= -1

        
        
            


class Game():
    '''
    Purpose: This is the game that will use all the other class over the course of this homework
    Instance variables: self.obslist is the list of obstacles, self.crash is a boolean value if the spacecraft crashes or not. self.obj is the obstacle position and the self.player is the starting position of the spacecraft. 
    Methods: __init__ calls all the instaence varaible and nesecary operations for our game. gameloop is the method for the game to keep running with some conditions.
    '''

    def __init__(self):
        self.obslist = []
        self.crash = False
        turtle.setworldcoordinates(0, 0, 1000, 1000)
        turtle.delay(0)
        for i in range(10):
            self.obj = Obstacle(random.uniform(100,900), random.uniform(500,900), random.uniform(5,5), random.uniform(5,0))
            self.obslist.append(self.obj)

        self.player = SpaceCraft(random.uniform(100,900), random.uniform(500,900), random.uniform(-5,5), random.uniform(-5,0))
        self.player.turtlesize(2)

        self.gameloop()

        turtle.onkeypress(self.player.thrust, 'Up')
        turtle.onkeypress(self.player.Left, 'Left')
        turtle.onkeypress(self.player.Right, 'Right')
        #turtle.onkey(self.player.move, 'Down')
        
        turtle.listen()
        turtle.mainloop()

    def gameloop(self):
        if self.player.ycor() >= 10 and not self.crash:
            for i in self.obslist:
                #i.obstacle_show()
                i.obs_move()
                pos_compare = ((((self.player.xcor() - i.xcor()) ** 2) + ((self.player.ycor() - i.ycor()) ** 2)) ** 0.5)
                if pos_compare < 15:
                    self.crash = True
                
                if (i.ypos > 1000 or i.ypos < 0) and (i.xpos < 0 or i.xpos > 1000):
                        self.obj.obs_move()
                        i.setpos(random.uniform(100,900), random.uniform(500,900), random.uniform(5,5), random.uniform(5,0))

            #if not self.crash:
            self.player.move()
            turtle.ontimer(self.gameloop, 30)

        else:
            turtle.hideturtle()
            turtle.penup()
            turtle.setpos(500,100)
            #if self.player.pos()[1] < 10:
            if -4 <= self.player.vy <= 4 and -4 <= self.player.vx <= 4 and self.crash:
                turtle.write("Successful landing!", False, align = "center", font = ("Comic Sans", 45, "normal"))
            else:
                turtle.write("You crashed!", False, align = "center", font = ("Comic Sans", 45, "normal"))
            

Game()
