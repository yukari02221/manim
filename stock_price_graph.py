from manim import *
import pandas as pd

# CSVファイルのパスを指定
file_path = 

def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def prepare_data(df):
    dates = df['timestamp'].tolist()
    close_prices = df['close'].tolist()
    return dates, close_prices

class StockPriceGraph(Scene):
    def construct(self):
        # CSVファイルの読み込み
        df = read_csv(file_path)
        dates, close_prices = prepare_data(df)
        
        # グラフの軸を作成
        axes = Axes(
            x_range=[0, len(dates), 10],  
            y_range=[min(close_prices), max(close_prices), (max(close_prices)-min(close_prices))/10],
            axis_config={"color": BLUE}
        )
        
        # 日付ラベルを追加
        x_labels = [Text(dates[i]).scale(0.3).next_to(axes.c2p(i, 0), DOWN) for i in range(0, len(dates), 10)]
        y_labels = [Text(f"{int(y)}").scale(0.2).next_to(axes.y_axis.n2p(y), LEFT, SMALL_BUFF) for y in range(int(min(close_prices)), int(max(close_prices)), int((max(close_prices)-min(close_prices))/10))]
        
        # 折れ線グラフの初期状態
        graph = self.create_graph(axes, [], [], GREEN)
        self.play(Create(axes), *[Write(label) for label in x_labels], *[Write(label) for label in y_labels])
        
        # 折れ線グラフをアニメーションで描画
        points = []
        for i in range(len(dates)):
            x_values = list(range(i+1))
            y_values = close_prices[:i+1]
            new_points = [axes.c2p(x_val, y_val) for x_val, y_val in zip(x_values, y_values)]
            self.update_graph(graph, new_points)
            points.append(new_points[-1])
            self.wait(0.01)
        
        # 最後に全体を描画
        lines = VGroup(*[Line(points[i], points[i + 1], color=GREEN) for i in range(len(points) - 1)])
        self.play(Create(lines))
        self.wait(2)
    
    def create_graph(self, axes, x_values, y_values, color):
        points = [axes.c2p(x_val, y_val) for x_val, y_val in zip(x_values, y_values)]
        lines = VGroup(*[Line(points[i], points[i + 1], color=color) for i in range(len(points) - 1)])
        return lines
    
    def update_graph(self, graph, new_points):
        if len(graph) == 0:
            return
        for i, point in enumerate(new_points[:-1]):
            graph[i].put_start_and_end_on(point, new_points[i+1])
