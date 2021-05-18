# -*- coding: utf8 -*-
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.recycleview import RecycleView
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ListProperty
from kivymd.uix.label import MDLabel
import random

root_kv = '''
<Test>:
    orientation: "vertical"
    padding: dp(50), dp(20)
    md_bg_color: app.theme_cls.primary_color

    val: ""
    dogru: 0
    yanlis: 0

    # Sonuncu doğru -> 1,  yanlış -> 0,  yok -> -1
    sonuncu: -1

    data: {}

    on_data:
        self.uret()


    MDBoxLayout:
        adaptive_height: True
        MDLabel:
            text: str(root.yanlis)
            theme_text_color: "Custom" if root.sonuncu == 0 else "Primary"
            halign: "right"
            text_color: 1, 0, 0, 1
        MDIcon:
            halign: "center"
            icon: "alpha-x-circle-outline"
        MDIcon:
            halign: "center"
            icon: "check-circle-outline"
        MDLabel:
            text: str(root.dogru)
            theme_text_color: "Custom" if root.sonuncu == 1 else "Primary"
            text_color: 0, 1, 0, 1


    MDBoxLayout:
        orientation: "vertical"
        MDLabel:
            id: test_key
            text: root.val
            halign: "center"
            theme_text_color: "Primary"
            font_style: "H2"

        MDTextField:
            id: test_key
            hint_text: "Buraya karşılığını girin"
            color_mode: 'custom'
            helper_text_mode: "on_focus"
            helper_text: "Üstteki ifadenin karşılığı nedir?"
            line_color_focus: 1, 1, 1, 1

            on_text_validate:
                root.sorgula()

        MDFillRoundFlatButton:
            id: test_button
            text: "Kontrol Et"
            md_bg_color: 0,0,0,1
            pos_hint: {"center_x": 0.5}
            on_press:
                root.sorgula(1)             

    MDBoxLayout:
        # Burada sayfanın yarısını boşluk oluştrmak için bunu ekledik
        orientation: "vertical"
        MDLabel:

<OgrenItem@MDLabel>:
    halign: 'center'
    #valign: 'top'
    # theme_text_color: "Primary"
    font_style: "H4"


BoxLayout:
    orientation:'vertical'

    # MDToolbar:
    #     title: 'Major Sistem'
    #     specific_text_color: 0.2, 0, 0.2, .8

    MDBottomNavigation:
        id: nav
        panel_color: .55, 0, .55, 1
        text_color_normal: 0, 0, 0, .7
        text_color_active: 1, 1, 1, .7

        MDBottomNavigationItem:
            name: 'harf_ogren'
            text: 'Öğren'
            icon: 'alphabet-latin'

            MDGridLayout:
                id: grid_harf
                cols: 4
                padding: 50, 0
                # adaptive_height: True
                md_bg_color: app.theme_cls.primary_color

        MDBottomNavigationItem:
            name: 'harf_test'
            text: 'Test'
            icon: 'alphabet-latin'

            Test:
                id: harf_test
                data: app.dict_harf

        MDBottomNavigationItem:
            name: 'sayi_ogren'
            text: 'Öğren'
            icon: 'numeric'


            BoxLayout:
                # spacing: dp(10)
                padding: dp(20), dp(20), dp(20), 0
                orientation: "vertical"
                canvas.before:
                    Color:
                        rgba: app.theme_cls.primary_color
                    Rectangle:
                        size: self.size

                MDBoxLayout:
                    adaptive_height: True

                    MDIconButton:
                        icon: 'magnify'

                    MDTextField:
                        id: search_field

                        hint_text: "Hızlı Arama"
                        color_mode: 'custom'
                        helper_text_mode: "on_focus"
                        helper_text: "Üstteki ifadeyi aşağıda bul"
                        line_color_focus: 1, 1, 1, 1

                        on_text: app.set_list_sayis(self.text, True)

                RecycleView:
                    data: app.sort_sayi_text
                    viewclass: 'OgrenItem'
                    RecycleBoxLayout:
                        default_size: None, dp(50)
                        default_size_hint: 1, None
                        size_hint_y: None
                        height: self.minimum_height
                        orientation: 'vertical'

        MDBottomNavigationItem:
            name: 'sayi_test'
            text: 'Test'
            icon: 'numeric'

            Test:
                id: sayi_test
                data: app.dict_sayi

'''


class OgrenPage(RecycleView):
    def __init__(self, **kwargs):
        super(OgrenPage, self).__init__(**kwargs)
        # self.data = [{'key': key, 'vals': ", ".join(vals)} for key, vals in data.items()]


def show_keyboard(widget):
    widget.focus = True


class Test(MDBoxLayout):
    key = 0

    def sorgula(self, timeout=0.2):
        widget = self.ids.test_key

        # Gelen önce düzenlenir
        gelen_key = widget.text.lower().strip(" ,.;-=")

        if type(self.key) is list:
            sorgu = gelen_key in self.key
        else:
            sorgu = gelen_key == self.key

        if sorgu:
            self.dogru += 1
            self.sonuncu = 1
        else:
            self.yanlis += 1
            self.sonuncu = 0

        self.uret()
        Clock.schedule_once(lambda x: show_keyboard(widget), timeout)

    def uret(self):
        # Text Field'i temizle
        self.ids.test_key.text = ""

        key = random.choice(list(self.data))
        vals = self.data[key]

        # Son üretilen ile şimdi üretilen değerler aynıysa tekrar üret
        if key in (self.key, self.val):
            return self.uret()

        if random.randint(0, 1):
            self.val = random.choice(vals)
            self.key = key
        else:
            self.val = key
            self.key = vals


