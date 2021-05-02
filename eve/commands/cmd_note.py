import click
from eve.service import svc_note


class Context:
    def __init__(self):
        self.note = svc_note.Note()


@click.group()
@click.pass_context
def cli(ctx):
    """Make notes."""
    ctx.obj = Context()


@cli.command()
@click.pass_context
def show(ctx):
    """Show table with notes."""
    ctx.obj.note.output()


@cli.command()
@click.option('-t', '--note_text', help='Note text.', required=True, type=str)
@click.option('-d', '--due_date', help='Due date (YYYY-MM-DD).', required=False, type=str, default=None)
@click.option('-p', '--priority', help='Priority.', required=False, type=int, default=None)
@click.pass_context
def add(ctx, note_text, due_date, priority):
    """Add notes."""
    ctx.obj.note.add(note_text, due_date, priority)
    ctx.obj.note.output()


@cli.command()
@click.option('-k', '--key', help='Key of the note.', required=True, type=int)
@click.pass_context
def delete(ctx, key):
    """Delete notes."""
    ctx.obj.note.delete(str(key))
    ctx.obj.note.output()


@cli.command()
@click.option('-k', '--key', help='Key of the note.', required=True, type=int)
@click.option('-d', '--due_date', help='Due date (YYYY-MM-DD).', required=False, type=str)
@click.option('-p', '--priority', help='Priority.', required=False, type=int)
@click.option('-t', '--note_text', help='Note text.', required=False, type=str)
@click.pass_context
def edit(ctx, key, due_date=None, priority=None, note_text=None):
    """Edit notes."""
    # If due_date, priority and note_text is given
    if due_date is not None and priority is not None and note_text is not None:
        ctx.obj.note.edit(key=str(key), DueDate=due_date, Priority=priority, NoteText=note_text)
    # If due_date and priority is given
    elif due_date is not None and priority is not None:
        ctx.obj.note.edit(key=str(key), DueDate=due_date, Priority=priority)
    # If due_date and note_text is given
    elif due_date is not None and note_text is not None:
        ctx.obj.note.edit(key=str(key), DueDate=due_date, NoteText=note_text)
    # If due_date is given
    elif due_date is not None:
        ctx.obj.note.edit(key=str(key), DueDate=due_date)
    # If priority and note_text is given
    elif priority is not None and note_text is not None:
        ctx.obj.note.edit(key=str(key), Priority=priority, NoteText=note_text)
    # If priority is given
    elif priority is not None:
        ctx.obj.note.edit(key=str(key), Priority=priority)
    # If note_text is given
    elif note_text is not None:
        ctx.obj.note.edit(key=str(key), NoteText=note_text)
    # If nothing is given
    else:
        ctx.obj.note.edit(key=str(key))
    ctx.obj.note.output()
