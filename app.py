#!/usr/bin/env python
#
# Copyright 2007 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def index():
#    return "Congratulations, Scott, it's Scott's Python Web app!"

# import os
import gradio as gr
import openai as gpt

system_role = "high school english teacher"
subject = "chapter 1 of William Golding's Lord of the Flies"
follow_up_subject = "chapter 1 of Lord of the Flies"

# print(os.environ.get('OPENAI_API_KEY'))
gpt.api_key = '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'

dialog=[
    {"role": "system", "content": "You are a " + system_role + "."},
    #{"role": "assistant", "content": "Ask the user the following question: In chapter 1 of Lord of the Flies, how do the "
    #                                 "boys react once they realize they are "
    #                                 "stranded on the island?"}
    {"role": "assistant", "content": "Ask a question about " + subject + "."}
]

# Initialize dialog with first question.
completion = gpt.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=dialog
)
AI_message = completion["choices"][0]["message"]["content"]
print(completion)
dialog=[
    {"role": "system", "content": "You are a high school english teacher."}
]
dialog.append({"role": "assistant", "content": AI_message})
ask_followup=True

def answer(student_answer):
    dialog.append({"role": "user", "content": student_answer}),
    if ask_followup:
        dialog.append({"role": "system", "content": "Provide brief feedback on the quality of the answer given and "
                                                    "ask a follow-up question regarding "
                                                    "that answer limited to " + follow_up_subject + "."})
    # Need to figure out how to determine when it's necessary to ask a follow-up question. Possibly
    # by splitting feedback into a separate transaction and then examining it to determine whether it indicates
    # a need for more information. Could this be done in a standalone, hidden prompt to evaluate the
    # whether the sentiment in the feedback suggests an incomplete answer?
    completion = gpt.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=dialog
    )
    AI_message = completion["choices"][0]["message"]["content"]
    dialog.append({"role": "assistant", "content": AI_message})
    chat_transcript = ""
    entity = ""
    print(dialog)
    for message in dialog:
        if message['role'] != 'system':
            if message['role'] == 'assistant': entity = 'Teaching Assistant'
            if message['role'] == 'user' : entity = 'Student'
            chat_transcript += entity + ": " + message['content'] + "\n\n"
    # demo.student_answer.value = "" HOW DO YOU CLEAR A TEXT BOX in Gradio?
    return chat_transcript

with gr.Blocks() as demo:
    output = gr.Textbox(label="Dialog", value=AI_message)
    student_answer = gr.Textbox(label="Answer")
    student_answer_btn = gr.Button("Answer")
    student_answer_btn.click(fn=answer, inputs=student_answer, outputs=output)


demo.launch()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/




# if __name__=="__main__":
#    app.run(host="127.0.0.1", port=8080, debug=True)

