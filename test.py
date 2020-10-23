import tkinter as tk
import math


class Model():

    width = 7 #横軸の盤面の数
    height = 15 #縦軸の盤面の数

    def __init__(self):
        self.data = [[0]*Model.width for i in range(Model.height)] #0の要素を入れた2次元配列の作成
        self.NumberX = math.floor(Model.width/2) #横軸
        self.NumberY = 0 #縦軸

    def map_all(self,list): #横が揃っているか判定する。揃っていたらTrueを返す
        judge = []
        if list: 
            for l in list[1:]:
                judge.append(list[0] == l)
            return all(judge)
        else:
            return False

    def leftModel(self): #左矢印キーが押されたら
        if self.NumberX > 0: #左端かどうか
            self.NumberX = self.NumberX-1

    def rightModel(self): #右矢印キーが押されたら
        if self.NumberX < Model.width-1: #右端かどうか
            self.NumberX = self.NumberX+1

    def downModel(self): #下矢印キーが押されたら
        if self.NumberY < Model.height-1 and self.data[self.NumberY+1][self.NumberX] != 2: #盤面の一番下かつしたブロックが2でないなら真
            self.NumberY = self.NumberY+1

    def update(self):
        for i in range(Model.height):#盤面をすべて0にする
            for j in range(Model.width):
                if self.data[i][j] == 1:
                    self.data[i][j] = 0

        if self.NumberY > 0:#ブロック2つ分を1にする
            self.data[self.NumberY-1][self.NumberX] = 1
            self.data[self.NumberY][self.NumberX] = 1

        if self.NumberY == Model.height-1 or self.data[self.NumberY+1][self.NumberX] == 2: #判定(一番下または下ブロックが2)
            self.data[self.NumberY-1][self.NumberX] = 2
            self.data[self.NumberY][self.NumberX] = 2

            for i in range(Model.height):
                if self.map_all(self.data[i]): #横が揃っているかどうか判定
                    for j in range(Model.width):
                        self.data[i][j] = 0

            self.NumberX = math.floor(Model.width/2)
            self.NumberY = 0

        self.NumberY = (self.NumberY+1)%Model.height


class View():

    def __init__(self, master, model, controller):
        self.master = master
        self.model = model
        self.controller = controller

        self.canvas = tk.Canvas(self.master,width=600,height=600,bg="black") #キャンバスの作成
        self.canvas.pack()

        for i in range(Model.height): #盤面を表示
            for j in range(Model.width):
                x = 50+30*j
                y = 70+30*i
                self.canvas.create_text(x+300,y+15,text=self.model.data[i][j],font=("Helvetica",15,"bold"),fill="white",tag="block") #文字盤面
                self.canvas.create_rectangle(x,y,x+30,y+30,outline="white") #盤面

    def update(self):

        self.canvas.delete("block")

        for i in range(Model.height): #ブロックを表示
            for j in range(Model.width):
                x = 50+30*j
                y = 70+30*i
                self.canvas.create_text(x+300,y+15,text=self.model.data[i][j],font=("Helvetica",15,"bold"),fill="white",tag="block")
                if self.model.data[i][j] == 1 or self.model.data[i][j] == 2: #dataが1か2のものを表示
                    self.canvas.create_rectangle(x,y,x+30,y+30,fill="red",outline="white",tag="block")


class Controller():

    UPDATE=750 #750ミリ秒間隔で繰り返し

    def __init__(self, master, model):
        self.master = master
        self.model = model

        self.master.after(self.UPDATE, self.update)

        self.master.bind("<Left>",self.leftController) #左矢印キー
        self.master.bind("<Right>",self.rightController) #右矢印キー
        self.master.bind("<Down>",self.downController) #下矢印キー

    def leftController(self,event): #左矢印キーが押されたら
        self.model.leftModel()

    def rightController(self,event): #右矢印キーが押されたら
        self.model.rightModel()

    def downController(self,event): #下矢印キーが押されたら
        self.model.downModel()

    def update(self): #ループ

        self.model.update()
        self.view.update()

        self.master.after(self.UPDATE, self.update)


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        master.geometry("600x600") #ウィンドウサイズ
        master.title("学習用テトリス") #タイトル名

        self.model = Model() #インスタンスmodelを生成
        self.controller = Controller(master, self.model) #インスタンスcontrollerを生成
        self.view = View(master, self.model, self.controller) #インスタンスviewを生成

        self.controller.view = self.view #引数の追加


def main():
    win = tk.Tk()
    app = Application(master = win)
    app.mainloop()


if __name__ == "__main__":
    main()