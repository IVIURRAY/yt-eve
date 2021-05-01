import json
from rich.console import Console
from rich.table import Table
from rich import box
import os.path
from datetime import date
import pathlib


class Note:
    def __init__(self):
        # Path to note-file
        self.note_file = os.path.join(pathlib.Path.home(), 'test2.json')  # rename for production and make it a hidden file
        # Check if note-file exists and if not create and populate it with sample data
        if not os.path.isfile(self.note_file):
            self.touch = '''
            {
            "1": {"CreationDate": "2021-04-24",
                "EditDate": null,
                "DueDate": "2021-04-29",
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
            print(f'{self.note_file} created...')
        # Load note-file into note-data
        with open(self.note_file, encoding='utf-8') as f:
            self.note_data = json.load(f)
            print(f'{self.note_file} loaded into class-object...')

    def output(self):
        # Create copy of note-data for output (because of the transformation-process)
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
        # Create table for output
        console = Console()
        table = Table(show_header=True,
                      box=box.ASCII,
                      # show_lines=True,
                      header_style='bold blue')
        table.add_column('Key', style='dim')
        table.add_column('CreationDate', style='dim')
        table.add_column('EditDate', style='dim')
        table.add_column('DueDate', style='dim')
        table.add_column('Priority', style='dim')
        table.add_column('NoteText')
        # Populate table with output-data
        for key in output_data:
            row = list()
            row.append(key)
            row.append(output_data[key]['CreationDate'])
            row.append(output_data[key]['EditDate'])
            row.append(output_data[key]['DueDate'])
            row.append(output_data[key]['Priority'])
            row.append(output_data[key]['NoteText'])
            table.add_row(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]))
        # Print table to console
        console.print(table)

    def add(self, note_text=None, due_date=None, priority=None):
        # Compose new note
        new_note = dict()
        key = str(len(self.note_data) + 1)
        new_note["CreationDate"] = str(date.today())
        new_note["EditDate"] = None
        new_note["DueDate"] = due_date
        new_note["Priority"] = priority
        new_note["NoteText"] = note_text
        # Append new_note to note_data
        self.note_data[key] = new_note
        print(f'New note with key {key} added...')
        # Save note_data to note_file
        self.save()

    def delete(self, key=None):
        if key is None:
            print(f'No key given...')
        else:
            # Delete key value from note_data for given key
            try:
                del self.note_data[key]
                print(f'Key {key} deleted...')
                # Assign new keys to note_data
                new_keys = list()
                for i in range(len(self.note_data)):
                    new_keys.append(str(i + 1))
                self.note_data = dict(zip(new_keys, list(self.note_data.values())))
                print(f'New enumeration for note-data applied...')
                # Save note-data to note-file
                self.save()
            except KeyError:
                print(f'Key {key} not existing...')

    def edit(self, key=None, **kwargs):
        if key is None:
            print(f'No key given...')
        else:
            # Edit values for given key
            edit_counter = 0
            try:
                self.note_data[key]['DueDate'] = kwargs['DueDate']
                edit_counter += 1
                prop = kwargs['DueDate']
                print(f'DueDate of key {key} changed to \'{prop}\'...')
            except KeyError:
                print(f'DueDate of key {key} not changed...')
            try:
                self.note_data[key]['Priority'] = kwargs['Priority']
                edit_counter += 1
                prop = kwargs['Priority']
                print(f'Priority of key {key} changed to \'{prop}\'...')
            except KeyError:
                print(f'Priority of key {key} not changed...')
            try:
                self.note_data[key]['NoteText'] = kwargs['NoteText']
                edit_counter += 1
                prop = kwargs['NoteText']
                print(f'NoteText of key {key} changed to \'{prop}\'...')
            except KeyError:
                print(f'NoteText of key {key} not changed...')
            # Set EditDate and save note-data to note-file if an edit happened
            if edit_counter > 0:
                self.note_data[key]['EditDate'] = str(date.today())
                self.save()

    def save(self):
        with open(self.note_file, 'w', encoding='utf-8') as f:
            json.dump(self.note_data, f, indent=2, ensure_ascii=False)
        print(f'{self.note_file} saved...')


# a = Note()
# a.output()
# a.add('This is a manual entry 1: Test äöüÄÖÜß')
# a.add('This is a manual entry 2', '2021-05-30')
# a.add('This is a manual entry 3', '2021-04-30', 2)
# a.delete('1')
# a.edit(key='3', DueDate='2021-04-28', Priority=1, NoteText='Entry edited.')
# a.output()
