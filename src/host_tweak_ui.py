#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
from host_tweak_handler import HostTweakHandler

"""
host切换工具
@author: thebye85
@date: 2013-06-06
"""
class HostTweakUI:
	
	#状态栏图标
	icon = "/usr/share/pixmaps/hosttweak/24x24/hosttweak.png"
	
	def __init__(self):
		self.ui_statusicon = None
		self.ui_window = None
		self.ui_textView = None
		self.ui_comboBox = None
		self.ui_deleteButton = None
		self.ui_comboBox_changed_event = True
		
		self.tweakHandler = HostTweakHandler()
		self.__init_ui()
		self.__show_ui()
	
	
	#初始化UI
	def __init_ui(self):
		#statusIcon
		statusicon = gtk.StatusIcon()
		self.ui_statusicon = statusicon
		#设置icon
		statusicon.set_from_file(self.icon)
		#右键点击icon触发的事件
		statusicon.connect("popup-menu", self.__statusicon_right_click_event)
		#左键点击icon触发的事件
		statusicon.connect("activate", self.__statusicon_left_click_event)

		#window
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.ui_window = window
		window.set_default_size(400, 500) #窗口大小
		window.set_position(gtk.WIN_POS_CENTER_ALWAYS) #默认在屏幕中间显示
		window.set_resizable(True)  
		window.set_title("host tweak v0.1")
		window.set_border_width(0)
        
		#VBox
		vbox = gtk.VBox(False, 0)
		vbox.set_border_width(10)
		vbox.show()
		
		self.ui_vbox = vbox
		
		window.add(vbox)
		
		
		#ScrolledWindow
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw, True, True, 0)
		
		#TextView
		textview = gtk.TextView()
		self.ui_textView = textview
		textbuffer = textview.get_buffer()
		#读取当前系统host
		#textbuffer.set_text(self.tweakHandler.get_current_host())
		textview.show()
		sw.add(textview)
		sw.show()
		
		#HSeparator
		separator = gtk.HSeparator()
		vbox.pack_start(separator, False, False, 10)
		separator.show()
		
		
		#ComboBoxBox
		hostComboBox = gtk.combo_box_new_text()
		self.ui_comboBox = hostComboBox
		#初始下拉选项，默认选中第1个选项
		self.__init_select_options()
		#注册事件
		hostComboBox.connect("changed", self.__on_select_changed)
		hostComboBox.show()
		vbox.pack_start(hostComboBox, False, False, 0)
		
		#HButtonBox
		hButtonBox = gtk.HButtonBox()
		vbox.pack_start(hButtonBox, False, False, 0)
