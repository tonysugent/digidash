from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from Gauges import RpmGauge, MphGauge, ShifterGauge
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

class Dashboard(Screen):

    def __init__(self,data,**kwargs):
        super(Dashboard, self).__init__(**kwargs)
        Window.size = (575, 300)
        self.cols = 2
        self.d = data
        self.rpmgauge = RpmGauge(size_gauge=256, size_text=25)
        self.mphgauge = MphGauge(size_gauge=256, size_text=25,pos=(300,0))
        self.shiftergauge = ShifterGauge(size_gauge=256, size_text=0)
        self.gear = Label(text="N",pos_hint={"x":-.02, "y":.3})
        self.cel_button = Button(color = (1, 0, .65, 1),
                                 size_hint = (.1,.175), pos_hint = {"x":0.576, "y": 0.4},
                                 background_normal = 'no_cel.png')
        self.add_widget(self.rpmgauge)
        self.add_widget(self.mphgauge)
        self.add_widget(self.shiftergauge)
        self.add_widget(self.cel_button)

        self.add_widget(self.gear)

        Clock.schedule_interval(lambda *t: self.gauge_increment(), 0.03)
        Clock.schedule_interval(lambda *t: self.cel_check(), .01)

    def gauge_increment(self):
        self.rpmgauge.value = self.d.getRpm()
        self.mphgauge.value = self.d.getMph()
        self.shiftergauge.value = self.d.getDownshift()
        self.gear.text = self.d.getGear()

    def cel_check(self):
        if self.d.getCel():
            self.cel_button.background_normal = 'cel1.png'



class CelScreen(Screen):
    pass


class MyApp(App):
    def __init__(self,data,**kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.data = data
        self.sm = ScreenManager()
        self.sm.add_widget(Dashboard(self.data))
    def build(self):
        return self.sm

