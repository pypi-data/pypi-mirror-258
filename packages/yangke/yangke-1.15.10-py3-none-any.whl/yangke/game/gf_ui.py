import os
import time

from PyQt6.QtGui import QPixmap

from yangke.common.QtImporter import (QKeyEvent, QAction, Qt, QHBoxLayout, QMessageBox, QKeyEvent, QVBoxLayout,
                                      QPushButton)

from yangke.common.qt import (YkWindow, run_app, logger, QApplication, QWidget, QLabel, QComboBox,
                              QLineEdit, YkItem, YkInputPanel, YkScrollArea, YkImageWidget, YkDialog, layout_to_widget)
from yangke.common.win.dminput import DMRemote
from yangke.common.win.keyboard import VkCode, CodeToKey
from yangke.game.gf import Step, Steps, Frame, NotExist, Exist, Region, AnchorRegion, RectRegion, Position, Offset
from yangke.base import start_threads, stop_threads, show_pic, pic2qlabel, pic2qpixmap
import pyautogui
from PIL import Image, ImageGrab


class StepWidget(YkItem):
    def __init__(self, idx, op, target, judge, condition, name, root_window):
        self.name = name
        self.step = Step(op, target, judge, condition)
        self.first_item = YkItem(f"步骤{idx}", f"<button on-click='btn_clicked'>删除步骤{idx}</button>",
                                 f"<button on-click='btn_clicked'>运行步骤{idx}</button>",
                                 size=[50, 20, 20])
        self.first_item.value.clicked.connect(root_window.btn_clicked)
        self.first_item.unit.clicked.connect(root_window.btn_clicked)
        self.op_data = {
            "click key": ["键位描述"],
            "press key": ["键位描述"],
            "release key": ["键位描述"],
            "left click": ["画面中的文字", "画面中的图片", "相对偏移", "自定义对象"],
            "right click": ["画面中的文字", "画面中的图片", "相对偏移", "自定义对象"],
            "double click": ["画面中的文字", "画面中的图片", "相对偏移", "自定义对象"],
        }

        self.item11 = QComboBox()
        self.item11.addItems(self.op_data.keys())
        # noinspection all
        self.item11.currentTextChanged.connect(self.change_op)
        self.item12 = QComboBox()
        self.item12.addItems(self.op_data["click key"])
        self.item12.currentTextChanged.connect(self.change_op_dest)
        self.item13_1: QLabel | None = None
        self.item13_2 = QLineEdit("")
        self.item13 = YkItem(None, self.item13_2, None, margins=[0, 0, 0, 0], size=[0, 50, 0], struct=0)

        self.item1 = YkItem(self.item11, self.item12, unit=self.item13,
                            size=[20, 20, 50])
        self.item21 = QComboBox()
        self.item21.addItems(["重复", "等待", "无"])
        self.item22 = QComboBox()
        self.item22.addItems(["直到"])
        self.item23 = QComboBox()
        self.item23.addItems(["无", "存在文字", "存在图片", "不存在文字", "不存在图片", "自定义条件"])
        self.item23.currentTextChanged.connect(self.change_condition)
        self.condition_item = YkItem(label=self.item21,
                                     value=self.item22,
                                     unit=self.item23,
                                     size=[20, 20, 50],
                                     margins=(10, 0, 10, 0))
        self.item31 = None
        self.item31_1: QLabel = QLabel("预览图")
        self.item31_2: QLineEdit = QLineEdit()
        self.prefer_obj_line: QLineEdit = None
        self.range_line = None
        self.bak_item = None
        super().__init__(label=self.first_item, value=self.item1, unit=self.condition_item, bak=self.bak_item,
                         direction="v", bgcolor="green")
        self.set_step(self.step)

    def set_step(self, step):
        try:
            self.item11.setCurrentText(step.op)
            if step.op in ["click key", "press key", "release key"]:
                self.item12.setCurrentText("键位描述")
                if isinstance(step.target, dict):
                    self.item13_2.setText(step.target.get("value"))
                else:
                    self.item13_2.setText(step.target)
            else:
                if isinstance(step.target, Offset):
                    self.item12.setCurrentText("相对偏移")
                    self.item13_1.setText(step.target.anchor_obj)
                    self.item13_2.setText(f"{step.target.dx},{step.target.dy}")
                elif step.target.get("__cls__") == "Offset":
                    ...
                elif step.target.get("__cls__") == "Picture":
                    self.item12.setCurrentText("画面中的图片")
                    self.item13_2.setText(step.target["path"])
                    self.item13_1.setPixmap(QPixmap(step.target["path"]))
                elif step.target.get("__cls__") == "Text":
                    self.item12.setCurrentText("画面中的文字")
                    self.item13_2.setText(step.target["text"])
            if step.judge == "wait":
                self.item22.setCurrentText("等待")
            elif step.judge == "repeat":
                self.item22.setCurrentText("重复")
            else:
                self.item22.setCurrentText("无")
            if step.condition is None:
                self.item23.setCurrentText("无")
            elif isinstance(step.condition, Exist):
                if step.condition.type_ == "text":
                    self.item23.setCurrentText("存在文字")
                    if isinstance(step.condition.value, list) and len(step.condition.value) == 1:
                        text = step.condition.value[0]
                        self.item31.setText(text)
                elif step.condition.type_ == "pic":
                    self.item23.setCurrentText("存在图片")
                    if isinstance(step.condition.value, list) and len(step.condition.value) == 1:
                        path = step.condition.value[0]
                        self.item31_2.setText(path)
                        self.item31_1.setPixmap(QPixmap(path))
            elif isinstance(step.condition, NotExist):
                if step.condition.type_ == "text":
                    self.item23.setCurrentText("不存在文字")
                    if isinstance(step.condition.value, list) and len(step.condition.value) == 1:
                        text = step.condition.value[0]
                        self.item31.setText(text)
                elif step.condition.type_ == "pic":
                    self.item23.setCurrentText("不存在图片")
                    if isinstance(step.condition.value, list) and len(step.condition.value) == 1:
                        path = step.condition.value[0]
                        self.item31_2.setText(path)
                        self.item31_1.setPixmap(QPixmap(path))
            else:
                self.item23.setCurrentText("自定义条件")
                self.prefer_obj_line.setText(step.condition.value)

            if isinstance(step.condition, Exist) or isinstance(step.condition, NotExist):
                if step.condition.anchor_name is not None:
                    self.prefer_obj_line.setText(step.condition.anchor_name)
                if step.condition.region is not None:
                    if isinstance(step.condition.region, list):
                        _ = [str(__) for __ in step.condition.region]
                        self.range_line.setText(",".join(_))


        except:
            logger.warning(f"StepWidget加载出错")

    def form_bak_item(self):
        condition = self.condition_item.get_value_and_unit()[1]
        if condition == "无":
            self.bak_item = None
            return self.bak_item
        elif condition == "存在文字" or condition == "不存在文字":
            self.item31 = QLineEdit()
            self.item31.setPlaceholderText("输入条件判断的文字")
        elif condition == "自定义条件":
            self.item31 = None
            self.prefer_obj_line = QLineEdit()
            self.prefer_obj_line.setPlaceholderText("输入自定义条件")
            self.range_line = None
            self.bak_item = YkItem(label=self.item31, value=self.prefer_obj_line, unit=self.range_line,
                                   size=[0, 90, 0], margins=[1, 10, 0, 10])
            return self.bak_item
        else:
            self.item31_1 = QLabel("预览图")
            self.item31_2 = QLineEdit("")
            self.item31_2.setPlaceholderText("图片路径")
            self.item31 = YkItem(self.item31_1, self.item31_2, f"<button on-click='capture_mini_pic'>截图</button>",
                                 size=[16, 22, 12], margins=[0, 0, 0, 0], struct=2, parent=self)
            self.item31.unit.clicked.connect(self.capture_mini_pic)
        self.prefer_obj_line = QLineEdit()
        self.prefer_obj_line.setPlaceholderText("输入参考点定义")
        self.range_line = QLineEdit()
        self.range_line.setPlaceholderText("输入查找区域定义")
        self.bak_item = YkItem(label=self.item31, value=self.prefer_obj_line, unit=self.range_line,
                               size=[50, 20, 20])

        return self.bak_item

    def get_step(self):
        op = self.item11.currentText()
        if self.item12.currentText() == "相对偏移":
            target = {
                "__cls__": "Offset",
                "value": self.item13.get_value(),
                "anchor": self.item13.get_label_text()
            }
        elif self.item12.currentText() == "画面中的图片":
            target = {
                "__cls__": "Pic",
                "value": self.item13.get_value(),
                "anchor": self.item13.get_label_text()
            }
        elif self.item12.currentText() == "画面中的文字":
            target = {
                "__cls__": "Text",
                "value": self.item13.get_value(),
            }
        elif self.item12.currentText() == "键位描述":
            target = {
                "__cls__": "Key",
                "value": self.item13.get_value(),
            }
        else:  # "自定义对象"
            target = {
                "__cls__": "UserDefObj",
                "value": self.item13.get_value(),
            }
        judge = self.item21.currentText()
        cond = self.item23.currentText()
        if self.item31 is not None:
            if isinstance(self.item31, QLineEdit):
                dest_obj = self.item31.text()
            elif isinstance(self.item31, YkItem):
                dest_obj = self.item31.get_value()
            else:
                dest_obj = None
        else:
            dest_obj = None
        judge = {"重复": "repeat", "等待": "wait", "无": None}.get(judge)
        anchor_name = None
        dest_range = None
        if self.prefer_obj_line.text() is not None:
            anchor_name = self.prefer_obj_line.text()
        _ = self.range_line.text()
        if _ is not None and _.strip() != "":
            dest_range = _.strip().split(",")
            try:
                dest_range = [int(_) for _ in dest_range]
            except:
                logger.error(f"目标区域中存在非数值类型字符{dest_range=}")

        if cond == "无":
            condition = None
        elif cond == "存在文字":
            condition = Exist(dest_obj, type_="text", region=dest_range, anchor_name=anchor_name)
        elif cond == "不存在文字":
            condition = NotExist(dest_obj, type_="text", region=dest_range, anchor_name=anchor_name)
        elif cond == "存在图片":
            condition = Exist(dest_obj, type_="pic", region=dest_range, anchor_name=anchor_name)
        elif cond == "不存在图片":
            condition = NotExist(dest_obj, type_="pic", region=dest_range, anchor_name=anchor_name)
        else:  # cond == "自定义条件"
            condition = self.item31.get_value()
        return Step(op=op, target=target, judge=judge, condition=condition)

    def change_op(self):
        op_name = self.item11.currentText()
        self.item12.clear()
        self.item12.addItems(self.op_data[op_name])

    def change_op_dest(self):
        op_type = self.item12.currentText()
        if op_type == "画面中的文字":
            self.item13.clear_all()
            self.item13.add_item(0, "")
            self.item13_2 = QLineEdit("")
            self.item13.add_item(1, self.item13_2)
            self.item13_2.setPlaceholderText("输入点击的文字")
            self.item13.set_size({"width": [0, 50, 0]})
        elif op_type == "键位描述":
            self.item13.clear_all()
            self.item13.add_item(0, "")
            self.item13_2 = QLineEdit("")
            self.item13.add_item(1, self.item13_2)
            self.item13_2.setPlaceholderText("输入键盘按键或组合键描述")
            self.item13.set_size({"width": [0, 50, 0]})
        elif op_type == "画面中的图片":
            self.item13.clear_all()
            self.item13_1 = QLabel("预览图")
            self.item13.add_item(0, self.item13_1)
            self.item13_2 = QLineEdit("")
            self.item13_2.setPlaceholderText("图片路径")
            self.item13.add_item(1, self.item13_2)
            self.item13.add_item(2, f"<button on-click='capture_mini_pic'>截图</button>")
            self.item13.set_size({"width": [16, 22, 12]})
            self.item13.unit.clicked.connect(self.capture_mini_pic)
        elif op_type == "相对偏移":
            self.item13.clear_all()
            self.item13_1 = QLineEdit("")
            self.item13_1.setPlaceholderText("输入偏移对象")
            self.item13_1.setToolTip("例如：step1.target/step1.condition")
            self.item13.add_item(0, self.item13_1)
            self.item13_2 = QLineEdit("")
            self.item13.add_item(1, self.item13_2)
            self.item13_2.setPlaceholderText("输入偏移参数")
            self.item13_2.setToolTip("例如：300, 100表示偏移dx=300, dy=200")
            self.item13.set_size({"width": [25, 25, 0]})
        elif op_type == "自定义对象":
            self.item13.clear_all()
            self.item13.add_item(0, "")
            self.item13_2 = QLineEdit("")
            self.item13.add_item(1, self.item13_2)
            self.item13_2.setPlaceholderText("")
            self.item13.set_size({"width": [0, 50, 0]})

    def change_condition(self):
        self.remove_item(3)
        self.add_item(3, self.form_bak_item())

    def capture_mini_pic(self):
        sender = self.sender()
        if isinstance(sender, QPushButton):
            text = sender.text()
            if text == "截图":
                pyautogui.hotkey("win", "shift", "s")
                sender.setText("粘贴")
            elif text == "粘贴":
                parent = sender.parent().parent()
                if isinstance(parent, YkItem) and parent.get_value() == "画面中的图片":
                    # 说明是鼠标点击的图片
                    step_name = sender.parent().parent().parent().label.label.text()  # 步骤1
                    file_name = f"{self.name}_{step_name}_click_obj.png"
                else:
                    # 说明是条件判断的图片
                    step_name = sender.parent().parent().parent().label.label.text()  # 步骤1
                    file_name = f"{self.name}_{step_name}_condition_obj.png"
                im = ImageGrab.grabclipboard()
                if isinstance(im, Image.Image):
                    im.save(file_name)
                    sender.parent().value.setText(file_name)
                    label: QLabel = sender.parent().label
                    label.setPixmap(QPixmap(file_name))
                    label.setScaledContents(True)
                elif im:
                    for filename in im:
                        print("filename:%s" % filename)
                        im = Image.open(filename)
                else:
                    print("clipboard is empty")

                sender.setText("截图")