#		hButtonBox.set_layout(gtk.BUTTONBOX_SPREAD)
		hButtonBox.set_layout(gtk.BUTTONBOX_EDGE)
		hButtonBox.show()
		
		#Button
		saveButton = gtk.Button("保存host")
		saveButton.connect("clicked", self.save_host)
		hButtonBox.pack_start(saveButton, False, False, 0)
		saveButton.show()
		
		#Button
		deleteButton = gtk.Button("删除host")
		self.ui_deleteButton = deleteButton
		deleteButton.connect("clicked", self.delete_host)
		hButtonBox.pack_start(deleteButton, False, False, 0)
		deleteButton.show()
		#判断是否要disable删除按钮
		self.__check_and_disable_delete_button()
		
		#Button
		saveNewButton = gtk.Button("另存为host")
		saveNewButton.connect("clicked", self.save_new_host)
		hButtonBox.pack_start(saveNewButton, False, False, 0)
		saveNewButton.show()
		
		#window.connect("destroy", self.__close_application)
		#点击关闭只隐藏窗体
		#window.connect("destroy", lambda w: self.ui_window.hide())
		window.connect("delete_event", self.__hide_window)
		window.show_all()
		
	
	
	#将hostContent显示在textView组件上
	def __show_host_on_text_view(self, hostContent):
		self.ui_textView.get_buffer().set_text(hostContent)
	
	
	def __init_select_options(self):
		#获取当前系统host对应的host配置名称
		systemHostName = self.tweakHandler.get_host_name_equals_system_host()
		
		#重新加载option并选中当前系统host
		self.__reload_select_options_and_select_option(systemHostName)
	
	
	#选中目标host选项，并显示相应的host内容
	def __select_combobox_option(self, targetHostName):
		#选中的option
		optionIndex = 0
		if(targetHostName):
			for hostName in self.tweakHandler.get_all_host_select_options():
				if(hostName == targetHostName):
					self.ui_comboBox.set_active(optionIndex)
					#textview显示选中的host
					self.__set_textview_text(self.tweakHandler.read_host(self.ui_comboBox.get_active_text()))
					return
				optionIndex = optionIndex + 1
			
		#未找到目标option，则选中第1个
		self.ui_comboBox.set_active(optionIndex)
		##textview显示选中的host
		self.__set_textview_text(self.tweakHandler.read_host(self.ui_comboBox.get_active_text()))

	
	#重新加载下拉选项并选中目标选项，如果targetHostName为空则选中第1个option
	def __reload_select_options_and_select_option(self, targetHostName = None):
		#关闭comboBox changed事件
		self.__disable_changed_event()
		#删除options
		self.ui_comboBox.get_model().clear()
		
		#匹配到的目标host名称
		matchedHostName = None
		#重新加载host名称，并显示当前host对应的option
		selectOptionList = self.tweakHandler.get_all_host_select_options()
		for hostName in selectOptionList:
			self.ui_comboBox.append_text(hostName)
			if(targetHostName and targetHostName == hostName):
				matchedHostName = hostName
				
		if(matchedHostName):
			self.__select_combobox_option(matchedHostName)	
		else:
			#没有匹配则显示第1个host
			self.__select_combobox_option(selectOptionList[0])	
		
		#打开comboBox changed事件
		self.__enable_changed_event()
		
	
	def __disable_changed_event(self):
		self.ui_comboBox_changed_event = False
		
	def __enable_changed_event(self):
		self.ui_comboBox_changed_event = True
	
	
	#获取当前选中的host名称
	def __get_comboxBox_selected_option(self):
		model = self.ui_comboBox.get_model() #获取全部select选项
		index = self.ui_comboBox.get_active() #返回当前选中选项的position，不存在则返回-1
		if(index != -1):
			return model[index][0]
		else:
			print "get comboBox selected option error|model=", model, "|index=", index
			return None
	
	#返回当前textview的内容	
	def __get_textview_text(self):
		buffer = self.ui_textView.get_buffer()
		start, end = buffer.get_bounds()
		return buffer.get_text(start, end)
	
	#设置textview内容
	def __set_textview_text(self, hostContent):
		self.ui_textView.get_buffer().set_text(hostContent)
	
	#保存新host
	def __on_clicked_save_new_host(self, dialog, responseId, input):
		#点击关闭或取消事件则直接关闭
		if(responseId == gtk.RESPONSE_DELETE_EVENT or responseId == gtk.RESPONSE_REJECT):
			dialog.destroy()
			return
		
		#获取输入框内容
		newHostName = input.get_text()
		if(not newHostName):
			return
		self.tweakHandler.save_new_host(newHostName, self.__get_textview_text())
		#重新加载option
		self.__reload_select_options_and_select_option(newHostName)
		#判断是否要disable删除按钮
		self.__check_and_disable_delete_button()
		dialog.destroy()
	
	
	
	#切换host
	def __on_select_changed(self, comboBox):
		if(self.ui_comboBox_changed_event == True):
			print "is_changed_event_valid"
			hostContent = self.tweakHandler.read_host(self.__get_comboxBox_selected_option())
			self.__show_host_on_text_view(hostContent)
		else:
			print "is_changed_event_invalid"
	
	
			
	#判断combobox如果只有一个option，则删除按钮不能点击	
	def __check_and_disable_delete_button(self):
		if(len(self.ui_comboBox.get_model()) <= 1):
			#button不可点击
			self.ui_deleteButton.set_sensitive(False)
		else:
			self.ui_deleteButton.set_sensitive(True)
	
	#另存为host
	def save_new_host(self, button):
		#弹出输入框，用户输入新的host名称
		input = gtk.Entry()
		#设置输入框最大长度
		input.set_max_length(30)
		dialog = gtk.Dialog(title="请输入新host名称", 
					parent=self.ui_window,
			   		flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			   		buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
				)
		dialog.vbox.pack_start(input)
		input.show()
		dialog.connect("response", self.__on_clicked_save_new_host, input)
		dialog.run()
		
		
	#使用当前host
#	def use_host(self, button):
#		self.tweakHandler.use_host(self.__get_textview_text())
	
	
	#保存host
	def save_host(self, button):
		currentHostName = self.__get_comboxBox_selected_option()
		currentHostContent = self.__get_textview_text()
		self.tweakHandler.save_host(currentHostName, currentHostContent)
	
	
	#删除host
	def delete_host(self, button):
		self.tweakHandler.delete_host(self.__get_comboxBox_selected_option())
		self.__reload_select_options_and_select_option()
		#判断是否要disable删除按钮
		self.__check_and_disable_delete_button()
	
	
	
	#左键点击icon事件
	def __statusicon_left_click_event(self, status_icon):
		#显示窗体
		self.ui_window.show_all()
		#显示到用户当前屏幕
		self.ui_window.present()
	
	
	#右键点击icon事件
	def __statusicon_right_click_event(self, status_icon, button, activate_time):
		menu = gtk.Menu()
