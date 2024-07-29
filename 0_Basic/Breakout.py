import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Breakout")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 10
        self.x = (800 - self.width) // 2
        self.y = 580
        self.speed = 10

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < 800 - self.width:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

class Ball:
    def __init__(self):
        self.radius = 10
        self.x = 400
        self.y = 300
        self.speed_x = 3
        self.speed_y = 3

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x <= 0 or self.x >= 800 - self.radius:
            self.speed_x = -self.speed_x
        if self.y <= 0:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 75, 20)
        self.score_value = 10

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick(i * (75 + 10) + 35, j * (20 + 10) + 50) for i in range(8) for j in range(5)]
        self.running = True
        self.clock = pygame.time.Clock()
        self.score = 0
        self.game_over = False
    def display_game_over(self, screen, font):
        game_over_text = font.render(f"Game Over! \n Score: {self.score}", True, (0, 0, 0))
        screen.blit(game_over_text, (200, 250))

    def display_restart_button(self, screen, font):
        restart_text = font.render("Restart", True, (0, 0, 0))
        restart_rect = restart_text.get_rect(center=(400, 350))
        pygame.draw.rect(screen, (200, 200, 200), restart_rect.inflate(20, 10))
        screen.blit(restart_text, restart_rect.topleft)
        return restart_rect

    def reset_game(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick(i * (75 + 10) + 35, j * (20 + 10) + 50) for i in range(8) for j in range(5)]
        self.score = 0
        self.game_over = False
        self.restart_rect = None

    def run(self):
        # display the score
        font = pygame.font.Font(None, 36)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                    if self.restart_rect and self.restart_rect.collidepoint(event.pos):
                        self.reset_game()

            keys = pygame.key.get_pressed()
            self.paddle.move(keys)
            self.ball.move()

            # Ball collision with paddle
            # increase the paddle_rect size to make it easier to hit the ball
            paddle_rect = pygame.Rect(self.paddle.x - 5,
                                      self.paddle.y - 5,
                                      self.paddle.width + 10,
                                      self.paddle.height + 10
                                      )
            ball_rect = pygame.Rect(self.ball.x, self.ball.y, self.ball.radius, self.ball.radius)
            if paddle_rect.colliderect(ball_rect):
                self.ball.speed_y = - self.ball.speed_y

            # Ball collision with bricks
            for brick in self.bricks[:]:
                if brick.rect.colliderect(ball_rect):
                    self.bricks.remove(brick)
                    self.ball.speed_y = -self.ball.speed_y
                    self.score += brick.score_value # increase the score according to the brick value
                    break

            # Game over if the ball hits the bottom
            if self.ball.y >= 600:
                self.game_over = True
                # display a end game message and add button to restart the game

            # Fill the screen with white
            screen.fill(WHITE)

            # Draw the paddle, ball, and bricks
            self.paddle.draw(screen)
            self.ball.draw(screen)
            for brick in self.bricks:
                brick.draw(screen)

            # Display the score
            score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10)) # display the score at the top left corner

            if self.game_over: #implicitly check if the game is over == True
                self.display_game_over(screen, font)
                self.restart_rect = self.display_restart_button(screen, font)

            # Update the display
            pygame.display.flip()
            # Control the frame rate
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()