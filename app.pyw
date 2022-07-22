import os
from ursina.prefabs.sky import Sky
from ursina import *
from random import *
import json
app = Ursina()                          # Initialise your Ursina app


try:
	# Opening JSON file
    with open('settings.json', 'r') as openfile:
        settings = json.load(openfile)
except:
	print("settings file not found")
	settings ={
    "CameraToPlayer" : "False",
    "Shader" : "unlit_shader",
    "PlayerSpeed" : 2.5,
    "EnemySpeed" : .75
}
	with open("settings.json", "w") as outfile:
		json.dump(settings, outfile)


#window.title = ''
window.fullscreen = False
window.exit_button.visible = False
window.borderless = False      
window.fps_counter.enabled = True
window.show_ursina_splash = False
#window.icon = ""
counter = 0
colors = [color.white,
color.smoke,
color.light_gray, 
color.gray,
color.dark_gray,
color.black,
color.red,
color.lime, 
color.green, 
color.turquoise,
color.cyan,
color.azure,
color.blue,
color.violet,
color.magenta,
color.pink,
color.brown,
color.olive,
color.peach,
color.gold,
color.salmon
]

player = Entity(
    model = "/assets/models/lambo.obj",
    color=color.yellow,
    y=1,
    texture = "/assets/textures/Lamborginhi Aventador_diffuse.jpeg",
    collider = "box",
    shader = settings["Shader"],
    scale= Vec3(0.005,0.005,0.005)
)
EditorCamera()
frame = 1
#land = Entity(model="cube",z = 15,scale=Vec3(104,1,104),texture = f"/assets/textures/road/00{frame}.jpg",shader = settings["Shader"])

land = Animation("assets/textures/road/00",fps=30,loop=True,scale=Vec2(104,104), rotation_x=90, y = 1)
land.start()
Collision = Entity(model= "wireframe_cube", scale = Vec3(10,10,3),z = -10,collider='box',visible = False, shader = settings["Shader"])
txt = Text(
    text=str(counter),
    origin = (0, -5),
    scale =3,
)

#Sky(texture = r"\assets\textures\white_pure.png",color = rgb(255, 214, 112), shader = settings["Shader"])
Sky(texture = r"assets\textures\white_pure.png",color=rgb(163, 244, 245), shader = settings["Shader"])
dodge = 0
enemy = Entity(model = "/assets/models/lambo.obj", x = randint(-4,4), y=1, z = 40, collider ="box",texture= "/assets/textures/Lamborginhi Aventador_diffuse.jpeg",shader = settings["Shader"], scale=Vec3(0.005,0.005,0.005), color =colors[randint(0,19)], rotation_y= 180)
txt.resolution = 1080 * txt.size
PlayerDead = False


def booltoint(x):
    if x == False:
        a = 1
    else:
        a = 0
    return a

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return True


def Playerdead_boolToggle():
    global PlayerDead
    PlayerDead = False

death = Text(text = "YOU DIED", origin = (0, -10),scale =3,color = color.red)


def update():
    global counter, txt, dodge, enemy, PlayerDead,frame
    player.x += held_keys["d"] * time.dt * settings["PlayerSpeed"] * booltoint(PlayerDead)
    player.x -= held_keys["a"] * time.dt * settings["PlayerSpeed"] * booltoint(PlayerDead)
    player.x += held_keys["right arrow"] * time.dt * settings["PlayerSpeed"] * booltoint(PlayerDead)
    player.x -= held_keys["left arrow"] * time.dt * settings["PlayerSpeed"] * booltoint(PlayerDead)
    if settings["CameraToPlayer"] == "True":
        camera.position = Vec3(player.x, 3, -20)
    else:
        camera.position = Vec3(0, 3, -20)
    counter += 0.1 * booltoint(PlayerDead)
    if PlayerDead == False:
        enemy.z -= settings["EnemySpeed"]
    destroy(txt)
    txt = Text(
        text= str(int(round_to_closest(counter, step= 1))),
        origin = (0, -5),
        scale =3,
    )
    txt.resolution = 1080 * txt.size
    if Collision.intersects().hit:
        if PlayerDead == False:
            
            Audio(sound_file_name="assets\sounds\pickupCoin.wav",auto_destroy=True)
            #ursfx([(0.0, 0.0), (0.01, 1.0), (0.25, 0.73), (0.41, 0.96), (0.61, 0.08)], volume=0.75, wave='sine', pitch=6, pitch_change=1, speed=1.4)
            destroy(enemy)
            dodge += 1
            enemy = Entity(model = "/assets/models/lambo.obj", x = randint(-4,4), y=1, z = 40, collider ="box",texture= "/assets/textures/Lamborginhi Aventador_diffuse.jpeg",shader = settings["Shader"], scale=Vec3(0.005,0.005,0.005), color = colors[randint(0,19)], rotation_y= 180)
    elif player.intersects().hit:
        Audio(sound_file_name="assets\sounds\hitHurt.wav", auto_destroy=True)
        destroy(enemy)
        PlayerDead = True
        land.pause()
        death.origin = (0, -4)
        if find("highscore.txt", "./") == True:
            with open("highscore.txt", "r") as outfile:
                highscore = int(outfile.read())
        else:
            highscore = 0
        if round_to_closest(counter, step=1) > highscore:
            hs = Text(text="New High Score!!!",origin = (0, -2),scale =3)
            with open("highscore.txt", "w") as outfile:
                outfile.write(str(int(round_to_closest(counter, step=1))))
    if player.x > 4:
        player.x = 4
    elif player.x < -4:
        player.x = -4

def input(key):
    if key == "enter":
        os.startfile(os.path.abspath("./app.pyw"))
        quit()
    elif key == "q":
        quit()
app.run()
