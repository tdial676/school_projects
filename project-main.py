'''
-----------------------------
Animation Template - Advanced
-----------------------------
This file contains the template for an advanced animation file. Remember to:
    - Declare your global game variables (SpriteLists, score, etc.)in
      the __init__() method
    - Initialize game variables (player, items, etc.) in the setup() method
    - Put the initial render code in the on_draw() method
    - Anything that changes over time (a.k.a. the actual animation part) goes
      in the update() method

Below the update() method are all of the mouse event methods, followed by the
key event methods. Feel free to use as many or as few of these as you like.
See each method for information on how they are used, feel free to delete any
of the methods that you don't use.
'''

import arcade
#We imported random because we use the random method for ball speed and number of balls
import random
# Size of the screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Title of the window
TITLE = 'Animation Template'

class MyGame(arcade.Window):
    '''
    Main application class.
    '''

    def __init__(self, width, height, title):
        ''' Initialize game parameters '''
        super().__init__(width, height, title)

        # Set the background color
        arcade.set_background_color(arcade.color.ORANGE)

        ### Declare global game variables (score, SpriteLists, etc.) here.
        ### These will be accessible from anywhere in the class.
        # declares our player
        self.player = None
        #declares how fast the player is moving
        self.speed = None
        # declares our ball list
        self.ball_lst = None
        # declares how often to drop the ball_lst
        self.time_since_last_ball = None
        #declares the score
        self.score = None
        # How many lives the player has
        self.lives_lst = None
        # creates a football
        self.football = None
        # ends game
        self.game_over = None
        # creates background music
        self.music = None

    def setup(self):
        ''' Set up your game here '''
        # Initialization code, background, player, items, etc.
        # defines music being played
        self.music = arcade.load_sound('sound/music.mp3')
        # plays the music
        arcade.play_sound(self.music)

        # Defines the player sprite and scale
        self.player = arcade.Sprite('img/Monkey.png', .3)
        # Sets player's intial position at the middle of the screen
        self.player.set_position(SCREEN_WIDTH/ 2, 50)
        # Defines ball_lst as a SpriteListlist
        self.ball_lst = arcade.SpriteList()

        # Loop that makes balls and append them to ball_lst
        for x in range(16):
            ball = self.make_ball()
            self.ball_lst.append(ball)

        # Defines the Players speed
        self.speed = 10
        # Define the time since last ball drop as zero
        self.time_since_last_ball = 0
        # Sets the score to zero to begin with
        self.score = 0

        # Set up a lives lst
        self.lives_lst = arcade.SpriteList()
        # Loop that makes the numerous lives on the screen
        for x in range(0, 50, 10):
            life = self.make_life(x)
            self.lives_lst.append(life)

        # football list
        self.football_lst = arcade.SpriteList()
        # Makes footballs
        for x in range(5):
            football = self.make_football()
            self.football_lst.append(football)
        #sets the game over to false
        self.game_over = False

    # A method that creates a scoreboard on the screen and keeps track of the score
    def make_score_board(self):
        # Sets the scoreboard position
        x = 450
        y = 550
        # Prints the score on screen
        arcade.draw_text(f'Score: {self.score}', x, y, arcade.color.PINK, 20)

    # Method that makes lives icon on the screen
    def make_life(self, x):
        life = arcade.Sprite('img/banana.png', 0.2)
        life.set_position(x+40, 550)
        return life

    # This method creates a ball
    def make_ball(self):
        #the sprite and scale we used
        ball = arcade.Sprite('img/basketball.png', 0.09)
        # Litims the ball drop within the SCREEN_WIDTH.
        ballX = random.randint(0, SCREEN_WIDTH)
        # New ball will be between 1 through 5 screen height off the top of window
        ballY = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT*5)
        #sets the ball drop speed randomly between 1 through 7 numbers.
        ball.change_y = -random.randint(1, 6)
        #sets the ball's initial position.
        ball.set_position(ballX, ballY)
        #this method returns ball
        return ball

    #method to make footballs
    def make_football(self):
        #the sprite and scale we used for football
        football = arcade.Sprite('img/football.png', 0.09)
        # Limits the ball drop within the SCREEN_WIDTH.
        footballX = random.randint(0, SCREEN_WIDTH)
        # New ball will be between 1 through 5 screen height off the top of window
        footballY = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT*5)
        #sets the ball drop speed randomly between two numbers.
        football.change_y = -random.randint(1, 9)
        #sets the ball's initial position.
        football.set_position(footballX, footballY)
        # returns the football
        return football




    def on_draw(self):
        ''' Automatically called for initial render of screen '''
        # This command has to happen before we start drawing
        arcade.start_render()
        # Draws the player
        self.player.draw()
        # draws the ball_lst
        self.ball_lst.draw()
        # Draws the scoreboard method which draws a scoreboard.
        self.make_score_board()
        #draws the lives icon which are moneys
        self.lives_lst.draw()
        #draws the footballs
        self.football_lst.draw()
        # if Game over is true it should print
        if self.game_over:
            arcade.draw_text("GAME OVER !!!!", 30, 90, arcade.color.RED, 70)


    def update(self, delta_time):
        '''
        Automatically called about 60 times per second.
        Put all of the logic to move, and the game logic here.
        '''

        # Loop through each ball
        for ball in self.ball_lst:
            #if the ball hits the bottom of the screen then it is killed. this
            #prevents laggyness
            if ball.center_y < 0:
                ball.kill()
                # also it takes away from the lives every time a ball hits the ground
                if len(self.lives_lst) > 0:
                    self.lives_lst.pop()

        # kills footballs that touch the ground
        # Prevents laggyness
        for football in self.football_lst:
            if football.center_y < 0:
                football.kill()


        # If the lives_lst is empty then it turns game_over to true
        # This ends the game
        if len(self.lives_lst) <= 0:
            self.game_over = True

        #THis checks for collision between the ball and the player
        caught = arcade.check_for_collision_with_list(self.player, self.ball_lst)
        # check for collision between player and bonus football
        bonus = arcade.check_for_collision_with_list(self.player, self.football_lst)

        '''For every collision between the ball and the player, this code
        makes that ball dissapear and adds 1 to the score and prints in the
        terminal and screen. For every football caught the score is multiplied by 2.'''

