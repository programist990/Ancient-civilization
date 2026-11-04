from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
import random, math

Window.size = (1180, 760)
Window.minimum_width, Window.minimum_height = 850, 560
Window.clearcolor = get_color_from_hex("#17231d")


class GameMap(Widget):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.world_size = (2200, 1600)
        self.cam_x, self.cam_y, self.zoom = 0, 0, 0.72
        self.drag_start = None
        self.drag_camera = None
        random.seed(17)
        self.objects = []
        for _ in range(75):
            self.objects.append({"type":"tree", "x":random.randint(70,2130),
                                 "y":random.randint(70,1530), "alive":True})
        for _ in range(38):
            self.objects.append({"type":"rock", "x":random.randint(70,2130),
                                 "y":random.randint(70,1530), "alive":True})
        self.landmarks = [
            {"name":"Порт", "x":1770, "y":390, "level":10},
            {"name":"Ж/Д станция", "x":1550, "y":1180, "level":15},
            {"name":"Аэропорт", "x":390, "y":1270, "level":30},
        ]
        self.buildings = []
        self.bind(pos=self.draw_map, size=self.draw_map)
        Clock.schedule_interval(lambda dt:self.draw_map(), 1/20)

    def to_screen(self, x, y):
        return self.x+(x-self.cam_x)*self.zoom, self.y+(y-self.cam_y)*self.zoom

    def to_world(self, x, y):
        return (x-self.x)/self.zoom+self.cam_x, (y-self.y)/self.zoom+self.cam_y

    def draw_map(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*get_color_from_hex("#294b35"))
            Rectangle(pos=self.pos, size=self.size)
            for gx in range(0,2200,240):
                for gy in range(0,1600,240):
                    sx,sy=self.to_screen(gx,gy)
                    if self.x-150<sx<self.right+150 and self.y-150<sy<self.top+150:
                        Color(0.40,0.57,0.36,0.18)
                        Ellipse(pos=(sx-70*self.zoom,sy-50*self.zoom),
                                size=(140*self.zoom,100*self.zoom))
            # Roads
            Color(*get_color_from_hex("#a79a78"))
            p1=self.to_screen(0,790); p2=self.to_screen(2200,790)
            Line(points=[*p1,*p2],width=max(2,15*self.zoom))
            p1=self.to_screen(1080,0); p2=self.to_screen(1080,1600)
            Line(points=[*p1,*p2],width=max(2,15*self.zoom))
            # Starting clearing
            cx,cy=self.to_screen(1080,790)
            Color(*get_color_from_hex("#78945c"))
            Ellipse(pos=(cx-180*self.zoom,cy-125*self.zoom),
                    size=(360*self.zoom,250*self.zoom))
            # Resources
            for obj in self.objects:
                if not obj["alive"]:
                    continue
                sx,sy=self.to_screen(obj["x"],obj["y"])
                if not(self.x-50<sx<self.right+50 and self.y-50<sy<self.top+50):
                    continue
                if obj["type"]=="tree":
                    Color(*get_color_from_hex("#173b27"))
                    Ellipse(pos=(sx-18*self.zoom,sy-12*self.zoom),
                            size=(36*self.zoom,34*self.zoom))
                    Color(*get_color_from_hex("#43864b"))
                    Ellipse(pos=(sx-20*self.zoom,sy-2*self.zoom),
                            size=(40*self.zoom,27*self.zoom))
                    Color(*get_color_from_hex("#755238"))
                    Rectangle(pos=(sx-3*self.zoom,sy-12*self.zoom),
                              size=(6*self.zoom,13*self.zoom))
                else:
                    Color(*get_color_from_hex("#78817e"))
                    Ellipse(pos=(sx-16*self.zoom,sy-10*self.zoom),
                            size=(32*self.zoom,23*self.zoom))
                    Color(*get_color_from_hex("#b4bcb5"))
                    Ellipse(pos=(sx-8*self.zoom,sy-1*self.zoom),
                            size=(13*self.zoom,8*self.zoom))
            # Player buildings
            for b in self.buildings:
                sx,sy=self.to_screen(b["x"],b["y"])
                Color(*get_color_from_hex("#704b35"))
                Rectangle(pos=(sx-24*self.zoom,sy-18*self.zoom),
                          size=(48*self.zoom,36*self.zoom))
                Color(*get_color_from_hex("#c47c51"))
                Line(rectangle=(sx-24*self.zoom,sy-18*self.zoom,
                               48*self.zoom,36*self.zoom),width=1.2)
                Color(*get_color_from_hex("#e1cda0"))
                Rectangle(pos=(sx-6*self.zoom,sy-18*self.zoom),
                          size=(12*self.zoom,16*self.zoom))
            # Abandoned transport landmarks
            for lm in self.landmarks:
                sx,sy=self.to_screen(lm["x"],lm["y"])
                if self.x-80<sx<self.right+80 and self.y-80<sy<self.top+80:
                    Color(*get_color_from_hex("#626d68"))
                    Rectangle(pos=(sx-32*self.zoom,sy-21*self.zoom),
                              size=(64*self.zoom,42*self.zoom))
                    Color(*get_color_from_hex("#c0b28b"))
                    Line(rectangle=(sx-32*self.zoom,sy-21*self.zoom,
                                   64*self.zoom,42*self.zoom),width=1.3)
                    Color(0.95,0.83,0.53,1)
                    Ellipse(pos=(sx-4*self.zoom,sy+24*self.zoom),
                            size=(8*self.zoom,8*self.zoom))
            Color(0.08,0.14,0.10,1)
            Line(rectangle=(self.x,self.y,self.width,self.height),width=1)

    def clamp_camera(self):
        vw,vh=self.width/self.zoom,self.height/self.zoom
        self.cam_x=max(0,min(2200-vw,self.cam_x))
        self.cam_y=max(0,min(1600-vh,self.cam_y))

    def on_touch_down(self,touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        if touch.is_mouse_scrolling:
            wx,wy=self.to_world(*touch.pos)
            self.zoom=max(.4,min(1.4,self.zoom*(1.12 if touch.button=="scrollup" else .89)))
            self.cam_x=wx-(touch.x-self.x)/self.zoom
            self.cam_y=wy-(touch.y-self.y)/self.zoom
            self.clamp_camera(); self.draw_map()
            return True
        self.drag_start=touch.pos
        self.drag_camera=(self.cam_x,self.cam_y)
        touch.grab(self)
        return True

    def on_touch_move(self,touch):
        if touch.grab_current is self and self.drag_start:
            dx=touch.x-self.drag_start[0]; dy=touch.y-self.drag_start[1]
            self.cam_x=self.drag_camera[0]-dx/self.zoom
            self.cam_y=self.drag_camera[1]-dy/self.zoom
            self.clamp_camera(); self.draw_map()
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self,touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            dx=touch.x-self.drag_start[0]; dy=touch.y-self.drag_start[1]
            if math.hypot(dx,dy)<dp(8):
                self.tap(*touch.pos)
            self.drag_start=None
            return True
        return super().on_touch_up(touch)

    def tap(self,sx,sy):
        wx,wy=self.to_world(sx,sy)
        nearby=[o for o in self.objects if o["alive"] and
                math.hypot(o["x"]-wx,o["y"]-wy)<45/self.zoom]
        if nearby:
            obj=min(nearby,key=lambda o:math.hypot(o["x"]-wx,o["y"]-wy))
            self.game.gather(obj)
            return
        for lm in self.landmarks:
            if math.hypot(lm["x"]-wx,lm["y"]-wy)<60/self.zoom:
                self.game.landmark_info(lm); return
        if self.game.build_mode:
            self.game.build_at(wx,wy)
        else:
            self.game.say("Выбери дерево или камень либо включи строительство.")

    def place_building(self,kind,x,y):
        self.buildings.append({"type":kind,"x":x,"y":y})
        self.draw_map()


class AncientCivilization(App):
    def build(self):
        self.title="Ancient Civilization — Prototype 0.1"
        self.money,self.wood,self.stone,self.metal=2500,35,20,0
        self.population,self.capacity=12,20
        self.level,self.xp,self.xp_need=1,0,100
        self.axe,self.pick=10,10
        self.build_mode=False
        self.building="house"
        self.timer=0
        self.message="Добро пожаловать! Собери ресурсы и построй первый дом."

        root=BoxLayout(orientation="vertical",padding=dp(6),spacing=dp(5))
        self.hud=Label(size_hint_y=None,height=dp(48),font_size="14sp",
                       color=get_color_from_hex("#f4edda"))
        root.add_widget(self.hud)
        self.map=GameMap(self)
        root.add_widget(self.map)
        bar=BoxLayout(size_hint_y=None,height=dp(46),spacing=dp(6))
        for title,callback in [
            ("Топор",lambda *_:self.say(f"Топор: {self.axe} применений. Нажимай на дерево.")),
            ("Кирка",lambda *_:self.say(f"Кирка: {self.pick} применений. Нажимай на камень.")),
            ("Строить",lambda *_:self.toggle_build()),
            ("Сменить здание",lambda *_:self.switch_building()),
        ]:
            bar.add_widget(Button(text=title,on_release=callback))
        root.add_widget(bar)
        self.status=Label(text=self.message,size_hint_y=None,height=dp(30),
                          font_size="13sp",color=get_color_from_hex("#f4edda"))
        root.add_widget(self.status)
        Clock.schedule_interval(self.tick,1)
        self.refresh()
        return root

    def refresh(self):
        self.hud.text=(f"УРОВЕНЬ {self.level}   XP {self.xp}/{self.xp_need}     "
                       f"Деньги: {self.money}   Дерево: {self.wood}   Камень: {self.stone}   "
                       f"Металл: {self.metal}   Население: {self.population}/{self.capacity}")
        self.status.text=self.message

    def say(self,text):
        self.message=text
        self.refresh()

    def gather(self,obj):
        if obj["type"]=="tree":
            if self.axe<=0:
                self.say("Топор израсходован. Для дальнейшей добычи нужен новый инструмент.")
                return
            self.axe-=1; self.wood+=5; text="Получено 5 дерева."
        else:
            if self.pick<=0:
                self.say("Кирка израсходована. Для дальнейшей добычи нужна новая.")
                return
            self.pick-=1; self.stone+=4; text="Получено 4 камня."
        obj["alive"]=False
        self.add_xp(10)
        self.say(text)
        self.map.draw_map()

    def toggle_build(self):
        self.build_mode=not self.build_mode
        self.say(f"Режим строительства: {self.building}. Нажми на свободное место." if self.build_mode
                 else "Режим строительства выключен.")

    def switch_building(self):
        self.building="shop" if self.building=="house" else "house"
        self.build_mode=True
        self.say(f"Выбрано здание: {self.building}. Нажми на свободное место.")

    def build_at(self,x,y):
        if self.building=="house":
            cost=(500,10,5); required=0
        else:
            cost=(800,15,5); required=10
        if self.money<cost[0] or self.wood<cost[1] or self.stone<cost[2]:
            self.say("Недостаточно денег или материалов.")
            return
        if self.population<required:
            self.say(f"Недостаточно населения: нужно {required}, есть {self.population}.")
            return
        self.money-=cost[0]; self.wood-=cost[1]; self.stone-=cost[2]
        self.map.place_building(self.building,x,y)
        if self.building=="house":
            self.capacity+=10
            self.say("Дом построен! Вместимость населения увеличена на 10.")
        else:
            self.say("Магазин построен! Он будет приносить деньги.")
        self.add_xp(25)
        self.build_mode=False
        self.refresh()

    def add_xp(self,amount):
        self.xp+=amount
        while self.xp>=self.xp_need:
            self.xp-=self.xp_need
            self.level+=1
            self.xp_need=int(self.xp_need*1.35)
            self.money+=500; self.wood+=10
            self.message=f"Новый уровень {self.level}! Награда: 500 денег и 10 дерева."
        self.refresh()

    def landmark_info(self,lm):
        if self.level<lm["level"]:
            self.say(f'{lm["name"]} заброшен. Откроется на {lm["level"]} уровне.')
        else:
            self.say(f'{lm["name"]}: уровень достигнут. Ремонт будет добавлен в следующей версии.')

    def tick(self,dt):
        self.timer+=dt
        if self.timer>=10:
            self.timer=0
            shops=sum(1 for b in self.map.buildings if b["type"]=="shop")
            if shops:
                self.money+=shops*25
                self.message=f"Магазины принесли {shops*25} денег."
            if self.population<self.capacity:
                self.population+=1
                self.message="В город приехал новый житель."
            self.refresh()


if __name__=="__main__":
    AncientCivilization().run()
