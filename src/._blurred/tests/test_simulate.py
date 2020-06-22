import simulate


def test_no_move():
    '''Check we don't move with no force'''
    ts = simulate.simulate(10,x=0.5,y=0.5,dy=0,dx=0,gy=0,gx=0,radius=0.1)
    assert ts[-1][1] == 0.5
    assert ts[-1][2] == 0.5


def test_bounds_x():
    '''Check we stay inside the box (x-axis)'''
    ts = simulate.simulate(10,x=0.5,y=0.5,dy=0,dx=0.5,gy=0,gx=0,radius=0.1)
    assert ts[-1][1] < 1
    ts = simulate.simulate(10,x=0.5,y=0.5,dy=0,dx=-0.5,gy=0,gx=0,radius=0.1)
    assert ts[-1][1] > 0


def test_bounds_y():
    '''Check we stay inside the box (y-axis)'''
    ts = simulate.simulate(10,x=0.5,y=0.5,dy=0.5,dx=0,gy=0,gx=0,radius=0.1)
    assert ts[-1][2] < 1
    ts = simulate.simulate(10,x=0.5,y=0.5,dy=-0.5,dx=0,gy=0,gx=0,radius=0.1)
    assert ts[-1][2] > 0
