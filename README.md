# 2D-bouncing
Simple 2D dataset of bouncing balls

![](example.gif)

## Initial proof-of-concept

- [x] White circle on black background
- [ ] Ball bounces off image edges
- [ ] Vary physical properties:
    - [ ] Starting position
    - [ ] Ball radius
    - [ ] Initial direction
    - [ ] Initial speed
    - [ ] Gravity
    - [ ] Ball mass
    - etc

Made of 2 components:
1. Script which takes in the simulation parameters (radius,speed,initial position), and calculates the position of the ball at each timestep
2. Script which takes the position and draws the ball as an image

    E.g. `./drawCircle.sh 10 50 frame_0.png` will draw a circle at (10,50)
