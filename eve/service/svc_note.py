import json
from rich.console import Console
from rich.table import Table
from rich import box
import os.path
from datetime import date
import pathlib


class Note:
    def __init__(self):
        # path to JSON-file where to store note-data
        self.path = str(pathlib.Path.home()) + '/test.json'  # rename for production and make it a hidden file

        # check if JSON-file already exists and if not create it with sample entries
        if os.path.isfile(self.path):
            pass
        else:
            self.touch = '''[
                {
                    "UID": 1,
                    "CreationDate": "2021-04-24",
                    "AlterationDate": null,
                    "DueDate": "2021-04-30",
                    "Priority": null,
                    "NoteTxt": "This is sample entry 1."
                },
                {
                    "UID": 2,
                    "CreationDate": "2021-04-24",
                    "AlterationDate": "2021-04-24",
                    "DueDate": "2021-04-29",
                    "Priority": 1,
                    "NoteTxt": "This is sample entry 2."
                },
                {
                    "UID": 3,
                    "CreationDate": "2021-04-24",
                    "AlterationDate": "2021-04-24",
                    "DueDate": "2021-04-28",
                    "Priority": 2,
                    "NoteTxt": "This is sample entry 3."
                }
            ]'''
            self.touch = json.loads(self.touch)
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.touch, f, indent=2, ensure_ascii=False)
            print(f'Created {self.path}')
        # Initialize instance variables
        self.data = None
        self.new_note = None

    def output(self):
        # read JSON-file
        with open(self.path, encoding='utf-8') as f:
            self.data = json.load(f)

        # transform null-values to str('N/A')
        for dic in self.data:
            for key in dic:
                if dic[key] is None:
                    dic[key] = 'N/A'

        # transform all values to str
        for dic in self.data:
            for key in dic:
                dic[key] = str(dic[key])

        # order by priority and due_date
        self.data = sorted(self.data, key=lambda k: k['Priority'])
        self.data = sorted(self.data, key=lambda k: k['DueDate'])

        # output data
        console = Console()
        table = Table(show_header=True,
                      box=box.ASCII,
                      #  show_lines=True,
                      header_style='bold blue')
        table.add_column('uid', style='dim')
        table.add_column('creation date', style='dim')
        table.add_column('alteration date', style='dim')
        table.add_column('due date', style='dim')
        table.add_column('priority', style='dim')
        table.add_column('note text')
        for dic in self.data:
            row = list()
            for key in dic:
                row.append(dic[key])
            table.add_row(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]))
        console.print(table)

    def add_note(self, note_txt, due_date=None, priority=None):
        # read JSON-file
        with open(self.path, encoding='utf-8') as f:
            self.data = json.load(f)

        # compose new_note
        uid = int(len(self.data)+1)
        self.new_note = dict()
        self.new_note["UID"] = uid
        self.new_note["CreationDate"] = str(date.today())
        self.new_note["AlterationDate"] = None
        self.new_note["DueDate"] = due_date
        self.new_note["Priority"] = priority
        self.new_note["NoteTxt"] = note_txt

        # append new_note to old_notes
        self.data.append(self.new_note)

        # write to JSON-file
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

        print(f'New note with uid {uid} added.')

    def del_note(self, uid):
        # read JSON-file
        with open(self.path, encoding='utf-8') as f:
            self.data = json.load(f)

        # delete data for given uid
        self.data = list(filter(lambda i: i["UID"] != int(uid), self.data))

        # assign new uids to data
        count = 0
        for dic in self.data:
            count += 1
            dic["UID"] = count

        # write to JSON-file
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

        print(f'Note with uid {uid} deleted.')

    def alter_note(self, uid, due_date=None, priority=None, note_txt=None):
        # read JSON-file
        with open(self.path, encoding='utf-8') as f:
            self.data = json.load(f)

        # alter entry with given uid
        for dic in self.data:
            if dic["UID"] == uid:
                dic["AlterationDate"] = str(date.today())
                if due_date is not None:
                    dic["DueDate"] = str(due_date)
                else:
                    pass
                if priority is not None:
                    dic["Priority"] = int(priority)
                else:
                    pass
                if note_txt is not None:
                    dic["NoteTxt"] = str(note_txt)
                else:
                    pass
                print(f'Note with uid {uid} altered.')
            else:
                pass

        # write to JSON-file
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)


a = Note()
# a.add_note('This is a manual entry 1: Test äöüÄÖÜß')
# a.add_note('This is a manual entry 2', '2021-05-30')
# a.add_note('This is a manual entry 3', '2021-04-30', 2)
# a.del_note(1)
# a.alter_note(3, due_date='2021-05-29', priority=1, note_txt='Changed entry. äöüÄÖÜß')
a.output()