class MainWindow(YkWindow):

    def __init__(self):
        super().__init__()
        self.temp_ = None
        self.add_input_panel("ui/ui_panel.yaml", domain="综合")
        self.thread = None
        self.running = False
        self.set_status_bar_label("天谕")
        self.frame: Frame | None = None
        self.add_input_panel("ui/ui_panel.yaml", domain="自定义步骤")
        panel: YkInputPanel = self.panels.get("自定义步骤")
        step_name = panel.get_values_and_units(need_unit=False)[0].strip()
        if step_name is None or step_name == "":
            panel.set_value("步骤序列名称", "自定义任务1")
            step_name = "自定义任务1"
        else:
            panel.set_value("步骤序列名称", step_name)
        if self.proj.get("temp_steps") is None or self.proj.get("temp_steps") == []:
            item = StepWidget(1, "press", "R", None, None, step_name, self)
            if panel is not None:
                panel.insert_item(1, item)
        else:
            for idx, step in enumerate(self.proj.get("temp_steps")):
                item = StepWidget(idx=idx + 1, root_window=self, name=step_name, **step)
                panel.insert_item(idx + 1, item)
            # self.add_content_tab(YkItem(), "存在条件设置")
        self.capture_ykimagewidget = YkImageWidget([], True, self.do_action)
        scroll = YkScrollArea()
        scroll.setWidget(self.capture_ykimagewidget)
        self.add_content_tab(widget=scroll, tab_name="CT截图")
        self._keyboard = False  # 模拟键盘功能是否开启
        self._mouse = False  # 模拟鼠标功能是否开启
        if self.proj.get("dm_sim_info") is None:
            self.proj.update({"dm_sim_info": {"key": "null",
                                              "add_key": "",
                                              "display": "gid2",
                                              "mouse": "dx.mouse.position.lock.api",
                                              "keypad": "windows",
                                              "public": "",
                                              "mode": "101:超级绑定模式.可隐藏目标进程中的dll，推荐使用",
                                              "port": 8765},
                              "sim_mode": "DM-remote"},
                             )
        if self.proj.get("temp_steps") is None:
            self.proj.update({
                "temp_steps": []
            })
        if self.proj.get("steps_repos") is None:
            self.proj.update({
                "steps_repos": {}
            })

        self.mode_repos = {
            "天谕": {
                "display": "dx.graphic.3d",
                "mouse": "dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor",
                "keypad": "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api|dx.keypad.raw.input",
                "public": "",
                "mode": "101:超级绑定模式.可隐藏目标进程中的dll，推荐使用",
            },
            "天谕1": {
                "display": "dx.graphic.3d.10plus",
                "mouse": "dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor|dx.mouse.raw.input",
                "keypad": "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api",
                "public": "",
                "mode": "0:推荐模式此模式比较通用，而且后台效果是最好的",
            },
            "笑傲江湖": {

            },
            "剑叁": {

            }
        }

        self.proj.get("dm_sim_info").update(self.mode_repos.get("天谕1"))

    def yk_signal_received(self, msg: dict):
        if msg.get("action") == "capture_window":
            self.capture_window()

    def set_sim_mode(self):
        _ = os.path.abspath(os.path.join(os.path.dirname(__file__), "ui", "ui_panel.yaml"))
        input_panel = YkInputPanel(from_file=_, domain="设置键鼠模拟方式", parent=self)

        dialog = YkDialog(self, widget=input_panel)
        dialog.set_size(600, 500)
        input_panel.apply_btn_connect()
        self.temp_ = {"input_panel": input_panel, "dialog": dialog}

        dm_sim_info = self.proj.get("dm_sim_info")
        input_panel.set_value("注册码", value=dm_sim_info.get("key") or "null")
        input_panel.set_value("附加码", value=dm_sim_info.get("add_key") or "")
        input_panel.set_value("显示", value=dm_sim_info.get("display") or "gdi2")
        input_panel.set_value("鼠标", value=dm_sim_info.get("mouse") or "dx.mouse.position.lock.api")
        input_panel.set_value("键盘", value=dm_sim_info.get("keypad") or "windows")
        input_panel.set_value("公共参数", value=dm_sim_info.get("public") or "")
        input_panel.set_value("模式", value=dm_sim_info.get("mode"))
        try:
            input_panel.set_value("端口", value=int(dm_sim_info.get("port")) or 8765)
        except:
            QMessageBox.warning(None, "错误提示", f"端口号必须是整数，当前为({dm_sim_info.get('port')})")
            input_panel.set_value("端口", value=8765)

    def _change_sim_mode(self):
        input_panel: YkInputPanel = self.temp_.get("input_panel")
        type_ = input_panel.get_item("模拟方式").get_value()
        input_panel.remove_item(index=list(range(1, input_panel.get_items_count())))
        if type_ == "DM-remote":
            dm_sim_info = self.proj.get("dm_sim_info")
            input_panel.append_item(YkItem("注册码", "", "", size=[30, 130, 0]), )
            input_panel.set_value("注册码", value=dm_sim_info.get("key") or "null")
            input_panel.append_item(YkItem("附加码", "", "", size=[30, 130, 0]), )
            input_panel.set_value("附加码", value=dm_sim_info.get("add_key") or "")
            input_panel.append_item(YkItem("显示", "", "", size=[30, 130, 0]), )
            input_panel.set_value("显示", value=dm_sim_info.get("display") or "gdi2")
            input_panel.append_item(YkItem("鼠标", "", "", size=[30, 130, 0]), )
            input_panel.set_value("鼠标", value=dm_sim_info.get("mouse") or "dx.mouse.position.lock.api")
            input_panel.append_item(YkItem("键盘", "", "", size=[30, 130, 0]), )
            input_panel.set_value("键盘", value=dm_sim_info.get("keypad") or "windows")
            input_panel.append_item(YkItem("公共参数", "", "", size=[30, 130, 0]), )
            input_panel.set_value("公共参数", value=dm_sim_info.get("public") or "")
            input_panel.append_item(YkItem("模式", "", "", size=[30, 130, 0]), )
            input_panel.set_value("模式",
                                  value=dm_sim_info.get("mode") or "101:超级绑定模式.可隐藏目标进程中的dll，推荐使用")
            input_panel.append_item(YkItem("端口", "", "", size=[30, 130, 0]), )
            input_panel.set_value("端口", value=dm_sim_info.get("port") or 8765)

        elif type_ == "Normal":
            pass

    def add_step(self):
        panel: YkInputPanel = self.panels.get("自定义步骤")
        idx = panel.get_items_count()
        name = panel.get_item("步骤序列名称").value.text()
        panel.insert_item(idx, StepWidget(idx, "press", "R", None, None, name, self))

    def init(self):
        self.init_frame()

        self.frame.init_chat(anchor="ui/ZhaoMu.png", anchor_region=AnchorRegion(0, "anchor.y1", "anchor.x1", -10),
                             channels=["世界", "团队", "队伍", "附近", "阵营", "地区"])
        suc = self.frame.init_task(anchor="任务", find_region=RectRegion(left=-350, top=300, right=-1, bottom=-500),
                                   anchor_region=AnchorRegion("anchor.x1", "anchor.y1", -10, "anchor.y1+400"))
        if not suc:
            self.frame.init_task(anchor="驻地", find_region=RectRegion(left=-350, top=300, right=-1, bottom=-500),
                                 anchor_region=AnchorRegion("anchor.x1-100", "anchor.y1", -10, "anchor.y1+400"))

        # self.frame.init_time(region=(-170, 0, -2, 30))
        self.frame.init_time(region=(-25, 5, -2, 25))
        # self.frame.turn_direction_to("青蛙", region=Region(width_child=1000, height_child=800))

    def run(self):
        self.init()
        settings = self.get_value_of_panel(need_dict=True, need_unit=False)
        key = settings.get("打怪技能按键")
        role = settings.get("游戏ID").strip()
        mode = settings.get("打怪模式")
        freq = float(settings.get("按键频率"))
        # self.frame = Frame(role)
        # link_pos = self.frame.task.get_text_link_pos_global("打开公会")
        # self.frame.show_region(link_pos)
        #
        # self.frame.left_click(*link_pos.get_center(), offset=(16, 0))
        # self.frame.dm.unbind_window()
        if mode == "无脑打怪":
            steps_重复按键 = Steps(
                steps=[
                    Step("press", key, None, None),
                ]
            )
        else:
            steps_重复按键 = Steps(
                steps=[
                    Step("press", key, "until",
                         NotExist("竹林偷伐者", last_time=20, region=Region(align="center", width_child=600)),
                         wait_method="repeat"),
                    Step("double-press", "space", "until",
                         Exist("竹林偷伐者", last_time=60, interval=10, region=Region(align="center", width_child=600)),
                         wait_method="repeat"),
                ]
            )
        self.thread = start_threads(self.frame.run_steps_forever, args_list=[steps_重复按键, freq])
        self._input_panel.get_button("运行").setDisabled(True)
        self._input_panel.get_button("停止").setDisabled(False)

    def stop(self):
        stop_threads(self.thread)
        self.running = False
        logger.debug(f"停止挂机")
        self._input_panel.get_button("停止").setDisabled(True)
        self._input_panel.get_button("运行").setDisabled(False)
        if self.proj.get("sim_mode") == "DM-remote":
            self.frame.dm.unbind_window()
            if self._mouse:
                self._mouse = False
            if self._keyboard:
                self._keyboard = False

    def init_frame(self, force_update=False):
        """
        绑定需要操作的窗口界面

        :params force_update： 已有绑定窗口时是否强制更新绑定的窗口
        """
        if self.frame is None or self.frame.window is None or force_update:
            settings = self.get_value_of_panel(need_dict=True, need_unit=False, domain="综合")
            role = settings.get("游戏ID").strip()

            self.frame = Frame(role,
                               sim_mode=self.proj.get("sim_mode"),
                               sim_info=self.proj.get("dm_sim_info"))
            if self.frame.window is None:
                self.statusBar1.showMessage("未找到游戏窗口")
                return None
        return self.frame

    def do_action(self, x, y, op):
        """
        执行操作，然后等待1s，截图显示
        """
        if self._mouse:  # 如果开启了鼠标模拟测试，则转发鼠标操作至绑定的窗口
            if self.frame is not None and self.frame.window is not None:
                if op == "left_click":
                    self.frame.left_click(x, y)
                elif op == "right_click":
                    self.frame.right_click(x, y)

    def capture_window(self):
        self.init_frame()
        if self.frame.window is None:
            return
        snapshot = self.frame.capture_window_xywh()
        if len(snapshot) == 0:  # snapshot == []
            return
        if self.capture_ykimagewidget is None:
            self.capture_ykimagewidget = YkImageWidget(snapshot, True, self.do_action)
            scroll = YkScrollArea()
            scroll.setWidget(self.capture_ykimagewidget)
            self.add_content_tab(widget=scroll, tab_name="CT截图")
            # self.add_content_tab(widget=self.capture_ykimagewidget, tab_name="CT截图")
        else:
            self.capture_ykimagewidget.replace_image(snapshot)

        if "CT截图" in self._content_tab.labels and self._content_tab.get_current_tab_name() != "CT截图":
            self._content_tab.activate_tab("CT截图")

    def real_time_capture(self):
        logger.info("开始实时截图")
        while self._mouse or self._keyboard:
            self.yk_signal.emit({"action": "capture_window"})
            time.sleep(0.1)
        logger.info("实时截图结束")

    def btn_clicked(self, anything=None, anything2=None, **kwargs):
        """
        在截图区域上点击时的响应时间
        """
        sender = self.sender()
        text = sender.text()
        if text == "截图":
            self.capture_window()
        elif text == "加载DM":
            sim_info = self.proj.get("dm_sim_info")
            dm_remote = DMRemote(key=sim_info.get("key"), add_key=sim_info.get("add_key"), port=sim_info.get("port"))
            if dm_remote.success:
                QMessageBox.information(None, "提示", "DM-remote加载成功")
            else:
                QMessageBox.information(None, "提示", f"DM-remote加载失败，{dm_remote.error_info}")
        elif text == "保存键鼠模拟方式":
            input_panel: YkInputPanel = self.temp_.get("input_panel")
            values = input_panel.get_values_and_units(need_unit=False, need_dict=True, need_label=True)
            self.proj.update({"sim_mode": values.get("模拟方式")})
            if values.get("模拟方式") == "DM-remote" or values.get("模拟方式") == "DM-local":
                try:
                    port = values.get("端口")
                except:
                    QMessageBox(None, "错误提示", f"端口号必须是整数，当前为({values.get('端口')})")
                    port = self.proj.get("dm_sim_info").get("port") or 8765
                self.proj.get("dm_sim_info").update({"key": values.get("注册码"),
                                                     "add_key": values.get("附加码"),
                                                     "display": values.get("显示"),
                                                     "mouse": values.get("鼠标"),
                                                     "keypad": values.get("键盘"),
                                                     "public": values.get("公共参数"),
                                                     "mode": values.get("模式"),
                                                     "port": port,
                                                     })
            else:
                pass
        elif text == "运行步骤序列":
            self.init_frame()
            panel: YkInputPanel = self.panels.get("自定义步骤")
            steps = []
            for i in range(1, panel.get_items_count()):
                _step = panel.get_item(f"步骤{i}")
                self.statusBar1.showMessage(f"执行步骤{i}")
                step = _step.get_step()
                steps.append(step)
            if self.frame.run_steps(Steps(steps)):
                self.statusBar1.showMessage("步骤序列执行完毕")
            else:
                self.statusBar1.showMessage("步骤序列执行失败，原因请查询日志")
        elif text == "保存步骤序列":
            panel: YkInputPanel = self.panels.get("自定义步骤")
            steps_name = panel.get_item("步骤序列名称").get_value()
            steps_json = []
            for i in range(1, panel.get_items_count()):
                _step = panel.get_item(f"步骤{i}")
                step = _step.get_step()
                steps_json.append(step.to_json())
            self.proj["temp_steps"] = steps_json
            self.proj["steps_repos"].update({steps_name: steps_json})
            self.statusBar1.showMessage(f"步骤序列 [{steps_name}] 保存成功")
        elif text.startswith("运行步骤"):
            self.statusBar1.showMessage("开始执行步骤")
            panel: YkInputPanel = self.panels.get("自定义步骤")
            idx = int(text.replace("运行步骤", ""))
            step_widget: StepWidget = panel.get_item(f"步骤{idx}")
            step: Step = step_widget.get_step()
            self.frame.run_steps(Steps([step]))
            self.statusBar1.showMessage("步骤执行完毕")
        elif text.startswith("删除步骤"):
            panel: YkInputPanel = self.panels.get("自定义步骤")
            panel.remove_item(-1)

    def event(self, event):
        if isinstance(event, QKeyEvent):
            if self._keyboard:
                if (event.key() in [Qt.Key_Tab, Qt.Key_F5]
                        and event.type() == QKeyEvent.Type.KeyRelease):
                    self.keyPressEvent(event)  # Qt默认Tab键会被窗口处理，不会传递给KeyPressEvent事件
                    return True  # 该事件已被处理
            else:
                return super().event(event)

        return super().event(event)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        """
        测试方法只支持短按，不支持按键不放，但按键不放可以在内部实现
        """
        if self._keyboard:  # 如果模拟键盘开启，则拦截所有键盘按键至绑定的窗口
            self.init_frame()
            modifiers = a0.modifiers()  # 是否按下组合键
            key_code = a0.key()

            if key_code in [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Shift]:
                return

            key = CodeToKey[key_code]
            if modifiers == Qt.NoModifier:
                self.frame.press_key(key=key)
            elif modifiers == Qt.KeyboardModifier.ControlModifier:
                self.frame.press_key(key=f"Ctrl+{key}")
            elif modifiers == Qt.KeyboardModifier.AltModifier:
                self.frame.press_key(key=f"Alt+{key}")
            elif modifiers == Qt.KeyboardModifier.ShiftModifier:
                self.frame.press_key(key=f"Shift+{key}")
            elif modifiers == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.AltModifier):
                self.frame.press_key(key=f"Ctrl+Alt+{key}")
        else:
            if self.capture_ykimagewidget.region_show:
                if a0.key() == Qt.Key_Escape:
                    self.capture_ykimagewidget.region_show = False
                    self.capture_window()
                    return
            super().keyPressEvent(a0)

    def keyReleaseEvent(self, *args, **kwargs):
        super().keyReleaseEvent(*args, **kwargs)

    def show_new_region(self):
        if self.capture_ykimagewidget is None:
            return
        geo = self.capture_ykimagewidget.geometry()
        self.capture_ykimagewidget.region_show = True

    def tool_click(self, k1):
        # 工具栏点击事件
        sender: QAction = self.sender()
        text: str = self.sender().text()
        if text == "模拟键盘":
            if self._keyboard:
                sender.setChecked(False)
                self._keyboard = False
            else:
                sender.setChecked(True)
                self._keyboard = True
                self.panels.get("综合").get_button("停止").setDisabled(False)
                if self._mouse is False:
                    start_threads(self.real_time_capture)
        elif text == "模拟鼠标":
            if self._mouse:
                sender.setChecked(False)
                self._mouse = False
            else:
                sender.setChecked(True)
                self._mouse = True
                self.panels.get("综合").get_button("停止").setDisabled(False)
                if self._keyboard is False:
                    start_threads(self.real_time_capture)
        elif text == "绑定窗口":
            self.init_frame()
            QMessageBox.information(self, "提示", "窗口绑定成功")
        elif text == "新建区域":
            self.show_new_region()
            self.capture_window()


run_app(MainWindow)
