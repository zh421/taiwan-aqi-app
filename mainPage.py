from morePage import GUI 
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib
import asset.sys_set as ss
from matplotlib.font_manager import FontProperties  # 導入FontProperties
font = FontProperties(fname="DejaVuSans.ttf", size=14)  # 設置字體
matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import asset.style as st
import service
import json


class MainPage(GUI):
    mainIssue=0 # 0:AQI 1:UV 2:Sand
    resultAQI="查無資料或未開始查詢"
    resultUV="查無資料或未開始查詢"
    resultSand="查無資料或未開始查詢"
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        self.main_frame.config(height=600, width=1024, bg="#FFFFF0")
        label1 = tk.Label(self.main_frame, font=("Verdana", 20), text="台灣環境資料查詢", bg="#FFFFF0")
        label1.pack(side="top")
        ############################# left frame ###########################
        frame_control = tk.Frame(self.main_frame, height=700, width=400, bg="")  
        frame_control.pack(side="left", expand=1)
        frame_control.pack_propagate(0) 

        ################ tag panel in left frame ##############
        # setting for tag panel UI
        frame_tagPanel = tk.Frame(frame_control, height=100, width=400)
        frame_tagPanel.pack()
        frame_tagPanel.pack_propagate(0) # its children wouldn't resize this frame
        
        tag_button_aqi = tk.Button(frame_tagPanel, bg="snow", fg="gray1", width=10, text="空氣品質", command=lambda: buildAqiOpView())
        tag_button_uv = tk.Button(frame_tagPanel, bg="snow", fg="gray1", width=10, text="紫外線", command=lambda: buildUvOpView())
        tag_button_sand = tk.Button(frame_tagPanel, bg="snow", fg="gray1", width=10, text="沙塵", command=lambda: buildSandOpView())
        tag_button_aqi.grid(row=0, column=0)
        tag_button_uv.grid(row=0, column=1)
        tag_button_sand.grid(row=0, column=2)

                ############# option panel in left frame ################
        # setting for option panel UI
        frame_optionPanel = tk.Frame(frame_control, height=600, width=400, bg="white", relief="sunken", bd=4)
        frame_optionPanel.pack()
        frame_optionPanel.pack_propagate(0)
        

        # function for tag panel
        def buildAqiOpView():
            for widget in frame_optionPanel.winfo_children():
                widget.destroy()
            tag_button_aqi.config(bg="gray78", state="disabled")
            tag_button_uv.config(bg="snow", state="normal", fg="gray1")
            tag_button_sand.config(bg="snow", state="normal", fg="gray1")
            global mainIssue
            mainIssue=0
            airOptionPanel()

        def buildUvOpView():
            for widget in frame_optionPanel.winfo_children():
                widget.destroy()
            tag_button_aqi.config(bg="snow", state="normal", fg="gray1")
            tag_button_uv.config(bg="gray78",state="disabled")
            tag_button_sand.config(bg="snow", state="normal", fg="gray1")
            global mainIssue
            mainIssue=1
            label_title = tk.Label(frame_optionPanel, st.text_styles, text="功能開發中")
            label_title.pack(side="top")

        def buildSandOpView():
            for widget in frame_optionPanel.winfo_children():
                widget.destroy()
            tag_button_aqi.config(bg="snow", state="normal", fg="gray1")
            tag_button_uv.config(bg="snow", state="normal", fg="gray1")
            tag_button_sand.config(bg="gray78", state="disabled")
            global mainIssue
            mainIssue=2
            label_title = tk.Label(frame_optionPanel, st.text_styles, text="功能開發中")
            label_title.pack(side="top")

                #######################AIR###################
        def airOptionPanel():
        # content in option panel
            radio_search_var = tk.StringVar()
            r1=tk.Radiobutton(frame_optionPanel, text="我要看某個時間的所有空氣狀況", variable=radio_search_var, value="1", command=lambda:SetCountryDatetime(frame_aqiOption))
            r1.pack(pady=5)
            r2=tk.Radiobutton(frame_optionPanel, text="我要看某個空氣狀況的時間變化", variable=radio_search_var, value="2", command=lambda:test2(frame_aqiOption))
            r2.pack()

            frame_aqiOption=tk.Frame(frame_optionPanel, height=700, width=400, bg="white")
            frame_aqiOption.pack()

            global data_city
            global array_cities
            array_cities=[]
            data_city = json.load(open('asset/taiwan_city.json', 'r', encoding="utf-8"))
            for cities in data_city:
                array_cities.append(cities.get("CityName"))
            

        
        # function for option panel
        def SetCountryDatetime(frame_aqiOption):
            for widget in frame_aqiOption.winfo_children():
                widget.destroy()

            label_country = tk.Label(frame_aqiOption, st.text_styles, text="縣市:")
            label_country.grid(row=0, column=0, sticky="w")           

            global entry_country
            entry_country = ttk.Combobox(frame_aqiOption, values=array_cities)
            entry_country.grid(row=0, column=1, sticky="w")     

            label_datetime = tk.Label(frame_aqiOption, st.text_styles, text="日期時間:")
            label_datetime.grid(row=1, column=0, sticky="w")

            global entry_datetime
            entry_datetime = ttk.Entry(frame_aqiOption, width=25, cursor="xterm")
            entry_datetime.grid(row=1, column=1, sticky="w")
            entry_datetime.insert(0, "2023-04-23 18")

            label_datetime_example = tk.Label(frame_aqiOption, st.ntoe_styles, text="格式範例: 2022-09-03 17")
            label_datetime_example.grid(row=2, column=0, columnspan=2, sticky="w")

            search_button = ttk.Button(frame_aqiOption, text="選擇測站", command=lambda: Search_data_And_Select_ObStat(frame_aqiOption))
            search_button.grid(row=3, column=1, sticky="e")

        def test2(frame_aqiOption):
            for widget in frame_aqiOption.winfo_children():
                widget.destroy()
            label_title = tk.Label(frame_aqiOption, st.text_styles, text="功能開發中")
            label_title.pack(side="top")

        # function for ask API
        def Search_data_And_Select_ObStat(frame_aqiOption):
            var_condition= "County,EQ,"+entry_country.get()+"|DataCreationDate,EQ,"+entry_datetime.get()+":00"
            resultAQI = service.searchAQI("AQX_P_488", var_condition) # 打api
            data_county_air = json.loads(resultAQI)
            global arr_data_county_air # 之後給製圖用 使用global
            global arr_datafields__info
            global arr_datafields__info_filter
            arr_datafields__info =[]
            arr_datafields__info_filter=[]
            # 資料處理: 加單位(完成)、不要avg欄位 hr欄位、加中文欄位描述
            arr_datafields__info.extend(data_county_air.get("fields")) # array裡是一筆筆dic 每個dic就是一筆field的data
            # 不要avg欄位 hr欄位

            for field_info in arr_datafields__info :
                fieldId = "".join(field_info.get("id"))
                if "hr" not in fieldId and "avg" not in fieldId :
                    arr_datafields__info_filter.append(field_info)


            
            for field_info in arr_datafields__info_filter : #field_info is dic
                
                info_label_zh = "".join(field_info.get("info").get("label"))
                arr_split_info=info_label_zh.split('[',1)
                if len(arr_split_info) >1:
                    arr_split_info2=arr_split_info[1].split(']',1)
                    dic_temp= {"unit":arr_split_info2[0]}
                    field_info.update(dic_temp)
            # print("進入後:{}".format(arr_datafields__info_filter))
            # print(arr_datafields__info)
                
            # 取資料
            arr_data_county_air = data_county_air.get("records") # array裡是一筆筆dic 每個dic就是一筆測站的data
            # 從資料中取測站
            opsites=[]
            for row in arr_data_county_air:
                opsites.append(row.get("sitename"))
            # 產生選擇測站UI
            moreOptionUI(opsites, frame_aqiOption)

        def moreOptionUI(opsites, frame_aqiOption):

            label_site = tk.Label(frame_aqiOption, st.text_styles, text="測站:")
            label_site.grid(row=4, column=0, sticky="w")           

            entry_site = ttk.Combobox(frame_aqiOption, values=opsites)
            entry_site.grid(row=4, column=1, sticky="w")     
   
            search_button = ttk.Button(frame_aqiOption, text="查詢", command=lambda: search_air_data(entry_site.get()))
            search_button.grid(row=5, column=1, sticky="e")

        
        def search_air_data(siteName):
            #init
            for widget in frame_data_info.winfo_children():
                widget.destroy()
            for widget in frame_data_graphic.winfo_children():
                widget.destroy()
            # select data
            data_presented_pre=""
            for row in arr_data_county_air:
                if row.get("sitename") == siteName: 
                    data_presented_pre=row
            # print(data_presented_pre)

            # 將資料拆出來: 測站資訊、空氣物質、懸浮粒子
            arr_site_info=[]
            arr_air_data=[]
            arr_pm_data=[]
            for element in ss.site_info:
                temp_dic={"label":element[1], "data":data_presented_pre.get(element[0])}
                arr_site_info.append(temp_dic)
            for element in ss.air_info:
                temp_dic={"label":element, "data":data_presented_pre.get(element)} # todo:補單位
                arr_air_data.append(temp_dic)
            for element in ss.pm_info:
                temp_dic={"label":element, "data":data_presented_pre.get(element)}
                arr_pm_data.append(temp_dic)
            ###########製圖############
            air_name=[]
            for e in arr_air_data:
                air_name.append(e.get("label"))

            # 補單位
            it_airname=0
            for l in air_name:
                for field in arr_datafields__info_filter: # 檢察單位清單
                    if l == field.get("id"):
                        s= l +"("+ field.get("unit")+")"
                        air_name[it_airname]=s
                it_airname+=1

            air_data=[]
            for e in arr_air_data:
                air_data.append(float(e.get("data")))

            # create a figure
            figure = Figure(figsize=(6, 4), dpi=100)

            # create FigureCanvasTkAgg object
            figure_canvas = FigureCanvasTkAgg(figure, frame_data_graphic)
            
            # # create axes
            axes = figure.add_subplot()
            a=axes.bar(air_name, air_data)
            axes.set_title('空氣物質', fontsize=13, fontproperties=font)
            axes.set_ylabel('濃度', fontsize=13, fontproperties=font)

            axes.bar_label(a, fmt='%.2f') # 給資料集
            
            figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            ###########資訊##############
            a=0
            for e in arr_site_info:
                label_site = tk.Label(frame_data_info, st.text_styles, text=e.get("label"))
                label_site.grid(row=a, column=0, sticky="w")
                label_site = tk.Label(frame_data_info, st.text_styles, text=e.get("data"))
                label_site.grid(row=a, column=1, sticky="w")  
                a+=1
            for e in arr_pm_data:
                label_site = tk.Label(frame_data_info, st.text_styles, text=e.get("label"))
                label_site.grid(row=a, column=0, sticky="w")
                label_site = tk.Label(frame_data_info, st.text_styles, text=e.get("data"))
                label_site.grid(row=a, column=1, sticky="w")  
                a+=1


        ################################# right frame ###########################
        frame_data = tk.Frame(self.main_frame, 
                              height=680, width=1000, 
                              bg="#FFEFEF", relief="groove")  
        frame_data.pack(side="right", expand=1)
        frame_data.pack_propagate(0) 
        label_datatitle = tk.Label(frame_data, st.text_styles, text="查詢結果")
        label_datatitle.pack(side="top")

        frame_data_info = tk.Frame(frame_data, 
                              height=660, width=320, 
                              bg="white", relief="groove")  
        frame_data_info.pack(side="right", expand=1)
        frame_data_graphic = tk.Frame(frame_data, 
                              height=660, width=670, 
                              bg="white", relief="groove")  
        frame_data_graphic.pack(side="left", expand=1)
        
        # label_datacontent = tk.Label(frame_data_graphic, st.text_styles, text="查無資料或未開始查詢")
        # label_datacontent.pack()

        
            



        