#		switchMenu = gtk.MenuItem()
#		switchMenu.set_label("切换host")
#		switchMenu.set_submenu(self.__buildHostMenuItems())

		about = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
		about.set_label("关于")
		quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		quit.set_label("退出")
		
		#加载己有host选项到menu菜单中
		for hostMenuItem in self.__buildHostMenuItems():
			menu.append(hostMenuItem)
		
		menu.append(gtk.SeparatorMenuItem())
		menu.append(about)
		menu.append(gtk.SeparatorMenuItem())
		menu.append(quit)

		about.connect("activate", self.__show_about_dialog)
		quit.connect("activate", self.__close_application)
		menu.show_all()
		menu.popup(None, None, self.__position, button, activate_time)
	
	
	#渲染出全部host选项
#	def __buildHostMenuItems(self):
#		#获取当前系统host对应的host配置名称
#		systemHostName = self.tweakHandler.get_host_name_equals_system_host()
#		#创建Menu
#		menu = gtk.Menu()
#		#获取全部可选择的host选项
#		selectOptionList = self.tweakHandler.get_all_host_select_options()
#		for hostName in selectOptionList:
#			hostMenuItem = gtk.CheckMenuItem(hostName)
#			menu.append(hostMenuItem)
#			if(systemHostName and systemHostName == hostName):
#				#当前host打勾
#				hostMenuItem.set_active(True)
#			#绑定点击item事件
#			hostMenuItem.connect("toggled", self.__host_menu_item_click, hostMenuItem)
#		
#		#设置控制变量，__host_menu_item_click函数中使用
#		self.__is_host_menu_item_clicked = False
#		return menu

	def __buildHostMenuItems(self):
		hostMenuItemList = []
		#获取当前系统host对应的host配置名称
		systemHostName = self.tweakHandler.get_host_name_equals_system_host()
		#获取全部可选择的host选项
		selectOptionList = self.tweakHandler.get_all_host_select_options()
		for hostName in selectOptionList:
			hostMenuItem = gtk.CheckMenuItem(hostName)
			hostMenuItemList.append(hostMenuItem)
			if(systemHostName and systemHostName == hostName):
				#当前host打勾
				hostMenuItem.set_active(True)
			#绑定点击item事件
			hostMenuItem.connect("toggled", self.__host_menu_item_click, hostMenuItem)
		
		#设置控制变量，__host_menu_item_click函数中使用
		self.__is_host_menu_item_clicked = False
		return hostMenuItemList
	
	
	#点击hostMenuItem
	def __host_menu_item_click(self, clickedMenuItem, previewHostMenuItem):
		if(self.__is_host_menu_item_clicked == True):
			return
		self.__is_host_menu_item_clicked = True
		
		previewHostMenuItem.set_active(False)
		clickedMenuItem.set_active(True)
		
		#点击选中的host名称
		clickedHostName = clickedMenuItem.get_label()
		#读取目标的host内容
		hostContent = self.tweakHandler.read_host(clickedHostName)
		#textview显示host内容
		self.__show_host_on_text_view(hostContent)
		#重新加载主窗口的select中option并选中当前系统host
		self.__reload_select_options_and_select_option(clickedHostName)
		
	
	#隐藏窗口
	def __hide_window(self, window, event):
		window.hide_all()
		return True
		
	#退出程序
	def __close_application(self, window):
		gtk.main_quit()
		

	def __position(self, menu):
		return gtk.status_icon_position_menu(menu, self.ui_statusicon)

	def __show_about_dialog(self, widget):
		about_dialog = gtk.AboutDialog()
		about_dialog.set_destroy_with_parent(True)
		about_dialog.set_name("hosttweak")
		about_dialog.set_comments("hosttweak是一个快速修改和切换/etc/hosts文件的工具")
		about_dialog.set_version("v0.1")
		about_dialog.set_authors(["大进 <xiaojin.nxj@alibaba-inc.com>", "thebye85 <thebye85@gmail.com>"])
		about_dialog.run()
		about_dialog.destroy()
	
	
	
	def __show_ui(self):
		gtk.main()
		return 0

