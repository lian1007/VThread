import os
import re
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from moviepy.editor import VideoFileClip, clips_array

font_style = ("Microsoft JhengHei", 14, "bold")

# 定義拼接影片的函數
def concatenate_videos(video_paths):
    try:
        # 按文件名排序
        video_paths.sort(key=lambda x: os.path.basename(x))
        clips = [VideoFileClip(path) for path in video_paths]
        # 找到最長的影片時長
        max_duration = max(clip.duration for clip in clips)
        # 將所有影片設置為與最長影片相同長度，如果影片短，則循環播放直到達到最長時間
        clips_with_loop = [clip.loop(duration=max_duration) for clip in clips]
        # 垂直拼接影片 (stack on top of each other)
        final_clip_vertical = clips_array([[clip] for clip in clips_with_loop])

        # 使用第一個影片的目錄作為儲存位置
        output_dir = os.path.dirname(video_paths[0])
        base_name = "Collage"
        output_path = os.path.join(output_dir, f"{base_name}.mp4")
        
        # 如果檔案已經存在，則添加數字後綴
        counter = 1
        while os.path.exists(output_path):
            output_path = os.path.join(output_dir, f"{base_name}{counter}.mp4")
            counter += 1
        
        # 儲存結果為新影片
        final_clip_vertical.write_videofile(output_path)
        messagebox.showinfo("完成", f"影片已成功串接並保存")

    except Exception as e:
        messagebox.showerror("錯誤", f"處理影片時發生錯誤: {e}")

# 拖曳事件處理函數
def on_drop(event):
    # 使用正則表達式來提取完整的文件路徑
    video_paths = re.findall(r'\{(.*?)\}', event.data)
    print(video_paths)
    valid_videos = []
    invalid_files = []  # 用於保存無效文件
    for video_path in video_paths:
        if os.path.isfile(video_path):
            ext = os.path.splitext(video_path)[1].lower()
            if ext in ['.mp4']:
                valid_videos.append(video_path)
            else:
                invalid_files.append(os.path.split(video_path)[1].lower())  # 收集無效類型的文件
        else:
            invalid_files.append(os.path.split(video_path)[1].lower())  # 收集無效的文件

    # 如果有無效文件，統一彈出一次警告
    if invalid_files:
        messagebox.showwarning("無效文件", f"文件無效或不支援: {', '.join(invalid_files)}")
    elif len(valid_videos) != 1:
        concatenate_videos(valid_videos)
    else:
        messagebox.showwarning("錯誤", f"單個影片檔案無需串接")

# 創建 TkinterDnD 窗口
root = TkinterDnD.Tk()
root.title("影片垂直拼接器")
root.geometry("300x200")

# 設置拖曳區域的標籤
label = tk.Label(root, text="請用影片打我", bg="#8D7CFF",fg="white",font=font_style)
label.pack(fill="both", expand=True)

# 綁定拖曳事件
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# 啟動主循環
root.mainloop()
