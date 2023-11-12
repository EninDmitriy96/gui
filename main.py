import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QPushButton
from PyQt5.QtCore import *
from gamecode import *


class QuizApp(QWidget):
    def __init__(self, questions_file, answers_file):
        super().__init__()
        self.data = {'who': 'player',  # вот это данные которыми обмениваются игра и оболчка, их не трогать!!!!
                     'player_hand': [],
                     'computer_hand': [],
                     'player_steps': [],
                     'plr_step': 0,
                     'comp_step': 'Взял карту',
                     'table': [],
                     'deck': []}
        self.materials = []
        for i in range(10):
            # materials.append((input('Вопрос: '), input('Ответ: '))) #по сути потом это будет словарь вопрос-ответ который нам даст Нейронка
            self.materials.append((f'{i} + {i}', str(i + i)))
        self.data = gamestart(self.materials, self.data)
        self.pressed = False
        self.questions = self.load_questions(questions_file)
        self.answers = self.load_answers(answers_file)
        self.initUI()

    def style_buttons(self):
        for radio_button in self.radio_buttons:
            radio_button.setStyleSheet("""QRadioButton {
                                                display: inline-block;
                                                cursor: pointer;
                                                padding: 0px 15px;
                                                line-height: 34px;
                                                border: 1px solid #999;
                                                border-radius: 6px;
                                                user-select: none;
                                                padding: 15px;
                                           }
                                           QRadioButton::indicator {
                                                image: url(:/images/radiobutton_unchecked.png);
                                           }
                                           QRadioButton:checked {
                                                background: #ffe0a6;
                                           }
                                           """)

    def load_questions(self, file):
        with open(file, 'r') as f:
            questions = f.readlines()
        return [question.strip() for question in questions]

    def load_answers(self, file):
        with open(file, 'r') as f:
            answers = f.readlines()
        return [answer.strip().split() for answer in answers]

    def initUI(self):
        self.layout = QVBoxLayout()
        self.user_move_info = QLabel()
        self.game_info_label = QLabel()
        self.score_label = QLabel()
        self.question_label = QLabel()
        self.computer_step_label = QLabel()
        self.computer_hand_label = QLabel()
        self.top_card_label = QLabel()
        self.question_label.setStyleSheet("""
            QLabel {
              font-size: 70px;
              font-weight: 600;
              padding: 150px;
              background-image: conic-gradient(#553c9a, #ee4b2b, #00c2cb);
                border-style: dashed;
                border-width: 2px;
                border-color: red;
                border-radius: 10px
            }
            """)
        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.user_move_info)
        self.layout.addWidget(self.game_info_label)
        self.layout.addWidget(self.score_label)
        self.layout.addWidget(self.computer_step_label)
        self.layout.addWidget(self.computer_hand_label)
        self.layout.addWidget(self.top_card_label)
        self.options_layout = QVBoxLayout()
        self.radio_buttons = []
        for i in range(len(self.answers[0])):
            rb = QRadioButton()
            self.radio_buttons.append(rb)
            self.options_layout.addWidget(rb)
        self.style_buttons()
        self.layout.addLayout(self.options_layout)

        self.submit_button = QPushButton('Submit')
        self.submit_button.setStyleSheet("""
                    QPushButton {
                        background-color: #ffe0a6;
                        border: none;
                        color: black;
                        padding: 15px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                    }
            """)
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

        self.current_question = 0
        self.show_question()

    def hide_buttons(self):
        for i in range(len(self.answers[self.current_question])):
            self.radio_buttons[i].setHidden(True)

    def add_buttons(self, n):
        while len(self.radio_buttons) < n:
            rb = QRadioButton()
            self.radio_buttons.append(rb)
            self.options_layout.addWidget(rb)
        self.style_buttons()

    def show_question(self):
        # if self.current_question < len(self.questions):
        self.question_label.setText(f"{self.data['table'][-1].type}, {self.data['table'][-1].text}")
        self.user_move_info.setText(f"Your move: {self.data['plr_step']}")
        self.computer_hand_label.setText(f"Computer`s cards remaining: {len(self.data['comp_hand'])}")
        self.computer_step_label.setText(f"{self.data['comp_step']}")
        # self.add_buttons(len(self.answers[self.current_question]))
        self.add_buttons(len(self.data['player_hand']))
        for i in range(len(self.data['player_hand'])):
            self.radio_buttons[i].setText(f"{self.data['player_hand'][i].type}, {self.data['player_hand'][i].text}")
            self.radio_buttons[i].setChecked(False)
            self.radio_buttons[i].setHidden(False)
        # else:
        #     self.question_label.setText('Quiz complete!')

    def submit(self):
        self.pressed = True
        step = -1
        for i in range(len(self.data['player_hand'])):
            if self.radio_buttons[i].isChecked():
                # Do something with the selected answer (e.g., check if it's correct)
                step = i
                print(
                    f'Question {self.current_question + 1} - Selected answer: {self.answers[self.current_question][i]}')
                break
        self.data['player_step'] = step
        self.data = gameprocess(self.materials, self.data)
        print(self.data)
        if len(self.data) == 3:
            print(f"Winner: f{self.data[0]}; Mistakes: {self.data[3]}")
            return
        self.hide_buttons()
        self.current_question += 1
        self.show_question()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    questions = 'questions.txt'
    answers = 'answers.txt'
    quiz_app = QuizApp(questions, answers)
    quiz_app.show()
    sys.exit(app.exec_())