# only updates the score if you have lives
        if len(self.lives_lst) > 1:
            for ball in caught:
                ball.kill()
                self.score += 1
                print(self.score)

            # IF FOOTBALL IS CAUGHT THEN MULTIPLY SCORE BY TWO
            for football in bonus:
                football.kill()
                self.score *= 2
                print(self.score)

        #this updates the player, football and ball list every update
        self.player.update()
        self.ball_lst.update()
        self.football_lst.update()

        #adds up the delta_time
        self.time_since_last_ball += delta_time

        # On each update, spawn another ball above the window
        #adds the delta time since last drop until its equal to one before updatingself.
        #prevents laggyness and lets us control the update times
        if self.time_since_last_ball >= 1:
            new_ball = self.make_ball()
            self.ball_lst.append(new_ball)
            self.time_since_last_ball = 0






    ############################################################
    # MOUSE METHODS: feel free to delete any you're not using! #
    ############################################################

    def on_mouse_motion(self, x, y, dx, dy):
        '''
        Automatically called whenever the mouse is moved
            x   float   x-coordinate at moment of update
            y   float   y-coordinate at moment of update
            dx  float   speed/direction of horizontal movement
            dy  float   speed/direction of vertical movement
        '''
        pass

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        '''
        Automatically called whenever the mouse is dragged (a.k.a. pressed and
        moved at the same time)
            x           float   x-coordinate at moment of update
            y           float   y-coordinate at moment of update
            dx          float   speed/direction of horizontal movement
            dy          float   speed/direction of vertical movement
            button      int     1 if left-click, 4 if right-click
            modifiers   int     (see reference at bottom of file)
        '''
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        '''
        Automatically called whenever the mouse is clicked
            x           float   x-coordinate of click
            y           float   y-coordinate of click
            button      int     1 if left-click, 4 if right-click
            modifiers   int     (see reference at bottom of file)
        '''
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        '''
        Automatically called whenever the mouse is clicked
            x           float   x-coordinate of click
            y           float   y-coordinate of click
            button      int     1 if left-click, 4 if right-click
            modifiers   int     (see reference at bottom of file)
        '''
        pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        '''
        Automatically called whenever the mouse is scrolled
            x           int     x-coordinate of scroll
            y           int     y-coordinate of scroll
            scroll_x    int     speed/direction of horizontal scroll
            scroll_y    int     speed/direction of vertical scroll
        '''
        pass

    ##########################################################
    # KEY METHODS: feel free to delete any you're not using! #
    ##########################################################

    def on_key_press(self, symbol, modifiers):
        '''
        Automatically called whenever a key is pressed
            symbol      int     code for key pressed (from ASCII table)
                                Note: chr(symbol) returns the string
            modifiers   int     (see reference at bottom of file)
        '''
        #if the user presses the left key the player moves left
        if symbol == arcade.key.LEFT:
            self.player.change_x = -self.speed
        #else if the user presses the right key the player moves right
        elif symbol == arcade.key.RIGHT:
            self.player.change_x = self.speed

    def on_key_release(self, symbol, modifiers):
        '''
        Automatically called whenever a key is released
            symbol      int     code for key pressed (from ASCII table)
                                Note: chr(symbol) returns the string
            modifiers   int     (see reference at bottom of file)
        '''
        #when either key is released the player does not change position
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.player.change_x = 0


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()



'''
Mouse event modifiers:
    0       (none)
    1       shift
    2       ctrl
    8       caps lock
    64      cmd
    132     alt/option
    512     fn
Test it out yourself for any combinations of these!
'''
