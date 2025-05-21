from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent

class FileModificationHandler(FileSystemEventHandler):
	
	def __init__(self, update):
		self.update = update
		super().__init__()
	
	def on_any_event(self, event):
		modified = not event.is_directory\
			and (
				type(event) is FileModifiedEvent\
				or type(event) is FileCreatedEvent
			)
		
		if modified:
			print('File updated!')
			self.update()
		
		else:
			pass

def observe_file_modifications(path: str, update) -> Observer:
	observer = Observer()
	observer.schedule(FileModificationHandler(update), path)
	observer.start()
	return observer
