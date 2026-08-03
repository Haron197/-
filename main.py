import sqlite3
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel

DB_NAME = "inspection_official.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. جدول التقارير الميدانية والتفاصيل الإدارية للأستاذ
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inspection_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prof_name TEXT, 
            work_place TEXT,
            degree TEXT,
            degree_date TEXT,
            inspection_date TEXT,
            mark_num TEXT
        )
    ''')
    
    # 2. جدول التوقيت الأسبوعي
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prof_name TEXT,
            day_name TEXT,
            time_slot TEXT,
            class_name TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

KV = '''
MDScreenManager:
    MainDashboardScreen:
    NewInspectionScreen:
    TimetableScreen:
    SearchProfScreen:

<MainDashboardScreen>:
    name: 'dashboard'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "منظومة التفتيش التربوي"
            subtitle: "المفتش: ضيف هارون"

        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "16dp"
                spacing: "12dp"
                size_hint_y: None
                height: self.minimum_height

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    size_hint_y: None
                    height: "90dp"
                    on_release: root.manager.current = 'search_prof'
                    md_bg_color: 0.20, 0.40, 0.60, 1

                    MDLabel:
                        text: "🔍 البحث السريع عن بطاقة أستاذ"
                        font_style: "H6"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        halign: "right"

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    size_hint_y: None
                    height: "90dp"
                    on_release: root.manager.current = 'new_inspection'
                    md_bg_color: 0.12, 0.31, 0.47, 1

                    MDLabel:
                        text: "📋 تسجيل زيارة تفتيش وملازمة إدارية"
                        font_style: "H6"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        halign: "right"

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    size_hint_y: None
                    height: "90dp"
                    on_release: root.manager.current = 'timetable'
                    md_bg_color: 0.18, 0.50, 0.45, 1

                    MDLabel:
                        text: "📅 إسناد وتعديل التوقيت الأسبوعي"
                        font_style: "H6"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        halign: "right"

<NewInspectionScreen>:
    name: 'new_inspection'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "التقرير التربوي والإداري الميداني"
            left_action_items: [["arrow-left", lambda x: setattr(root.manager, 'current', 'dashboard')]]

        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "16dp"
                spacing: "10dp"
                size_hint_y: None
                height: self.minimum_height

                MDTextField:
                    id: prof_name
                    hint_text: "اسم ولقب الأستاذ *"
                    mode: "rectangle"

                MDTextField:
                    id: work_place
                    hint_text: "مكان العمل / المؤسسة *"
                    mode: "rectangle"

                MDTextField:
                    id: degree
                    hint_text: "الدرجة *"
                    mode: "rectangle"

                MDTextField:
                    id: degree_date
                    hint_text: "تاريخ سريان الدرجة (مثال: 2023-01-15) *"
                    mode: "rectangle"

                MDTextField:
                    id: inspection_date
                    hint_text: "تاريخ زيارة التفتيش الحالية *"
                    mode: "rectangle"

                MDTextField:
                    id: mark_num
                    hint_text: "العلامة الممنوحة (/20) *"
                    mode: "rectangle"

                MDFillRoundFlatButton:
                    text: "حفظ البطاقة والتقرير الميداني"
                    size_hint_x: 1
                    on_release: root.save_inspection()

<TimetableScreen>:
    name: 'timetable'
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "جدول التوقيت الأسبوعي"
            left_action_items: [["arrow-left", lambda x: setattr(root.manager, 'current', 'dashboard')]]

        MDBoxLayout:
            orientation: 'vertical'
            padding: "12dp"
            spacing: "8dp"

            MDTextField:
                id: search_prof
                hint_text: "اسم الأستاذ لإسناد/تعديل التوقيت *"
                mode: "rectangle"

            MDScrollView:
                MDBoxLayout:
                    id: schedule_grid
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: "12dp"

            MDFillRoundFlatButton:
                text: "حفظ الجدول الأسبوعي"
                size_hint_x: 1
                on_release: root.save_timetable()

