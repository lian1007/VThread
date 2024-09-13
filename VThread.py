import os
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from moviepy.editor import VideoFileClip, clips_array

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
        # # 儲存結果為新影片
        final_clip_vertical.write_videofile("Output.mp4")
        messagebox.showinfo("完成", f"影片已成功串接，並保存")
    except Exception as e:
        messagebox.showerror("錯誤", f"處理影片時發生錯誤: {e}")

# 拖曳事件處理函數
def on_drop(event):
    video_paths = event.data.strip('{}').split()
    valid_videos = []
    print(video_paths,valid_videos)
    for video_path in video_paths:
        if os.path.isfile(video_path):
            # 檢查文件擴展名是否為 mp4 或 mov
            ext = os.path.splitext(video_path)[1].lower()
            if ext in ['.mp4']:
                valid_videos.append(video_path)
            else:
                # 彈出警告窗口，提示無效的文件類型
                messagebox.showwarning("無效類型", f"文件類型只支援 mp4 與 mov 檔")
        else:
            # 彈出警告窗口，提示無效的文件
            messagebox.showwarning("無效文件", f"無效的文件: {video_path}")

    if valid_videos:
        concatenate_videos(valid_videos)


# # 定義影片檔案路徑列表
# video_paths = ['00.mp4', '01.mp4', '02.mp4']

# # 讀取所有影片檔案為 VideoFileClip 物件
# clips = [VideoFileClip(path) for path in video_paths]

# # 找到最長的影片時長
# max_duration = max(clip.duration for clip in clips)

# # 將所有影片設置為與最長影片相同長度，如果影片短，則循環播放直到達到最長時間
# clips_with_loop = [clip.loop(duration=max_duration) for clip in clips]

# # 垂直拼接影片 (stack on top of each other)
# final_clip_vertical = clips_array([[clip] for clip in clips_with_loop])

# # 儲存結果為新影片
# final_clip_vertical.write_videofile("Output.mp4")

# 創建 TkinterDnD 窗口
root = TkinterDnD.Tk()
root.title("影片拖曳拼接器")
root.geometry("400x200")

# 設置拖曳區域的標籤
label = tk.Label(root, text="將影片文件拖曳至此", width=40, height=10, bg="lightgray")
label.pack(pady=40)

# 綁定拖曳事件
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# 啟動主循環
root.mainloop()