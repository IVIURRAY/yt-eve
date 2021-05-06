import json
from rich.console import Console
from rich.table import Table
from rich import box
import os.path
from datetime import date
import pathlib


class Note:
    def __init__(self):
        # Console API from rich module
        self.console = Console()
        # Highlight color 1 for outputs ==> Affected objects (e. g. files, properties etc.)
        self.color = 'bold dodger_blue1'
        # Highlight color 2 for outputs ==> Warnings (e. g. reached due dates etc.)
        self.color2 = 'bright_red'
        # Path to note-file
        self.note_file = os.path.join(pathlib.Path.home(), '.kirk_note.json')
        # Check if note-file exists and if not create and populate it with sample data
        if not os.path.isfile(self.note_file):
            self.touch = '''
            {
            "1": {"CreationDate": "2021-04-24",
                "EditDate": null,
                "DueDate": "2030-10-29",
                "Priority": null,
                "NoteText": "This is sample entry 1."},
            "2": {"CreationDate": "2021-04-24",
                "EditDate": "2021-04-24",
                "DueDate": "2021-04-29",
                "Priority": 1,
                "NoteText": "This is sample entry 2."},
            "3": {"CreationDate": "2021-04-24",
                "EditDate": "2021-04-24",
                "DueDate": "2021-04-28",
                "Priority": 2,
                "NoteText": "This is sample entry 3."}
            }
            '''
            self.touch = json.loads(self.touch)
            with open(self.note_file, 'w', encoding='utf-8') as f:
                json.dump(self.touch, f, indent=2, ensure_ascii=False)
            self.console.log(f'[{self.color}]{self.note_file}[/] created...')
        # Load note-file into note-data
        with open(self.note_file, encoding='utf-8') as f:
            self.note_data = json.load(f)
            self.console.log(f'[{self.color}]{self.note_file}[/] loaded into class-object...')

    def output(self):
        # Create copy of note-data for output (because of the transformation-process necessary for rich-table)
        output_data = self.note_data
        # Transform None-values of output-data to str('None') and the other values to str()
        for key in output_data:
            for attribute in output_data[key]:
                if output_data[key][attribute] is None:
                    output_data[key][attribute] = 'None'
                else:
                    output_data[key][attribute] = str(output_data[key][attribute])
        # Order output-data by 'Priority' and 'DueDate'
        output_data = dict(sorted(output_data.items(), key=lambda x: x[1]['Priority']))
        output_data = dict(sorted(output_data.items(), key=lambda x: x[1]['DueDate']))
        # Create rich-table for output
        table = Table(show_header=True,
                      box=box.ASCII,
                      # show_lines=True,
                      header_style=self.color)
        table.add_column('Key', style='dim')
        table.add_column('CreationDate', style='dim')
        table.add_column('EditDate', style='dim')
        table.add_column('DueDate', style='dim')
        table.add_column('Priority', style='dim')
        table.add_column('NoteText')
        # Populate rich-table with output-data
        for key in output_data:
            row = list()
            row.append(key)
            row.append(output_data[key]['CreationDate'])
            row.append(output_data[key]['EditDate'])
            row.append(output_data[key]['DueDate'])
            row.append(output_data[key]['Priority'])
            row.append(output_data[key]['NoteText'])
            # Check if DueDate is <= current date and highlight DueDate if it is
            if row[3] <= str(date.today()):
                table.add_row(str(row[0]), str(row[1]), str(row[2]), str(f'[{self.color2}]'+row[3]+'[/]'),
                              str(row[4]), str(row[5]))
            else:
                table.add_row(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]))
        # Print rich-table to console
        self.console.print(table)

    def add(self, note_text=None, due_date=None, priority=None):
        # Compose new note
        new_note = dict()
        key = str(len(self.note_data) + 1)
        new_note["CreationDate"] = str(date.today())
        new_note["EditDate"] = None
        new_note["DueDate"] = due_date
        new_note["Priority"] = priority
        new_note["NoteText"] = note_text
        # Append new note to note-data
        self.note_data[key] = new_note
        self.console.log(f'New note with key [{self.color}]{key}[/] added...')
        # Save note-data to note-file
        self.save()

    def delete(self, key=None):
        if key is None:
            self.console.log(f'No key given...')
        else:
            # Delete key value from note-data for given key
            try:
                self.note_data.pop(key)
                self.console.log(f'Key [{self.color}]{key}[/] deleted...')
                # Assign new keys to note-data
                new_keys = list()
                for i, note in enumerate(self.note_data):
                    new_keys.append(str(i + 1))
                self.note_data = dict(zip(new_keys, list(self.note_data.values())))
                self.console.log(f'New enumeration for note-data applied...')
                # Save note-data to note-file
                self.save()
            except KeyError:
                self.console.log(f'Key [{self.color}]{key}[/] not existing...')

    def edit(self, key=None, **kwargs):
        if key is None:
            self.console.log(f'No key given...')
        else:
            # Edit values for given key
            edit_counter = 0
            if key not in self.note_data:
                self.console.log(f'No note found for given key [{self.color}]{key}[/]...')
                return
            for item_key, value in kwargs.items():
                self.note_data[key][item_key] = value
                edit_counter += 1
                self.console.log(f'{item_key} of key [{self.color}]{key}[/] changed to [{self.color}]{value}[/]...')
            if edit_counter == 0:
                self.console.log(f'No values of key [{self.color}]{key}[/] changed...')
            else:
                self.console.log(f'[{self.color}]{edit_counter}[/] values of key [{self.color}]{key}[/] changed...')
                self.note_data[key]['EditDate'] = str(date.today())
                self.save()

    def save(self):
        with open(self.note_file, 'w', encoding='utf-8') as f:
            json.dump(self.note_data, f, indent=2, ensure_ascii=False)
        self.console.log(f'[{self.color}]{self.note_file}[/] saved...')