<SearchProfScreen>:
    name: 'search_prof'
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "بطاقة الأستاذ والتوقيت الأسبوعي"
            left_action_items: [["arrow-left", lambda x: setattr(root.manager, 'current', 'dashboard')]]

        MDBoxLayout:
            orientation: 'vertical'
            padding: "16dp"
            spacing: "12dp"

            MDTextField:
                id: prof_search_input
                hint_text: "ادخل اسم ولقب الأستاذ للبحث..."
                mode: "rectangle"

            MDFillRoundFlatButton:
                text: "عرض البطاقة الشاملة"
                size_hint_x: 1
                on_release: root.search_prof_info()

            MDScrollView:
                MDBoxLayout:
                    id: results_container
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: "10dp"
'''

class MainDashboardScreen(MDScreen):
    pass

class NewInspectionScreen(MDScreen):
    def save_inspection(self):
        name = self.ids.prof_name.text.strip()
        work = self.ids.work_place.text.strip()
        deg = self.ids.degree.text.strip()
        deg_date = self.ids.degree_date.text.strip()
        insp_date = self.ids.inspection_date.text.strip()
        mark = self.ids.mark_num.text.strip()

        if name:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO inspection_reports 
                (prof_name, work_place, degree, degree_date, inspection_date, mark_num) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, work, deg, deg_date, insp_date, mark))
            
            conn.commit()
            conn.close()
            
            self.ids.prof_name.text = ""
            self.ids.work_place.text = ""
            self.ids.degree.text = ""
            self.ids.degree_date.text = ""
            self.ids.inspection_date.text = ""
            self.ids.mark_num.text = ""
            self.manager.current = 'dashboard'

class TimetableScreen(MDScreen):
    inputs_dict = {}

    def on_enter(self):
        grid = self.ids.schedule_grid
        grid.clear_widgets()
        self.inputs_dict = {}

        days = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس"]
        time_slots = [
            "08:00 - 09:00", "09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00",
            "13:00 - 14:00", "14:00 - 15:00", "15:00 - 16:00", "16:00 - 17:00"
        ]

        for day in days:
            grid.add_widget(MDLabel(
                text=f"📌 يوم {day}", 
                font_style="Subtitle1", 
                theme_text_color="Primary",
                size_hint_y=None, 
                height="30dp"
            ))

            for slot in time_slots:
                field = MDTextField(
                    hint_text=f"حصـة ({slot}) - ادخل القسم",
                    mode="rectangle",
                    size_hint_y=None,
                    height="40dp"
                )
                key = f"{day}_{slot}"
                self.inputs_dict[key] = field
                grid.add_widget(field)

    def save_timetable(self):
        prof = self.ids.search_prof.text.strip()
        if not prof:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM timetable WHERE prof_name = ?", (prof,))

        for key, field in self.inputs_dict.items():
            class_name = field.text.strip()
            if class_name:
                day, slot = key.split("_", 1)
                cursor.execute(
                    "INSERT INTO timetable (prof_name, day_name, time_slot, class_name) VALUES (?, ?, ?, ?)",
                    (prof, day, slot, class_name)
                )

        conn.commit()
        conn.close()
        self.manager.current = 'dashboard'

class SearchProfScreen(MDScreen):
    def search_prof_info(self):
        prof_name = self.ids.prof_search_input.text.strip()
        container = self.ids.results_container
        container.clear_widgets()

        if not prof_name:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # 1. جلب البيانات الإدارية والتفتيشية للأستاذ
        cursor.execute('''
            SELECT work_place, degree, degree_date, inspection_date, mark_num 
            FROM inspection_reports 
            WHERE prof_name LIKE ? 
            ORDER BY id DESC LIMIT 1
        ''', (f"%{prof_name}%",))
        
        info = cursor.fetchone()

        container.add_widget(MDLabel(
            text=f"👤 بطاقة الأستاذ: {prof_name}",
            font_style="H6",
            size_hint_y=None,
            height="35dp"
        ))

        if info:
            work_place, degree, degree_date, insp_date, mark = info
            
            card_data = [
                f"🏫 مكان العمل: {work_place if work_place else 'غير محدد'}",
                f"🏅 الدرجة الحالية: {degree if degree else 'غير محددة'}",
                f"📅 تاريخ سريان الدرجة: {degree_date if degree_date else 'غير محدد'}",
                f"📝 تاريخ آخر زيارة تفتيش: {insp_date if insp_date else 'غير محدد'}",
                f"📊 العلامة الممنوحة: {mark if mark else 'غير محددة'} / 20"
            ]

            for line in card_data:
                container.add_widget(MDLabel(
                    text=line,
                    font_style="Body1",
                    theme_text_color="Custom",
                    text_color=(0.1, 0.2, 0.4, 1),
                    size_hint_y=None,
                    height="28dp"
                ))
        else:
            container.add_widget(MDLabel(
                text="⚠️ لا توجد بيانات إدارية أو تقارير مسجلة لهذا الأستاذ.",
                font_style="Caption",
                size_hint_y=None,
                height="20dp"
            ))

        # 2. جلب وتنسيق التوقيت الأسبوعي
        cursor.execute('''
            SELECT day_name, time_slot, class_name 
            FROM timetable 
            WHERE prof_name LIKE ? 
            ORDER BY id
        ''', (f"%{prof_name}%",))
        
        schedules = cursor.fetchall()

        container.add_widget(MDLabel(
            text="--------------------------------------------------",
            size_hint_y=None, height="15dp"
        ))

        container.add_widget(MDLabel(
            text="📅 جدول التوقيت الأسبوعي الكامل:",
            font_style="Subtitle1",
            theme_text_color="Primary",
            size_hint_y=None,
            height="35dp"
        ))

        if schedules:
            current_day = ""
            for day, slot, class_name in schedules:
                if day != current_day:
                    current_day = day
                    container.add_widget(MDLabel(
                        text=f"🔹 يوم {day}:",
                        font_style="Subtitle2",
                        theme_text_color="Custom",
                        text_color=(0, 0.4, 0.3, 1),
                        size_hint_y=None,
                        height="30dp"
                    ))
                container.add_widget(MDLabel(
                    text=f"   • الحصة ({slot}) ◄ القسم: {class_name}",
                    font_style="Body2",
                    size_hint_y=None,
                    height="22dp"
                ))
        else:
            container.add_widget(MDLabel(
                text="❌ لم يتم إدخال جدول التوقيت الأسبوعي لهذا الأستاذ بعد.",
                font_style="Caption",
                size_hint_y=None,
                height="20dp"
            ))

        conn.close()

class InspectionAndroidApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(KV)

if __name__ == '__main__':
    InspectionAndroidApp().run()
