<picture align="center">
    <img alt="Ilo robot" src="https://images.squarespace-cdn.com/content/v1/6312fe2115db3003bd2ec2f1/546df043-e044-4003-867b-802738eb1332/LOGO+ILO+PYTHON.png?format=100w 100w, https://images.squarespace-cdn.com/content/v1/6312fe2115db3003bd2ec2f1/546df043-e044-4003-867b-802738eb1332/LOGO+ILO+PYTHON.png?format=300w 300w, https://images.squarespace-cdn.com/content/v1/6312fe2115db3003bd2ec2f1/546df043-e044-4003-867b-802738eb1332/LOGO+ILO+PYTHON.png?format=500w 500w, https://images.squarespace-cdn.com/content/v1/6312fe2115db3003bd2ec2f1/546df043-e044-4003-867b-802738eb1332/LOGO+ILO+PYTHON.png?format=750w 750w, https://images.squarespace-cdn.com/content/v1/6312fe2115db3003bd2ec2f1/546df043-e044-4003-867b-802738eb1332/LOGO+ILO+PYTHON.png?format=1000w 1000w, https://images.squarespace-cdn.com/content/v1/6312fe2115db3003bd2ec2f1/546df043-e044-4003-867b-802738eb1332/LOGO+ILO+PYTHON.png?format=1500w 1500w, https://images.squarespace-cdn.com/content/v1/6312fe2115db3003bd2ec2f1/546df043-e044-4003-867b-802738eb1332/LOGO+ILO+PYTHON.png?format=2500w 2500w">
</picture>

---

# Ilo robot

A package that lets users control ilo the new educational robot using python command lines.

## Features

- Moves the robot in **many directions** with python commands line
- Creates **movement loops**
- Play with the robot in **real time** with your keyboard
- Use **colored plates** to make the robot move

## Where to get it ?

```
# with pip
pip install ilo
```

## Dependencies

- [Keyboard - Take full control of your keyboard with this small Python library. Hook global events, register hotkeys, simulate key presses and much more.](https://pypi.org/project/keyboard/)

Don't worry, this dependency is automatically installed with the ilo library.

## Example

```
import ilo

ilo.connection()

print("ilo is connected")

ilo.set_led_color_rgb(200,0,0)      # color is red
ilo.set_led_color_rgb(0,0,200)      # color is blue

while true:

    print("Ilo moves forward"
    ilo.move(front)
    
    while ilo.get_distance() > 20:
        pass
        
    ilo.stop()
    print("Ilo has encountered an obstacle")
    
    if ilo.get_distance() > 20:
        ilo.move(right, 80)
        print("ilo moves to the right at 80% of its speed")
    
    else:
        ilo.move(left, 70)
        print("ilo moves to the left at 70% of its speed")
```

## About us

Find us on our [***website***](https://ilorobot.com) ;)
