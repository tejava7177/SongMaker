import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("주흔의 통합앱")
        self.setGeometry(100, 100, 500, 400)

        tabs = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        # 각 탭에 레이아웃 추가
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(QLabel("첫 번째 기능 (예: 파일 변환)"))
        tab1.setLayout(tab1_layout)

        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(QLabel("두 번째 기능 (예: 데이터 분석)"))
        tab2.setLayout(tab2_layout)

        tab3_layout = QVBoxLayout()
        tab3_layout.addWidget(QLabel("세 번째 기능 (예: 그래프 시각화)"))
        tab3.setLayout(tab3_layout)

        tabs.addTab(tab1, "파일 변환")
        tabs.addTab(tab2, "데이터 분석")
        tabs.addTab(tab3, "그래프")

        self.setCentralWidget(tabs)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainApp()
    mainWin.show()
    sys.exit(app.exec_())