class MajorSistem(MDApp):
    dict_harf = {
        "0": ["r", "y"],
        "1": ["l", "j"],
        "2": ["n", "z"],
        "3": ["m"],
        "4": ["d", "t"],
        "5": ["v", "c", "ç"],
        "6": ["b", "h"],
        "7": ["k", "f"],
        "8": ["s", "ş"],
        "9": ["p", "g", "ğ"]
    }

    dict_sayi = {
        "0": ["arı"],
        "1": ["aile"],
        "2": ["anı", "ana"],
        "3": ["emmi"],
        "4": ["at", "ada"],
        "5": ["av", "aç"],
        "6": ["oba", "abi"],
        "7": ["ok"],
        "8": ["aş", "asa"],
        "9": ["ip", "ağ"],
        "10": ["lira"],
        "11": ["lale"],
        "12": ["laz"],
        "13": ["alim", "elma"],
        "14": ["jet", "alet", "elit"],
        "15": ["alev", "lav"],
        "16": ["lobi"],
        "17": ["ulak", "laik"],
        "18": ["lise"],
        "19": ["algı", "laga luga"],
        "20": ["zar"],
        "21": ["zula"],
        "22": ["nine"],
        "23": ["zam", "nam", "nem"],
        "24": ["zıt", "net"],
        "25": ["inç"],
        "26": ["izbe"],
        "27": ["zeki", "zaaf"],
        "28": ["ons", "neşe"],
        "29": ["zig zag", "zıp zıp"],
        "30": ["mor", "mera"],
        "31": ["mal"],
        "32": ["muz"],
        "33": ["mum"],
        "34": ["moda"],
        "35": ["mavi"],
        "36": ["imha", "mıh"],
        "37": ["muaf"],
        "38": ["masa", "mesai", "maaş"],
        "39": ["imge", "map"],
        "40": ["dayı"],
        "41": ["deli"],
        "42": ["tuz", "dana"],
        "43": ["tim"],
        "44": ["data"],
        "45": ["dava", "taç"],
        "46": ["deha"],
        "47": ["taka", "toka"],
        "48": ["taş", "tas"],
        "49": ["dağ", "tepe", "dip"],
        "50": ["çay"],
        "51": ["vali"],
        "52": ["çin", "çan", "can"],
        "53": ["cam", "çam", "çim"],
        "54": ["çatı"],
        "55": ["avcı", "çivi"],
        "56": ["çaba"],
        "57": ["çakı"],
        "58": ["vasi"],
        "59": ["çağ", "çap"],
        "60": ["bar"],
        "61": ["bal"],
        "62": ["ben", "biz"],
        "63": ["bim", "ham"],
        "64": ["bit", "batı"],
        "65": ["baca", "bacı", "hacı"],
        "66": ["baba"],
        "67": ["book"],
        "68": ["baş"],
        "69": ["bp", "hp", "bağ"],
        "70": ["kar"],
        "71": ["fil", "akıl"],
        "72": ["kız"],
        "73": ["kum"],
        "74": ["kedi"],
        "75": ["keçi"],
        "76": ["kaba", "fobi"],
        "77": ["fake", "kafe"],
        "78": ["kaş", "fiş"],
        "79": ["kapı"],
        "80": ["sarı"],
        "81": ["salı"],
        "82": ["saz"],
        "83": ["şam", "sim"],
        "84": ["set"],
        "85": ["suç", "saç"],
        "86": ["şah", "soba"],
        "87": ["saf", "şef"],
        "88": ["şase"],
        "89": ["sap", "sopa"],
        "90": ["peri", "gri"],
        "91": ["pil", "göl"],
        "92": ["göz"],
        "93": ["gemi", "gömü"],
        "94": ["gıda"],
        "95": ["güç", "göç"],
        "96": ["gebe"],
        "97": ["pak", "gök"],
        "98": ["paşa"],
        "99": ["gaip"]
    }

    list_harf = [{'key': key, 'vals': ", ".join(vals)} for key, vals in dict_harf.items()]

    list_sayi = [{'key': key, 'vals': ", ".join(vals)} for key, vals in dict_sayi.items()]

    list_sayi_text = [{'text': ", ".join([key, *vals])} for key, vals in dict_sayi.items()]

    sort_sayi_text = ListProperty(list_sayi_text)

    def set_list_sayis(self, text="", search=False):
        self.sort_sayi_text = [txt for txt in self.list_sayi_text if text in txt["text"]]

    def build(self):
        self.root = Builder.load_string(root_kv)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "500"

        layout = self.root.ids.grid_harf
        for rakam, harfs in self.dict_harf.items():
            layout.add_widget(MDLabel(text=f"{rakam}", halign="center", theme_text_color="Primary", font_style="H2"))
            layout.add_widget(MDLabel(text=", ".join(harfs), halign="center", theme_text_color="Primary"))

        return self.root


MajorSistem().run()